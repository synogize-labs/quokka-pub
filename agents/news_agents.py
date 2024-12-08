from swarm import Swarm, Agent
from utils.news_search import NewsSearchTool
import os
import logging
from pathlib import Path
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize NewsSearchTool with API key
news_tool = NewsSearchTool(api_key=os.getenv("PERPLEXITY_API_KEY"))

class NewsAgentLogger:
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
    
    def log_interaction(self, agent_name: str, messages: list, response: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"agent_{agent_name}_{timestamp}.md"
        
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"# Agent Interaction Log\n\n")
            f.write(f"## Metadata\n")
            f.write(f"- **Timestamp**: {timestamp}\n")
            f.write(f"- **Agent**: {agent_name}\n")
            f.write(f"- **Request Type**: {response.get('type', 'post')}\n")
            f.write(f"- **Tone**: {response.get('tone', 'neutral')}\n")
            f.write(f"- **Topic**: {response.get('topic', 'general')}\n\n")
            
            f.write(f"## News Sources\n")
            f.write(response.get('news_data', 'No news data available'))
            f.write("\n\n")
            
            if response.get('citations'):
                f.write("### Citations\n")
                for citation in response['citations']:
                    f.write(f"- {citation}\n")
                f.write("\n")
            
            f.write(f"## Generated Content\n")
            f.write("```\n")
            f.write(response.get('content', ''))
            f.write("\n```\n")
            
            f.write(f"\n## Original Conversation\n")
            for idx, msg in enumerate(messages, 1):
                f.write(f"### Message {idx}\n")
                f.write(f"- **Role**: {msg.get('role', 'unknown')}\n")
                f.write(f"- **Content**:\n")
                f.write("```\n")
                f.write(msg.get('content', ''))
                f.write("\n```\n\n")

agent_logger = NewsAgentLogger()

def search_news_for_topic(topic: str) -> str:
    """Search for news articles about a specific topic."""
    logger.info(f"Searching news with query: {topic}")
    result = news_tool.search_everything(query=topic)
    return result['content']

# Single Agent for News Processing
news_agent = Agent(
    name="News Agent",
    instructions=f"""You are a news research and content creation agent. Today's date is {datetime.now().strftime('%B %d, %Y')}.
    
    For each request, analyze it and respond with a JSON structure containing:
    {{
      "type": "meme|video|image|post",  // Default to "post" if not specified
      "tone": "funny|serious|critical|positive|negative|neutral",  // Default to "neutral"
      "topic": "main topic of the request",
      "news_data": "relevant news from search",
      "content": "generated content in requested format"
    }}
    
    Content format guidelines:
    - meme: "Setup: <setup text>\\nPunchline: <punchline text>"
    - video: Scene-by-scene description
    - image: Detailed visual composition
    - post: Social media text with hashtags
    
    Example for "Create a funny meme about AI news":
    {{
      "type": "meme",
      "tone": "funny",
      "topic": "AI developments",
      "news_data": "<searched news content>",
      "content": "Setup: When AI says it'll make your job easier\\nPunchline: But now you're debugging AI prompts instead of code"
    }}
    
    Always use the searched news data as the foundation for your content.
    Include relevant hashtags for social media posts.
    Maintain factual accuracy while adapting to the requested style.""",
    functions=[search_news_for_topic]
) 