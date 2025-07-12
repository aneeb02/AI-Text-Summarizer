import os
from groq import Groq
from dotenv import load_dotenv
from typing import Optional, Dict, Any

class TextSummarizerAgent:
    """
    A basic AI Agent that uses Groq's API with Llama models to summarize text.
    """
    def __init__(self, model_name: str = "llama3-8b-8192"):
        """
        Initialize the Text Summarizer Agent
        
        Args:
            model_name: The Groq model to use (default: llama3-8b-8192)
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize Groq client
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        
        # Agent configuration
        self.system_prompt = """You are a professional text summarizer. Your task is to:
                                1. Read the provided text carefully
                                2. Extract the key points and main ideas
                                3. Create a concise, coherent summary
                                4. Maintain the original meaning while reducing length
                                5. Use clear, professional language

                                Keep summaries informative but concise."""

    def summarize(self, text: str, max_length: Optional[int] = None, style: str = "professional") -> Dict[str, Any]:
        """
        Summarize the provided text
        
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
        Summarize multiple texts in batch
        
        Args:
            texts: List of texts to summarize
            **kwargs: Additional arguments passed to summarize()
            
        Returns:
            List of summary results
        """
        results = []
        for i, text in enumerate(texts):
            print(f"Processing text {i+1}/{len(texts)}...")
            result = self.summarize(text, **kwargs)
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

def main():
    """
    Example usage of the TextSummarizerAgent
    """
    # Sample text for demonstration
    sample_text = """
    Learn the power of vibe coding and how it pairs perfectly with n8n to build full-stack AI-driven apps.

We just published a crash course on the freeCodeCamp.org YouTube channel that will teach you the power of VibeCoding and how to automate real-world workflows using n8n. This course starts by demystifying what software engineers actually do and introduces you to the VibeCoding movement, which is an approach that blends human creativity with AI-driven automation. Paulo Dichone from Vinci bits created this course.

You’ll learn about the origins of VibeCoding, why it’s accessible to everyone, and how it can transform your approach to building software. The course walks through the entire vibe coding workflow, connecting it to core software engineering principles so you can vibe code like a pro.

A key part of this course is n8n, an open-source workflow automation tool that lets you connect different apps, APIs, and services without writing tons of code. Think of n8n as a visual platform where you can drag, drop, and link together building blocks to automate tasks, process data, and build complex backend systems.

You will learn how to set up n8n, create your first workflows and webhooks, and use AI coding agents to build powerful frontends that interact with your automated backend. Along the way, you’ll tackle real challenges like processing files, handling binary data, and troubleshooting workflow issues.

Here are the different sections covered in this course:

What do Software Engineers do?

Vibe Coding - Who Started This Movement?

Fear Not Vibe Coding - Here’s Why

Vibe Coding - the Full Workflow

Bring it All Together - Vibecoding and Software Engineering Principles - Vibecoding Like an Engineer

LLM and Context - Why Does it Matter?

The Path to Follow when Vibe Coding

How To Think About Vibe Coding to Build Production Applications

Setting up N8N

Basics on N8N - Create your First Workflow and Webhooks

Leveraging AI Coding Agents to Build the Frontend - Intro to Bolt.new - Upload Files to our N8N Backend

Adding an N8N Switch Node to our Backend Workflow - Processing PDF, TXT, and CSV Files

Understanding Binary Files and Troubleshooting N8N Issues

An Overview of the Workflow Architecture - Bulletproofing the Workflow for Further Processing Downstream

Adding a Code Node to our N8N Workflow for Processing Data

Deconstructing the Field Extraction Node Code

Combining Extracted Data through the Code Node

Testing the Workflow - Full File Upload and File Processing Workflow

Final Thoughts and Where to Go From Here

By the end of this course, you’ll have the VibeCoding mindset and a production-ready AI automation system built with n8n and AI tools. Watch the full course on the freeCodeCamp.org YouTube channel (2-hour watch).
    """
    
    try:
        # Initialize the agent
        print("🤖 Initializing Text Summarizer Agent...")
        agent = TextSummarizerAgent()
        
        print(f"✅ Agent initialized successfully!")
        print(f"📡 Using model: {agent.model_name}")
        print("-" * 50)
        
        # Test different summarization styles
        styles = ["professional", "casual", "bullet_points"]
        
        for style in styles:
            print(f"\n📝 Summarizing in {style} style...")
            result = agent.summarize(sample_text, max_length=100, style=style)
            
            if result.get("error"):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Summary ({style}):")
                print(result["summary"])
                print(f"\n📊 Stats:")
                print(f"   Original: {result['original_length']} words")
                print(f"   Summary: {result['summary_length']} words")
                print(f"   Compression: {result['compression_ratio']}x")
                print("-" * 50)
        
        # Show available models
        print("\n🔍 Available models:")
        models = agent.get_available_models()
        for model in models[:5]:  # Show first 5 models
            print(f"   - {model}")
            
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("Make sure you have:")
        print("1. Installed required packages: pip install groq python-dotenv")
        print("2. Set up your .env file with GROQ_API_KEY")

if __name__ == "__main__":
    main()
