import os
from groq import Groq
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
from textblob import TextBlob
import re
from datetime import datetime

class EnhancedTextSummarizerAgent:
    """
    Enhanced AI Agent with sentiment analysis and web interface support.
    Uses Groq's API with Llama models for summarization and TextBlob for sentiment analysis.
    """
    
    def __init__(self, model_name: str = "llama3-8b-8192"):
        """
        Initialize the Enhanced Text Summarizer Agent
        
        Args:
            model_name: The Groq model to use (default: llama3-8b-8192)
        """
       
        # Initialize Groq client
        self.api_key = "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"
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        
        # Agent configuration
        self.system_prompt = """You are a professional text summarizer with analytical capabilities. Your task is to:
1. Read the provided text carefully
2. Extract the key points and main ideas
3. Create a concise, coherent summary
4. Maintain the original meaning while reducing length
5. Use clear, professional language
6. Be aware of the emotional tone and context

Keep summaries informative but concise."""

        # Sentiment analysis configuration
        self.sentiment_labels = {
            'positive': {'threshold': 0.1, 'emoji': '😊', 'color': 'success'},
            'negative': {'threshold': -0.1, 'emoji': '😞', 'color': 'danger'},
            'neutral': {'threshold': 0.0, 'emoji': '😐', 'color': 'secondary'}
        }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of the provided text
        
        Args:
            text: The text to analyze
            
        Returns:
            Dict containing sentiment analysis results
        """
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            
            # Get polarity (-1 to 1) and subjectivity (0 to 1)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment label
            if polarity > self.sentiment_labels['positive']['threshold']:
                sentiment_label = 'positive'
            elif polarity < self.sentiment_labels['negative']['threshold']:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
            
            # Get additional info
            sentiment_info = self.sentiment_labels[sentiment_label]
            
            # Calculate confidence (distance from neutral)
            confidence = abs(polarity)
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment_label,
                'emoji': sentiment_info['emoji'],
                'color': sentiment_info['color'],
                'confidence': round(confidence, 3),
                'description': self._get_sentiment_description(polarity, subjectivity)
            }
            
        except Exception as e:
            return {
                'error': f"Failed to analyze sentiment: {str(e)}",
                'sentiment': 'unknown'
            }

    def _get_sentiment_description(self, polarity: float, subjectivity: float) -> str:
        """Generate human-readable sentiment description"""
        # Determine polarity description
        if polarity > 0.5:
            pol_desc = "very positive"
        elif polarity > 0.1:
            pol_desc = "positive"
        elif polarity < -0.5:
            pol_desc = "very negative"
        elif polarity < 0:
            pol_desc = "negative"
        else:
            pol_desc = "neutral"
        
        # Determine subjectivity description
        if subjectivity > 0.7:
            subj_desc = "highly subjective"
        elif subjectivity > 0.3:
            subj_desc = "moderately subjective"
        else:
            subj_desc = "objective"
        
        return f"The text is {pol_desc} and {subj_desc}."

    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract key phrases from text using simple NLP techniques
        
        Args:
            text: The text to extract keywords from
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keywords/phrases
        """
        try:
            # Clean and normalize text
            text = re.sub(r'[^\w\s]', '', text.lower())
            words = text.split()
            
            # Remove common stop words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
                'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
                'her', 'its', 'our', 'their', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
                'above', 'below', 'between', 'among', 'through', 'during', 'before', 'after', 'above', 'below'
            }
            
            # Filter words
            filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
            
            # Count frequency
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top keywords
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in keywords[:max_keywords]]
            
        except Exception as e:
            return [f"Error extracting keywords: {str(e)}"]

    def summarize_with_analysis(self, text: str, max_length: Optional[int] = None, 
                              style: str = "professional", include_sentiment: bool = True,
                              include_keywords: bool = True) -> Dict[str, Any]:
        """
        Summarize text with comprehensive analysis
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary (in words)
            style: Style of summary ("professional", "casual", "bullet_points")
            include_sentiment: Whether to include sentiment analysis
            include_keywords: Whether to include keyword extraction
            
        Returns:
            Dict containing summary, sentiment analysis, and keywords
        """
        try:
            # Get basic summary
            summary_result = self.summarize(text, max_length, style)
            
            # Add timestamp
            summary_result['timestamp'] = datetime.now().isoformat()
            
            # Add sentiment analysis if requested
            if include_sentiment:
                sentiment_result = self.analyze_sentiment(text)
                summary_result['sentiment_analysis'] = sentiment_result
            
            # Add keyword extraction if requested
            if include_keywords:
                keywords = self.extract_keywords(text)
                summary_result['keywords'] = keywords
            
            return summary_result
            
        except Exception as e:
            return {
                'error': f"Failed to analyze text: {str(e)}",
                'summary': None,
                'timestamp': datetime.now().isoformat()
            }

    def summarize(self, text: str, max_length: Optional[int] = None, style: str = "professional") -> Dict[str, Any]:
        """
        Summarize the provided text (original method enhanced)
        
        Args:
            text: The text to summarize
            max_length: Optional maximum length for the summary (in words)
            style: Style of summary ("professional", "casual", "bullet_points")
            
        Returns:
            Dict containing the summary and metadata
        """
        try:
            # Prepare the user prompt
            user_prompt = f"Please summarize the following text"
            
            if max_length:
                user_prompt += f" in approximately {max_length} words"
            
            if style == "bullet_points":
                user_prompt += " using bullet points"
            elif style == "casual":
                user_prompt += " in a casual, conversational tone"
            elif style == "technical":
                user_prompt += " focusing on technical details and terminology"
            else:
                user_prompt += " in a professional tone"
            
            user_prompt += f":\n\n{text}"
            
            # Make the API call
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model_name,
                temperature=0.3,  # Lower temperature for more focused summaries
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            
            # Extract the summary
            summary = chat_completion.choices[0].message.content
            
            return {
                "summary": summary,
                "original_length": len(text.split()),
                "summary_length": len(summary.split()),
                "compression_ratio": round(len(text.split()) / len(summary.split()), 2),
                "model_used": self.model_name,
                "style": style
            }
            
        except Exception as e:
            return {
                "error": f"Failed to summarize text: {str(e)}",
                "summary": None
            }

    def batch_summarize(self, texts: list, **kwargs) -> list:
        """
        Summarize multiple texts in batch with analysis
        
        Args:
            texts: List of texts to summarize
            **kwargs: Additional arguments passed to summarize_with_analysis()
            
        Returns:
            List of summary results with analysis
        """
        results = []
        for i, text in enumerate(texts):
            print(f"Processing text {i+1}/{len(texts)}...")
            result = self.summarize_with_analysis(text, **kwargs)
            results.append(result)
        return results

    def get_available_models(self) -> list:
        """
        Get list of available Groq models
        
        Returns:
            List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

    def get_agent_stats(self) -> Dict[str, Any]:
        """
        Get agent statistics and information
        
        Returns:
            Dict containing agent information
        """
        return {
            "model_name": self.model_name,
            "available_styles": ["professional", "casual", "bullet_points", "technical"],
            "features": [
                "Text Summarization",
                "Sentiment Analysis", 
                "Keyword Extraction",
                "Batch Processing",
                "Multiple Output Styles"
            ],
            "sentiment_analysis": {
                "polarity_range": "(-1 to 1)",
                "subjectivity_range": "(0 to 1)",
                "supported_sentiments": ["positive", "negative", "neutral"]
            }
        }

def main():
    """
    Example usage of the EnhancedTextSummarizerAgent
    """
    # Sample texts with different sentiments
    texts = {
        "positive": """
        I absolutely love this new technology! It's incredible how AI has revolutionized 
        our daily lives. The possibilities are endless, and I'm excited to see what 
        amazing innovations will come next. This is truly the future we've been waiting for!
        """,
        
        "negative": """
        I'm really concerned about the rapid advancement of AI. There are serious risks 
        that we're not addressing properly. Job displacement, privacy concerns, and 
        ethical issues are mounting. We need to be much more careful about how we 
        develop and deploy these technologies.
        """,
        
        "neutral": """
        Artificial intelligence is a field of computer science that aims to create 
        systems capable of performing tasks that typically require human intelligence. 
        These systems use algorithms and data to make decisions, recognize patterns, 
        and solve problems. The technology has applications in various industries 
        including healthcare, finance, and transportation.
        """
    }
    
    try:
        # Initialize the enhanced agent
        print("🚀 Initializing Enhanced Text Summarizer Agent...")
        agent = EnhancedTextSummarizerAgent()
        
        print(f"✅ Agent initialized successfully!")
        print(f"📡 Using model: {agent.model_name}")
        print("=" * 60)
        
        # Test sentiment analysis on different texts
        for sentiment_type, text in texts.items():
            print(f"\n🔍 Analyzing {sentiment_type.upper()} text...")
            result = agent.summarize_with_analysis(text, max_length=50)
            
            if result.get("error"):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"📝 Summary: {result['summary']}")
                
                if 'sentiment_analysis' in result:
                    sentiment = result['sentiment_analysis']
                    print(f"💭 Sentiment: {sentiment['emoji']} {sentiment['sentiment'].upper()}")
                    print(f"    Polarity: {sentiment['polarity']} | Subjectivity: {sentiment['subjectivity']}")
                    print(f"    {sentiment['description']}")
                
                if 'keywords' in result:
                    print(f"🔑 Keywords: {', '.join(result['keywords'][:5])}")
                
                print(f"📊 Stats: {result['original_length']} → {result['summary_length']} words ({result['compression_ratio']}x)")
                print("-" * 60)
        
        # Show agent capabilities
        print("\n🛠️ Agent Capabilities:")
        stats = agent.get_agent_stats()
        for feature in stats['features']:
            print(f"   ✓ {feature}")
            
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("Make sure you have:")
        print("1. Installed required packages: pip install -r requirements.txt")
        print("2. Set up your .env file with GROQ_API_KEY")

if __name__ == "__main__":
    main()
