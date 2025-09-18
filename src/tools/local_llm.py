# src/tools/local_llm.py - Using your Anaconda AI Navigator API server
import os
import sys
import logging
import requests
from typing import Optional, List, Dict, Any

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.settings import settings

logger = logging.getLogger(__name__)

class LocalLLM:
    """Local Language Model using your Anaconda AI Navigator API server"""
    
    def __init__(self):
        # Your model is running on port 8080, not the default Ollama port
        self.api_url = "http://127.0.0.1:8080"
        self.model_name = "Meta-Llama-3-8B-Instruct_Q4_K_M.gguf"  # From your screenshot
        self.model_loaded = False
        self._test_connection()
        
    def _test_connection(self):
        """Test if we can connect to your model API"""
        try:
            # Test the health endpoint
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                self.model_loaded = True
                print("✅ Connected to your local Llama 3 model API!")
                print(f"   Model: {self.model_name}")
                print(f"   Server: {self.api_url}")
            else:
                print(f"⚠️  API responded with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to model API at {self.api_url}")
            print("   Make sure your Anaconda AI Navigator model is running")
            print(f"   Error: {e}")
    
    def generate_research_summary(self, query: str, sources_text: str, max_length: int = 1500) -> str:
        """Generate a research summary based on query and sources"""
        
        if not self.model_loaded:
            return "❌ Model API not available. Please start your model in Anaconda AI Navigator."
        
        system_message = """You are a professional research assistant. Your task is to analyze multiple sources and create a comprehensive, well-structured research report.

Guidelines:
- Write in clear, academic prose
- Synthesize information from all sources
- Include key findings and insights
- Maintain objectivity and cite important points
- Structure with clear sections and conclusions"""

        user_prompt = f"""Research Query: {query}

Available Sources:
{sources_text}

Please create a comprehensive research report that:
1. Addresses the research query directly
2. Synthesizes key information from all sources
3. Provides clear insights and analysis
4. Maintains academic rigor

Research Report:"""

        return self._generate_response(user_prompt, system_message, max_length)
    
    def generate_citation(self, source_info: Dict[str, Any], style: str = "apa") -> str:
        """Generate proper citation for a source"""
        
        if not self.model_loaded:
            # Simple fallback citation
            return f"{source_info.get('title', 'Unknown')}. Retrieved from {source_info.get('url', 'Unknown URL')}"
        
        system_message = f"You are a citation expert. Generate a proper {style.upper()} style citation for the given source."
        
        user_prompt = f"""Source Information:
Title: {source_info.get('title', 'Unknown Title')}
URL: {source_info.get('url', 'No URL')}
Source Type: {source_info.get('source_type', 'web')}
Publication Date: {source_info.get('publish_date', 'No date available')}

Generate a {style.upper()} citation:"""

        return self._generate_response(user_prompt, system_message, 200)
    
    def evaluate_source_relevance(self, query: str, source_content: str) -> float:
        """Evaluate how relevant a source is to the research query (0.0 to 1.0)"""
        
        if not self.model_loaded:
            # Simple keyword matching fallback
            query_words = set(query.lower().split())
            content_words = set(source_content.lower().split())
            overlap = len(query_words.intersection(content_words))
            return min(overlap / len(query_words), 1.0) if query_words else 0.0
        
        system_message = """You are a research evaluation expert. Rate how relevant a source is to a research query on a scale of 0.0 to 1.0, where:
- 1.0 = Extremely relevant, directly addresses the query
- 0.7-0.9 = Highly relevant, covers most aspects
- 0.4-0.6 = Moderately relevant, some useful information
- 0.1-0.3 = Slightly relevant, tangential information
- 0.0 = Not relevant at all

Respond with ONLY the numerical score (e.g., 0.8)"""

        user_prompt = f"""Research Query: {query}

Source Content: {source_content[:1000]}...

Relevance Score:"""

        try:
            response = self._generate_response(user_prompt, system_message, 50)
            # Extract number from response
            import re
            match = re.search(r'(\d+\.?\d*)', response)
            if match:
                score = float(match.group(1))
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
        except:
            pass
        
        # Fallback to keyword matching
        query_words = set(query.lower().split())
        content_words = set(source_content.lower().split())
        overlap = len(query_words.intersection(content_words))
        return min(overlap / len(query_words), 1.0) if query_words else 0.0
    
    def _generate_response(self, prompt: str, system_message: str = None, max_tokens: int = None) -> str:
        """Generate response from your local model API"""
        
        if not self.model_loaded:
            return "❌ Model API not connected"
        
        max_tokens = max_tokens or settings.MAX_TOKENS
        
        try:
            # Format the request for your API server
            # Based on your chat template, we'll format it properly
            if system_message:
                formatted_prompt = f"<|start_header_id|>system<|end_header_id|>\n{system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            else:
                formatted_prompt = f"<|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            
            # API request payload - adjust based on your server's API format
            payload = {
                "prompt": formatted_prompt,
                "max_tokens": max_tokens,
                "temperature": settings.TEMPERATURE,
                "top_p": settings.TOP_P,
                "top_k": settings.TOP_K,
                "repeat_penalty": settings.REPEAT_PENALTY,
                "stop": ["<|eot_id|>", "<|end_of_text|>"]
            }
            
            # Try common API endpoints
            endpoints_to_try = [
                "/v1/completions",
                "/completions", 
                "/generate",
                "/api/generate"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = requests.post(
                        f"{self.api_url}{endpoint}",
                        json=payload,
                        timeout=60,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Handle different response formats
                        if 'choices' in result:
                            return result['choices'][0].get('text', '').strip()
                        elif 'response' in result:
                            return result['response'].strip()
                        elif 'generated_text' in result:
                            return result['generated_text'].strip()
                        elif 'text' in result:
                            return result['text'].strip()
                        else:
                            print(f"Unknown response format: {result}")
                            
                except requests.exceptions.RequestException:
                    continue  # Try next endpoint
            
            return f"❌ Could not get response from model API"
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"❌ Error generating response: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "model_name": self.model_name,
            "api_url": self.api_url,
            "model_loaded": self.model_loaded,
            "server_type": "Anaconda AI Navigator",
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS
        }

# Global instance for the research agent
_local_llm_instance = None

def get_local_llm() -> LocalLLM:
    """Get or create the global LocalLLM instance"""
    global _local_llm_instance
    if _local_llm_instance is None:
        _local_llm_instance = LocalLLM()
    return _local_llm_instance