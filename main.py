"""
Constraining LLMs with Finite State Machines
============================================

Main demonstration script showcasing different FSM constraints
for LLM outputs using the Groq API.

Usage:
    python main.py [--example EXAMPLE_NAME] [--api-key API_KEY]

Examples:
    python main.py --example json
    python main.py --example email  
    python main.py --example conversation
    python main.py --example code
    python main.py --example all
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import (
    FiniteStateMachine, State, StateType, Transition, FSMBuilder,
    TextConstraints, StructuralConstraints, ContentConstraints
)
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def print_banner():
    """Print application banner."""
    print("🤖 Constraining LLMs with Finite State Machines")
    print("=" * 50)
    print("A demonstration of FSM-based LLM output constraints")
    print("using the Groq API for structured text generation.")
    print()


def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import groq
        groq_available = True
    except ImportError:
        groq_available = False
    
    try:
        import pydantic
        pydantic_available = True
    except ImportError:
        pydantic_available = False
    
    print("📦 Dependency Check:")
    print(f"   Groq API: {'✅ Available' if groq_available else '❌ Missing (pip install groq)'}")
    print(f"   Pydantic: {'✅ Available' if pydantic_available else '❌ Missing (pip install pydantic)'}")
    print()
    
    return groq_available, pydantic_available


def demo_basic_fsm():
    """Demonstrate basic FSM functionality."""
    print("🔧 Basic FSM Demonstration")
    print("-" * 30)
    
    # Create a simple state machine for greeting flow
    fsm = FiniteStateMachine("start")
    
    # Add states
    fsm.add_state(State("start", StateType.INITIAL))
    fsm.add_state(State("greeting", StateType.INTERMEDIATE))
    fsm.add_state(State("response", StateType.FINAL))
    
    # Add transitions
    fsm.add_transition(Transition(
        "start", "greeting",
        lambda x: any(word in x.lower() for word in ["hello", "hi", "hey"]),
        "Greeting detected"
    ))
    
    fsm.add_transition(Transition(
        "greeting", "response",
        lambda x: any(word in x.lower() for word in ["how", "what", "good"]),
        "Response to greeting"
    ))
    
    # Test the FSM
    test_inputs = [
        "Hello there!",
        "Hi, how are you?",
        "Good morning"
    ]
    
    for input_text in test_inputs:
        fsm.reset()
        print(f"Input: '{input_text}'")
        
        success = fsm.transition(input_text)
        print(f"  Transition: {'✅ Success' if success else '❌ Failed'}")
        print(f"  Current state: {fsm.current_state}")
        print(f"  Is final: {fsm.is_final_state()}")
        print()


def demo_json_constraint():
    """Demonstrate JSON structure constraint."""
    print("📄 JSON Structure Constraint")
    print("-" * 32)
    
    # Create JSON FSM
    json_fsm = FSMBuilder.create_json_fsm()
    
    # Test cases
    test_cases = [
        '{"name": "John", "age": 30}',
        '{"invalid": json',
        '{"product": "laptop", "price": 999.99}',
        'not json at all'
    ]
    
    for test in test_cases:
        json_fsm.reset()
        result = json_fsm.transition(test)
        status = "✅ Valid JSON" if result and json_fsm.is_final_state() else "❌ Invalid JSON"
        print(f"{status}: {test[:40]}{'...' if len(test) > 40 else ''}")
    
    print()


def demo_email_constraint():
    """Demonstrate email format constraint."""
    print("📧 Email Format Constraint")
    print("-" * 28)
    
    # Create email FSM
    email_fsm = FSMBuilder.create_email_fsm()
    
    # Test cases
    test_emails = [
        "user@example.com",
        "invalid.email",
        "alice.smith@company.org", 
        "@domain.com",
        "test@test.co.uk"
    ]
    
    for email in test_emails:
        email_fsm.reset()
        result = email_fsm.transition(email)
        is_valid = result and email_fsm.is_final_state()
        status = "✅ Valid Email" if is_valid else "❌ Invalid Email"
        print(f"{status}: {email}")
    
    print()


def demo_constraints():
    """Demonstrate various constraint types."""
    print("🔒 Constraint Demonstrations")
    print("-" * 30)
    
    # Text constraints
    print("Text Constraints:")
    max_length_validator = TextConstraints.max_length(10)
    print(f"  'short' (max 10): {max_length_validator('short')}")
    print(f"  'very long text' (max 10): {max_length_validator('very long text')}")
    
    # Pattern matching
    email_validator = TextConstraints.valid_email()
    print(f"  'test@email.com': {email_validator('test@email.com')}")
    print(f"  'invalid-email': {email_validator('invalid-email')}")
    
    # Structural constraints
    print("\nStructural Constraints:")
    balanced_validator = StructuralConstraints.has_balanced_brackets()
    print(f"  '(hello [world])': {balanced_validator('(hello [world])')}")
    print(f"  '(unbalanced [': {balanced_validator('(unbalanced [')}")
    
    print()


def demo_with_groq_api(api_key: str):
    """Demonstrate FSM constraints with actual Groq API."""
    print("🚀 Live Groq API Demonstration")
    print("-" * 35)
    
    try:
        # Initialize Groq client
        client = GroqClient(api_key)
        config = ConstrainedLLMConfig(
            max_tokens=150,
            temperature=0.3,
            max_retries=2
        )
        constrained_llm = ConstrainedLLM(client, config)
        
        # Test with JSON constraint
        print("📄 JSON Generation Test:")
        json_fsm = FSMBuilder.create_json_fsm()
        
        try:
            response = constrained_llm.generate_with_constraints(
                prompt="Create a JSON object for a person with name and age",
                fsm=json_fsm,
                guidance_prompt="Generate only valid JSON format"
            )
            print(f"✅ Generated: {response.text}")
            print(f"📊 Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()
        
        # Test with email constraint
        print("📧 Email Generation Test:")
        email_fsm = FSMBuilder.create_email_fsm()
        
        try:
            response = constrained_llm.generate_with_constraints(
                prompt="Generate a professional email address for John Smith",
                fsm=email_fsm,
                guidance_prompt="Generate only valid email addresses"
            )
            print(f"✅ Generated: {response.text}")
            print(f"📊 Tokens: {response.tokens_used}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {str(e)}")
        print("Make sure your API key is valid and you have internet connection.")


def run_example(example_name: str, api_key: str = None):
    """Run a specific example."""
    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")
    
    examples_dir = Path(__file__).parent / "examples"
    
    if example_name == "json":
        print("Running JSON constraint example...")
        os.system(f"cd '{examples_dir}' && python json_constraint.py")
    elif example_name == "email":
        print("Running email constraint example...")
        os.system(f"cd '{examples_dir}' && python email_constraint.py")
    elif example_name == "conversation":
        print("Running conversation flow example...")
        os.system(f"cd '{examples_dir}' && python conversation_flow.py")
    elif example_name == "code":
        print("Running code generation example...")
        os.system(f"cd '{examples_dir}' && python code_generation.py")
    elif example_name == "all":
        for ex in ["json", "email", "conversation", "code"]:
            print(f"\n{'='*50}")
            run_example(ex, api_key)
    else:
        print(f"❌ Unknown example: {example_name}")
        print("Available examples: json, email, conversation, code, all")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Constraining LLMs with Finite State Machines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Run basic demos
  python main.py --example json            # Run JSON constraint example
  python main.py --example all             # Run all examples
  python main.py --api-key YOUR_KEY        # Use specific API key
        """
    )
    
    parser.add_argument(
        "--example", "-e",
        choices=["json", "email", "conversation", "code", "all"],
        help="Run specific example"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        help="Groq API key (or set GROQ_API_KEY environment variable)"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # If specific example requested, run it
    if args.example:
        if args.api_key:
            os.environ["GROQ_API_KEY"] = args.api_key
        run_example(args.example, args.api_key)
        return
    
    # Otherwise run basic demonstrations
    groq_available, pydantic_available = check_dependencies()
    
    # Basic FSM demo (always available)
    demo_basic_fsm()
    
    # Constraint demos (always available)
    demo_constraints()
    
    # JSON and email demos (don't require API)
    demo_json_constraint()
    demo_email_constraint()
    
    # API demo (requires Groq API key)
    api_key = args.api_key or os.getenv("GROQ_API_KEY")
    if api_key and groq_available:
        demo_with_groq_api(api_key)
    else:
        print("🔑 Groq API Demonstration")
        print("-" * 28)
        if not groq_available:
            print("❌ Groq package not installed. Install with: pip install groq")
        elif not api_key:
            print("❌ GROQ_API_KEY not set. Set with: export GROQ_API_KEY='your-key'")
        else:
            print("❌ API demonstration not available")
        print()
    
    # Show available examples
    print("📚 Available Examples:")
    print("   python main.py --example json          # JSON structure constraints")
    print("   python main.py --example email         # Email format constraints")
    print("   python main.py --example conversation  # Conversation flow constraints")
    print("   python main.py --example code          # Code generation constraints")
    print("   python main.py --example all           # Run all examples")
    print()
    print("🎯 To use with Groq API, set GROQ_API_KEY environment variable")
    print("   or use --api-key flag")


if __name__ == "__main__":
    main()
