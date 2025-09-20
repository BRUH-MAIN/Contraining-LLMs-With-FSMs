#!/usr/bin/env python3
"""
LaTeX Math FSM - Streamlit App Launcher (Python)
===============================================

Alternative launcher for systems where bash scripts might have issues.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_and_install_streamlit():
    """Check if streamlit is available, install if not."""
    try:
        import streamlit
        print("✅ Streamlit is available!")
        return True
    except ImportError:
        print("📥 Streamlit not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("\n💡 Try creating a virtual environment:")
            print("   python3 -m venv venv")
            print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            print("   pip install -r requirements.txt")
            print("   python launch_app.py")
            return False

def main():
    """Main launcher function."""
    print("🧮 LaTeX Math FSM - Python Launcher")
    print("===================================")
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found. Please run from the project directory.")
        sys.exit(1)
    
    # Check and install dependencies
    if not check_and_install_streamlit():
        sys.exit(1)
    
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n⚠️  GROQ_API_KEY not set. LLM features will be disabled.")
        print("   To enable LLM features, set your API key:")
        print("   export GROQ_API_KEY='your_api_key_here'")
        print()
    
    # Launch Streamlit
    print("🚀 Launching Streamlit app...")
    print("   The app will open in your default browser")
    print("   Press Ctrl+C to stop the app")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
