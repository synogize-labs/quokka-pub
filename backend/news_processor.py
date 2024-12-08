from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import json
import logging
from datetime import datetime
import os
from typing import Dict, Optional
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsProcessor:
    def __init__(self):
        load_dotenv()
        
        # Initialize Perplexity client
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Set up logging directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize Vectara client if available
        try:
            from utils.vectara_client import VectaraClient
            self.vectara_client = VectaraClient()
            # Create default corpus if needed
            if not self.vectara_client.corpus_key:
                self.vectara_client.get_or_create_corpus(
                    name="News Archive",
                    description="Archive of news search results and summaries"
                )
        except Exception as e:
            logger.warning(f"Vectara client initialization failed: {str(e)}")
            self.vectara_client = None

    def search_news(self, query: str) -> Dict:
        """Search for news using Perplexity API."""
        messages = [
            {
                "role": "system",
                "content": """You are a news research assistant. Search for and summarize recent news articles about the given topic. 
                Include specific details and cite your sources using numbered references like [1], [2], etc.
                Make sure each citation in the text corresponds to the numbered sources you provide."""
            },
            {
                "role": "user",
                "content": f"Find and summarize recent news about: {query}"
            }
        ]
        
        try:
            print("\nSearching news...\n")
            # First make a non-streaming call to get citations
            response_with_citations = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
                stream=False
            )
            
            # Extract citations
            citations = getattr(response_with_citations, 'citations', [])
            citations = [f"[{i+1}] {url}" for i, url in enumerate(citations)] if citations else []
            
            # Now make streaming call for content
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
                stream=True
            )
            
            # Handle streaming response
            content_parts = []
            for chunk in response:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content_part = chunk.choices[0].delta.content
                    if content_part:
                        content_parts.append(content_part)
                        print(content_part, end='', flush=True)
            
            print("\n\nProcessing response...\n")
            
            # Combine content parts
            content = ''.join(content_parts)
            
            # Print citations for debugging
            print("\nCitations found:")
            for citation in citations:
                print(citation)
            
            return {
                'content': content,
                'citations': citations,
                'metadata': {
                    'id': getattr(response_with_citations, 'id', None),
                    'model': getattr(response_with_citations, 'model', None),
                    'created': getattr(response_with_citations, 'created', None),
                    'usage': {
                        'prompt_tokens': getattr(response_with_citations.usage, 'prompt_tokens', 0),
                        'completion_tokens': getattr(response_with_citations.usage, 'completion_tokens', 0),
                        'total_tokens': getattr(response_with_citations.usage, 'total_tokens', 0)
                    } if hasattr(response_with_citations, 'usage') else {}
                }
            }
            
        except Exception as e:
            logger.error(f"Error in search_news: {str(e)}")
            raise

    def generate_content(self, prompt: str, news_data: Dict) -> Dict:
        """Generate formatted content based on news data."""
        messages = [
            {
                "role": "system",
                "content": """Generate a response in JSON format with these fields:
                {
                    "type": "meme|video|image|post",  // Default to "post"
                    "tone": "funny|serious|critical|positive|negative|neutral",  // Default to "neutral"
                    "topic": "main topic",
                    "news_data": "summary of the news",
                    "content": "generated content with hashtags if post"
                }
                When referencing sources, use the same citation numbers from the input news."""
            },
            {
                "role": "user",
                "content": f"Create content for: {prompt}\nBased on this news with citations:\n{news_data.get('content', '')}\n\nAvailable citations:\n" + 
                          "\n".join(news_data.get('citations', []))
            }
        ]
        
        try:
            print("\nGenerating content...\n")
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
                stream=True  # Enable streaming
            )
            
            # Handle streaming response
            content_parts = []
            for chunk in response:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content_part = chunk.choices[0].delta.content
                    if content_part:
                        content_parts.append(content_part)
                        print(content_part, end='', flush=True)
            
            print("\n\nParsing response...\n")
            
            # Combine content parts
            response_content = ''.join(content_parts)
            
            # Try to parse JSON response
            try:
                content = json.loads(response_content)
            except json.JSONDecodeError:
                content = {
                    "type": "post",
                    "tone": "neutral",
                    "topic": prompt,
                    "news_data": str(news_data.get('content', '')),
                    "content": response_content
                }
            
            return content
            
        except Exception as e:
            logger.error(f"Error in generate_content: {str(e)}")
            raise

    def save_markdown_log(self, request_id: str, prompt: str, news_data: Dict, content: Dict) -> Path:
        """Save interaction log as markdown."""
        log_file = self.logs_dir / f"news_interaction_{request_id}.md"
        
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                # Basic metadata
                f.write("# News Interaction Log\n\n")
                f.write("## Metadata\n")
                f.write(f"- **Timestamp**: {datetime.now().isoformat()}\n")
                f.write(f"- **Request ID**: {request_id}\n")
                f.write(f"- **Original Prompt**: {prompt}\n")
                f.write(f"- **Content Type**: {str(content.get('type', 'post'))}\n")
                f.write(f"- **Tone**: {str(content.get('tone', 'neutral'))}\n")
                f.write(f"- **Topic**: {str(content.get('topic', 'general'))}\n\n")
                
                # Perplexity API details
                f.write("## Perplexity API Details\n")
                f.write("```json\n")
                f.write(json.dumps(news_data.get('metadata', {}), indent=2))
                f.write("\n```\n\n")
                
                # Citations
                if news_data.get('citations'):
                    f.write("## Citations\n")
                    for citation in news_data['citations']:
                        f.write(f"- {str(citation)}\n")
                    f.write("\n")
                
                # News data
                f.write("## News Data\n")
                f.write(str(news_data.get('content', '')))
                f.write("\n\n")
                
                # Generated content
                f.write("## Generated Content\n")
                f.write("```\n")
                f.write(str(content.get('content', '')))
                f.write("\n```\n")
            
            return log_file
            
        except Exception as e:
            logger.error(f"Error writing markdown log: {str(e)}")
            raise

    def process(self, prompt: str) -> Dict:
        """Process a news request from start to finish."""
        request_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Step 1: Search for news
            news_data = self.search_news(prompt)
            all_citations = {citation.split('] ')[1]: i+1 
                            for i, citation in enumerate(news_data['citations'])}
            
            # Step 2: Generate formatted content
            content = self.generate_content(prompt, news_data)
            
            # Extract any new citations from the generated content
            content_text = content.get('content', '')
            citation_pattern = r'\[(\d+)\]'
            used_citations = set(re.findall(citation_pattern, content_text))
            
            # Update citation indices if needed
            if used_citations:
                next_index = len(all_citations) + 1
                updated_content = content_text
                
                for citation_num in used_citations:
                    citation_url = f"citation_{citation_num}"  # You might need to extract the actual URL
                    if citation_url not in all_citations:
                        all_citations[citation_url] = next_index
                        next_index += 1
                    
                    # Update the citation number in the content
                    old_ref = f"[{citation_num}]"
                    new_ref = f"[{all_citations[citation_url]}]"
                    updated_content = updated_content.replace(old_ref, new_ref)
                
                content['content'] = updated_content
            
            # Rebuild citations list with updated indices
            citations = [f"[{idx}] {url}" for url, idx in sorted(all_citations.items(), key=lambda x: x[1])]
            news_data['citations'] = citations
            
            # Step 3: Save logs
            md_file = self.save_markdown_log(request_id, prompt, news_data, content)
            
            # Step 4: Upload to Vectara if available
            if self.vectara_client and self.vectara_client.corpus_key:
                try:
                    upload_success = self.vectara_client.upload_markdown(md_file)
                    if upload_success:
                        logger.info(f"Successfully uploaded to Vectara: {md_file}")
                    else:
                        logger.warning(f"Failed to upload to Vectara: {md_file}")
                except Exception as e:
                    logger.error(f"Vectara upload error: {str(e)}")
            
            return {
                **content,
                'citations': citations,
                'metadata': news_data['metadata']
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "type": "error",
                "tone": "neutral",
                "topic": prompt,
                "content": f"An error occurred: {str(e)}",
                "news_data": ""
            }

def main():
    processor = NewsProcessor()
    
    print("News Processing System")
    print("=====================")
    print("Enter your request (or 'exit' to quit)")
    print("Examples:")
    print("- Create a funny meme about AI development")
    print("- Write a serious post about climate change")
    print("- Make a video script about space exploration")
    print()
    
    while True:
        prompt = input("Request: ").strip()
        if prompt.lower() in ['exit', 'quit']:
            break
            
        print("\nProcessing request...\n")
        result = processor.process(prompt)
        
        print("\nGenerated Response:")
        print(f"Type: {result.get('type', 'post')}")
        print(f"Tone: {result.get('tone', 'neutral')}")
        print(f"Topic: {result.get('topic', '')}")
        print("\nContent:")
        print(result.get('content', ''))
        
        if result.get('citations'):
            print("\nSources:")
            for citation in result['citations']:
                print(f"- {citation}")
        print()

if __name__ == "__main__":
    main() 