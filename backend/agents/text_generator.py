import os
from openai import OpenAI
from typing import Dict, Any
import json
from dotenv import load_dotenv

class ContentGenerationError(Exception):
    """Custom exception for content generation errors"""
    pass

class TextGenerator:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OPENAI_API_KEY in .env file")
            
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # System prompt for the AI model
        self.system_prompt = """
        You are a creative social media writer.
        Create engaging and humorous content for Twitter.
        Keep text within 280 characters.
        Include 2-3 relevant hashtags.
        
        You must respond in this exact JSON format:
        {
            "text": "Your creative text here",
            "hashtags": ["#hashtag1", "#hashtag2"]
        }
        """

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        Generate social media content based on the given prompt.
        
        Args:
            prompt (str): The input prompt for content generation
            
        Returns:
            Dict[str, Any]: A dictionary containing generated text and hashtags
            
        Raises:
            ContentGenerationError: If content generation fails
        """
        try:
            # Create chat completion request
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Create viral social media content for: {prompt}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response content
            content = json.loads(response.choices[0].message.content)
            
            # Validate response format
            if "text" not in content:
                raise ContentGenerationError("Response missing required 'text' field")
                
            return {
                "text_post": content["text"],
                "hashtags": content.get("hashtags", [])
            }
                
        except Exception as e:
            raise ContentGenerationError(f"Content generation failed: {str(e)}")

def main():
    # Example prompt for testing
    prompt = "Create a humorous post about AI replacing jobs for a Twitter audience."
    try:
        # Initialize generator and create content
        generator = TextGenerator()
        result = generator.generate_content(prompt)
        
        # Print results
        print("\nInput prompt:")
        print(f'"{prompt}"\n')
        print("Generated content:")
        text_with_hashtags = f'{result["text_post"]} {" ".join(result["hashtags"])}'
        print(f'Text Post: "{text_with_hashtags}"')
    except (ContentGenerationError, ValueError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
