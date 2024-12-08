import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

class ContentGenerationError(Exception):
    """Custom exception for content generation errors"""
    pass

class ImageGenerator:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variables
        self.api_key = os.getenv("DEEPINFRA_TOKEN")
        if not self.api_key:
            raise ValueError("Missing DEEPINFRA_TOKEN in .env file")
            
        # Set FLUX API endpoint
        self.api_url = 'https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-pro'

    def generate_image(self, prompt: str) -> Dict[str, Any]:
        """
        Generate an AI image based on the given prompt.
        
        Args:
            prompt (str): The input prompt for image generation
            
        Returns:
            Dict[str, Any]: A dictionary containing image data
            
        Raises:
            ContentGenerationError: If image generation fails
        """
        try:
            headers = {
                'Authorization': f'bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'prompt': prompt
            }

            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Assuming the API returns image data in the response
            return {
                "image_url": result.get("image_url")  # Adjust this based on actual API response structure
            }
                
        except Exception as e:
            raise ContentGenerationError(f"Image generation failed: {str(e)}")

def main():
    # Example prompt for testing
    prompt = "Create a humorous post about AI replacing jobs for a Twitter audience."
    try:
        # Initialize generator and create image
        generator = ImageGenerator()
        result = generator.generate_image(prompt)
        
        # Print results
        print("\nInput prompt:")
        print(f'"{prompt}"\n')
        print("Generated content:")
        print(f'Image URL: {result["image_url"]}')
    except (ContentGenerationError, ValueError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
