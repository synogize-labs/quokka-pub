from news_processor import NewsProcessor
from agents.news_swarm import NewsSwarmProcessor
import asyncio
import json

async def test_news_flow():
    news_processor = NewsProcessor()
    news_swarm = NewsSwarmProcessor()
    
    test_prompt = "Latest developments in LLMs"
    
    try:
        print("1. Fetching news...")
        news_data = news_processor.search_news(test_prompt)
        
        print("\n2. Synthesizing content...")
        processed_data = await news_swarm.process_content(news_data, "text")
        
        print("\n3. Structured Output:")
        print(json.dumps(processed_data, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_news_flow())