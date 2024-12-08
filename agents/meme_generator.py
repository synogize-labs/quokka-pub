import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

class MemeGenerationError(Exception):
    """Custom exception for meme generation errors"""
    pass

class MemeGenerator:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get credentials from environment variables
        self.imgflip_username = os.getenv("IMGFLIP_USERNAME")
        self.imgflip_password = os.getenv("IMGFLIP_PASSWORD")
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Validate credentials
        if not all([self.imgflip_username, self.imgflip_password, self.api_key]):
            raise ValueError("Missing required environment variables. Please check .env file")
            
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # System prompt for meme generation
        self.system_prompt = """
        You are a meme creator. Given a topic or prompt, select the most suitable meme template and create funny text for it.
        You must respond in valid JSON format with these exact fields, WITHOUT ANY COMMENTS:
        {
            "template_id": "61579",
            "top_text": "TOP TEXT HERE",
            "bottom_text": "BOTTOM TEXT HERE",
            "explanation": "Brief explanation why this template was chosen"
        }
        
        Available template IDs:
        - 61579: One Does Not Simply
        - 87743020: Two Buttons
        - 112126428: Distracted Boyfriend
        - 181913649: Drake Hotline Bling
        - 101470: Ancient Aliens
        
        Important: Return ONLY the JSON object, no comments allowed in the JSON.
        """

    def generate_caption(self, prompt: str) -> Dict[str, Any]:
        """
        Generate meme content using GPT-4o
        
        Args:
            prompt (str): Input prompt for meme generation
            
        Returns:
            Dict[str, Any]: Dictionary containing template ID and text content
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Create a funny meme for this topic: {prompt}"}
                ]
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            import json
            parsed_content = json.loads(content)
            
            # Ensure template_id is string
            if 'template_id' in parsed_content:
                parsed_content['template_id'] = str(parsed_content['template_id'])
                
            return parsed_content
            
        except Exception as e:
            raise MemeGenerationError(f"Content generation failed: {str(e)}")

    def generate_meme_img(self, template_id: str, top_text: str, bottom_text: str) -> Dict[str, Any]:
        """
        Generate meme using Imgflip API
        
        Args:
            template_id (str): ID of the meme template
            top_text (str): Text for top of meme
            bottom_text (str): Text for bottom of meme
            
        Returns:
            Dict[str, Any]: Dictionary containing meme URLs
        """
        try:
            url = 'https://api.imgflip.com/caption_image'
            payload = {
                'template_id': template_id,
                'username': self.imgflip_username,
                'password': self.imgflip_password,
                'text0': top_text,
                'text1': bottom_text
            }
            
            response = requests.post(url, data=payload)
            result = response.json()
            
            if response.status_code == 200 and result['success']:
                return {
                    'url': result['data']['url'],
                    'page_url': result['data']['page_url']
                }
            raise MemeGenerationError(f"Generation failed: {result.get('error_message', 'Unknown error')}")
                
        except Exception as e:
            raise MemeGenerationError(f"Meme generation failed: {str(e)}")

    def generate_meme(self, prompt: str) -> Dict[str, str]:
        """
        Generate complete meme from prompt
        
        Args:
            prompt (str): Input prompt for meme generation
            
        Returns:
            Dict[str, str]: Dictionary containing meme URL
        """
        try:
            # Get GPT-generated content
            content = self.generate_caption(prompt)
            
            # Generate meme
            result = self.generate_meme_img(
                template_id=content['template_id'],
                top_text=content['top_text'],
                bottom_text=content['bottom_text']
            )
            
            return {
                'url': result['url']
            }
            
        except Exception as e:
            raise MemeGenerationError(str(e))

def main():
    try:
        # Initialize generator
        generator = MemeGenerator()
        
        # Example prompt
        prompt = "Create a humorous post about AI replacing jobs for a Twitter audience."
        
        print(f"\nGenerating meme for prompt: '{prompt}'")
        result = generator.generate_meme(prompt)
        
        print("\nSuccess!")
        print(f"Image URL: {result['url']}")
        
    except (MemeGenerationError, ValueError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
