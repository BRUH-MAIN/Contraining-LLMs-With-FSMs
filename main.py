"""
HTTP Status Code Constraint with LLMs
====================================

Simple demonstration of HTTP status code constraints for LLM outputs.

Usage:
    python main.py

Examples:
    python main.py  # All valid HTTP codes
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import FiniteStateMachine, State, StateType, Transition
from src.fsm.constraints import HTTPConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def print_banner():
    """Print application banner."""
    print("🚀 HTTP Status Code Constraint with LLMs")
    print("=" * 45)
    print("Constraining LLM outputs to valid HTTP status codes")
    print()


def create_any_http_code_fsm():
    """Create FSM for any valid HTTP status code."""
    fsm = FiniteStateMachine("start")
    
    # Create and add states
    start_state = State("start", StateType.INITIAL)
    http_code_state = State("http_code", StateType.FINAL,
                           validators=[HTTPConstraints.valid_http_status_code()])
    
    fsm.add_state(start_state)
    fsm.add_state(http_code_state)
    
    # Add transitions
    transition = Transition("start", "http_code", 
                          lambda x: True,  # Accept any input, constraint validation happens at state level
                          "Generate valid HTTP code")
    fsm.add_transition(transition)
    
    return fsm


def demo_all_http_codes():
    """Demonstrate any valid HTTP code constraint."""
    print("🟢 HTTP Status Code Validation Demo")
    print("-" * 35)
    
    # Create FSM for any HTTP code
    fsm = create_any_http_code_fsm()
    
    # Create LLM client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
        
    client = GroqClient(api_key=api_key)
    
    # Create constrained LLM
    config = ConstrainedLLMConfig(
        model="llama3-8b-8192",
        max_tokens=10,
        temperature=0.7
    )
    
    constrained_llm = ConstrainedLLM(client, config)
    
    # Test prompts
    prompts = [
        "Server error HTTP code",
        "What's a redirect status code?",
        "random 3 digit number",
    ]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        try:
            response = constrained_llm.generate_with_constraints(prompt, fsm)
            print(f"✅ Generated HTTP Code: {response.text}")
            print(f"   Model: {response.model}")
            print(f"   Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function."""
    print_banner()
    demo_all_http_codes()


if __name__ == "__main__":
    main()
