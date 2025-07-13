import os
import sys

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

def main():
    """Main launcher function"""
    print("🚀 AI Text Summarizer Web Application Launcher")
    print("=" * 50)

    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")

    # Check TextBlob corpora
    print("🔍 Checking TextBlob corpora...")
    try:
        import textblob
        textblob.TextBlob("test").sentiment
        print("✅ TextBlob corpora available")
    except Exception as e:
        print(f"❌ TextBlob corpora not available: {e}")
        print("Please run: python -m textblob.download_corpora")
        sys.exit(1)

    print("\n🎯 Starting web application...")
    print("🌐 Web interface will be available at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)

    # Start Flask app
    try:
        from app import app
        port = int(os.environ.get("PORT", 8000))
        app.run(host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
