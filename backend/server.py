from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.text_generator import TextGenerator
from agents.meme_generator import MemeGenerator
from agents.video_generator import VideoGenerator
from agents.image_generator import ImageGenerator
from fastapi.middleware.cors import CORSMiddleware
from agents.news_swarm import NewsSwarmProcessor
from news_processor import NewsProcessor
from fastapi.responses import JSONResponse
import os
import requests
from openai import OpenAI

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class GenerateRequest(BaseModel):
    prompt: str

# Response model
class GenerateResponse(BaseModel):
    text: str

# Meme Request model
class GenerateMemeRequest(BaseModel):
    prompt: str

# Meme Response model
class GenerateMemeResponse(BaseModel):
    url: str

# Video Request model
class GenerateVideoRequest(BaseModel):
    prompt: str

# Video Response model
class GenerateVideoResponse(BaseModel):
    url: str

# Image Request model
class GenerateImageRequest(BaseModel):
    prompt: str

# Image Response model
class GenerateImageResponse(BaseModel):
    url: str

# Prompt Request model
class GetPromptRequest(BaseModel):
    input: str
    tone: str
    type: str
    platform: str

# Prompt Response model
class GetPromptResponse(BaseModel):
    prompt: str
    link: str

# Trending Response model
class TrendingResponse(BaseModel):
    topics: list[str]

# Refine Request model
class RefineRequest(BaseModel):
    prompt: str
    refine: str

# Refine Response model
class RefineResponse(BaseModel):
    prompt: str

# Initialize generators
generator = TextGenerator()
meme_generator = MemeGenerator()
video_generator = VideoGenerator()
image_generator = ImageGenerator()

# Initialize processors
news_processor = NewsProcessor()
news_swarm = NewsSwarmProcessor()

@app.post("/generate_text", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    try:
        # TODO: could just extract the return from the prompt instead of run it again
        
        # Get news data
        news_data = news_processor.search_news(request.prompt)
        
        # Process through swarm
        processed_data = await news_swarm.process_content(news_data, "text")
        
        # Generate final content using existing generator
        result = generator.generate_content(processed_data)
        
        # Extract the text content, handling both possible formats
        if isinstance(result, dict):
            # If result is a dictionary, try to get text_post or text
            text_content = result.get('text_post', '') or result.get('text', '')
        else:
            # If result is not a dictionary, convert to string
            text_content = str(result)
        
        return GenerateResponse(text=text_content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_meme", response_model=GenerateMemeResponse)
async def generate_meme(request: GenerateMemeRequest):
    try:
        # Generate meme using MemeGenerator
        result = meme_generator.generate_meme(request.prompt)
        
        return GenerateMemeResponse(
            url=result["url"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_video", response_model=GenerateVideoResponse)
async def generate_video(request: GenerateVideoRequest):
    try:
        # Generate video using VideoGenerator
        result = video_generator.generate_video(request.prompt)
        
        return GenerateVideoResponse(url=result["url"])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_image", response_model=GenerateImageResponse)
async def generate_image(request: GenerateImageRequest):
    try:
        # Generate image using ImageGenerator
        result = image_generator.generate_image(request.prompt)
        
        return GenerateImageResponse(
            url=result["image_url"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_prompt", response_model=GetPromptResponse)
async def get_prompt(request: GetPromptRequest):
    try:
        # Initialize news processor
        news_processor = NewsProcessor()
        
        # Create base prompt based on request parameters
        base_prompt = f"Create {request.type} content about {request.input} "
        base_prompt += f"that is suitable for {request.platform} "
        base_prompt += f"in a {request.tone} tone."
        
        # Process through news flow to get enhanced prompt and relevant links
        result = news_processor.process(base_prompt)
        
        # Extract the main content, removing JSON formatting if present
        content = result.get('content', '')
        if content.startswith('```'):
            # Remove JSON code blocks
            content = '\n'.join([
                line for line in content.split('\n')
                if not line.startswith('```') and not line.startswith('{') and not line.startswith('}')
            ]).strip()
        
        # Format the prompt in a simple way that works with all generators
        formatted_prompt = f"""Create {request.type} about:
{request.input}

Style:
- Platform: {request.platform}
- Tone: {request.tone}

Content Suggestion:
{content}

Key Points:
{result.get('news_data', '')}"""
        
        # Extract citation links
        citation_links = []
        for citation in result.get('citations', []):
            if '] ' in citation:
                url = citation.split('] ')[1].strip()
                citation_links.append(url)
        
        resource_link = citation_links[0] if citation_links else ""
        
        return GetPromptResponse(
            prompt=formatted_prompt,
            link=resource_link
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending", response_model=TrendingResponse)
async def get_trending_topics():
    try:
        # Mock trending topics
        # mock_topics = [
        #     "AI replacing jobs",
        #     "World Cup Finals",
        #     "Climate Change Summit 2024",
        #     "Space Tourism",
        #     "Viral AI Art Trends",
        #     "Global Tech Layoffs",
        #     "New Gaming Consoles",
        #     "Sustainable Fashion"
        # ]
        
        # return TrendingResponse(topics=mock_topics)

        # Initialize OpenAI client for topic extraction
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Fetch headlines from NewsAPI
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("NEWS_API_KEY not found in environment variables")
            
        # Get headlines from multiple categories to ensure diverse topics
        categories = ['technology', 'business', 'science', 'sports', 'entertainment']
        all_headlines = []
        
        for category in categories:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
            response = requests.get(url)
            news_data = response.json()
            
            if news_data["status"] == "ok":
                headlines = [article["title"] for article in news_data["articles"] if article.get("title")]
                all_headlines.extend(headlines)
        
        # Create prompt for GPT to extract topics
        prompt = f"""Extract 5 trending topics from these headlines, focusing on technology, innovation, global events, and cultural trends.
        
        Requirements:
        - Each topic should be 2-4 words
        - Include at least 2 tech-related topics
        - Focus on future-oriented and trending subjects
        - Make topics sound exciting and shareable
        - Format similar to these examples:
          - AI replacing jobs
          - World Cup Finals
          - Climate Change Summit
          - Space Tourism
          - Viral AI Art Trends
          - Global Tech Layoffs
        
        Headlines:
        {' | '.join(all_headlines)}
        """
        
        # Get topics from GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a trend analyst specializing in technology and cultural trends. Extract engaging, forward-looking topics that would interest a tech-savvy audience."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        # Process response into list of topics
        topics_text = response.choices[0].message.content
        topics = [
            # Remove numbering (like "1.", "2.") and clean up whitespace
            topic.strip('- ').strip().split('. ', 1)[-1].strip()
            for topic in topics_text.split('\n') 
            if topic.strip('- ').strip()
        ][:5]  # Limit to 5 topics
        
        return TrendingResponse(topics=topics)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine", response_model=RefineResponse)
async def refine_prompt(request: RefineRequest):
    try:
        # Combine original prompt with refinement instruction
        refined_prompt = f"{request.prompt} Additionally, {request.refine}"
        
        return RefineResponse(prompt=refined_prompt)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))