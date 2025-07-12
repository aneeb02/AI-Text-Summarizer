from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from enhanced_agent import EnhancedTextSummarizerAgent
import os
import json
from datetime import datetime
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize Bootstrap
bootstrap = Bootstrap5(app)

# Initialize the AI agent
try:
    agent = EnhancedTextSummarizerAgent()
    agent_initialized = True
except Exception as e:
    print(f"Failed to initialize agent: {e}")
    agent = None
    agent_initialized = False

@app.route('/')
def index():
    """Main page with the summarization interface"""
    return render_template('index.html', agent_initialized=agent_initialized)

@app.route('/about')
def about():
    """About page explaining the agent capabilities"""
    if agent_initialized:
        stats = agent.get_agent_stats()
        return render_template('about.html', stats=stats)
    else:
        return render_template('about.html', stats=None)

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint for text summarization"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'success': False
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'error': 'Empty text provided',
                'success': False
            }), 400
        
        # Get parameters
        max_length = data.get('max_length', None)
        style = data.get('style', 'professional')
        include_sentiment = data.get('include_sentiment', True)
        include_keywords = data.get('include_keywords', True)
        
        # Validate max_length
        if max_length is not None:
            try:
                max_length = int(max_length)
                if max_length < 10 or max_length > 1000:
                    return jsonify({
                        'error': 'Max length must be between 10 and 1000 words',
                        'success': False
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'error': 'Invalid max_length value',
                    'success': False
                }), 400
        
        # Validate style
        valid_styles = ['professional', 'casual', 'bullet_points', 'technical']
        if style not in valid_styles:
            return jsonify({
                'error': f'Invalid style. Must be one of: {", ".join(valid_styles)}',
                'success': False
            }), 400
        
        # Perform summarization with analysis
        result = agent.summarize_with_analysis(
            text=text,
            max_length=max_length,
            style=style,
            include_sentiment=include_sentiment,
            include_keywords=include_keywords
        )
        
        if result.get('error'):
            return jsonify({
                'error': result['error'],
                'success': False
            }), 500
        
        # Format response
        response = {
            'success': True,
            'summary': result['summary'],
            'metadata': {
                'original_length': result['original_length'],
                'summary_length': result['summary_length'],
                'compression_ratio': result['compression_ratio'],
                'model_used': result['model_used'],
                'style': result['style'],
                'timestamp': result['timestamp']
            }
        }
        
        # Add sentiment analysis if included
        if include_sentiment and 'sentiment_analysis' in result:
            response['sentiment_analysis'] = result['sentiment_analysis']
        
        # Add keywords if included
        if include_keywords and 'keywords' in result:
            response['keywords'] = result['keywords']
        
        return jsonify(response)
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in summarize endpoint: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.route('/api/batch-summarize', methods=['POST'])
def api_batch_summarize():
    """API endpoint for batch text summarization"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'No texts provided',
                'success': False
            }), 400
        
        texts = data['texts']
        if not isinstance(texts, list) or len(texts) == 0:
            return jsonify({
                'error': 'Texts must be a non-empty list',
                'success': False
            }), 400
        
        if len(texts) > 10:
            return jsonify({
                'error': 'Maximum 10 texts allowed per batch',
                'success': False
            }), 400
        
        # Get parameters
        max_length = data.get('max_length', None)
        style = data.get('style', 'professional')
        include_sentiment = data.get('include_sentiment', True)
        include_keywords = data.get('include_keywords', True)
        
        # Process batch
        results = agent.batch_summarize(
            texts=texts,
            max_length=max_length,
            style=style,
            include_sentiment=include_sentiment,
            include_keywords=include_keywords
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results)
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in batch summarize endpoint: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.route('/api/sentiment', methods=['POST'])
def api_sentiment():
    """API endpoint for sentiment analysis only"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'success': False
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'error': 'Empty text provided',
                'success': False
            }), 400
        
        # Perform sentiment analysis
        result = agent.analyze_sentiment(text)
        
        if result.get('error'):
            return jsonify({
                'error': result['error'],
                'success': False
            }), 500
        
        return jsonify({
            'success': True,
            'sentiment_analysis': result
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in sentiment endpoint: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.route('/api/keywords', methods=['POST'])
def api_keywords():
    """API endpoint for keyword extraction only"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'success': False
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'error': 'Empty text provided',
                'success': False
            }), 400
        
        max_keywords = data.get('max_keywords', 10)
        
        # Perform keyword extraction
        keywords = agent.extract_keywords(text, max_keywords)
        
        return jsonify({
            'success': True,
            'keywords': keywords
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in keywords endpoint: {error_msg}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.route('/api/models')
def api_models():
    """API endpoint to get available models"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        models = agent.get_available_models()
        return jsonify({
            'success': True,
            'models': models,
            'current_model': agent.model_name
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in models endpoint: {error_msg}")
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint to get agent statistics"""
    if not agent_initialized:
        return jsonify({
            'error': 'AI Agent not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        stats = agent.get_agent_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in stats endpoint: {error_msg}")
        return jsonify({
            'error': f'An unexpected error occurred: {error_msg}',
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting AI Agent Web Interface...")
    print(f"📡 Agent Status: {'✅ Initialized' if agent_initialized else '❌ Not Initialized'}")
    
    if not agent_initialized:
        print("⚠️  Make sure you have:")
        print("   1. Installed required packages: pip install -r requirements.txt")
        print("   2. Set up your .env file with GROQ_API_KEY")
        print("   3. Downloaded TextBlob corpora: python -m textblob.download_corpora")
    
    app.run(debug=True, port=5000)
