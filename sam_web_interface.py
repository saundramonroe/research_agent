# web_app.py - Improved Flask Web Interface with Better Bullet Point Formatting
from flask import Flask, render_template_string, request, jsonify
import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from src.agent import get_research_agent
from config.settings import settings

app = Flask(__name__)
research_agent = None

def initialize_agent():
    global research_agent
    if research_agent is None:
        try:
            research_agent = get_research_agent()
            return True, "Research agent initialized successfully!"
        except Exception as e:
            return False, f"Failed to initialize agent: {str(e)}"
    return True, "Research agent already initialized"

# Improved HTML Template with Better Bullet Point Styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Research Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .main-content { padding: 30px; }
        
        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .tab {
            padding: 15px 25px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .tab:hover { background: #f8f9fa; }
        .tab.active { border-bottom-color: #667eea; color: #667eea; }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .research-form {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .form-group { margin-bottom: 20px; }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        input[type="text"], textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .search-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .search-btn:hover { transform: translateY(-2px); }
        .search-btn:disabled { opacity: 0.6; transform: none; cursor: not-allowed; }
        
        .results { margin-top: 30px; }
        
        .result-section {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .result-section h3 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
            font-size: 1.3em;
        }
        
        .result-section h4 {
            color: #444;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.1em;
            font-weight: 600;
        }
        
        /* IMPROVED BULLET POINT STYLING */
        .result-section ul {
            margin: 15px 0;
            padding-left: 40px;
        }
        
        .result-section ol {
            margin: 15px 0;
            padding-left: 40px;
        }
        
        .result-section li {
            margin-bottom: 12px;
            padding-left: 8px;
            line-height: 1.7;
        }
        
        .result-section ul li {
            list-style-type: disc;
            list-style-position: outside;
        }
        
        .result-section ol li {
            list-style-type: decimal;
            list-style-position: outside;
        }
        
        /* Nested lists */
        .result-section ul ul, .result-section ol ul {
            margin: 8px 0;
            padding-left: 25px;
        }
        
        .result-section ul ol, .result-section ol ol {
            margin: 8px 0;
            padding-left: 25px;
        }
        
        /* Better paragraph spacing */
        .result-section p {
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        /* Pre-formatted text styling */
        .result-section pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            overflow-x: auto;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .source-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        
        .source-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .source-meta {
            color: #666;
            font-size: 14px;
        }
        
        .samples {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .samples h4 {
            color: #1976d2;
            margin-bottom: 15px;
        }
        
        .sample-query {
            background: white;
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .sample-query:hover {
            background: #f0f8ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Local Research Agent Powered by Anaconda</h1>
            <p>Powered by Meta-Llama-3-8B-Instruct via Anaconda AI Catalog</p>
            <p>Sources: arXiv Academic Papers + Wikipedia | Everything runs locally!</p>
        </div>
        
        <div class="main-content">
            <div class="tabs">
                <div class="tab active" onclick="showTab('research')">🔍 Research</div>
                <div class="tab" onclick="showTab('status')">📊 Status</div>
                <div class="tab" onclick="showTab('history')">📚 History</div>
                <div class="tab" onclick="showTab('about')">ℹ️ About</div>
            </div>
            
            <div id="research" class="tab-content active">
                <div class="research-form">
                    <div class="form-group">
                        <label for="query">Research Query</label>
                        <textarea id="query" rows="3" placeholder="Enter your research question (e.g., 'machine learning transformers', 'renewable energy benefits')"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="maxSources">Maximum Sources</label>
                        <select id="maxSources">
                            <option value="3">3 sources</option>
                            <option value="5" selected>5 sources</option>
                            <option value="7">7 sources</option>
                            <option value="10">10 sources</option>
                        </select>
                    </div>
                    
                    <button class="search-btn" onclick="startResearch()">🔍 Start Research</button>
                </div>
                
                <div class="samples">
                    <h4>💡 Sample Queries</h4>
                    <div class="sample-query" onclick="setQuery('machine learning transformers')">Academic: "machine learning transformers"</div>
                    <div class="sample-query" onclick="setQuery('quantum computing algorithms')">Science: "quantum computing algorithms"</div>
                    <div class="sample-query" onclick="setQuery('renewable energy benefits')">General: "renewable energy benefits"</div>
                    <div class="sample-query" onclick="setQuery('artificial intelligence ethics')">Technology: "artificial intelligence ethics"</div>
                </div>
                
                <div id="results" class="results"></div>
            </div>
            
            <div id="status" class="tab-content">
                <div class="result-section">
                    <h3>📊 System Status</h3>
                    <div id="statusContent">Click "Refresh Status" to check system status...</div>
                    <br>
                    <button class="search-btn" onclick="checkStatus()">🔄 Refresh Status</button>
                </div>
            </div>
            
            <div id="history" class="tab-content">
                <div class="result-section">
                    <h3>📚 Research History</h3>
                    <div id="historyContent">Click "Refresh History" to view past research...</div>
                    <br>
                    <button class="search-btn" onclick="loadHistory()">🔄 Refresh History</button>
                </div>
            </div>
            
            <div id="about" class="tab-content">
                <div class="result-section">
                    <h3>About Local Research Agent</h3>
                    <p>This research agent combines packages from Anaconda’s Secure Governance with policy enforcement with local secure models to provide comprehensive research capabilities.</p>
                    
                    <h4>Anaconda AI Platform Technology Stack</h4>
                    <ul>
                        <li><strong>Language Model:</strong> Via Anaconda’s secure and governed model repository Meta-Llama-3-8B-Instruct (running locally)</li>
                       <li><strong>Package and Environment Management:</strong> Enabled by packages with Anaconda Secure Governance</li>
                        <li><strong>Academic Search:</strong> arXiv API for scientific papers</li>
                        <li><strong>General Knowledge:</strong> Wikipedia API for encyclopedic information</li>
                        <li><strong>Interface:</strong> Flask web framework for user-friendly interface</li>
                    </ul>
                    
                    <h4>How It Works</h4>
                    <ol>
                        <li><strong>Search Phase:</strong> Queries arXiv and Wikipedia for relevant sources</li>
                        <li><strong>Analysis Phase:</strong> Your local Llama 3 model evaluates source relevance</li>
                        <li><strong>Synthesis Phase:</strong> Generates comprehensive research reports</li>
                        <li><strong>Citation Phase:</strong> Creates properly formatted citations</li>
                    </ol>
                    
                    <h4>Privacy & Security</h4>
                    <ul>
                        <li>Everything runs locally on your machine</li>
                        <li>No data sent to external APIs (except for source searching)</li>
                        <li>Your queries and results stay private</li>
                        <li>No API keys required</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            const tabButtons = document.querySelectorAll('.tab');
            tabButtons.forEach(button => button.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function setQuery(query) {
            document.getElementById('query').value = query;
        }
        
        async function startResearch() {
            const query = document.getElementById('query').value.trim();
            const maxSources = document.getElementById('maxSources').value;
            const resultsDiv = document.getElementById('results');
            const searchBtn = document.querySelector('.search-btn');
            
            if (!query) {
                alert('Please enter a research query');
                return;
            }
            
            searchBtn.disabled = true;
            searchBtn.textContent = '🔄 Researching...';
            resultsDiv.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Conducting research on: "${query}"</p>
                    <p>This may take 30-60 seconds...</p>
                </div>
            `;
            
            try {
                const response = await fetch('/research', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, max_sources: parseInt(maxSources) })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultsDiv.innerHTML = `
                        <div class="result-section">
                            <h3>📝 Research Report</h3>
                            <div style="white-space: pre-wrap;">${data.report}</div>
                        </div>
                        
                        <div class="result-section">
                            <h3>📚 Sources (${data.sources.length})</h3>
                            ${data.sources.map((source, i) => `
                                <div class="source-item">
                                    <div class="source-title">${i + 1}. ${source.title}</div>
                                    <div class="source-meta">
                                        Type: ${source.source_type} | 
                                        Relevance: ${source.relevance_score.toFixed(2)} | 
                                        <a href="${source.url}" target="_blank">View Source</a>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div class="result-section">
                            <h3>📖 Citations</h3>
                            ${data.citations.map((citation, i) => `<p>${i + 1}. ${citation}</p>`).join('')}
                        </div>
                        
                        <div class="result-section">
                            <h3>📊 Research Summary</h3>
                            <p><strong>Query:</strong> ${data.query}</p>
                            <p><strong>Research Time:</strong> ${data.research_time.toFixed(1)} seconds</p>
                            <p><strong>Confidence Score:</strong> ${data.confidence_score.toFixed(2)}/1.0</p>
                            <p><strong>Sources Found:</strong> ${data.sources.length}</p>
                        </div>
                    `;
                } else {
                    resultsDiv.innerHTML = `
                        <div class="result-section">
                            <h3>❌ Error</h3>
                            <p>${data.error}</p>
                        </div>
                    `;
                }
            } catch (error) {
                resultsDiv.innerHTML = `
                    <div class="result-section">
                        <h3>❌ Error</h3>
                        <p>Failed to conduct research: ${error.message}</p>
                    </div>
                `;
            } finally {
                searchBtn.disabled = false;
                searchBtn.textContent = '🔍 Start Research';
            }
        }
        
        async function checkStatus() {
            const statusDiv = document.getElementById('statusContent');
            statusDiv.innerHTML = 'Loading status...';
            
            try {
                const response = await fetch('/status');
                const data = await response.json();
                statusDiv.innerHTML = `<pre>${data.status}</pre>`;
            } catch (error) {
                statusDiv.innerHTML = `Error loading status: ${error.message}`;
            }
        }
        
        async function loadHistory() {
            const historyDiv = document.getElementById('historyContent');
            historyDiv.innerHTML = 'Loading history...';
            
            try {
                const response = await fetch('/history');
                const data = await response.json();
                historyDiv.innerHTML = `<pre>${data.history}</pre>`;
            } catch (error) {
                historyDiv.innerHTML = `Error loading history: ${error.message}`;
            }
        }
        
        document.getElementById('query').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                startResearch();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/research', methods=['POST'])
def research():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        max_sources = data.get('max_sources', 5)
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'})
        
        if research_agent is None:
            success, msg = initialize_agent()
            if not success:
                return jsonify({'success': False, 'error': msg})
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(research_agent.research(query, max_sources=max_sources))
        finally:
            loop.close()
        
        return jsonify({
            'success': True,
            'query': result.query,
            'report': result.report,
            'sources': [{
                'title': s.title,
                'url': s.url,
                'source_type': s.source_type.title(),
                'relevance_score': s.relevance_score
            } for s in result.sources],
            'citations': result.citations,
            'confidence_score': result.confidence_score,
            'research_time': result.research_time
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/status')
def status():
    try:
        if research_agent is None:
            success, msg = initialize_agent()
            if not success:
                return jsonify({'status': msg})
        
        status = research_agent.get_model_status()
        
        status_text = f"""📊 MODEL STATUS
LLM Connected: {'✅ Yes' if status['llm_loaded'] else '❌ No'}
Search Available: {'✅ Yes' if status['search_available'] else '❌ No'}
"""
        
        if status['model_info']:
            info = status['model_info']
            status_text += f"""
Model: {info.get('model_name', 'Unknown')}
API Server: {info.get('api_url', 'Unknown')}
Server Type: {info.get('server_type', 'Unknown')}
"""
        
        return jsonify({'status': status_text})
    except Exception as e:
        return jsonify({'status': f'Error getting status: {str(e)}'})

@app.route('/history')
def history():
    try:
        if research_agent is None:
            return jsonify({'history': 'Agent not initialized'})
        
        history = research_agent.get_research_history()
        if not history:
            return jsonify({'history': '📚 No research history yet. Start by asking a question!'})
        
        history_text = f"📚 Research History ({len(history)} queries)\n\n"
        for i, result in enumerate(history, 1):
            history_text += f"{i}. {result.query}\n"
            history_text += f"   Confidence: {result.confidence_score:.2f}\n"
            history_text += f"   Sources: {len(result.sources)}\n"
            history_text += f"   Time: {result.research_time:.1f}s\n\n"
        
        return jsonify({'history': history_text})
    except Exception as e:
        return jsonify({'history': f'Error getting history: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Initializing research agent for web interface...")
    init_success, init_message = initialize_agent()
    print(init_message)
    
    print(f"\n🌐 Starting Local Research Agent Web Interface")
    print(f"📍 Server: http://127.0.0.1:{settings.GRADIO_SERVER_PORT}")
    print(f"🔒 Local only - not accessible from internet")
    print(f"💡 Press Ctrl+C to stop")
    
    app.run(host=settings.GRADIO_SERVER_NAME, port=settings.GRADIO_SERVER_PORT, debug=False)


