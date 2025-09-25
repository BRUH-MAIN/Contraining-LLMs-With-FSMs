"""
LaTeX Math FSM Demo
==================

Demonstrates token-by-token FSM for LaTeX mathematical expressions.
The FSM moves state by state for each token of a valid LaTeX math expression.

Usage:
    python main.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import LaTeXMathFSM
from src.llm.unified_client import create_auto_client


def print_banner():
    """Print application banner."""
    print("🧮 LaTeX Math Token-by-Token FSM")
    print("=" * 40)
    print("Each token transitions to the next state")
    print()


def demo_latex_fsm():
    """Demonstrate the LaTeX Math FSM."""
    print("🟢 LaTeX Math FSM Demo")
    print("-" * 30)
    
    # Create LaTeX Math FSM
    fsm = LaTeXMathFSM()
    
    # Test various inputs
    test_inputs = ["$x^2$", "$\\frac{a}{b}$", "$\\alpha + \\beta$", "$\\sum_{i=1}^n x_i$", "x + y", "$x^$"]
    
    for test_input in test_inputs:
        print(f"\n📝 Testing: '{test_input}'")
        fsm.reset()
        
        result = fsm.process_input(test_input)
        print(f"   Result: {result}")
        print(f"   Path: {' -> '.join(fsm.path)}")
        
        if result:
            print(f"   ✅ Valid LaTeX expression")
        else:
            print(f"   ❌ Invalid LaTeX expression")


def demo_with_llm():
    """Demonstrate with LLM generation."""
    print("\n🤖 LLM Generation Demo")
    print("-" * 25)
    
    # Create unified LLM client (auto-select best available model)
    try:
        client = create_auto_client(prefer_local=False)
        print("✅ LLM client initialized")
        
        # Show model info
        info = client.get_model_info()
        print(f"📊 Using model: {info.get('primary_model_type', 'unknown')}")
        if info.get('fallback_available', False):
            print(f"📋 Fallback available: {info.get('fallback_model', {}).get('model_type', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Failed to initialize LLM client: {e}")
        print("💡 Try setting GROQ_API_KEY or installing: pip install torch transformers accelerate")
        return
        
    fsm = LaTeXMathFSM()
    
    # Test prompts
    prompts = [
        "Generate a LaTeX expression for x squared",
        "Create a fraction with a and b in LaTeX",
        "Generate a LaTeX expression with Greek letters"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"🧪 Test {i}/{len(prompts)}")
        print(f"{'='*60}")
        
        try:
            response = client.generate_with_latex_fsm(prompt, fsm, verbose=True)
            print(f"\n🎉 Final Result: {response}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"{'='*60}")
            
            # Try with fallback if available
            try:
                current_info = client.get_model_info()
                if current_info.get('fallback_available', False):
                    print("🔄 Attempting with fallback model...")
                    # Force switch to fallback would require implementation
                    # For now, just show the error
            except:
                pass


def main():
    """Main function."""
    print_banner()
    demo_latex_fsm()
    demo_with_llm()


if __name__ == "__main__":
    main()
