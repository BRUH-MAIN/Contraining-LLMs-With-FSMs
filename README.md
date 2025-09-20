# LaTeX Math FSM - Quick Start

## Overview

This project demonstrates a **token-by-token finite state machine (FSM)** for constraining LaTeX mathematical expressions. The FSM processes each token individually and transitions through states to validate mathematical syntax:

1. **start** → **math_mode** (accepts $, $$, \[)
2. **math_mode** → **superscript/subscript/content** (processes variables, operators, commands)
3. **Various states** for handling fractions, braces, commands, etc.

## Key Features

- ✅ **Token-by-token processing**: FSM moves state by state for each LaTeX token
- ✅ **Real-time validation**: Only valid LaTeX math expressions can complete the FSM path
- ✅ **Comprehensive coverage**: Supports 200+ LaTeX math commands, Greek letters, operators
- ✅ **Multi-model LLM integration**: Support for both Groq API and local Hugging Face models
- ✅ **Automatic fallback**: Seamlessly switch between API and local models
- ✅ **Local model support**: Run google/gemma-2-2b-it locally with GPU acceleration

## Quick Demo

```bash
# Run the LaTeX FSM demo
python3 demo_latex.py

# Run the integration demo showing LLM constraint
python3 main.py

# Run the interactive Streamlit web interface
streamlit run streamlit_app.py
```

## Web Interface

Launch the interactive Streamlit web application:

### Option 1: Using uv (Recommended if you have uv)
```bash
# Install dependencies and run directly
uv run streamlit run streamlit_app.py
```

### Option 2: Automatic Setup with existing venv
```bash
# Use the startup script (detects existing venv)
./run_app.sh
```

### Option 3: Manual Setup
```bash
# Activate your virtual environment first
source .venv/bin/activate  # or your venv path

# Install dependencies if needed
pip install -r requirements.txt

# Set your Groq API key (optional, for LLM features)
export GROQ_API_KEY="your_api_key_here"

# Launch the web interface
streamlit run streamlit_app.py
```

The web interface provides:
- 🔬 **FSM Demo**: Test LaTeX expressions with step-by-step validation
- 🤖 **LLM Generation**: Generate LaTeX using AI with FSM constraints
- 🎯 **Model Selection**: Choose between Groq API, Local Gemma, or Auto mode
- 🔄 **Automatic Fallback**: Seamless switching between available models
- 🗺️ **FSM Visualizer**: Interactive state diagram and current state tracking
- 📋 **Real-time Feedback**: Live validation and error reporting

## Example Output

```
📝 Testing: '$\frac{x^2}{y}$'
   Tokens: ['$', '\frac', '{', 'x', '^', '2', '}', '{', 'y', '}', '$']
   Step 1: '$' | start → math_mode ✅
   Step 2: '\frac' | math_mode → fraction_num ✅
   Step 3: '{' | fraction_num → content ✅
   Step 4: 'x' | content → content ✅
   Step 5: '^' | content → content ✅
   Step 6: '2' | content → content ✅
   Step 7: '}' | content → math_mode ✅
   Step 8: '{' | math_mode → content ✅
   Step 9: 'y' | content → content ✅
   Step 10: '}' | content → math_mode ✅
   Step 11: '$' | math_mode → end_state ✅
   
   Result: ✅ VALID
   Final State: end_state
```

## Code Structure

```
src/
├── fsm/
│   ├── __init__.py
│   └── latex_math_fsm.py    # Token-by-token LaTeX math FSM
└── llm/
    ├── __init__.py
    ├── simple_client.py     # Groq API client
    ├── local_client.py      # Local Hugging Face model client  
    └── unified_client.py    # Unified interface with auto-fallback
```

## Model Options

### 1. Groq API (Default)
- **Model**: llama-3.1-8b-instant
- **Setup**: Requires GROQ_API_KEY environment variable
- **Advantages**: Fast, cloud-based, no local compute requirements

### 2. Local Gemma Model
- **Model**: google/gemma-3-270m
- **Setup**: Requires torch, transformers, accelerate packages + Hugging Face authentication
- **Advantages**: Privacy, no API costs, offline operation, lightweight (270M parameters)
- **Requirements**: ~2GB VRAM recommended, Hugging Face account with Gemma access

### 3. Auto Mode
- **Behavior**: Automatically selects best available model
- **Fallback**: Switches between Groq and local models as needed
- **Recommended**: For most users, provides best reliability

## Installation

### Basic Requirements
```bash
pip install -r requirements.txt
```

### For Local Gemma Model Support
```bash
# Install PyTorch (choose appropriate version for your system)
pip install torch torchvision torchaudio

# Install Transformers and related packages
pip install transformers accelerate huggingface-hub

# Set up Hugging Face authentication (for local models):

# Method 1: CLI login
huggingface-cli login

# Method 2: Environment variable
export HF_TOKEN="your_hf_token_here"

# Method 3: Add to .env file
echo "HF_TOKEN=your_hf_token_here" >> .env

# Note: Some models require access requests
# Visit model pages on Hugging Face to request access if needed
```

## Usage with LLM

```python
from src.fsm import LaTeXMathFSM
from src.llm import SimpleGroqClient

# Create FSM
fsm = LaTeXMathFSM()

# Create LLM client (requires GROQ_API_KEY environment variable)
client = SimpleGroqClient()

# Generate LaTeX math with FSM constraints
result = client.generate_with_latex_fsm("Generate a fraction with x and y", fsm)
print(f"Generated: {result}")  # e.g., "$\frac{x}{y}$"
```

## Setup

1. Install dependencies:
```bash
pip install groq python-dotenv
```

2. Set up environment:
```bash
# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
```

3. Run demos:
```bash
python3 demo_latex.py              # LaTeX FSM demo
python3 demo_latex_integration.py  # Integration demo with simulated LLM
```

## How the LaTeX Math FSM Works

The FSM processes LaTeX mathematical expressions token by token:

1. **State: start** 
   - Accepts: $, $$, \[ (math mode delimiters)
   - Transitions to: math_mode

2. **State: math_mode**
   - Accepts: variables (x,y,z), numbers (0-9), operators (+,-,=), commands (\frac, \alpha, etc.)
   - Transitions to: superscript, subscript, content, or end_state

3. **State: superscript/subscript**
   - Accepts: single characters or { for grouped expressions
   - Transitions to: content or back to math_mode

4. **State: content**
   - Handles content inside braces {}
   - Tracks brace depth for proper nesting
   - Transitions back to math_mode when braces close

## Supported LaTeX Math Elements

- **Math Modes**: `$...$`, `$$...$$`, `\[...\]`
- **Variables**: `a-z`, `A-Z`
- **Numbers**: `0-9`
- **Operators**: `+`, `-`, `=`, `*`, `/`, `<`, `>`, etc.
- **Greek Letters**: `\alpha`, `\beta`, `\gamma`, `\theta`, `\pi`, etc.
- **Functions**: `\sin`, `\cos`, `\tan`, `\ln`, `\log`, `\exp`, etc.
- **Structures**: `\frac{a}{b}`, `x^2`, `x_{i}`, `\sqrt{x}`, `\sum`, `\int`
- **Delimiters**: `()`, `[]`, `{}`, `||`, `\langle`, `\rangle`
- **Environments**: `\begin{matrix}...\end{matrix}` (basic support)
