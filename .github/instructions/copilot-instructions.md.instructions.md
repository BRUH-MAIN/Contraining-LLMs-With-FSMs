---
applyTo: '**'
---

# LaTeX Math FSM - AI Assistant Instructions

## Project Overview

This project implements a **finite state machine (FSM) for constraining Large Language Models (LLMs)** to generate valid LaTeX mathematical expressions. The FSM processes LaTeX math expressions **token-by-token**, ensuring syntactic validity through state transitions.

### Core Concept
- **Token-by-token processing**: Each LaTeX token moves the FSM through specific states
- **Real-time validation**: Only valid LaTeX math expressions can complete the FSM path
- **LLM constraint**: Guide language models to generate syntactically correct LaTeX math

## Project Structure

```
/
├── .github/                      # GitHub configuration
│   └── instructions/            # AI assistant instructions
│       └── copilot-instructions.md.instructions.md
├── src/                         # Main source code
│   ├── fsm/                    # Finite State Machine implementation
│   │   ├── __init__.py        # FSM module exports
│   │   └── latex_math_fsm.py  # Main LaTeX Math FSM class
│   ├── llm/                   # LLM integration
│   │   ├── __init__.py        # LLM module exports  
│   │   └── simple_client.py   # Groq API client with FSM constraints
│   └── __init__.py            # Package initialization
├── streamlit_app.py           # Interactive Streamlit web interface
├── demo_latex.py              # Interactive FSM demonstration
├── main.py                    # Main application entry point
├── run_app.sh                 # Streamlit app launcher script
├── pyproject.toml            # Project configuration (uv compatible)
├── uv.lock                   # UV lock file for dependencies
├── requirements.txt          # Pip dependencies
├── QUICK_START.md           # Quick setup instructions
├── README.md                # Project documentation
├── LICENSE                  # Project license
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
└── .python-version         # Python version specification
```

## Key Components

### 1. LaTeXMathFSM (`src/fsm/latex_math_fsm.py`)

**Purpose**: Core FSM implementation for LaTeX math validation

**Key Features**:
- **States**: `start`, `math_mode`, `command`, `superscript`, `subscript`, `fraction_num`, `content`, `end_state`
- **Token processing**: Individual LaTeX tokens (variables, operators, commands, delimiters)
- **Validation**: Supports 200+ LaTeX commands, Greek letters, operators
- **Depth tracking**: Maintains brace `{}`, bracket `[]`, and parenthesis `()` nesting

**Core Methods**:
```python
def process_token(token: str) -> bool         # Process single token
def process_input(latex_str: str) -> bool     # Process complete expression
def tokenize(latex_str: str) -> List[str]     # Split LaTeX into tokens
def get_current_possibilities() -> List[str]  # Valid next tokens
def is_complete() -> bool                     # Check if valid final state
```

**Valid Commands Include**:
- Greek letters: `\alpha`, `\beta`, `\gamma`, etc.
- Math operators: `\frac`, `\sqrt`, `\sum`, `\int`, etc.
- Functions: `\sin`, `\cos`, `\ln`, `\log`, etc.
- Relations: `\leq`, `\geq`, `\equiv`, etc.

### 2. SimpleGroqClient (`src/llm/simple_client.py`)

**Purpose**: LLM integration with FSM-guided generation

**Key Features**:
- **Groq API integration**: Uses Groq's fast inference API
- **FSM-constrained generation**: Guides LLM output through valid FSM states
- **Token-by-token guidance**: Chooses next valid tokens based on FSM state
- **Detailed logging**: Step-by-step generation process tracking

**Core Methods**:
```python
def generate_with_latex_fsm(prompt: str, fsm) -> str  # FSM-guided generation
def generate_constrained_step_by_step(prompt: str, fsm) -> str  # Detailed step generation
def extract_latex_expression(text: str) -> str       # Extract LaTeX from text
```

### 3. Streamlit Web Interface (`streamlit_app.py`)

**Purpose**: Interactive web application for demonstrating FSM and LLM integration

**Key Features**:
- **FSM Demo**: Interactive LaTeX expression testing with step-by-step validation
- **LLM Generation**: AI-powered LaTeX generation with FSM constraints
- **FSM Visualizer**: Real-time state diagram and transition tracking
- **User-friendly UI**: Clean interface with error handling and feedback

**Main Sections**:
```python
def render_fsm_demo()        # Test LaTeX expressions interactively
def render_llm_generation()  # Generate LaTeX using AI with constraints
def render_fsm_visualizer()  # Visualize FSM states and transitions
def render_sidebar()         # Navigation and settings
```

## Coding Guidelines

### Python Style
- **PEP 8 compliance**: Follow Python style guidelines
- **Type hints**: Use typing annotations for all functions
- **Docstrings**: Google-style docstrings for classes and methods
- **Variable names**: Descriptive names (`latex_expr`, `fsm_state`, `token_list`)

### FSM Implementation Rules
1. **State transitions**: All transitions must be explicitly defined
2. **Token validation**: Validate each token before processing
3. **Depth tracking**: Maintain proper nesting for braces/brackets
4. **Error handling**: Graceful failure for invalid tokens
5. **State logging**: Track FSM path for debugging

### LLM Integration Patterns
1. **Reset FSM**: Always reset before new generation
2. **Step-by-step**: Process one token at a time
3. **Validation**: Verify each token with FSM before adding
4. **Fallback**: Provide simple valid expressions if generation fails
5. **Logging**: Verbose output for debugging generation process

### Streamlit UI Guidelines
1. **Session state**: Use `st.session_state` for FSM and client persistence
2. **Error handling**: Graceful error messages and user feedback
3. **Environment loading**: Always call `load_dotenv()` for API keys
4. **Real-time updates**: Immediate validation feedback in UI
5. **Accessibility**: Clear navigation and user-friendly interface

## Development Patterns

### Adding New LaTeX Commands
```python
# In latex_math_fsm.py VALID_COMMANDS
VALID_COMMANDS = {
    # Add new command here
    "newcommand",  # New LaTeX command
    # ... existing commands
}
```

### Extending FSM States
```python
def process_token(self, token: str) -> bool:
    if self.state == "new_state":
        # Handle new state logic
        if token in valid_tokens:
            self.state = "next_state"
            return True
    return False
```

### Testing New Features
```python
# Always test with demo_latex.py
python demo_latex.py

# Test specific expressions
fsm = LaTeXMathFSM()
result = fsm.process_input("$\\new_command{x}$")
print(f"Valid: {result}")

# Test in Streamlit interface
uv run streamlit run streamlit_app.py
```

### Adding Streamlit Components
```python
# Follow existing patterns in streamlit_app.py
def new_feature_section():
    """Add new UI section with proper styling."""
    st.header("🆕 New Feature")
    
    # Use consistent styling classes
    st.markdown('<div class="info-box">Feature description</div>', 
                unsafe_allow_html=True)
    
    # Maintain session state
    if 'new_feature_state' not in st.session_state:
        st.session_state.new_feature_state = default_value
```

## Dependencies

### Required Packages
- **groq**: Groq API client (`pip install groq`)
- **python-dotenv**: Environment variable management
- **streamlit**: Web interface framework (`pip install streamlit`)
- **plotly**: Interactive visualizations (`pip install plotly`)
- **pandas**: Data manipulation (`pip install pandas`)
- **Python 3.11+**: Modern Python features

### Environment Setup
```bash
# Using uv (recommended)
uv sync
uv run streamlit run streamlit_app.py

# Using pip
pip install -r requirements.txt
streamlit run streamlit_app.py

# Set up environment variables (copy from template)
cp .env.example .env
# Edit .env file and add your API key:
echo "GROQ_API_KEY=your_api_key_here" >> .env
```

## Common Tasks

### Running Demos
```bash
# FSM demonstration
python demo_latex.py

# Full integration demo  
python main.py

# Web interface (recommended)
uv run streamlit run streamlit_app.py

# Alternative web launch
./run_app.sh
```

### Testing FSM
```python
from src.fsm import LaTeXMathFSM

fsm = LaTeXMathFSM()
test_cases = ["$x^2$", "$\\frac{a}{b}$", "$\\alpha + \\beta$"]

for case in test_cases:
    fsm.reset()
    result = fsm.process_input(case)
    print(f"'{case}': {'✅' if result else '❌'}")
```

### LLM Generation
```python
from src.llm import SimpleGroqClient
from src.fsm import LaTeXMathFSM

client = SimpleGroqClient()
fsm = LaTeXMathFSM()

result = client.generate_with_latex_fsm(
    "Generate a quadratic equation", 
    fsm, 
    verbose=True
)
```

## Error Handling

### Common Issues
1. **Invalid tokens**: FSM rejects unrecognized LaTeX commands
2. **Incomplete expressions**: Missing closing delimiters (`$`, `}`)
3. **Nesting errors**: Unbalanced braces/brackets
4. **State errors**: Invalid transitions between states

### Debugging Tips
1. **Use verbose mode**: Enable detailed logging in demos
2. **Check FSM path**: Review state transition history
3. **Validate tokens**: Test individual tokens with FSM
4. **Check possibilities**: Review valid next tokens for current state

## Performance Considerations

### FSM Performance
- **Token processing**: O(1) per token
- **State transitions**: Minimal computational overhead
- **Memory usage**: Lightweight state tracking

### LLM Performance  
- **API calls**: Minimize requests through batching
- **Token selection**: Efficient possibility filtering
- **Generation speed**: Fast inference with Groq API

## Security & Best Practices

### API Security
- **Environment variables**: Store API keys securely
- **Input validation**: Sanitize LaTeX input strings
- **Error handling**: Don't expose API errors to users

### Code Quality
- **Unit tests**: Test FSM transitions and edge cases
- **Documentation**: Keep docstrings up to date
- **Version control**: Commit frequently with clear messages
- **Code review**: Review FSM state logic carefully

## When Making Changes

1. **Understand the FSM**: Study state transitions before modifying
2. **Test thoroughly**: Run demos after any changes
3. **Document changes**: Update docstrings and comments
4. **Maintain consistency**: Follow existing patterns
5. **Consider edge cases**: Test invalid inputs and edge conditions

This project demonstrates the power of combining formal methods (FSMs) with modern AI to ensure structured, valid output generation.