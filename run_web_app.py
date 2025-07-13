#!/usr/bin/env python3
"""
Launcher script for the AI Text Summarizer Web Application
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'flask': 'flask',
        'textblob': 'textblob',
        'groq': 'groq',
        'python-dotenv': 'dotenv',
        'bootstrap-flask': 'flask_bootstrap'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and contains required variables"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your GROQ_API_KEY")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY' not in content:
            print("❌ GROQ_API_KEY not found in .env file!")
            print("Please add your Groq API key to the .env file")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 AI Text Summarizer Web Application Launcher")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")
    
    # Check environment file
    print("🔍 Checking environment configuration...")
    if not check_env_file():
        sys.exit(1)
    print("✅ Environment configuration OK")
    
    # Check TextBlob corpora
    print("🔍 Checking TextBlob corpora...")
    try:
        import textblob
        # Test if corpora are available
        textblob.TextBlob("test").sentiment
        print("✅ TextBlob corpora available")
    except Exception as e:
        print(f"❌ TextBlob corpora not available: {e}")
        print("Please run: python -m textblob.download_corpora")
        sys.exit(1)
    
    print("\n🎯 Starting web application...")
    print("📱 The web interface will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run( host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
