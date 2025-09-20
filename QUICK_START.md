# Quick Setup Instructions
# ========================

# Since you're using uv for dependency management:

## Method 1: Set API key and run with uv
export GROQ_API_KEY="your_api_key_here"
uv run streamlit run streamlit_app.py

## Method 2: One-liner with API key
GROQ_API_KEY="your_api_key_here" uv run streamlit run streamlit_app.py

## Method 3: Use .env file (recommended)
# Create a .env file in project root:
echo "GROQ_API_KEY=your_api_key_here" > .env
uv run streamlit run streamlit_app.py

## Method 4: Activate uv environment and run script
uv sync  # Make sure deps are installed
source .venv/bin/activate  # uv creates .venv by default
export GROQ_API_KEY="your_api_key_here"
./run_app.sh
