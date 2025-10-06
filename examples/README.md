# Example Scripts and Demonstrations

This directory contains example scripts demonstrating various aspects of the LaTeX Math FSM.

## Available Examples

### 🧪 `demo_latex.py`
Interactive command-line demonstration of the FSM functionality.

**Features:**
- Test individual LaTeX expressions
- Step-by-step token processing
- State transition visualization
- Interactive input validation

**Usage:**
```bash
python examples/demo_latex.py
```

### 🚀 `main.py`
Main application entry point showing full integration.

**Features:**
- FSM demonstration
- LLM client integration
- End-to-end LaTeX generation
- Error handling examples

**Usage:**
```bash  
python examples/main.py
```

### 📓 `reference_notebook.ipynb`
Jupyter notebook showing a simpler FSM approach (for comparison).

**Content:**
- HTTP status code FSM example
- Token-by-token constraint approach
- Direct logit manipulation
- Comparison with our approach

**Usage:**
```bash
jupyter notebook examples/reference_notebook.ipynb
```

## Example LaTeX Expressions

### ✅ Valid Expressions
```latex
$x^2$                           # Simple superscript
$\frac{a+b}{c-d}$              # Fraction with operators
$\sum_{i=1}^n \alpha_i x^i$    # Complex sum notation
$\int_0^\infty e^{-x} dx$      # Integral with limits
$\sqrt{x^2 + y^2}$             # Square root
$\alpha + \beta \cdot \gamma$   # Greek letters
```

### ❌ Invalid Expressions
```latex
$x^$                    # Incomplete superscript
$\frac{a}{$            # Unmatched braces
$\unknown{x}$          # Unknown command
x^2                    # Missing math delimiters
$\frac{a}$             # Incomplete fraction
```

## Programming Examples

### Basic FSM Usage
```python
from src.fsm import LaTeXMathFSM

# Initialize FSM
fsm = LaTeXMathFSM()

# Test expression
expression = "$x^2 + y^2$"
result = fsm.process_input(expression)
print(f"'{expression}' is {'valid' if result else 'invalid'}")

# Step-by-step processing
fsm.reset()
tokens = fsm.tokenize(expression)
for token in tokens:
    print(f"Processing '{token}' in state '{fsm.state}'")
    if not fsm.process_token(token):
        print(f"Error: Token '{token}' rejected!")
        break
```

### LLM Integration
```python
from src.fsm import LaTeXMathFSM
from src.llm import SimpleGroqClient

# Initialize components
fsm = LaTeXMathFSM()
client = SimpleGroqClient()

# Generate constrained LaTeX
prompt = "Generate a quadratic equation"
result = client.generate_with_latex_fsm(prompt, fsm, verbose=True)
print(f"Generated: {result}")

# Validate result
fsm.reset()
is_valid = fsm.process_input(result)
print(f"Validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
```

### Advanced Usage
```python
from src.fsm import LaTeXMathFSM

fsm = LaTeXMathFSM()

# Get valid next tokens
expression = "$\\frac{x"
tokens = fsm.tokenize(expression)
for token in tokens:
    fsm.process_token(token)

possibilities = fsm.get_current_possibilities()
print(f"Valid next tokens: {possibilities[:10]}")

# Check current state
state_info = fsm.get_state_info()
print(f"Current state: {state_info}")
```

## Custom Examples

### Educational Use Cases
```python
def validate_student_input(latex_expr):
    """Validate student LaTeX input with feedback."""
    fsm = LaTeXMathFSM()
    
    if fsm.process_input(latex_expr):
        return "✅ Correct LaTeX syntax!"
    else:
        # Provide specific feedback
        tokens = fsm.tokenize(latex_expr)
        for i, token in enumerate(tokens):
            if not fsm.process_token(token):
                return f"❌ Error at token '{token}' (position {i+1})"
        return "❌ Expression incomplete"

# Test with student inputs
student_expressions = [
    "$x^2$",           # Correct
    "$x^$",            # Incomplete superscript
    "$\\frac{a}{b}$",  # Correct fraction
    "$\\frac{a}$"      # Incomplete fraction
]

for expr in student_expressions:
    feedback = validate_student_input(expr)
    print(f"{expr:<15} -> {feedback}")
```

### Content Generation
```python
def generate_math_expressions(topics, count=5):
    """Generate multiple LaTeX expressions for given topics."""
    from src.llm import SimpleGroqClient
    from src.fsm import LaTeXMathFSM
    
    client = SimpleGroqClient()
    fsm = LaTeXMathFSM()
    
    results = []
    for topic in topics:
        print(f"Generating expressions for: {topic}")
        for i in range(count):
            prompt = f"Generate a LaTeX math expression about {topic}"
            result = client.generate_with_latex_fsm(prompt, fsm)
            results.append((topic, result))
            fsm.reset()
    
    return results

# Generate expressions for different topics
topics = ["quadratic equations", "trigonometry", "calculus", "linear algebra"]
expressions = generate_math_expressions(topics, 3)

for topic, expr in expressions:
    print(f"{topic:<20} | {expr}")
```

## Running Examples

### Prerequisites
```bash
# Ensure dependencies are installed
uv sync
# or
pip install -r requirements.txt

# Set up environment variables (for LLM examples)
cp .env.example .env
# Edit .env and add GROQ_API_KEY
```

### Command Line
```bash
# Basic FSM demo
python examples/demo_latex.py

# Full integration demo
python examples/main.py

# Custom examples
python -c "
from examples.demo_latex import main
main()
"
```

### In Scripts
```python
import sys
sys.path.append('.')  # Add project root to path

from src.fsm import LaTeXMathFSM
from src.llm import SimpleGroqClient

# Your code here
```

## Creating New Examples

When adding new examples:

1. **Clear Purpose**: Define what the example demonstrates
2. **Documentation**: Add docstrings and comments
3. **Error Handling**: Show proper error handling patterns
4. **Multiple Use Cases**: Include various scenarios
5. **README Updates**: Update this file with new examples

### Template for New Examples
```python
"""
Example: [Brief Description]
==========================

This example demonstrates [specific functionality].

Usage:
    python examples/new_example.py

Features:
    - Feature 1
    - Feature 2
    - Feature 3
"""

from src.fsm import LaTeXMathFSM
from src.llm import SimpleGroqClient

def main():
    """Main example function."""
    print("🧮 LaTeX Math FSM - [Example Name]")
    
    # Initialize components
    fsm = LaTeXMathFSM()
    
    # Example logic here
    
    print("✅ Example completed successfully!")

if __name__ == "__main__":
    main()
```

---

*Examples help users understand how to effectively use the LaTeX Math FSM!* 📚