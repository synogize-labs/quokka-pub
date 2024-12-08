import os
from dotenv import load_dotenv
import requests
import json
from typing import Dict, List, Optional
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectaraClient:
    def __init__(self):
        load_dotenv()
        
        # Validate API key
        self.api_key = os.getenv("VECTARA_API_KEY")
        if not self.api_key:
            raise ValueError("VECTARA_API_KEY must be set in environment variables")
        
        self.base_url = "https://api.vectara.io/v2"
        
        # Try to get existing corpus key from environment
        self.corpus_key = os.getenv("VECTARA_CORPUS_KEY")
        if self.corpus_key:
            logger.info(f"Using existing corpus key from environment: {self.corpus_key}")
        else:
            logger.info("No corpus key found in environment variables")

    def create_corpus(self, name: str, description: str) -> Optional[str]:
        """
        Create a new corpus in Vectara.
        
        Args:
            name: Name of the corpus
            description: Description of the corpus
            
        Returns:
            str: Corpus key if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/corpora"
            
            # Generate corpus key with timestamp to ensure uniqueness
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            corpus_key = f"corpus-{name.lower().replace(' ', '-')}-{timestamp}"
            
            payload = {
                "key": corpus_key,
                "name": name,
                "description": description,
                "queries_are_answers": False,
                "documents_are_questions": False,
                "filter_attributes": [
                    {
                        "name": "source",
                        "level": "document",
                        "description": "Source of the document",
                        "indexed": True,
                        "type": "text"
                    },
                    {
                        "name": "timestamp",
                        "level": "document",
                        "description": "Document timestamp",
                        "indexed": True,
                        "type": "text"
                    }
                ]
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-api-key": self.api_key
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                corpus_data = response.json()
                self.corpus_key = corpus_key
                logger.info(f"Created corpus: {name} (Key: {self.corpus_key})")
                return self.corpus_key
            else:
                logger.error(f"Failed to create corpus: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating corpus: {str(e)}")
            return None

    def upload_markdown(self, file_path: Path, corpus_key: Optional[str] = None) -> bool:
        """
        Upload a markdown file to specified Vectara corpus using multipart/form-data.
        
        Args:
            file_path: Path to the markdown file
            corpus_key: Optional corpus key. Uses self.corpus_key if not provided.
            
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            corpus_key = corpus_key or self.corpus_key
            if not corpus_key:
                raise ValueError("No corpus key provided or set")
            
            url = f"{self.base_url}/corpora/{corpus_key}/upload_file"
            
            # Extract metadata from filename
            filename = file_path.name
            timestamp = filename.split('_')[2].split('.')[0] if '_' in filename else None
            
            # Prepare metadata
            metadata = {
                "source": filename,
                "timestamp": timestamp,
                "contentType": "text/markdown"
            }
            
            # Prepare multipart form data
            files = {
                'file': (
                    filename,
                    open(file_path, 'rb'),
                    'text/markdown'
                ),
                'metadata': (
                    None,
                    json.dumps(metadata),
                    'application/json'
                )
            }
            
            headers = {
                "Accept": "application/json",
                "x-api-key": self.api_key
            }
            
            logger.info(f"Uploading markdown file: {filename} to corpus: {corpus_key}")
            
            response = requests.post(
                url,
                headers=headers,
                files=files
            )
            
            if response.status_code == 201:
                logger.info(f"Document uploaded successfully: {filename}")
                return True
            else:
                logger.error(f"Upload failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading markdown: {str(e)}")
            return False

    def search_content(self, query: str, corpus_key: Optional[str] = None, num_results: int = 5) -> List[Dict]:
        """
        Search content in specified Vectara corpus.
        
        Args:
            query: Search query
            corpus_key: Optional corpus key. Uses self.corpus_key if not provided.
            num_results: Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results with content and metadata
        """
        try:
            corpus_key = corpus_key or self.corpus_key
            if not corpus_key:
                raise ValueError("No corpus key provided or set")
                
            url = f"{self.base_url}/corpora/{corpus_key}/query"
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-api-key": self.api_key
            }
            
            payload = {
                "query": query,
                "search": {
                    "lexical_interpolation": 0.025,
                    "limit": num_results
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                results = []
                response_data = response.json()
                
                for result in response_data.get('search_results', []):
                    results.append({
                        'content': result.get('text', ''),
                        'metadata': result.get('document_metadata', {}),
                        'score': result.get('score', 0),
                        'document_id': result.get('document_id', '')
                    })
                
                return results
            else:
                logger.error(f"Search failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            return []

    def get_or_create_corpus(self, name: str, description: str) -> Optional[str]:
        """
        Get existing corpus key or create a new corpus if none exists.
        
        Args:
            name: Name for new corpus if creation is needed
            description: Description for new corpus if creation is needed
            
        Returns:
            str: Corpus key (existing or newly created), None if creation fails
        """
        if self.corpus_key:
            return self.corpus_key
        
        return self.create_corpus(name, description)

def main():
    """Test the VectaraClient functionality"""
    client = VectaraClient()
    
    # Create a new corpus
    corpus_key = client.get_or_create_corpus(
        name="News Archive",
        description="Archive of news search results and summaries"
    )
    
    if corpus_key:
        # Test uploading a markdown file
        test_file = Path("../logs/news_interaction_20241208_182035.md")
        if test_file.exists():
            success = client.upload_markdown(test_file, corpus_key)
            print(f"Upload {'successful' if success else 'failed'}")
            
            # Test searching
            if success:
                results = client.search_content("What is the latest news on the moon?", corpus_key)
                for result in results:
                    print("\nSearch Result:")
                    print(f"Score: {result['score']}")
                    print(f"Content: {result['content'][:200]}...")
                    print(f"Metadata: {result['metadata']}")
        else:
            print("Failed to upload markdown file")
    else:  
        print("Failed to create corpus")
                    

if __name__ == "__main__":
    main() 