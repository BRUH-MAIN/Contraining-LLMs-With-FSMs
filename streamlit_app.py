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
from src.llm.unified_client import UnifiedLLMClient, ModelType, create_auto_client

# Import FSM visualizer components
try:
    from tools.fsm_visualizer import (
        create_interactive_fsm_diagram,
        create_token_flow_visualization,
        create_state_statistics_chart,
        render_fsm_trace_table,
        render_fsm_complexity_metrics,
        render_state_description,
        create_transition_matrix_heatmap
    )
    VISUALIZER_AVAILABLE = True
except ImportError:
    VISUALIZER_AVAILABLE = False

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
    .selected-token {
        background-color: #28a745;
        color: white;
        padding: 8px;
        border-radius: 4px;
        text-align: center;
        font-weight: bold;
    }
    .fsm-step {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .state-display {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'fsm' not in st.session_state:
        st.session_state.fsm = LaTeXMathFSM()
    
    if 'selected_model_type' not in st.session_state:
        st.session_state.selected_model_type = "groq"
    
    if 'llm_client' not in st.session_state or st.session_state.get('model_type_changed', False):
        initialize_llm_client()
        st.session_state.model_type_changed = False

def initialize_llm_client():
    """Initialize the LLM client based on selected model type."""
    try:
        if st.session_state.selected_model_type == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.session_state.llm_client = None
                st.session_state.llm_available = False
                st.session_state.llm_error = "GROQ_API_KEY not found in environment"
                return
            
            st.session_state.llm_client = UnifiedLLMClient(
                model_type=ModelType.GROQ,
                groq_api_key=api_key,
                auto_fallback=True
            )
        elif st.session_state.selected_model_type == "local":
            st.session_state.llm_client = UnifiedLLMClient(
                model_type=ModelType.LOCAL_GEMMA,
                local_model_name="google/gemma-3-270m",
                auto_fallback=True
            )
        elif st.session_state.selected_model_type == "auto":
            st.session_state.llm_client = create_auto_client(prefer_local=False)
        
        st.session_state.llm_available = True
        st.session_state.llm_error = None
        
    except Exception as e:
        st.session_state.llm_client = None
        st.session_state.llm_available = False
        st.session_state.llm_error = str(e)

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
        - ✅ LLM integration for constrained generation (Groq API + Local Models)
        """)

def render_model_selection_sidebar():
    """Render the model selection sidebar."""
    with st.sidebar:
        st.header("🤖 Model Selection")
        
        model_options = {
            "groq": "🌐 Groq API (llama-3.1-8b-instant)",
            "local": "💻 Local Model (google/gemma-3-270m)",
            "auto": "🔄 Auto (with fallback)"
        }
        
        selected_model = st.selectbox(
            "Choose LLM Model:",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            index=0 if st.session_state.selected_model_type == "groq" else 
                  1 if st.session_state.selected_model_type == "local" else 2,
            help="Select which model to use for LaTeX generation"
        )
        
        # Check if model type changed
        if selected_model != st.session_state.selected_model_type:
            st.session_state.selected_model_type = selected_model
            st.session_state.model_type_changed = True
            st.rerun()
        
        # Display current model status
        st.markdown("---")
        st.markdown("**Current Status:**")
        
        if st.session_state.llm_available:
            st.success("✅ Model loaded successfully")
            
            # Display model info if available
            try:
                if hasattr(st.session_state.llm_client, 'get_model_info'):
                    model_info = st.session_state.llm_client.get_model_info()
                    
                    with st.expander("📊 Model Details"):
                        st.json(model_info)
            except Exception as e:
                st.info(f"Model info unavailable: {e}")
        else:
            st.error("❌ Model not available")
            if hasattr(st.session_state, 'llm_error'):
                st.error(f"Error: {st.session_state.llm_error}")
        
        # Reload button
        if st.button("🔄 Reload Model", help="Reinitialize the selected model"):
            st.session_state.model_type_changed = True
            st.rerun()

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
    
    # Debug: Show LLM status
    st.markdown("**🔍 Debug Info:**")
    st.markdown(f"- LLM Available: `{st.session_state.get('llm_available', 'Not set')}`")
    st.markdown(f"- Selected Model: `{st.session_state.get('selected_model_type', 'Not set')}`")
    st.markdown(f"- LLM Client: `{type(st.session_state.get('llm_client', 'None'))}`")
    
    if st.session_state.get('llm_available', False) and hasattr(st.session_state.llm_client, 'get_model_info'):
        try:
            model_info = st.session_state.llm_client.get_model_info()
            st.markdown(f"- Primary Model: `{model_info.get('primary_model_type', 'Unknown')}`")
            st.markdown(f"- Fallback Available: `{model_info.get('fallback_available', False)}`")
        except:
            pass
    
    if not st.session_state.get('llm_available', False):
        st.markdown(f"- Error: `{st.session_state.get('llm_error', 'No error info')}`")
    
    if not st.session_state.llm_available:
        st.error(f"LLM not available: {st.session_state.llm_error}")
        
        if st.session_state.selected_model_type == "groq":
            st.info("To enable Groq API features, set your GROQ_API_KEY environment variable and restart the app.")
        elif st.session_state.selected_model_type == "local":
            st.info("Local model requires torch and transformers packages. Install with: pip install torch transformers accelerate")
        else:
            st.info("Auto mode requires either Groq API key or transformers packages to be available.")
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
        
        # Add a quick test button
        if st.button("🧪 Quick Test - Simple Expression"):
            test_simple_generation()
    
    # Process generation if button clicked
    if generate_button and prompt:
        generate_latex_expression(prompt, verbose, max_attempts)

def test_simple_generation():
    """Test generation with a very simple, known-to-work expression."""
    st.markdown("### 🧪 Quick Test")
    
    fsm = LaTeXMathFSM()
    fsm.reset()
    
    # Manual step-through of a simple expression: $x$
    steps = ["$", "x", "$"]
    result = ""
    
    st.markdown("Testing simple expression: `$x$`")
    
    for i, token in enumerate(steps):
        st.markdown(f"**Step {i+1}:** Processing token `{token}`")
        
        if fsm.process_token(token):
            result += token
            st.success(f"✅ Accepted → State: `{fsm.state}` → Expression: `{result}`")
        else:
            st.error(f"❌ Rejected by FSM")
            break
    
    if fsm.is_complete():
        st.success(f"🎉 **Success!** Generated: `{result}`")
    else:
        st.error(f"❌ **Failed** - Final state: `{fsm.state}`, Complete: `{fsm.is_complete()}`")

def generate_with_streamlit_verbose(prompt: str, fsm):
    """Generate LaTeX with LLM and display step-by-step process in Streamlit."""
    
    # Step 1: Show generation process header
    st.markdown("#### 🧮 LaTeX Generation Process")
    
    # Step 2: Generate LLM response using direct user prompt
    st.markdown("**🎯 Calling LLM...**")
    
    try:
        response = st.session_state.llm_client.generate_simple(prompt, max_tokens=30, temperature=0.1)
        st.markdown(f"**🎯 Raw LLM Response:** `{response}`")
    except Exception as e:
        st.error(f"LLM call failed: {str(e)}")
        return "$x$"  # Fallback
    
    # Step 4: Extract LaTeX expression
    latex_expr = st.session_state.llm_client.extract_latex_expression(response)
    
    if latex_expr:
        st.markdown(f"**🔍 Extracted LaTeX Expression:** `{latex_expr}`")
        
        # Step 5: Test with FSM step by step
        st.markdown(f"**🧪 Testing '{latex_expr}' with LaTeX FSM...**")
        
        # Reset FSM and test step by step
        fsm.reset()
        tokens = fsm.tokenize(latex_expr)
        
        # Show tokenization
        st.markdown(f"**Tokens:** `{tokens}`")
        
        # Process each token with visualization
        valid = True
        for i, token in enumerate(tokens):
            prev_state = fsm.state
            success = fsm.process_token(token)
            new_state = fsm.state
            
            status_icon = "✅" if success else "❌"
            st.markdown(
                f"**Token {i + 1}:** `{token}` | "
                f"`{prev_state}` → `{new_state}` {status_icon}"
            )
            
            if not success:
                valid = False
                break
        
        # Final result
        is_complete = fsm.is_complete() if valid else False
        
        if valid and is_complete:
            st.success(f"✅ LLM output '{latex_expr}' is valid!")
            return latex_expr
        else:
            st.warning(f"❌ LLM output '{latex_expr}' rejected by FSM")
            st.info("🔧 Using fallback expression...")
            return "$x$"  # Simple fallback
    else:
        st.warning("❌ No valid LaTeX expression found in LLM response")
        st.info("🔧 Using fallback expression...")
        return "$x$"  # Simple fallback

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
                
                # Show step-by-step FSM-guided generation with custom verbose display
                result = generate_with_streamlit_verbose(prompt, fsm)
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

def generate_with_detailed_fsm_steps(prompt: str, fsm):
    """Generate LaTeX with detailed step-by-step FSM filtering visualization."""
    
    # Create container for step-by-step process
    steps_container = st.container()
    
    with steps_container:
        st.markdown("#### 🔄 Step-by-Step FSM-Guided Generation")
        
        # Initialize
        result_expr = ""
        max_steps = 15  # Reduced to prevent infinite loops
        
        # Reset FSM
        fsm.reset()
        
        for step in range(max_steps):
            st.markdown(f"**Step {step + 1}:**")
            
            # Create columns for step display
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                st.markdown(f"**Current State:**")
                st.code(fsm.state)
                st.markdown(f"**Expression so far:**")
                st.code(result_expr if result_expr else "(empty)")
            
            # Get valid next tokens from FSM
            valid_tokens = fsm.get_current_possibilities()
            
            # Limit tokens for display but keep all for selection
            display_tokens = valid_tokens[:15] if len(valid_tokens) > 15 else valid_tokens
            
            with col2:
                st.markdown("**FSM Valid Tokens:**")
                if valid_tokens:
                    # Display as badges
                    tokens_html = " ".join([f'<span class="token-step">{token}</span>' for token in display_tokens])
                    if len(valid_tokens) > 15:
                        tokens_html += f'<span class="token-step">...+{len(valid_tokens)-15} more</span>'
                    st.markdown(tokens_html, unsafe_allow_html=True)
                else:
                    st.warning("No valid tokens available")
                    break
            
            # Choose token with improved logic
            chosen_token = choose_token_for_prompt(prompt, valid_tokens, fsm.state, result_expr, step)
            
            with col3:
                if chosen_token:
                    st.markdown("**Selected Token:**")
                    st.markdown(f'<div style="background-color: #28a745; color: white; padding: 8px; border-radius: 4px; text-align: center;"><strong>{chosen_token}</strong></div>', unsafe_allow_html=True)
                    
                    # Process the token
                    if fsm.process_token(chosen_token):
                        result_expr += chosen_token
                        st.success(f"✅ Token accepted → New state: `{fsm.state}`")
                        
                        # Check if complete
                        if fsm.is_complete():
                            st.success("🎉 **Complete valid expression generated!**")
                            break
                    else:
                        st.error("❌ Token rejected by FSM")
                        break
                else:
                    st.markdown("**Decision:**")
                    st.info("🏁 Ending generation (no suitable token)")
                    break
            
            st.markdown("---")
        else:
            # Hit max steps
            st.warning(f"⚠️ Reached maximum steps ({max_steps}). Generation incomplete.")
        
        # Return result or fallback
        if fsm.is_complete():
            return result_expr
        else:
            st.info(f"Generated incomplete expression: `{result_expr}`. Using simple fallback.")
            return "$x$"

def choose_token_for_prompt(prompt: str, valid_tokens: list, current_state: str, current_expr: str, step: int = 0) -> str:
    """Choose the most appropriate token based on prompt and FSM state with more reliable selection."""
    import random
    
    if not valid_tokens:
        return None
        
    prompt_lower = prompt.lower()
    
    # Ensure we end the expression properly
    if "$" in valid_tokens and len(current_expr) > 4:
        # End if we have meaningful content and we're in math_mode
        if current_state == "math_mode" and any(char in current_expr for char in "xyzabc123"):
            # End after step 6 or if expression is getting long
            if step >= 6 or len(current_expr) > 8:
                return "$"
    
    # State-specific reliable logic
    if current_state == "start":
        # Always start with math mode delimiter
        return "$" if "$" in valid_tokens else valid_tokens[0]
    
    elif current_state == "math_mode":
        # Early steps - build main content
        if step <= 2:
            # Content-based selection with prompt analysis
            if "fraction" in prompt_lower and "\\frac" in valid_tokens:
                return "\\frac"
            elif "sum" in prompt_lower and "\\sum" in valid_tokens:
                return "\\sum"
            elif "alpha" in prompt_lower and "\\alpha" in valid_tokens:
                return "\\alpha"
            elif "beta" in prompt_lower and "\\beta" in valid_tokens:
                return "\\beta"
            elif "integral" in prompt_lower and "\\int" in valid_tokens:
                return "\\int"
            
            # Variable selection - prefer x for equations
            variables = ["x", "y", "z", "a", "b"]
            available_vars = [var for var in variables if var in valid_tokens]
            if available_vars:
                if "equation" in prompt_lower and "x" in available_vars:
                    return "x"
                else:
                    return available_vars[0]  # Take first available
        
        # Middle steps - add operations
        elif step <= 4:
            # If we have a variable, consider operations
            if any(var in current_expr for var in ["x", "y", "z", "a", "b"]):
                if "quadratic" in prompt_lower or "square" in prompt_lower:
                    if "^" in valid_tokens and "^" not in current_expr:
                        return "^"
                
                # Add operators occasionally
                operators = ["+", "-", "="]
                available_ops = [op for op in operators if op in valid_tokens]
                if available_ops and random.random() < 0.4:
                    return available_ops[0]
            
            # Add numbers or more variables
            numbers = ["1", "2", "3"]
            available_nums = [num for num in numbers if num in valid_tokens]
            if available_nums:
                return available_nums[0]
        
        # Later steps - try to end
        else:
            if "$" in valid_tokens:
                return "$"
    
    elif current_state in ["superscript", "subscript"]:
        # Handle superscripts/subscripts simply
        if "2" in valid_tokens and ("square" in prompt_lower or "quadratic" in prompt_lower):
            return "2"
        
        # Simple superscript/subscript tokens
        simple_tokens = ["2", "1", "n", "i", "{"]
        available = [token for token in simple_tokens if token in valid_tokens]
        if available:
            return available[0]
    
    elif current_state == "fraction_num":
        # Always open brace for fraction numerator
        return "{" if "{" in valid_tokens else valid_tokens[0]
    
    elif current_state == "content":
        # Inside braces - add simple content then close
        if "}" in valid_tokens and len([c for c in current_expr if c == "}"]) < len([c for c in current_expr if c == "{"]):
            # We have unclosed braces, sometimes close them
            if random.random() < 0.7:  # 70% chance to close
                return "}"
        
        # Add simple content
        simple_content = ["a", "b", "x", "y", "1", "2"]
        available = [token for token in simple_content if token in valid_tokens]
        if available:
            return available[0]
    
    # Fallback - choose the most reasonable token
    # Prefer meaningful tokens over punctuation
    priority_tokens = ["x", "y", "a", "b", "1", "2", "$", "}", "+", "-"]
    for token in priority_tokens:
        if token in valid_tokens:
            return token
    
    # Last resort - first available token
    return valid_tokens[0] if valid_tokens else None

def render_fsm_visualizer():
    """Render enhanced FSM state visualizer with interactive components."""
    st.header("🗺️ FSM State Visualizer")
    
    if not VISUALIZER_AVAILABLE:
        st.warning("⚠️ Advanced visualizer components not available. Install plotly with: `uv add plotly`")
        render_basic_fsm_visualizer()
        return
    
    # Current FSM state
    fsm = st.session_state.fsm
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 State Diagram", 
        "🔍 Live Demo", 
        "📈 Statistics", 
        "🗃️ Transition Matrix",
        "📚 State Reference"
    ])
    
    with tab1:
        st.subheader("Interactive State Diagram")
        
        # Render complexity metrics
        render_fsm_complexity_metrics(fsm)
        
        # Interactive FSM diagram
        fig = create_interactive_fsm_diagram()
        st.plotly_chart(fig, use_container_width=True, key="interactive_fsm_diagram")
        
        # State legend
        st.markdown("""
        **State Legend:**
        - 🟢 **Start/End**: Entry and exit points
        - 🔵 **Math Mode**: Core mathematical processing
        - 🟠 **Commands**: LaTeX command handling
        - 🟣 **Content**: Brace content processing
        - 🔴 **Special**: Superscript/subscript handling
        """)
    
    with tab2:
        st.subheader("Live FSM Demonstration")
        
        # Input for testing
        test_expr = st.text_input(
            "🧪 Test LaTeX Expression:",
            value="$\\frac{x^2}{y+1}$",
            help="Enter a LaTeX expression to see step-by-step FSM processing"
        )
        
        if st.button("🚀 Process Expression", type="primary"):
            if test_expr:
                # Reset FSM and process
                fsm.reset()
                
                with st.spinner("Processing expression..."):
                    try:
                        # Tokenize and process step by step
                        tokens = fsm.tokenize(test_expr)
                        states = ["start"]
                        all_possibilities = []
                        
                        for token in tokens:
                            possibilities = fsm.get_current_possibilities()
                            all_possibilities.append(possibilities.copy())
                            
                            if fsm.process_token(token):
                                states.append(fsm.state)
                            else:
                                st.error(f"❌ FSM rejected token: '{token}'")
                                break
                        
                        # Check if complete
                        is_complete = fsm.is_complete()
                        
                        # Show results
                        col1, col2 = st.columns([3, 1])
                        
                        with col2:
                            st.metric("✅ Valid Expression", "Yes" if is_complete else "No")
                            st.metric("🔢 Tokens Processed", len(tokens))
                            st.metric("🔄 State Changes", len(states))
                        
                        with col1:
                            if len(tokens) > 1 and len(states) > 1:
                                # Token flow visualization
                                flow_fig = create_token_flow_visualization(tokens, states)
                                st.plotly_chart(flow_fig, use_container_width=True, key="token_flow_viz")
                        
                        # Detailed trace table
                        render_fsm_trace_table(tokens, states[1:], all_possibilities)
                        
                        # State usage statistics
                        if len(fsm.path) > 1:
                            stats_fig = create_state_statistics_chart(fsm.path)
                            st.plotly_chart(stats_fig, use_container_width=True, key="state_stats_chart")
                        
                    except Exception as e:
                        st.error(f"Error processing expression: {str(e)}")
            else:
                st.warning("Please enter a LaTeX expression to test.")
    
    with tab3:
        st.subheader("FSM Statistics & Metrics")
        
        # Current state info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current State")
            st.info(f"**State:** `{fsm.state}`")
            st.info(f"**Brace Depth:** `{fsm.brace_depth}`")
            st.info(f"**Path Length:** `{len(fsm.path)}`")
            
            # Valid next tokens
            possibilities = fsm.get_current_possibilities()
            st.markdown("#### Valid Next Tokens")
            if possibilities:
                # Show first 10 possibilities
                for i, token in enumerate(possibilities[:10]):
                    st.markdown(f"• `{token}`")
                if len(possibilities) > 10:
                    st.markdown(f"... and {len(possibilities) - 10} more")
            else:
                st.markdown("*No valid tokens (terminal state)*")
        
        with col2:
            st.markdown("#### FSM Path")
            if len(fsm.path) > 1:
                path_str = " → ".join(fsm.path)
                st.markdown(f"`{path_str}`")
                
                # Path statistics
                stats_fig = create_state_statistics_chart(fsm.path)
                st.plotly_chart(stats_fig, use_container_width=True, key="path_stats_chart")
            else:
                st.markdown("*FSM not yet used*")
        
        # Command categories
        st.markdown("#### Supported LaTeX Commands")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Greek Letters (24)**")
            greek = ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon"]
            for cmd in greek:
                st.markdown(f"• `{cmd}`")
            st.markdown("• *...and more*")
        
        with col2:
            st.markdown("**Functions (20+)**")
            funcs = ["\\frac", "\\sqrt", "\\sum", "\\int", "\\sin"]
            for cmd in funcs:
                st.markdown(f"• `{cmd}`")
            st.markdown("• *...and more*")
        
        with col3:
            st.markdown("**Operators (30+)**")
            ops = ["\\leq", "\\geq", "\\neq", "\\rightarrow", "\\cdot"]
            for cmd in ops:
                st.markdown(f"• `{cmd}`")
            st.markdown("• *...and more*")
    
    with tab4:
        st.subheader("State Transition Matrix")
        
        # Transition matrix heatmap
        matrix_fig = create_transition_matrix_heatmap(fsm)
        st.plotly_chart(matrix_fig, use_container_width=True, key="transition_matrix_heatmap")
        
        st.markdown("""
        **How to Read This Matrix:**
        - **Rows**: Source states (where transitions start from)
        - **Columns**: Target states (where transitions go to)  
        - **Colors**: Darker blue indicates more frequent transitions
        - **Interactive**: Hover over cells to see transition details
        """)
    
    with tab5:
        st.subheader("State Reference Guide")
        
        # State selector
        all_states = ['START', 'MATH_MODE', 'COMMAND', 'CONTENT', 'SUPERSCRIPT', 'SUBSCRIPT', 'END_STATE']
        selected_state = st.selectbox(
            "Select a state to view details:",
            all_states,
            index=all_states.index('MATH_MODE') if 'MATH_MODE' in all_states else 0
        )
        
        # Render state description
        render_state_description(selected_state)
        
        # Example expressions for each state
        st.markdown("#### Example Expressions")
        
        examples = {
            'START': ['Ready to accept: $, $$, \\['],
            'MATH_MODE': ['$x^2$', '$\\alpha + \\beta$', '$\\frac{a}{b}$'],
            'COMMAND': ['$\\frac{...}$', '$\\sum_{...}$', '$\\sqrt{...}$'],
            'CONTENT': ['${x+1}$', '${\\alpha^2}$', '${a+b+c}$'],
            'SUPERSCRIPT': ['$x^2$', '$e^{i\\pi}$', '$a^{n+1}$'],
            'SUBSCRIPT': ['$x_i$', '$a_{i+1}$', '$\\sum_{n=1}$'],
            'END_STATE': ['Complete valid expressions']
        }
        
        if selected_state in examples:
            for example in examples[selected_state]:
                st.code(example, language='latex')

def render_basic_fsm_visualizer():
    """Render basic FSM visualizer without advanced components."""
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
    
    # Render model selection sidebar
    render_model_selection_sidebar()
    
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
