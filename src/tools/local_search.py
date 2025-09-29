# src/tools/local_search.py - Search Tools
import asyncio
import time
import sys
import os
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.settings import settings

class Source:
    def __init__(self, title, url, content, relevance_score, source_type="web", publish_date=None):
        self.title = title
        self.url = url
        self.content = content
        self.relevance_score = relevance_score
        self.source_type = source_type
        self.publish_date = publish_date

class LocalSearchTool:
    def __init__(self):
        self.rate_limiter = RateLimiter(settings.REQUESTS_PER_MINUTE)
        self._check_available_engines()
    
    def _check_available_engines(self):
        self.engines = {}
        
        # Skip DuckDuckGo completely
        self.engines['duckduckgo'] = False
        
        try:
            import arxiv
            self.engines['arxiv'] = True
            print("✅ arXiv academic search available")
        except ImportError:
            self.engines['arxiv'] = False
            print("⚠️  arXiv not available - install with: conda install arxiv")
        
        try:
            import wikipedia
            self.engines['wikipedia'] = True
            print("✅ Wikipedia search available")
        except ImportError:
            self.engines['wikipedia'] = False
            print("⚠️  Wikipedia not available - install with: conda install wikipedia-api")
    
    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        print(f"🔍 Searching for: {query}")
        all_sources = []
        
        # Search arXiv (academic papers)  
        if self.engines.get('arxiv') and settings.ENABLE_ARXIV:
            academic_sources = await self._search_arxiv(query, max_results // 2)
            all_sources.extend(academic_sources)
        
        # Search Wikipedia (encyclopedia)
        if self.engines.get('wikipedia') and settings.ENABLE_WIKIPEDIA:
            wiki_sources = await self._search_wikipedia(query, max_results // 2)
            all_sources.extend(wiki_sources)
        
        # If no search engines available, provide demo data
        if not all_sources and not any(self.engines.values()):
            print("⚠️  No search engines available - using demo data")
            return self._get_demo_sources(query)
        
        # Remove duplicates and return best results
        unique_sources = self._remove_duplicates(all_sources)
        return unique_sources[:max_results]
    
    async def _search_arxiv(self, query: str, max_results: int) -> List[Source]:
        sources = []
        try:
            import arxiv
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            for paper in client.results(search):
                source = Source(
                    title=paper.title,
                    url=paper.entry_id,
                    content=paper.summary,
                    relevance_score=0.9,
                    source_type="academic",
                    publish_date=paper.published.strftime("%Y-%m-%d") if paper.published else None
                )
                sources.append(source)
            
            print(f"   ✅ Found {len(sources)} academic papers")
        except Exception as e:
            print(f"   ❌ Academic search failed: {e}")
        
        return sources
    
    async def _search_wikipedia(self, query: str, max_results: int) -> List[Source]:
        sources = []
        try:
            import wikipedia
            search_results = wikipedia.search(query, results=max_results)
            
            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    source = Source(
                        title=page.title,
                        url=page.url,
                        content=page.summary,
                        relevance_score=0.7,
                        source_type="encyclopedia"
                    )
                    sources.append(source)
                except wikipedia.exceptions.DisambiguationError as e:
                    try:
                        page = wikipedia.page(e.options[0])
                        source = Source(
                            title=page.title,
                            url=page.url,
                            content=page.summary,
                            relevance_score=0.6,
                            source_type="encyclopedia"
                        )
                        sources.append(source)
                    except:
                        continue
                except:
                    continue
            
            print(f"   ✅ Found {len(sources)} Wikipedia articles")
        except Exception as e:
            print(f"   ❌ Wikipedia search failed: {e}")
        
        return sources
    
    def _get_demo_sources(self, query: str) -> List[Source]:
        return [
            Source(
                title=f"Introduction to {query}",
                url="https://demo.example.com/intro",
                content=f"This is an introductory overview of {query}. This demo content shows what a real research source would look like. In actual use, this would be replaced with real search results from arXiv and Wikipedia.",
                relevance_score=0.7,
                source_type="web"
            ),
            Source(
                title=f"Academic Research on {query}",
                url="https://demo.example.com/academic",
                content=f"Academic research demonstrates that {query} involves multiple complex factors and considerations. This demo content represents what would normally be an academic paper from arXiv with detailed research findings.",
                relevance_score=0.8,
                source_type="academic"
            )
        ]
    
    def _remove_duplicates(self, sources: List[Source]) -> List[Source]:
        seen_urls = set()
        unique_sources = []
        
        for source in sources:
            if source.url not in seen_urls:
                seen_urls.add(source.url)
                unique_sources.append(source)
        
        return unique_sources
    
    async def extract_content(self, url: str) -> str:
        # Since we're not using web scraping anymore, just return empty
        return ""

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    async def wait(self):
        now = time.time()
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.requests.append(now)
# src/tools/local_search.py - Free Search Tools (No API Keys!)
import asyncio
import time
import sys
import os
from typing import List, Dict, Any


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.settings import settings

class Source:
    def __init__(self, title, url, content, relevance_score, source_type="web", publish_date=None):
        self.title = title
        self.url = url
        self.content = content
        self.relevance_score = relevance_score
        self.source_type = source_type
        self.publish_date = publish_date

class LocalSearchTool:
    def __init__(self):
        self.rate_limiter = RateLimiter(settings.REQUESTS_PER_MINUTE)
        self._check_available_engines()
    
    def _check_available_engines(self):
        self.engines = {}
        
        
        self.engines['duckduckgo'] = False
        
        try:
            import arxiv
            self.engines['arxiv'] = True
            print("✅ arXiv academic search available")
        except ImportError:
            self.engines['arxiv'] = False
            print("⚠️  arXiv not available - install with: conda install arxiv")
        
        try:
            import wikipedia
            self.engines['wikipedia'] = True
            print("✅ Wikipedia search available")
        except ImportError:
            self.engines['wikipedia'] = False
            print("⚠️  Wikipedia not available - install with: conda install wikipedia-api")
    
    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        print(f"🔍 Searching for: {query}")
        all_sources = []
        
        if self.engines.get('arxiv') and settings.ENABLE_ARXIV:
            academic_sources = await self._search_arxiv(query, max_results // 4)
            all_sources.extend(academic_sources)
        
        if self.engines.get('wikipedia') and settings.ENABLE_WIKIPEDIA:
            wiki_sources = await self._search_wikipedia(query, max_results // 4)
            all_sources.extend(wiki_sources)
        
        if not all_sources and not any(self.engines.values()):
            print("⚠️  No search engines available - using demo data")
            return self._get_demo_sources(query)
        
        unique_sources = self._remove_duplicates(all_sources)
        return unique_sources[:max_results]
         
    async def _search_arxiv(self, query: str, max_results: int) -> List[Source]:
        sources = []
        try:
            import arxiv
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            for paper in client.results(search):
                source = Source(
                    title=paper.title,
                    url=paper.entry_id,
                    content=paper.summary,
                    relevance_score=0.9,
                    source_type="academic",
                    publish_date=paper.published.strftime("%Y-%m-%d") if paper.published else None
                )
                sources.append(source)
            
            print(f"   ✅ Found {len(sources)} academic papers")
        except Exception as e:
            print(f"   ❌ Academic search failed: {e}")
        
        return sources
    
    async def _search_wikipedia(self, query: str, max_results: int) -> List[Source]:
        sources = []
        try:
            import wikipedia
            search_results = wikipedia.search(query, results=max_results)
            
            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    source = Source(
                        title=page.title,
                        url=page.url,
                        content=page.summary,
                        relevance_score=0.7,
                        source_type="encyclopedia"
                    )
                    sources.append(source)
                except:
                    continue
            
            print(f"   ✅ Found {len(sources)} Wikipedia articles")
        except Exception as e:
            print(f"   ❌ Wikipedia search failed: {e}")
        
        return sources
    
    def _get_demo_sources(self, query: str) -> List[Source]:
        return [
            Source(
                title=f"Introduction to {query}",
                url="https://demo.example.com/intro",
                content=f"This is an introductory overview of {query}. This demo content shows what a real research source would look like.",
                relevance_score=0.7,
                source_type="web"
            ),
            Source(
                title=f"Academic Research on {query}",
                url="https://demo.example.com/academic",
                content=f"Academic research demonstrates that {query} involves multiple complex factors and considerations.",
                relevance_score=0.8,
                source_type="academic"
            )
        ]
    
    def _remove_duplicates(self, sources: List[Source]) -> List[Source]:
        seen_urls = set()
        unique_sources = []
        
        for source in sources:
            if source.url not in seen_urls:
                seen_urls.add(source.url)
                unique_sources.append(source)
        
        return unique_sources
    
    async def extract_content(self, url: str) -> str:
        if url.startswith('https://demo.example.com'):
            return ""
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            await self.rate_limiter.wait()
            
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                        element.decompose()
                    
                    text = soup.get_text()
                    clean_text = ' '.join(text.split())
                    
                    return clean_text[:5000]
        except Exception as e:
            print(f"   ⚠️  Could not extract content from {url}: {e}")
        
        return ""
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    async def wait(self):
        now = time.time()
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.requests.append(now)
