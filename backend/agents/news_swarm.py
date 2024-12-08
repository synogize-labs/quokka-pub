from swarm import Swarm, Agent
from typing import Dict, Any
import logging
import json
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

analyze_agent = Agent(
    name="News Synthesizer",
    model="gpt-4o-mini",  # Specify the model explicitly
    instructions="""You are a news synthesis expert. Respond ONLY with a JSON object, no additional text.

    Required format:
    {
        "key_facts": ["fact1", "fact2", "fact3"],
        "main_entities": ["company1", "technology1", "person1"],
        "core_message": "single sentence summary",
        "tone": "positive|negative|neutral",
        "citations": ["[1]", "[2]"],
        "target_audience": "description of ideal audience"
    }""",
)

class NewsSwarmProcessor:
    def __init__(self):
        self.client = Swarm()

    async def process_content(self, news_data: Dict, target_format: str) -> Dict:
        """Process news into structured data for generators."""
        try:
            initial_message = {
                "role": "user",
                "content": f"""Analyze and structure this news content:
                {news_data.get('content', '')}
                
                Citations:
                {news_data.get('citations', [])}
                
                Return ONLY a JSON object following the required format."""
            }

            response = self.client.run(
                agent=analyze_agent,
                messages=[initial_message]
            )

            return json.loads(response.messages[-1]["content"])

        except Exception as e:
            logger.error(f"Error in news synthesis: {str(e)}")
            return {
                "key_facts": [],
                "main_entities": [],
                "core_message": news_data.get('content', '')[:200],
                "tone": "neutral",
                "citations": news_data.get('citations', []),
                "target_audience": "general"
            }