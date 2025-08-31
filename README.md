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
- ✅ **LLM integration**: Generate valid LaTeX math using constrained decoding

## Quick Demo

```bash
# Run the LaTeX FSM demo
python3 demo_latex.py

# Run the integration demo showing LLM constraint
python3 demo_latex_integration.py
```

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
    └── simple_client.py     # Simplified Groq client
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
