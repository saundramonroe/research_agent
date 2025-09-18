# src/agent.py - Research Agent with your local API
import asyncio
import time
import sys
import os
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.settings import settings

@dataclass
class Source:
    title: str
    url: str
    content: str
    relevance_score: float
    source_type: str = "web"
    publish_date: Optional[str] = None

@dataclass
class ResearchResult:
    query: str
    report: str
    sources: List[Source]
    citations: List[str]
    confidence_score: float
    research_time: float

class LocalResearchAgent:
    def __init__(self):
        print("🤖 Initializing Local Research Agent with your Llama 3 model...")
        self.llm = None
        self.search_tool = None
        self.research_history = []
        self._initialize_tools()
    
    def _initialize_tools(self):
        try:
            from src.tools.local_llm import get_local_llm
            self.llm = get_local_llm()
            print("✅ Local LLM connected")
            
            from src.tools.local_search import LocalSearchTool
            self.search_tool = LocalSearchTool()
            print("✅ Search tools initialized")
        except Exception as e:
            print(f"❌ Error initializing tools: {e}")
            raise
    
    async def research(self, query: str, max_sources: int = None) -> ResearchResult:
        start_time = time.time()
        max_sources = max_sources or settings.DEFAULT_MAX_SOURCES
        
        print(f"\n🔍 Starting research on: {query}")
        print("=" * 50)
        
        try:
            print("📚 Step 1: Searching for sources...")
            sources = await self.search_tool.search(query, max_sources)
            
            if not sources:
                return ResearchResult(
                    query=query,
                    report="❌ No sources found for this query.",
                    sources=[],
                    citations=[],
                    confidence_score=0.0,
                    research_time=time.time() - start_time
                )
            
            print(f"   Found {len(sources)} initial sources")
            
            print("🎯 Step 2: Evaluating source relevance...")
            enhanced_sources = await self._enhance_sources(query, sources)
            
            best_sources = self._filter_best_sources(enhanced_sources, max_sources)
            print(f"   Selected {len(best_sources)} high-quality sources")
            
            print("📝 Step 3: Generating research report...")
            report = await self._generate_report(query, best_sources)
            
            print("📖 Step 4: Creating citations...")
            citations = self._generate_citations(best_sources)
            
            confidence = self._calculate_confidence(best_sources)
            research_time = time.time() - start_time
            
            result = ResearchResult(
                query=query,
                report=report,
                sources=best_sources,
                citations=citations,
                confidence_score=confidence,
                research_time=research_time
            )
            
            self.research_history.append(result)
            
            print(f"✅ Research completed in {research_time:.1f} seconds")
            print(f"   Confidence Score: {confidence:.2f}")
            print("=" * 50)
            
            return result
            
        except Exception as e:
            print(f"❌ Research failed: {e}")
            return ResearchResult(
                query=query,
                report=f"❌ Research failed due to error: {str(e)}",
                sources=[],
                citations=[],
                confidence_score=0.0,
                research_time=time.time() - start_time
            )
    
    async def _enhance_sources(self, query: str, sources):
        enhanced_sources = []
        
        for i, source in enumerate(sources):
            print(f"   Evaluating source {i+1}/{len(sources)}: {source.title[:50]}...")
            
            if source.source_type == "web":
                try:
                    full_content = await self.search_tool.extract_content(source.url)
                    if full_content and len(full_content) > len(source.content):
                        source.content = full_content
                except:
                    pass
            
            if self.llm and self.llm.model_loaded:
                try:
                    relevance = self.llm.evaluate_source_relevance(query, source.content)
                    source.relevance_score = relevance
                except:
                    pass
            
            enhanced_sources.append(source)
        
        return enhanced_sources
    
    def _filter_best_sources(self, sources, max_sources: int):
        sorted_sources = sorted(sources, key=lambda s: s.relevance_score, reverse=True)
        return sorted_sources[:max_sources]
    
    async def _generate_report(self, query: str, sources):
        if not sources:
            return "No sources available to generate report."
        
        sources_text = ""
        for i, source in enumerate(sources, 1):
            sources_text += f"\nSource {i} - {source.title} ({source.source_type}):\n"
            sources_text += f"{source.content[:1000]}...\n"
            sources_text += f"URL: {source.url}\n"
            sources_text += "-" * 40 + "\n"
        
        if self.llm and self.llm.model_loaded:
            try:
                report = self.llm.generate_research_summary(query, sources_text)
                return report
            except Exception as e:
                print(f"   ⚠️  LLM report generation failed: {e}")
        
        fallback_report = f"# Research Report: {query}\n\n"
        fallback_report += f"Based on {len(sources)} sources, here are the key findings:\n\n"
        
        for i, source in enumerate(sources, 1):
            fallback_report += f"## Finding {i}: {source.title}\n"
            fallback_report += f"**Source:** {source.source_type.title()}\n"
            fallback_report += f"**Relevance:** {source.relevance_score:.2f}\n\n"
            fallback_report += f"{source.content[:500]}...\n\n"
        
        return fallback_report
    
    def _generate_citations(self, sources):
        citations = []
        
        for source in sources:
            try:
                source_info = {
                    'title': source.title,
                    'url': source.url,
                    'source_type': source.source_type,
                    'publish_date': source.publish_date
                }
                
                if self.llm and self.llm.model_loaded:
                    try:
                        citation = self.llm.generate_citation(source_info, settings.DEFAULT_CITATION_STYLE)
                        citations.append(citation)
                        continue
                    except:
                        pass
                
                if source.source_type == "academic":
                    citation = f"{source.title}. arXiv. Retrieved from {source.url}"
                elif source.source_type == "encyclopedia":
                    citation = f"{source.title}. Wikipedia. Retrieved from {source.url}"
                else:
                    citation = f"{source.title}. Retrieved from {source.url}"
                
                citations.append(citation)
            except Exception as e:
                citations.append(f"Citation error for: {source.title}")
        
        return citations
    
    def _calculate_confidence(self, sources):
        if not sources:
            return 0.0
        
        avg_relevance = sum(s.relevance_score for s in sources) / len(sources)
        source_types = len(set(s.source_type for s in sources))
        diversity_score = min(source_types / 3.0, 1.0)
        count_score = min(len(sources) / 5.0, 1.0)
        academic_count = sum(1 for s in sources if s.source_type == "academic")
        academic_bonus = min(academic_count / len(sources), 0.2)
        
        confidence = (avg_relevance * 0.4 + diversity_score * 0.2 + count_score * 0.2 + academic_bonus * 0.2)
        return min(confidence, 1.0)
    
    def get_research_history(self):
        return self.research_history.copy()
    
    def get_model_status(self):
        status = {
            "llm_loaded": self.llm and self.llm.model_loaded if self.llm else False,
            "search_available": bool(self.search_tool),
            "model_info": {}
        }
        
        if self.llm:
            status["model_info"] = self.llm.get_model_info()
        
        return status

_research_agent = None

def get_research_agent():
    global _research_agent
    if _research_agent is None:
        _research_agent = LocalResearchAgent()
    return _research_agent
