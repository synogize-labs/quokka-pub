from news_processor import NewsProcessor
from agents.news_swarm import NewsSwarmProcessor
from agents.image_generator import ImageGenerator
import asyncio
import json

async def test_image_flow():
    # Initialize all components
    news_processor = NewsProcessor()
    news_swarm = NewsSwarmProcessor()
    image_generator = ImageGenerator()
    
    test_prompt = "Latest developments in LLMs"
    
    try:
        print("1. Fetching news...")
        news_data = news_processor.search_news(test_prompt)
        
        print("\n2. Synthesizing content...")
        processed_data = await news_swarm.process_content(news_data, "image")
        
        print("\n3. Generating image prompt...")
        # Create a detailed image prompt from the synthesized data
        image_prompt = (
            f"Create a visual representation of: {processed_data['core_message']}\n"
            f"Key elements to include: {', '.join(processed_data['key_facts'][:2])}\n"
            f"Style: Professional technology visualization with {processed_data['tone']} tone"
        )
        
        print("\n4. Generating image...")
        image_result = image_generator.generate_image(image_prompt)
        
        print("\n5. Final Output:")
        print(json.dumps({
            "image_url": image_result["image_url"],
            "prompt_used": image_prompt,
            "source_facts": processed_data["key_facts"],
            "citations": processed_data["citations"]
        }, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_image_flow())