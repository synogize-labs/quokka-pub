# Quokka

An intelligent AI agent that autonomously retrieves daily news, processes them, and generates engaging social media content across multiple formats (text, images, videos, and memes).

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge)](https://openai.com/)
[![Vectara](https://img.shields.io/badge/Vectara-FF6B6B?style=for-the-badge)](https://vectara.com/)
[![Replicate](https://img.shields.io/badge/Replicate-000000?style=for-the-badge)](https://replicate.com/)
[![Perplexity](https://img.shields.io/badge/Perplexity-734F96?style=for-the-badge)](https://www.perplexity.ai/)
[![ImgFlip](https://img.shields.io/badge/ImgFlip-FF3366?style=for-the-badge)](https://imgflip.com/)
[![NewsAPI](https://img.shields.io/badge/NewsAPI-1CA0F1?style=for-the-badge)](https://newsapi.org/)
[![Swarm](https://img.shields.io/badge/Swarm-FFA500?style=for-the-badge)](https://swarm.dev/)
[![License](https://img.shields.io/badge/license-CC--BY--NC--ND-blue.svg?style=for-the-badge)](LICENSE)

</div>

## 🎯 Challenge Overview

This project was built for the AI Agents / RAG Challenge, focusing on creating an autonomous system that:

- Retrieves relevant daily news articles
- Synthesizes information intelligently
- Generates multi-format social media content
- Adapts content based on user preferences

## 🔄 System Architecture

![architecture](image.png)

## ✨ Key Features

### Content Generation

- **Text Posts**: Platform-optimized social media content
- **Image Generation**: AI-powered visuals for news stories
- **Video Creation**: Dynamic video content
- **Meme Generation**: Trending meme templates with AI-generated captions

### Intelligent Processing

- **News Retrieval**: Real-time news fetching and filtering
- **Smart Summarization**: Context-aware content synthesis
- **Multi-Platform Optimization**: Format-specific content adaptation
- **Citation Management**: Automatic source tracking and linking

### User Experience

- **Customizable Tone**: Formal, casual, humorous, etc.
- **Platform-Specific Formatting**: Optimized for Twitter, LinkedIn, Instagram
- **Interactive Refinement**: Multi-turn content improvement
- **Trending Topics**: Automatic trend detection and suggestions

## 🛠️ Technical Stack

### Backend Framework

- FastAPI for high-performance API endpoints
- Python 3.8+ for core logic

### AI Models & Services

- OpenAI for text generation
- Flux for image generation
- Replicate AI for video generation
- ImgFlip for meme generation

### News & Data Sources

- NewsAPI for current events
- Perplexity API for deep research
- Vectara for data storage and query

## 🚀 Getting Started

### Prerequisites

python 3.8+
pip
git

### Installation

1. Clone the repository

2. Install dependencies

```
pip install -r requirements.txt
```

3. Set up environment variables (.env)

```
OPENAI_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_token_here
DEEPINFRA_TOKEN=your_token_here
IMGFLIP_USERNAME=your_username
IMGFLIP_PASSWORD=your_password
```

4. Start the server

```
uvicorn server:app --reload
```

## 📚 API Documentation

### Content Generation Endpoints

#### Generate Text

```
POST /generate_text
{
"prompt": "string"
}
```

#### Generate Meme

```
POST /generate_meme
{
"prompt": "string"
}
```

#### Generate Video

```
POST /generate_video
{
"prompt": "string"
}
```

#### Generate Image

```
POST /generate_image
{
"prompt": "string"
}
```

### Utility Endpoints

#### Get Enhanced Prompt

```
POST /get_prompt
{
"input": "string",
"tone": "string",
"type": "string",
"platform": "string"
}
```

#### Get Trending Topics

```
GET /trending
```

#### Refine Prompt

```
POST /refine
{
"prompt": "string",
"refine": "string"
}
```

## 📁 Project Structure

```
Backend/
├── server.py # Main FastAPI application
├── news_processor.py # News processing logic
├── requirements.txt # Project dependencies
├── agents/
│ ├── text_generator.py # Text generation agent
│ ├── meme_generator.py # Meme generation agent
│ ├── video_generator.py # Video generation agent
│ ├── image_generator.py # Image generation agent
│ └── news_swarm.py # News processing swarm
└── utils/
├── news_search.py # News search utilities
└── vectara_client.py # Vector store client
```

## 🏆 Challenge Specific Features

### RAG Implementation

- Advanced news article retrieval and vectorization
- Context-aware content generation
- Comprehensive source citation management

### Agentic Behavior

- Smart task prioritization
- Interactive multi-turn refinement
- Proactive content suggestions

### Bonus Features

- ✅ AI-powered video generation
- ✅ Template-based meme creation
- ✅ Dynamic content format selection
- ✅ Unified post preview interface

## 📄 License

This project is licensed under the CC-BY-NC-ND License

## 🙏 Acknowledgments

- Challenge organizers for the opportunity
- Vectara for vector store capabilities
- Groq for compute resources
- OpenAI for AI models
- Replicate for video generation
- ImgFlip for meme templates
- All other sponsors and contributors

---

<div align="center">

_This project was created as part of the AI Agents / RAG Challenge 2024_

</div>
