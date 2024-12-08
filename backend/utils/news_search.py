from openai import OpenAI
import os
from datetime import datetime
from typing import Dict
from pathlib import Path
import json
import logging
from .vectara_client import VectaraClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsSearchTool:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        # Create logs directory if it doesn't exist
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Configure file handler for logging
        self.logger = logging.getLogger(__name__)
        fh = logging.FileHandler(self.logs_dir / "news_api.log")
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)
        
        # Initialize Vectara client and get/create corpus if needed
        try:
            self.vectara_client = VectaraClient()
            self.corpus_id = self.vectara_client.get_or_create_corpus(
                name="News Search Archive",
                description="Archive of news search results and summaries"
            )
            if not self.corpus_id:
                self.logger.warning("Failed to get or create Vectara corpus")
        except ValueError as e:
            self.logger.warning(f"Vectara client initialization failed: {str(e)}")
            self.vectara_client = None
            self.corpus_id = None
    
    def _log_api_interaction(self, query: str, response: dict):
        """Log API interactions to a markdown file and upload to Vectara"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"api_interaction_{timestamp}.md"
        
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# Perplexity API Interaction Log\n\n")
            f.write(f"## Metadata\n")
            f.write(f"- **Timestamp**: {timestamp}\n")
            f.write(f"- **Query**: {query}\n")
            f.write(f"- **Model**: {response.get('model')}\n\n")
            
            f.write(f"## Response\n")
            f.write("### Summary\n")
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            f.write(f"{content}\n\n")
            
            f.write("### Citations\n")
            for citation in response.get('citations', []):
                f.write(f"- {citation}\n")
            f.write("\n")
            
            f.write("### Usage Stats\n")
            usage = response.get('usage', {})
            f.write(f"- Prompt Tokens: {usage.get('prompt_tokens')}\n")
            f.write(f"- Completion Tokens: {usage.get('completion_tokens')}\n")
            f.write(f"- Total Tokens: {usage.get('total_tokens')}\n")
            
        self.logger.info(f"API interaction logged to {log_file}")
        
        # Upload to Vectara if client is available
        if self.vectara_client and self.corpus_id:
            try:
                upload_success = self.vectara_client.upload_markdown(
                    log_file,
                    corpus_id=self.corpus_id
                )
                if upload_success:
                    self.logger.info(f"Successfully uploaded log to Vectara: {log_file}")
                else:
                    self.logger.warning(f"Failed to upload log to Vectara: {log_file}")
            except Exception as e:
                self.logger.error(f"Error uploading to Vectara: {str(e)}")
        
        return log_file
    
    def search_everything(self, query: str) -> Dict:
        """Search news using Perplexity API."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a news research assistant. Search for and summarize recent news articles about the given topic. Include specific details."
                },
                {
                    "role": "user",
                    "content": f"Find and summarize recent news about: {query}"
                }
            ]
            
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
            )
            
            # Format raw response as a readable string
            raw_response_text = (
                f"Raw Perplexity API Response:\n"
                f"===========================\n"
                f"ID: {response.id}\n"
                f"Model: {response.model}\n"
                f"Created: {response.created}\n\n"
                f"Choices:\n"
            )
            
            for choice in response.choices:
                raw_response_text += f"  Role: {choice.message.role}\n"
                raw_response_text += f"  Content: {choice.message.content[:200]}...\n"
            
            raw_response_text += f"\nUsage:\n"
            raw_response_text += f"  Prompt tokens: {response.usage.prompt_tokens}\n"
            raw_response_text += f"  Completion tokens: {response.usage.completion_tokens}\n"
            raw_response_text += f"  Total tokens: {response.usage.total_tokens}\n"
            
            citations = getattr(response, 'citations', [])
            if citations:
                raw_response_text += f"\nCitations:\n"
                for citation in citations:
                    raw_response_text += f"  - {citation}\n"
            
            raw_response_text += "===========================\n"
            
            # Print for debugging
            print(raw_response_text)
            
            # Return both the raw response and structured data
            return {
                'content': response.choices[0].message.content if response.choices else "",
                'citations': citations,
                'raw_response': raw_response_text,
                'metadata': {
                    'id': response.id,
                    'model': response.model,
                    'created': response.created,
                    'usage': {
                        'prompt_tokens': response.usage.prompt_tokens,
                        'completion_tokens': response.usage.completion_tokens,
                        'total_tokens': response.usage.total_tokens
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in search_everything: {str(e)}")
            raise