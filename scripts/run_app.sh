#!/bin/bash

# LaTeX Math FSM - Streamlit App Launcher
# =====================================

echo "🧮 LaTeX Math FSM - Starting Streamlit App"
echo "=========================================="

# Virtual environment setup
VENV_DIR="venv"

# Check for existing virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "� Found existing virtual environment at $VENV_DIR"
elif [ -d ".venv" ]; then
    echo "📁 Found existing virtual environment at .venv"
    VENV_DIR=".venv"
elif [ ! -z "$VIRTUAL_ENV" ]; then
    echo "🔧 Using currently active virtual environment: $VIRTUAL_ENV"
    VENV_DIR=""
else
    echo "❌ No virtual environment found."
    echo "   Please activate your existing virtual environment first:"
    echo "   source your_venv/bin/activate"
    echo "   Or create a new one:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    exit 1
fi

# Activate virtual environment if we found one
if [ ! -z "$VENV_DIR" ]; then
    echo "🔧 Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to activate virtual environment at $VENV_DIR"
        exit 1
    fi
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        exit 1
    fi
    echo "✅ Dependencies installed!"
else
    echo "✅ Streamlit found!"
fi

# Check for Groq API key
if [ -z "$GROQ_API_KEY" ]; then
    echo ""
    echo "⚠️  GROQ_API_KEY not set. LLM features will be disabled."
    echo "   To enable LLM features, set your API key:"
    echo "   export GROQ_API_KEY='your_api_key_here'"
    echo ""
fi

# Launch the app
echo "🚀 Launching Streamlit app..."
echo "   The app will open in your default browser"
echo "   Press Ctrl+C to stop the app"
echo ""

streamlit run streamlit_app.py
