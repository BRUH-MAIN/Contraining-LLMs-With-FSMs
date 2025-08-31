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
from src.llm import SimpleGroqClient


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
    
    # Create LLM client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
        
    client = SimpleGroqClient(api_key)
    fsm = LaTeXMathFSM()
    
    # Test prompts
    prompts = [
        "Generate a LaTeX expression for x squared",
        "Create a fraction with a and b in LaTeX"
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


def main():
    """Main function."""
    print_banner()
    demo_latex_fsm()
    demo_with_llm()


if __name__ == "__main__":
    main()
