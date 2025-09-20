"""
LaTeX Math FSM - Streamlit Web Interface
=======================================

Interactive web application for demonstrating LaTeX Math FSM and LLM integration.

Features:
- Test LaTeX expressions with step-by-step FSM validation
- Generate LaTeX expressions using LLM with FSM constraints
- Visualize FSM states and transitions
- Real-time feedback and error handling

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path
import os
from typing import List, Dict, Optional
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import LaTeXMathFSM
from src.llm import SimpleGroqClient

# Page configuration
st.set_page_config(
    page_title="LaTeX Math FSM",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .success-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 10px 0;
    }
    .error-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 10px 0;
    }
    .info-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 10px 0;
    }
    .latex-display {
        font-family: 'Times New Roman', serif;
        font-size: 18px;
        padding: 15px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        margin: 10px 0;
    }
    .token-step {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 3px;
        padding: 5px 8px;
        margin: 2px;
        display: inline-block;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'fsm' not in st.session_state:
        st.session_state.fsm = LaTeXMathFSM()
    
    if 'llm_client' not in st.session_state:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            try:
                st.session_state.llm_client = SimpleGroqClient(api_key)
                st.session_state.llm_available = True
            except Exception as e:
                st.session_state.llm_client = None
                st.session_state.llm_available = False
                st.session_state.llm_error = str(e)
        else:
            st.session_state.llm_client = None
            st.session_state.llm_available = False
            st.session_state.llm_error = "GROQ_API_KEY not found in environment"

def render_header():
    """Render the application header."""
    st.title("🧮 LaTeX Math FSM")
    st.markdown("### Interactive demonstration of token-by-token LaTeX validation")
    
    # Info about the project
    with st.expander("ℹ️ About this project"):
        st.markdown("""
        This application demonstrates a **Finite State Machine (FSM)** that validates LaTeX mathematical expressions 
        token-by-token. The FSM processes each LaTeX token individually and transitions through states to ensure 
        syntactic validity.
        
        **Key Features:**
        - ✅ Token-by-token processing of LaTeX expressions
        - ✅ Real-time validation and state visualization  
        - ✅ Support for 200+ LaTeX commands and operators
        - ✅ LLM integration for constrained generation
        """)

def render_fsm_demo():
    """Render the FSM demonstration interface."""
    st.header("🔬 FSM Demonstration")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        test_input = st.text_input(
            "Enter LaTeX expression to test:",
            value="$\\frac{x^2}{y}$",
            help="Try expressions like: $x^2$, $\\alpha + \\beta$, $\\sum_{i=1}^n x_i$"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        test_button = st.button("🧪 Test Expression", type="primary")
    
    # Predefined examples
    st.markdown("**Quick Examples:**")
    example_cols = st.columns(4)
    examples = [
        "$x^2$",
        "$\\frac{a}{b}$", 
        "$\\alpha + \\beta$",
        "$\\sum_{i=1}^n x_i$"
    ]
    
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(f"`{example}`", key=f"example_{i}"):
                st.session_state.test_input = example
                test_input = example
                test_button = True
    
    # Process the input if button clicked or example selected
    if test_button and test_input:
        process_latex_expression(test_input)

def process_latex_expression(latex_expr: str):
    """Process and display results for a LaTeX expression."""
    st.markdown(f"### Testing: `{latex_expr}`")
    
    # Reset FSM
    fsm = st.session_state.fsm
    fsm.reset()
    
    # Tokenize
    tokens = fsm.tokenize(latex_expr)
    st.markdown(f"**Tokens:** `{tokens}`")
    
    # Process step by step
    st.markdown("**Step-by-step processing:**")
    
    results = []
    valid = True
    
    for i, token in enumerate(tokens):
        prev_state = fsm.state
        success = fsm.process_token(token)
        new_state = fsm.state
        
        results.append({
            'step': i + 1,
            'token': token,
            'prev_state': prev_state,
            'new_state': new_state,
            'success': success
        })
        
        if not success:
            valid = False
            break
    
    # Display results
    for result in results:
        status_icon = "✅" if result['success'] else "❌"
        st.markdown(
            f"**Step {result['step']}:** `{result['token']}` | "
            f"`{result['prev_state']}` → `{result['new_state']}` {status_icon}"
        )
    
    # Final validation
    is_complete = fsm.is_complete() if valid else False
    
    # Results summary
    col1, col2 = st.columns(2)
    
    with col1:
        if valid and is_complete:
            st.markdown('<div class="success-box">✅ <strong>VALID</strong> - Expression is syntactically correct!</div>', 
                       unsafe_allow_html=True)
        elif valid:
            st.markdown('<div class="error-box">⚠️ <strong>INCOMPLETE</strong> - Expression is not complete</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ <strong>INVALID</strong> - Expression contains syntax errors</div>', 
                       unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**Final State:** `{fsm.state}`")
        st.markdown(f"**FSM Path:** `{' → '.join(fsm.path)}`")
    
    # State information
    with st.expander("🔍 Detailed FSM State"):
        state_info = fsm.get_state_info()
        st.json(state_info)

def render_llm_generation():
    """Render the LLM generation interface."""
    st.header("🤖 LLM-Guided Generation")
    
    if not st.session_state.llm_available:
        st.error(f"LLM not available: {st.session_state.llm_error}")
        st.info("To enable LLM features, set your GROQ_API_KEY environment variable and restart the app.")
        return
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_input(
            "Describe the LaTeX expression you want to generate:",
            value="Generate a quadratic equation",
            help="Describe what kind of mathematical expression you want"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        generate_button = st.button("🎯 Generate LaTeX", type="primary")
    
    # Predefined prompts
    st.markdown("**Example Prompts:**")
    prompt_cols = st.columns(3)
    prompt_examples = [
        "Generate a fraction with variables",
        "Create a summation expression", 
        "Show a quadratic formula"
    ]
    
    for i, example in enumerate(prompt_examples):
        with prompt_cols[i]:
            if st.button(f"`{example}`", key=f"prompt_{i}"):
                st.session_state.generation_prompt = example
                prompt = example
                generate_button = True
    
    # Generation options
    with st.expander("⚙️ Generation Settings"):
        verbose = st.checkbox("Show detailed generation process", value=True)
        max_attempts = st.slider("Maximum generation attempts", 1, 5, 3)
    
    # Process generation if button clicked
    if generate_button and prompt:
        generate_latex_expression(prompt, verbose, max_attempts)

def generate_latex_expression(prompt: str, verbose: bool, max_attempts: int):
    """Generate LaTeX expression using LLM with FSM constraints."""
    st.markdown(f"### Generating for: `{prompt}`")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for attempt in range(max_attempts):
        progress_bar.progress((attempt + 1) / max_attempts)
        status_text.text(f"Generation attempt {attempt + 1}/{max_attempts}...")
        
        try:
            # Reset FSM for each attempt
            fsm = LaTeXMathFSM()
            
            if verbose:
                st.markdown(f"**Attempt {attempt + 1}:**")
                
                # Create a container for real-time updates
                generation_container = st.container()
                
                with generation_container:
                    # Capture generation process
                    result = st.session_state.llm_client.generate_with_latex_fsm(
                        prompt, fsm, verbose=False  # We'll handle verbose output ourselves
                    )
            else:
                result = st.session_state.llm_client.generate_with_latex_fsm(
                    prompt, fsm, verbose=False
                )
            
            if result and result != "$x$":  # Don't accept fallback
                # Success!
                status_text.text("✅ Generation successful!")
                
                # Display result
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown('<div class="success-box">🎉 <strong>Generated Expression:</strong></div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="latex-display"><code>{result}</code></div>', 
                               unsafe_allow_html=True)
                
                with col2:
                    # Verify with FSM
                    test_fsm = LaTeXMathFSM()
                    is_valid = test_fsm.process_input(result)
                    
                    if is_valid:
                        st.markdown('<div class="success-box">✅ FSM Validated</div>', 
                                   unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-box">❌ FSM Rejected</div>', 
                                   unsafe_allow_html=True)
                
                # Option to test the generated expression
                if st.button("🧪 Test Generated Expression"):
                    process_latex_expression(result)
                
                return
                
        except Exception as e:
            st.error(f"Generation error on attempt {attempt + 1}: {str(e)}")
    
    # All attempts failed
    status_text.text("❌ Generation failed after all attempts")
    st.error("Could not generate a valid LaTeX expression. Try a different prompt or check your API key.")

def render_fsm_visualizer():
    """Render FSM state visualizer."""
    st.header("🗺️ FSM State Visualizer")
    
    # Current FSM state
    fsm = st.session_state.fsm
    current_state = fsm.state
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**FSM States and Transitions:**")
        
        # Define FSM states and their relationships
        states = {
            "start": {"description": "Initial state", "color": "#e3f2fd"},
            "math_mode": {"description": "Inside $ ... $ or \\[ ... \\]", "color": "#f3e5f5"},
            "command": {"description": "After backslash \\", "color": "#fff3e0"},
            "superscript": {"description": "After ^ symbol", "color": "#e8f5e8"},
            "subscript": {"description": "After _ symbol", "color": "#fff8e1"},
            "fraction_num": {"description": "Reading fraction numerator", "color": "#fce4ec"},
            "content": {"description": "Reading content inside braces", "color": "#f1f8e9"},
            "end_state": {"description": "Valid complete expression", "color": "#e0f2f1"}
        }
        
        # Display states
        for state, info in states.items():
            bg_color = "#ffeb3b" if state == current_state else info["color"]
            emphasis = "**" if state == current_state else ""
            
            st.markdown(
                f'<div style="background-color: {bg_color}; padding: 8px; margin: 4px; border-radius: 4px;">'
                f'{emphasis}<code>{state}</code>{emphasis}: {info["description"]}'
                f'</div>',
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown("**Current State Info:**")
        st.markdown(f"**State:** `{current_state}`")
        st.markdown(f"**Brace Depth:** `{fsm.brace_depth}`")
        st.markdown(f"**Bracket Depth:** `{fsm.bracket_depth}`")
        st.markdown(f"**Paren Depth:** `{fsm.paren_depth}`")
        
        # Valid next tokens
        possibilities = fsm.get_current_possibilities()[:10]
        if possibilities:
            st.markdown("**Valid Next Tokens:**")
            for token in possibilities:
                st.markdown(f"• `{token}`")

def render_sidebar():
    """Render the sidebar with navigation and settings."""
    with st.sidebar:
        st.title("🧮 LaTeX Math FSM")
        
        # Navigation
        page = st.selectbox(
            "Navigate to:",
            ["FSM Demo", "LLM Generation", "FSM Visualizer"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        # API Key status
        if st.session_state.llm_available:
            st.success("✅ Groq API Connected")
        else:
            st.error("❌ Groq API Not Available")
            if st.button("🔄 Retry Connection"):
                initialize_session_state()
                st.rerun()
        
        # Reset FSM
        if st.button("🔄 Reset FSM"):
            st.session_state.fsm.reset()
            st.success("FSM Reset!")
        
        st.markdown("---")
        
        # Quick info
        st.markdown("### 📋 Quick Info")
        st.markdown("""
        **Supported Commands:**
        - Greek letters: `\\alpha`, `\\beta`
        - Functions: `\\frac`, `\\sqrt`, `\\sum`
        - Operators: `^`, `_`, `+`, `-`
        - And 200+ more!
        """)
        
        # Links
        st.markdown("### 🔗 Links")
        st.markdown("- [Project Repository](https://github.com)")
        st.markdown("- [LaTeX Documentation](https://www.latex-project.org/)")
        
        return page

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get current page
    current_page = render_sidebar()
    
    # Render content based on selected page
    if current_page == "FSM Demo":
        render_fsm_demo()
    elif current_page == "LLM Generation":
        render_llm_generation()
    elif current_page == "FSM Visualizer":
        render_fsm_visualizer()

if __name__ == "__main__":
    main()
