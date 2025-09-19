## Local Research Agent

A privacy-focused research assistant powered by Meta-Llama-3-8B-Instruct running locally via Anaconda AI Navigator. This agent combines academic search capabilities with AI-powered analysis to generate comprehensive research reports while maintaining the privacy of all your data.


## Featuress

### Core Capabilities
- **Local AI Processing**: Uses Meta-Llama-3-8B-Instruct running locally via Anaconda AI Navigator
- **Multi-Source Research**: Searches arXiv academic papers and Wikipedia articles
- **AI-Powered Analysis**: Evaluates source relevance and synthesizes information
- **Citation Generation**: Creates properly formatted academic citations (APA style)
- **Research Reports**: Generates comprehensive, structured research summaries
- **Privacy First**: All processing happens locally - no data sent to external services

### Interface Options
- **Web Interface**: Beautiful, responsive Flask-based web application
- **Jupyter Notebook**: Interactive notebook interface for development
- **Command Line**: Direct Python API access
- **RESTful API**: HTTP endpoints for integration with other tools

### Technical Features
- **Anaconda Integration**: Leverages Anaconda's secure package governance
- **Async Processing**: Non-blocking search and analysis operations
- **Research History**: Tracks previous queries with confidence scores
- **Source Filtering**: Relevance scoring and intelligent source selection
- **Configurable**: Adjustable parameters for different use cases

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │ Jupyter Notebook│    │   Command Line  │
│    (Flask)      │    │    Interface    │    │   Interface     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Research Agent        │
                    │      (Core Logic)         │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     Local LLM Tool       │
                    │   (Model Interface)      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  Anaconda AI Navigator    │
                    │   (Meta-Llama-3-8B)      │
                    └───────────────────────────┘

    ┌─────────────────┐              ┌─────────────────┐
    │   arXiv API     │              │  Wikipedia API  │
    │ (Academic Papers│              │ (Encyclopedia)  │
    └─────────────────┘              └─────────────────┘
```

## Requirements

### Software Requirements
- **Python**: 3.8 or higher
- **Anaconda AI Navigator**: With Meta-Llama-3-8B-Instruct model loaded
- **Operating System**: macOS, Linux, or Windows

### Hardware Requirements
- **RAM**: Minimum 8GB (16GB+ recommended for better performance)
- **Storage**: 2GB free space for dependencies
- **GPU**: Optional but recommended (CUDA or Metal support for faster inference)
- **CPU**: Multi-core processor recommended for concurrent operations

### Network Requirements
- Internet connection for initial package installation
- Internet access for arXiv and Wikipedia searches (search operations only)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd research_agent
```

### 2. Set Up Anaconda Environment
```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate research_agent_local
```

### 3. Install Additional Dependencies
```bash
# Core packages
pip install arxiv wikipedia-api aiohttp beautifulsoup4 flask requests

# Jupyter support (optional)
pip install jupyter ipywidgets
```

### 4. Set Up Anaconda AI Navigator
1. Launch Anaconda AI Navigator
2. Load the Meta-Llama-3-8B-Instruct model
3. Start the local inference server (should run on http://127.0.0.1:8080)
4. Verify the model is running and accessible

### 5. Initialize Project Structure
```bash
# Create required directories
mkdir -p data/vector_store data/research_cache outputs/reports logs models

# Set up Python path (for development)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Configuration

### Basic Configuration
The main configuration is in `config/settings.py`:

```python
# Model settings
MODEL_API_URL = "http://127.0.0.1:8080"  # Your Anaconda AI Navigator
MODEL_NAME = "Meta-Llama-3-8B-Instruct_Q4_K_M.gguf"

# AI parameters
TEMPERATURE = 0.3          # Response creativity (0.0-1.0)
MAX_TOKENS = 1500          # Maximum response length
DEFAULT_MAX_SOURCES = 5    # Sources per research query

# Search settings
ENABLE_ARXIV = True        # Academic papers
ENABLE_WIKIPEDIA = True    # Encyclopedia articles
```

### Environment Variables
You can override settings using environment variables:

```bash
export MODEL_API_URL="http://127.0.0.1:8080"
export MAX_SOURCES="7"
export TEMPERATURE="0.2"
```

### Hardware Optimization
For different hardware setups:

```python
# GPU-optimized (in config/settings.py)
N_GPU_LAYERS = -1          # Use all GPU layers
USE_MLOCK = True           # Lock in GPU memory

# CPU-optimized
N_GPU_LAYERS = 0           # CPU only
N_THREADS = 8              # CPU threads to use
```

## Usage

### Web Interface

#### Option 1: Standalone Web Server
```bash
python web_app.py
```
Then open http://127.0.0.1:7860 in your browser.

#### Option 2: Jupyter Notebook
```python
# In a Jupyter cell
import os
os.chdir('/path/to/research_agent')

# Run the web interface cell
exec(open('jupyter_web_interface.py').read())
```

### Command Line Interface
```bash
# Interactive research mode
python main.py

# Run demo queries
python main.py demo

# Single query
python -c "
from src.agent import get_research_agent
import asyncio

async def research():
    agent = get_research_agent()
    result = await agent.research('machine learning transformers')
    print(result.report)

asyncio.run(research())
"
```

### Python API
```python
from src.agent import get_research_agent
import asyncio

# Initialize agent
agent = get_research_agent()

# Conduct research
async def main():
    result = await agent.research(
        query="renewable energy benefits",
        max_sources=7
    )
    
    print(f"Report: {result.report}")
    print(f"Sources: {len(result.sources)}")
    print(f"Confidence: {result.confidence_score}")

asyncio.run(main())
```

### Jupyter Notebook Interface
```python
# Cell 1: Setup
import os
os.chdir('/path/to/research_agent')

from src.agent import get_research_agent
agent = get_research_agent()

# Cell 2: Research
result = await agent.research("quantum computing algorithms")

# Cell 3: Display results
from IPython.display import display, Markdown
display(Markdown(result.report))
```

## Project Structure

```
research_agent/
├── README.md                  # This file
├── environment.yml           # Conda environment specification
├── main.py                   # Command line interface
├── web_app.py               # Flask web interface
├── requirements.txt          # Python dependencies
│
├── config/                  # Configuration files
│   ├── __init__.py
│   └── settings.py          # Main configuration
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── agent.py             # Main research agent
│   ├── tools/               # Tool modules
│   │   ├── __init__.py
│   │   ├── local_llm.py     # LLM interface
│   │   └── local_search.py  # Search tools
│   ├── utils/               # Utility functions
│   └── memory/              # Memory/storage components
│
├── data/                    # Data storage
│   ├── vector_store/        # Semantic search database
│   ├── research_cache/      # Cached search results
│   └── raw/                 # Raw data files
│
├── outputs/                 # Generated outputs
│   └── reports/             # Research reports
│
├── logs/                    # Log files
├── models/                  # Model files (if using local GGUF)
├── tests/                   # Unit tests
└── docs/                    # Documentation
```

## API Reference

### Research Agent API

#### `get_research_agent()`
Creates and returns a research agent instance.

#### `agent.research(query, max_sources=5)`
Conducts research on a given query.

**Parameters:**
- `query` (str): Research question
- `max_sources` (int): Maximum number of sources to analyze

**Returns:**
```python
ResearchResult(
    query: str,                 # Original query
    report: str,               # Generated research report
    sources: List[Source],     # List of sources used
    citations: List[str],      # Formatted citations
    confidence_score: float,   # Quality score (0.0-1.0)
    research_time: float      # Time taken in seconds
)
```

### Web API Endpoints

#### `POST /research`
Conducts research via HTTP API.

**Request:**
```json
{
    "query": "machine learning transformers",
    "max_sources": 5
}
```

**Response:**
```json
{
    "success": true,
    "query": "machine learning transformers",
    "report": "...",
    "sources": [...],
    "citations": [...],
    "confidence_score": 0.85,
    "research_time": 45.2
}
```

#### `GET /status`
Returns system status and model information.

#### `GET /history`
Returns research history for the current session.

## Troubleshooting

### Common Issues

#### Model Connection Issues
```bash
# Check if Anaconda AI Navigator is running
curl http://127.0.0.1:8080/health

# Expected response: HTTP 200 OK
```

#### Import Errors in Jupyter
```python
# Ensure you're in the correct directory
import os
os.chdir('/path/to/research_agent')

# Add to Python path
import sys
sys.path.append(os.getcwd())
```

#### Port Already in Use
```bash
# Find process using port 7860
lsof -ti:7860

# Kill the process
kill $(lsof -ti:7860)

# Or use a different port
python web_app.py --port 7861
```

#### Search Engine Issues
```bash
# Test arXiv connectivity
python -c "import arxiv; print('arXiv OK')"

# Test Wikipedia connectivity  
python -c "import wikipedia; print('Wikipedia OK')"

# Install missing packages
pip install arxiv wikipedia-api
```

#### Memory Issues
For systems with limited RAM:

```python
# In config/settings.py
MAX_SOURCES_PER_QUERY = 3    # Reduce sources
MAX_TOKENS = 800            # Reduce response length
N_CTX = 2048               # Reduce context window
```

### Performance Optimization

#### GPU Acceleration
```python
# Enable GPU layers (config/settings.py)
N_GPU_LAYERS = -1          # Use all available GPU layers
USE_MLOCK = True           # Lock model in GPU memory
```

#### CPU Optimization
```python
# Optimize for CPU-only systems
N_GPU_LAYERS = 0           # Disable GPU
N_THREADS = os.cpu_count() # Use all CPU cores
USE_MMAP = True           # Memory map model file
```

#### Network Optimization
```python
# Adjust request limits for slower connections
REQUESTS_PER_MINUTE = 10   # Slower request rate
SEARCH_TIMEOUT = 15        # Longer timeout
```

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export RESEARCH_DEBUG=1
```

### Getting Help

1. **Check the logs**: Look in `logs/` directory for error messages
2. **Verify model status**: Use the status endpoint or web interface
3. **Test components individually**: Test search, LLM, and agent separately
4. **Check system resources**: Ensure adequate RAM and CPU availability

## Contributing

### Development Setup
```bash
# Install development dependencies
pip install -e .
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Format code
black src/ tests/
```

### Code Structure Guidelines
- **Modularity**: Keep components loosely coupled
- **Async Support**: Use asyncio for I/O operations
- **Error Handling**: Implement comprehensive error handling
- **Documentation**: Document all public APIs
- **Testing**: Write tests for new features

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## Security Considerations

### Data Privacy
- All AI processing occurs locally on your machine
- Search queries are sent to arXiv and Wikipedia APIs
- No personal data or research results are transmitted to external services
- Research history is stored locally only

### Network Security
- Web interface binds to localhost only (127.0.0.1)
- No external network access required for core functionality
- API endpoints are not exposed to external networks

### Model Security
- Uses Anaconda's governed model repository
- Model runs in isolated local environment
- No model data transmitted over network

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- **Anaconda**: For providing secure AI model governance and infrastructure
- **Meta**: For the Llama 3 language model
- **arXiv**: For providing access to academic research papers
- **Wikimedia**: For Wikipedia's open knowledge base
- **Open Source Community**: For the various libraries that make this project possible

---

**Note**: This project prioritizes privacy and local processing. While it requires internet connectivity for searching academic papers and Wikipedia articles, all AI processing and analysis happens locally on your machine.

