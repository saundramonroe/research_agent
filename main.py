# main.py - Simple Interface for Local Research Agent
import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.agent import get_research_agent
from config.settings import settings

def print_banner():
    print("\n" + "="*60)
    print("🤖 LOCAL RESEARCH AGENT")
    print("   Powered by Your Meta-Llama-3-8B-Instruct")
    print("   Connected via Anaconda AI Navigator")
    print("   Sources: arXiv + Wikipedia")
    print("   No API keys needed - Everything runs locally!")
    print("="*60)

def print_model_status(agent):
    status = agent.get_model_status()
    
    print("\n📊 MODEL STATUS:")
    print(f"   LLM Connected: {'✅ Yes' if status['llm_loaded'] else '❌ No'}")
    print(f"   Search Available: {'✅ Yes' if status['search_available'] else '❌ No'}")
    
    if status['model_info']:
        info = status['model_info']
        print(f"   Model: {info.get('model_name', 'Unknown')}")
        print(f"   API Server: {info.get('api_url', 'Unknown')}")

def print_research_result(result):
    print(f"\n📋 RESEARCH REPORT")
    print("="*50)
    print(f"Query: {result.query}")
    print(f"Research Time: {result.research_time:.1f} seconds")
    print(f"Confidence: {result.confidence_score:.2f}/1.0")
    print(f"Sources Found: {len(result.sources)}")
    print("="*50)
    
    print("\n📝 REPORT:")
    print(result.report)
    
    if result.sources:
        print(f"\n📚 SOURCES ({len(result.sources)}):")
        for i, source in enumerate(result.sources, 1):
            print(f"\n{i}. {source.title}")
            print(f"   Type: {source.source_type.title()}")
            print(f"   Relevance: {source.relevance_score:.2f}")
            print(f"   URL: {source.url}")
    
    if result.citations:
        print(f"\n📖 CITATIONS:")
        for i, citation in enumerate(result.citations, 1):
            print(f"{i}. {citation}")

async def interactive_mode():
    print_banner()
    
    print("🚀 Initializing research agent...")
    try:
        agent = get_research_agent()
        print_model_status(agent)
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    print("\n🔍 Enter your research queries (or 'quit' to exit)")
    print("   Academic Examples: 'machine learning transformers', 'quantum computing'")
    print("   General Examples: 'renewable energy benefits', 'how photosynthesis works'")
    
    while True:
        try:
            print("\n" + "-"*30)
            query = input("🔍 Research Query: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Local Research Agent!")
                break
            
            if query.lower() == 'status':
                print_model_status(agent)
                continue
            
            if query.lower() == 'history':
                history = agent.get_research_history()
                print(f"\n📚 Research History ({len(history)} queries):")
                for i, result in enumerate(history, 1):
                    print(f"{i}. {result.query} ({result.confidence_score:.2f} confidence)")
                continue
            
            print(f"\n🔍 Researching: {query}")
            result = await agent.research(query)
            print_research_result(result)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

async def quick_demo():
    print_banner()
    print("🚀 Running Quick Demo...")
    
    try:
        agent = get_research_agent()
        print_model_status(agent)
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    demo_queries = [
        "artificial intelligence",
        "renewable energy",
        "quantum computing"
    ]
    
    for query in demo_queries:
        print(f"\n{'='*60}")
        print(f"🔍 Demo Query: {query}")
        print('='*60)
        
        result = await agent.research(query, max_sources=3)
        print_research_result(result)
        
        input("\n⏸️  Press Enter to continue to next demo...")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        asyncio.run(quick_demo())
    else:
        asyncio.run(interactive_mode())

if __name__ == "__main__":
    main()
