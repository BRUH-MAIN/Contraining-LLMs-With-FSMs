#!/usr/bin/env python3

"""
Simple HTTP Status Code Constraint Demo
=======================================

Demonstrates HTTP status code constraints without LLM integration.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import FiniteStateMachine, State, StateType, Transition
from src.fsm.constraints import HTTPConstraints

def print_banner():
    """Print application banner."""
    print("🚀 HTTP Status Code Constraint Demo")
    print("=" * 40)
    print("Validating HTTP status codes using FSM constraints")
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
                          lambda x: True,  # Accept any input, validation at state level
                          "Generate server error code")
    fsm.add_transition(transition)
    
    return fsm

def demo_server_errors():
    """Demonstrate server error code constraint."""
    print("🔴 Server Error Codes (5xx) Demo")
    print("-" * 35)
    
    fsm = create_server_error_fsm()
    
    test_codes = [
        ("504", "Gateway Timeout"),
        ("503", "Service Unavailable"), 
        ("500", "Internal Server Error"),
        ("502", "Bad Gateway"),
        ("404", "Not Found (should fail)"),
        ("200", "OK (should fail)"),
        ("abc", "Invalid (should fail)")
    ]
    
    for code, description in test_codes:
        fsm.reset()
        success = fsm.transition(code)
        status = "✅ Valid" if success and fsm.is_final_state() else "❌ Invalid"
        print(f"{status} - {code}: {description}")
    
    print()

def demo_client_errors():
    """Demonstrate client error code constraint."""
    print("🟡 Client Error Codes (4xx) Demo")
    print("-" * 35)
    
    fsm = FiniteStateMachine("start")
    
    # Create and add states
    start_state = State("start", StateType.INITIAL)
    client_error_state = State("client_error", StateType.FINAL,
                              validators=[HTTPConstraints.client_error_codes()])
    
    fsm.add_state(start_state)
    fsm.add_state(client_error_state)
    
    # Add transitions
    transition = Transition("start", "client_error", 
                          lambda x: True,
                          "Generate client error code")
    fsm.add_transition(transition)
    
    test_codes = [
        ("404", "Not Found"),
        ("401", "Unauthorized"), 
        ("403", "Forbidden"),
        ("400", "Bad Request"),
        ("504", "Gateway Timeout (should fail)"),
        ("200", "OK (should fail)"),
        ("xyz", "Invalid (should fail)")
    ]
    
    for code, description in test_codes:
        fsm.reset()
        success = fsm.transition(code)
        status = "✅ Valid" if success and fsm.is_final_state() else "❌ Invalid"
        print(f"{status} - {code}: {description}")
    
    print()

def demo_all_http_codes():
    """Demonstrate any valid HTTP code constraint."""
    print("🟢 All Valid HTTP Codes Demo")
    print("-" * 30)
    
    fsm = FiniteStateMachine("start")
    
    # Create and add states
    start_state = State("start", StateType.INITIAL)
    http_code_state = State("http_code", StateType.FINAL,
                           validators=[HTTPConstraints.valid_http_status_code()])
    
    fsm.add_state(start_state)
    fsm.add_state(http_code_state)
    
    # Add transitions
    transition = Transition("start", "http_code", 
                          lambda x: True,
                          "Generate valid HTTP code")
    fsm.add_transition(transition)
    
    test_codes = [
        ("200", "OK (Success)"),
        ("301", "Moved Permanently (Redirect)"),
        ("404", "Not Found (Client Error)"), 
        ("500", "Internal Server Error (Server Error)"),
        ("100", "Continue (Informational)"),
        ("999", "Invalid code (should fail)"),
        ("42", "Too short (should fail)"),
        ("abc", "Not numeric (should fail)")
    ]
    
    for code, description in test_codes:
        fsm.reset()
        success = fsm.transition(code)
        status = "✅ Valid" if success and fsm.is_final_state() else "❌ Invalid"
        print(f"{status} - {code}: {description}")
    
    print()

def main():
    """Main function."""
    print_banner()
    
    demo_server_errors()
    demo_client_errors() 
    demo_all_http_codes()
    
    print("🎉 HTTP Status Code Constraint Demo Complete!")
    print("\nTo test with LLM integration:")
    print("1. Ensure your GROQ_API_KEY is set in .env file")
    print("2. Run: python main.py")

if __name__ == "__main__":
    main()
