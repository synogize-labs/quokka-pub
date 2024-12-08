import os
import replicate
import openai
from dotenv import load_dotenv
from typing import Dict, Optional

class VideoGenerator:
    """
    A class for generating videos using AI models.
    Combines OpenAI's for prompt enhancement and Replicate's video generation model.
    """
    
    def __init__(self):
        # Initialize environment variables from .env file
        load_dotenv()
        
        # Validate required API tokens
        if not os.getenv('REPLICATE_API_TOKEN'):
            raise ValueError("Please set REPLICATE_API_TOKEN in your .env file")
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("Please set OPENAI_API_KEY in your .env file")
        
        # Configure OpenAI API key for GPT access
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Set default video generation parameters
        self.default_config = {
            "aspect_ratio": "16:9",
            "negative_prompt": "low quality, worst quality, deformed, distorted, watermark"
        }

    def generate_prompt(self, user_prompt: str) -> str:
        """
        Enhance a simple video prompt using GPT-4 to create detailed cinematic descriptions.
        
        Args:
            user_prompt (str): Basic video idea from user
            
        Returns:
            str: Enhanced detailed prompt for video generation
        """
        try:
            # Create a detailed prompt using GPT-4
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a video prompt engineering expert. Create natural, descriptive video prompts 
                        that focus on real-world details and human elements. Here's an example of a good prompt:

                        'A woman with long brown hair and light skin smiles at another woman with long blonde hair. 
                        The woman with brown hair wears a black jacket and has a small, barely noticeable mole on her right cheek. 
                        The camera angle is a close-up, focused on the woman with brown hair's face. 
                        The lighting is warm and natural, likely from the setting sun, casting a soft glow on the scene. 
                        The scene appears to be real-life footage.'

                        When creating prompts, include:
                        - Specific physical descriptions (facial features, clothing, hair)
                        - Natural lighting and atmosphere details
                        - Precise camera angles and framing
                        - Small, realistic details that add authenticity
                        - Clear but natural composition

                        Keep descriptions concise but detailed, focusing on visual elements that create a realistic scene.
                        Avoid abstract concepts and focus on tangible, observable details."""
                    },
                    {
                        "role": "user",
                        "content": f"Create a detailed video generation prompt based on this idea: {user_prompt}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract and display the enhanced prompt
            detailed_prompt = response.choices[0].message.content.strip()
            print("\n=== Generated Detailed Prompt ===")
            print(detailed_prompt)
            print("==============================\n")
            return detailed_prompt
            
        except Exception as e:
            print(f"Error generating detailed prompt: {str(e)}")
            return user_prompt

    def generate_video(self, prompt: str) -> Dict[str, str]:
        """
        Generate video based on the provided prompt and configuration.
        
        Args:
            prompt (str): The video description prompt
            
        Returns:
            Dict[str, str]: Dictionary containing video URL
        """
        try:
            # Combine default and custom configurations
            input_config = {**self.default_config}
            input_config["prompt"] = self.generate_prompt(prompt)
            
            # Generate video using Replicate API
            output = replicate.run(
                "fofr/ltx-video:983ec70a06fd872ef4c29bb6b728556fc2454125a5b2c68ab51eb8a2a9eaa46a",
                input=input_config,
                use_file_output=False
            )
            
            video_url = output[0] if isinstance(output, list) else output
            
            return {
                "url": video_url
            }
                
        except Exception as e:
            raise Exception(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    # Example usage of the VideoGenerator class
    generator = VideoGenerator()
    generator.generate_video("A robot working in an office")