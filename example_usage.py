#!/usr/bin/env python3
"""
Simple example showing how to use the TextSummarizerAgent
"""

from text_summarizer_agent import TextSummarizerAgent

def main():
    # Initialize the agent
    agent = TextSummarizerAgent()
    
    # Example 1: Basic summarization
    print("=" * 60)
    print("EXAMPLE 1: Basic Text Summarization")
    print("=" * 60)
    
    article = """
    The rise of remote work has fundamentally changed how businesses operate and how employees 
    approach their careers. What began as a temporary response to the global pandemic has evolved 
    into a permanent shift in workplace culture. Companies that once insisted on in-person 
    collaboration have discovered that many tasks can be completed just as effectively from home.
    
    This transformation has brought both opportunities and challenges. On the positive side, 
    employees enjoy greater flexibility, reduced commuting time, and better work-life balance. 
    Companies benefit from access to a global talent pool and reduced overhead costs associated 
    with maintaining large office spaces.
    
    However, remote work also presents obstacles. Communication can become more difficult, 
    company culture may suffer, and some employees struggle with isolation and maintaining 
    boundaries between work and personal life. Additionally, certain collaborative tasks 
    and creative processes may be more challenging to execute remotely.
    
    As we move forward, the future of work will likely involve a hybrid model that combines 
    the benefits of both remote and in-person work, allowing organizations to adapt to the 
    changing needs of their workforce while maintaining productivity and innovation.
    """
    
    result = agent.summarize(article, max_length=80)
    print(f"Original text: {result['original_length']} words")
    print(f"Summary: {result['summary_length']} words")
    print(f"Compression ratio: {result['compression_ratio']}x")
    print(f"\nSummary:\n{result['summary']}")
    
    # Example 2: Different styles
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Different Summarization Styles")
    print("=" * 60)
    
    short_text = """
    Machine learning is a subset of artificial intelligence that enables computers to learn 
    and improve from experience without being explicitly programmed. It involves algorithms 
    that can identify patterns in data and make predictions or decisions based on those patterns. 
    Common applications include image recognition, natural language processing, recommendation 
    systems, and autonomous vehicles. The field has grown rapidly due to increased computational 
    power and the availability of large datasets.
    """
    
    styles = ["professional", "casual", "bullet_points"]
    
    for style in styles:
        print(f"\n--- {style.upper()} STYLE ---")
        result = agent.summarize(short_text, max_length=50, style=style)
        print(result['summary'])

if __name__ == "__main__":
    main()
