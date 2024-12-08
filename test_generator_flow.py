from news_processor import NewsProcessor
from agents.news_swarm import NewsSwarmProcessor
from agents.text_generator import TextGenerator
import asyncio
import json

async def test_full_flow():
    # Initialize all components
    news_processor = NewsProcessor()
    news_swarm = NewsSwarmProcessor()
    text_generator = TextGenerator()
    
    test_prompt = "best supplements for muscle growth"
    
    try:
        print("1. Fetching news...")
        news_data = news_processor.search_news(test_prompt)
        
        print("\n2. Synthesizing content...")
        processed_data = await news_swarm.process_content(news_data, "text")
        
        print("\n3. Generating social media content...")
        generated_content = text_generator.generate_content(processed_data)
        
        print("\n4. Final Output:")
        print(json.dumps(generated_content, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_full_flow())