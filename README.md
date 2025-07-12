# AI Text Summarizer Agent

An enhanced AI Agent built with Python that uses Groq's API and Llama models for text summarization, sentiment analysis, and keyword extraction. This project demonstrates how to create a comprehensive AI agent with both command-line and web interfaces.

## Features

- **Text Summarization**: Multiple styles (professional, casual, bullet-point, technical)
- **Sentiment Analysis**: Polarity and subjectivity analysis with emoji indicators
- **Keyword Extraction**: Automatic extraction of key terms and phrases
- **Web Interface**: Modern, responsive web UI with Bootstrap
- **API Endpoints**: RESTful API for programmatic access
- **Batch Processing**: Process multiple texts at once
- **Compression Metrics**: Track original vs. summary length and compression ratios
- **Model Selection**: Support for different Groq/Llama models

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

### 4. Run the Application

**Option A: Web Interface (Recommended)**
```bash
# Launch the web application
python run_web_app.py

# Then visit: http://localhost:5000
```

**Option B: Command Line**
```bash
# Test the basic agent
python text_summarizer_agent.py

# Test the enhanced agent with sentiment analysis
python enhanced_agent.py

# Run usage examples
python example_usage.py
```

## Usage

### Web Interface

1. **Launch the web app**: `python run_web_app.py`
2. **Open your browser**: Visit `http://localhost:5000`
3. **Use the interface**: 
   - Enter text to summarize
   - Choose style (professional, casual, bullet_points, technical)
   - Set max length (optional)
   - Enable/disable sentiment analysis and keyword extraction
   - Click "Summarize" to get results

### Command Line Usage

#### Basic Agent
```python
from text_summarizer_agent import TextSummarizerAgent

# Initialize the agent
agent = TextSummarizerAgent()

# Summarize text
text = "Your long text here..."
result = agent.summarize(text, max_length=100, style="professional")

print(result["summary"])
print(f"Compression: {result['compression_ratio']}x")
```

#### Enhanced Agent with Sentiment Analysis
```python
from enhanced_agent import EnhancedTextSummarizerAgent

# Initialize the enhanced agent
agent = EnhancedTextSummarizerAgent()

# Comprehensive analysis
result = agent.summarize_with_analysis(
    text=text,
    max_length=100,
    style="professional",
    include_sentiment=True,
    include_keywords=True
)

print(f"Summary: {result['summary']}")
print(f"Sentiment: {result['sentiment_analysis']['sentiment']} {result['sentiment_analysis']['emoji']}")
print(f"Keywords: {', '.join(result['keywords'][:5])}")
```

### API Usage

The web application also provides REST API endpoints:

```bash
# Summarize text
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here...",
    "style": "professional",
    "max_length": 100,
    "include_sentiment": true,
    "include_keywords": true
  }'

# Sentiment analysis only
curl -X POST http://localhost:5000/api/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'

# Keyword extraction only
curl -X POST http://localhost:5000/api/keywords \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here...", "max_keywords": 10}'
```

## How It Works

### 1. Agent Architecture

The `TextSummarizerAgent` class follows a simple but effective pattern:

- **Initialization**: Sets up the Groq client and model configuration
- **System Prompt**: Defines the agent's role and behavior
- **Processing**: Handles the text summarization logic
- **Response**: Returns structured results with metadata

### 2. Key Components

```python
class TextSummarizerAgent:
    def __init__(self, model_name="llama3-8b-8192"):
        # Initialize Groq client
        # Set up system prompt
        # Configure model parameters
    
    def summarize(self, text, max_length=None, style="professional"):
        # Prepare prompts
        # Make API call
        # Process response
        # Return structured result
```

### 3. System Prompt Design

The agent uses a carefully crafted system prompt that:
- Defines the agent's role as a professional summarizer
- Provides clear instructions for the summarization task
- Ensures consistent output quality
- Maintains the original text's meaning

## Customization

### Adding New Features

1. **Custom Styles**: Add new summarization styles by modifying the `summarize()` method
2. **Different Models**: Change the model by passing a different `model_name` parameter
3. **Advanced Prompts**: Modify the `system_prompt` for specialized use cases
4. **Output Formats**: Extend the return dictionary with additional metadata

### Example: Adding a "Technical" Style

```python
# In the summarize method
if style == "technical":
    user_prompt += " focusing on technical details and terminology"
```

## Available Models

The agent supports various Groq models:
- `llama3-8b-8192` (default)
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

## Error Handling

The agent includes comprehensive error handling:
- API key validation
- Network error handling
- Malformed response handling
- Graceful degradation with error messages

## Best Practices

1. **API Key Security**: Always use environment variables for API keys
2. **Rate Limiting**: Be mindful of API rate limits for batch processing
3. **Text Length**: Very long texts may hit token limits
4. **Model Selection**: Choose appropriate models based on your needs (speed vs. quality)

## Next Steps

This basic agent can be extended with:
- **Web Interface**: Build a Flask/FastAPI web app
- **File Processing**: Handle PDFs, Word documents, etc.
- **Streaming**: Implement real-time summarization
- **Caching**: Add result caching for efficiency
- **Multi-language**: Support for different languages
- **Sentiment Analysis**: Add sentiment detection
- **Keyword Extraction**: Include key phrase identification

## Contributing

Feel free to extend this agent with new features! Some ideas:
- Add support for more output formats
- Implement different summarization algorithms
- Add text preprocessing capabilities
- Create a command-line interface

## License

This project is provided as-is for educational purposes.
