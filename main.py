"""
Simple HTTP Status Code FSM Demo
==============================

Demonstrates digit-by-digit FSM for HTTP status codes.
The FSM moves state by state for each digit of a valid HTTP code.

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

from src.fsm import HTTPCodeFSM
from src.llm import SimpleGroqClient


def print_banner():
    """Print application banner."""
    print("🚀 HTTP Status Code Digit-by-Digit FSM")
    print("=" * 40)
    print("Each digit transitions to the next state")
    print()


def demo_http_fsm():
    """Demonstrate the HTTP code FSM."""
    print("🟢 HTTP Status Code FSM Demo")
    print("-" * 30)
    
    # Create HTTP code FSM
    fsm = HTTPCodeFSM()
    
    # Test various inputs
    test_inputs = ["404", "200", "500", "301", "123", "999"]
    
    for test_input in test_inputs:
        print(f"\n📝 Testing: '{test_input}'")
        fsm.reset()
        
        result = fsm.process_input(test_input)
        print(f"   Result: {result}")
        print(f"   Path: {' -> '.join(fsm.path)}")
        
        if result:
            print(f"   ✅ Valid HTTP code")
        else:
            print(f"   ❌ Invalid HTTP code")


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
    fsm = HTTPCodeFSM()
    
    # Test prompts
    prompts = [
        "Generate a server error HTTP status code",
        "What's a successful HTTP status code?"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"🧪 Test {i}/{len(prompts)}")
        print(f"{'='*60}")
        
        try:
            response = client.generate_with_fsm(prompt, fsm, verbose=True)
            print(f"\n🎉 Final Result: {response}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"{'='*60}")


def main():
    """Main function."""
    print_banner()
    demo_http_fsm()
    demo_with_llm()


if __name__ == "__main__":
    main()
