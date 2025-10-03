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
│   │   ├── simple_client.py   # Groq API client with FSM constraints
│   │   ├── local_client.py    # Local LLM client integration
│   │   └── unified_client.py  # Unified client interface
│   └── __init__.py            # Package initialization
├── examples/                   # Example scripts and demonstrations
│   ├── demo_latex.py          # Interactive FSM demonstration
│   ├── main.py                # Main application entry point
│   ├── reference_notebook.ipynb # Jupyter notebook examples
│   └── README.md              # Examples documentation
├── tools/                     # Utility tools and visualizers
│   ├── fsm_diagram.py         # FSM diagram generation
│   ├── fsm_visualizer.py      # Interactive FSM visualization
│   └── README.md              # Tools documentation
├── scripts/                   # Utility scripts
│   ├── run_app.sh             # Streamlit app launcher script
│   └── README.md              # Scripts documentation
├── tests/                     # Test files
│   └── README.md              # Testing documentation
├── docs/                      # Documentation
│   ├── FSM_DOCUMENTATION.md   # FSM detailed documentation
│   ├── MERMAID_DIAGRAMS.md    # Diagram documentation
│   └── README_DIAGRAMS.md     # Diagram usage guide
├── assets/                    # Static assets
│   ├── latex_fsm_detailed.png # FSM diagram images
│   ├── latex_fsm_simplified.png
│   └── latex_fsm_trace.png
├── streamlit_app.py           # Interactive Streamlit web interface
├── pyproject.toml            # Project configuration (uv compatible)
├── uv.lock                   # UV lock file for dependencies
├── requirements.txt          # Pip dependencies
├── QUICK_START.md           # Quick setup instructions
├── README.md                # Project documentation
├── PROJECT_SUMMARY.md       # Project overview
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # Project license
├── .env.example            # Environment variables template
├── .env                    # Environment variables (create from template)
├── .gitignore              # Git ignore patterns
└── .python-version         # Python version specification
```

## Key Components

### 1. LaTeXMathFSM (`src/fsm/latex_math_fsm.py`)

**Purpose**: Core FSM implementation for LaTeX math validation

**Key Features**:
- **States**: `start`, `math_mode`, `command`, `command_name`, `brace_open`, `content`, `superscript`, `subscript`, `fraction_num`, `fraction_den`, `matrix_mode`, `end_state`
- **Token processing**: Individual LaTeX tokens (variables, operators, commands, delimiters)
- **Validation**: Supports 200+ LaTeX commands, Greek letters, operators
- **Depth tracking**: Maintains brace `{}`, bracket `[]`, and parenthesis `()` nesting
- **Environment support**: Matrix environments, align, equation environments

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
- Arrows: `\rightarrow`, `\leftarrow`, `\Rightarrow`, etc.
- Delimiters: `\left`, `\right`, `\big`, `\Big`, etc.
- Text formatting: `\text`, `\mathbf`, `\mathit`, etc.
- Environments: `\begin`, `\end`, `matrix`, `pmatrix`, etc.
- Special symbols: `\infty`, `\nabla`, `\partial`, etc.

### 2. LLM Clients (`src/llm/`)

The project includes multiple LLM client implementations for different use cases:

#### SimpleGroqClient (`src/llm/simple_client.py`)

**Purpose**: Groq API integration with FSM-guided generation

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

#### LocalClient (`src/llm/local_client.py`)

**Purpose**: Local LLM integration for offline operation

**Key Features**:
- **Local model support**: Works with local LLM deployments (Gemma models)
- **Offline capability**: No internet connection required
- **FSM integration**: Same FSM-guided generation as remote clients
- **Customizable models**: Support for various local model architectures
- **GPU acceleration**: Automatic CUDA detection and usage

#### UnifiedClient (`src/llm/unified_client.py`)

**Purpose**: Unified interface for all LLM clients

**Key Features**:
- **Client abstraction**: Single interface for multiple LLM backends
- **Dynamic switching**: Change between local and remote clients
- **Configuration management**: Handle different client configurations
- **Fallback support**: Automatic fallback to alternative clients
- **Model types**: Support for GROQ and LOCAL_GEMMA model types

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

### 4. Tools and Visualizers (`tools/`)

**Purpose**: Utility tools for FSM visualization and diagram generation

#### FSM Visualizer (`tools/fsm_visualizer.py`)

**Key Features**:
- **Interactive diagrams**: Real-time FSM state visualization with Plotly
- **Token flow tracking**: Visual representation of token processing
- **State statistics**: Charts and metrics for FSM performance
- **Transition matrices**: Heatmaps of state transitions
- **Complexity metrics**: Analysis of FSM behavior patterns

**Core Functions**:
```python
def create_interactive_fsm_diagram()         # Interactive state diagram
def create_token_flow_visualization()        # Token processing visualization
def create_state_statistics_chart()          # State usage statistics
def render_fsm_trace_table()                # Step-by-step trace table
def create_transition_matrix_heatmap()       # Transition frequency heatmap
```

#### FSM Diagram Generator (`tools/fsm_diagram.py`)

**Purpose**: Generate static FSM diagrams for documentation

**Key Features**:
- **Static diagram generation**: Create PNG/SVG diagrams
- **Mermaid diagram support**: Generate mermaid syntax for documentation
- **Customizable layouts**: Different visualization styles
- **Export capabilities**: Save diagrams in various formats

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
python examples/demo_latex.py

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

### Integrating New LLM Clients
```python
# When adding a new LLM client to src/llm/
class NewLLMClient:
    """New LLM client implementation."""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def generate_with_latex_fsm(self, prompt: str, fsm) -> str:
        """Generate LaTeX with FSM constraints."""
        fsm.reset()
        # Implementation specific to your LLM backend
        return generated_latex
    
    def extract_latex_expression(self, text: str) -> str:
        """Extract LaTeX from generated text."""
        # Standard extraction logic
        return extracted_latex

# Update unified_client.py to include new client
# Update __init__.py to export new client
```

## Dependencies

### Project Configuration
- **Version**: 0.3.0 (as defined in pyproject.toml)
- **Python**: 3.11+ required
- **Package Manager**: UV recommended, pip supported
- **Development**: Uses uv.lock for reproducible builds

### Required Packages
- **groq**: Groq API client (`pip install groq`)
- **python-dotenv**: Environment variable management
- **streamlit**: Web interface framework (`pip install streamlit`)
- **plotly**: Interactive visualizations (`pip install plotly`)
- **pandas**: Data manipulation (`pip install pandas`)
- **torch**: PyTorch for local model support
- **transformers**: Hugging Face transformers for local models
- **accelerate**: Hugging Face acceleration library
- **matplotlib**: Plotting library for visualizations
- **networkx**: Network graph library for FSM diagrams
- **Python 3.11+**: Modern Python features

### Environment Setup
```bash
# Using uv (recommended)
uv sync
uv run streamlit run streamlit_app.py

# Using pip
pip install -r requirements.txt
streamlit run streamlit_app.py

# Set up environment variables (copy from template if needed)
cp .env.example .env  # Only if .env doesn't exist
# Edit .env file and add your API key:
echo "GROQ_API_KEY=your_api_key_here" >> .env
```

## Common Tasks

### Running Demos
```bash
# FSM demonstration
python examples/demo_latex.py

# Full integration demo  
python examples/main.py

# Web interface (recommended)
uv run streamlit run streamlit_app.py

# Alternative web launch
./scripts/run_app.sh

# Generate FSM diagrams
python tools/fsm_diagram.py
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

### Testing with Examples
```python
# Use the demo script for comprehensive testing
python examples/demo_latex.py

# Test with main.py for LLM integration
python examples/main.py

# Interactive testing with Streamlit
uv run streamlit run streamlit_app.py
```

### LLM Generation
```python
from src.llm.unified_client import create_auto_client
from src.fsm import LaTeXMathFSM

client = create_auto_client()  # Automatically detects available clients
fsm = LaTeXMathFSM()

result = client.generate_with_latex_fsm(
    "Generate a quadratic equation", 
    fsm, 
    verbose=True
)
```

### Testing Different LLM Clients
```python
from src.llm.unified_client import UnifiedLLMClient, ModelType, create_auto_client
from src.fsm import LaTeXMathFSM

# Test with Groq client (default)
groq_client = UnifiedLLMClient(model_type=ModelType.GROQ)
fsm = LaTeXMathFSM()
groq_result = groq_client.generate_with_latex_fsm("Generate a quadratic", fsm)

# Test with local client
local_client = UnifiedLLMClient(model_type=ModelType.LOCAL_GEMMA)
fsm.reset()
local_result = local_client.generate_with_latex_fsm("Generate a quadratic", fsm)

# Test with auto client (handles availability detection)
auto_client = create_auto_client()
fsm.reset()
auto_result = auto_client.generate_with_latex_fsm("Generate a quadratic", fsm)
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
- **Unit tests**: Test FSM transitions and edge cases (tests/ directory structure ready)
- **Documentation**: Keep docstrings up to date
- **Version control**: Commit frequently with clear messages
- **Code review**: Review FSM state logic carefully
- **FSM documentation**: Detailed docs in `docs/FSM_DOCUMENTATION.md`
- **Diagrams**: Mermaid diagrams in `docs/MERMAID_DIAGRAMS.md`

## Documentation Structure

The project includes comprehensive documentation:

### Core Documentation (`docs/`)
- **FSM_DOCUMENTATION.md**: Detailed FSM implementation and theory
- **MERMAID_DIAGRAMS.md**: State diagrams in Mermaid format
- **README_DIAGRAMS.md**: Guide for diagram generation and usage

### Quick References
- **QUICK_START.md**: Fast setup and basic usage
- **PROJECT_SUMMARY.md**: High-level project overview
- **CONTRIBUTING.md**: Guidelines for contributors

### Component Documentation
- **examples/README.md**: Example scripts and usage patterns
- **tools/README.md**: Utility tools and visualizers
- **scripts/README.md**: Automation scripts
- **tests/README.md**: Testing strategy and guidelines

## When Making Changes

1. **Understand the FSM**: Study state transitions before modifying
2. **Test thoroughly**: Run demos after any changes
3. **Document changes**: Update docstrings and comments
4. **Maintain consistency**: Follow existing patterns
5. **Consider edge cases**: Test invalid inputs and edge conditions

This project demonstrates the power of combining formal methods (FSMs) with modern AI to ensure structured, valid output generation.