"""
HTTP Status Code Constraint with LLMs
====================================

Simple demonstration of HTTP status code constraints for LLM outputs.

Usage:
    python main.py [--example server|client|all]

Examples:
    python main.py --example server  # Server error codes (5xx)
    python main.py --example client  # Client error codes (4xx)
    python main.py --example all     # All valid HTTP codes
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import FiniteStateMachine, State, StateType, Transition, FSMBuilder
from src.fsm.constraints import HTTPConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def print_banner():
    """Print application banner."""
    print("🚀 HTTP Status Code Constraint with LLMs")
    print("=" * 45)
    print("Constraining LLM outputs to valid HTTP status codes")
    print()


def create_server_error_fsm():
    """Create FSM for server error codes (5xx)."""
    fsm = FiniteStateMachine("start")
    
    # Create and add states
    start_state = State("start", StateType.INITIAL)
    server_error_state = State("server_error", StateType.FINAL,
                              validators=[HTTPConstraints.server_error_codes()])
    
    fsm.add_state(start_state)
    fsm.add_state(server_error_state)
    
    # Add transitions
    transition = Transition("start", "server_error", 
                          lambda x: True,  # Accept any input, constraint validation happens at state level
                          "Generate server error code")
    fsm.add_transition(transition)
    
    return fsm


def create_client_error_fsm():
    """Create FSM for client error codes (4xx)."""
    fsm = FiniteStateMachine("start")
    
    # Create and add states
    start_state = State("start", StateType.INITIAL)
    client_error_state = State("client_error", StateType.FINAL,
                              validators=[HTTPConstraints.client_error_codes()])
    
    fsm.add_state(start_state)
    fsm.add_state(client_error_state)
    
    # Add transitions
    transition = Transition("start", "client_error", 
                          lambda x: True,  # Accept any input, constraint validation happens at state level
                          "Generate client error code")
    fsm.add_transition(transition)
    
    return fsm


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


def demo_server_errors():
    """Demonstrate server error code constraint."""
    print("🔴 Server Error Codes (5xx) Demo")
    print("-" * 35)
    
    # Create FSM for server errors
    fsm = create_server_error_fsm()
    
    # Create LLM client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
        
    client = GroqClient(api_key=api_key)
    
    # Create constrained LLM
    config = ConstrainedLLMConfig(
        model="mixtral-8x7b-32768",
        max_tokens=10,
        temperature=0.7
    )
    
    constrained_llm = ConstrainedLLM(client, fsm, config)
    
    # Test prompts
    prompts = [
        "What HTTP status code indicates a gateway timeout?",
        "Give me a server error code for when the service is unavailable",
        "What's the HTTP code for internal server error?",
    ]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        try:
            response = constrained_llm.generate(prompt)
            print(f"✅ Generated HTTP Code: {response.text}")
            print(f"   Model: {response.model}")
            print(f"   Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_client_errors():
    """Demonstrate client error code constraint."""
    print("🟡 Client Error Codes (4xx) Demo")
    print("-" * 35)
    
    # Create FSM for client errors
    fsm = create_client_error_fsm()
    
    # Create LLM client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return
        
    client = GroqClient(api_key=api_key)
    
    # Create constrained LLM
    config = ConstrainedLLMConfig(
        model="mixtral-8x7b-32768",
        max_tokens=10,
        temperature=0.7
    )
    
    constrained_llm = ConstrainedLLM(client, fsm, config)
    
    # Test prompts
    prompts = [
        "What HTTP status code means 'Not Found'?",
        "Give me the error code for unauthorized access",
        "What's the HTTP code for forbidden access?",
    ]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        try:
            response = constrained_llm.generate(prompt)
            print(f"✅ Generated HTTP Code: {response.text}")
            print(f"   Model: {response.model}")
            print(f"   Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_all_http_codes():
    """Demonstrate any valid HTTP code constraint."""
    print("🟢 All Valid HTTP Codes Demo")
    print("-" * 30)
    
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
        model="mixtral-8x7b-32768",
        max_tokens=10,
        temperature=0.7
    )
    
    constrained_llm = ConstrainedLLM(client, fsm, config)
    
    # Test prompts
    prompts = [
        "Give me the HTTP code for successful request",
        "What's a redirect status code?",
        "Provide any valid HTTP status code",
    ]
    
    for prompt in prompts:
        print(f"\n📝 Prompt: {prompt}")
        try:
            response = constrained_llm.generate(prompt)
            print(f"✅ Generated HTTP Code: {response.text}")
            print(f"   Model: {response.model}")
            print(f"   Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='HTTP Status Code Constraint Demo')
    parser.add_argument('--example', choices=['server', 'client', 'all'], 
                       default='all', help='Which example to run')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.example == 'server':
        demo_server_errors()
    elif args.example == 'client':
        demo_client_errors()
    elif args.example == 'all':
        demo_server_errors()
        print("\n" + "="*50 + "\n")
        demo_client_errors()
        print("\n" + "="*50 + "\n")
        demo_all_http_codes()


if __name__ == "__main__":
    main()
