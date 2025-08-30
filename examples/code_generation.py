"""
Example 4: Custom FSM for Code Generation
==========================================

This example demonstrates how to create a custom FSM for constraining
LLM to generate valid Python function code.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.fsm import FiniteStateMachine, State, StateType, Transition, StructuralConstraints, TextConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def create_python_function_fsm():
    """Create an FSM for Python function structure."""
    fsm = FiniteStateMachine("start")
    
    # States
    fsm.add_state(State("start", StateType.INITIAL))
    fsm.add_state(State("def_keyword", StateType.INTERMEDIATE))
    fsm.add_state(State("function_name", StateType.INTERMEDIATE))
    fsm.add_state(State("parameters", StateType.INTERMEDIATE))
    fsm.add_state(State("colon", StateType.INTERMEDIATE))
    fsm.add_state(State("docstring", StateType.INTERMEDIATE))
    fsm.add_state(State("function_body", StateType.INTERMEDIATE))
    fsm.add_state(State("return_statement", StateType.FINAL))
    fsm.add_state(State("error", StateType.ERROR))
    
    # Validators for function name
    function_name_validators = [
        TextConstraints.matches_pattern(r'[a-zA-Z_][a-zA-Z0-9_]*'),
        TextConstraints.min_length(2),
        TextConstraints.max_length(30)
    ]
    
    fsm.states["function_name"].validators = function_name_validators
    
    # Transitions
    fsm.add_transition(Transition(
        "start", "def_keyword",
        lambda x: x.strip().startswith("def "),
        "Start with 'def' keyword"
    ))
    
    fsm.add_transition(Transition(
        "def_keyword", "function_name",
        lambda x: "def " in x and any(c.isalpha() for c in x.split("def ")[-1]),
        "Add function name"
    ))
    
    fsm.add_transition(Transition(
        "function_name", "parameters",
        lambda x: "(" in x,
        "Add parameters in parentheses"
    ))
    
    fsm.add_transition(Transition(
        "parameters", "colon",
        lambda x: "):" in x,
        "Close parameters and add colon"
    ))
    
    fsm.add_transition(Transition(
        "colon", "docstring",
        lambda x: '"""' in x or "'''" in x,
        "Add docstring"
    ))
    
    fsm.add_transition(Transition(
        "colon", "function_body",
        lambda x: any(keyword in x.lower() for keyword in ["if", "for", "while", "try", "return", "print"]),
        "Add function body without docstring"
    ))
    
    fsm.add_transition(Transition(
        "docstring", "function_body",
        lambda x: any(keyword in x.lower() for keyword in ["if", "for", "while", "try", "return", "print"]),
        "Add function body after docstring"
    ))
    
    fsm.add_transition(Transition(
        "function_body", "return_statement",
        lambda x: "return" in x.lower(),
        "Add return statement"
    ))
    
    return fsm


def main():
    """Demonstrate Python function constraint."""
    print("Python Function Code Constraint Example")
    print("=" * 45)
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY environment variable not set!")
        print("   Set it with: export GROQ_API_KEY='your-api-key'")
        print("   Using mock example instead...\n")
        
        # Mock example without actual API call
        demo_python_function_fsm()
        return
    
    try:
        # Initialize Groq client
        client = GroqClient()
        
        # Configure constrained LLM
        config = ConstrainedLLMConfig(
            max_tokens=300,
            temperature=0.4,  # Lower temperature for more structured code
            max_retries=3
        )
        
        constrained_llm = ConstrainedLLM(client, config)
        
        # Create Python function FSM
        python_fsm = create_python_function_fsm()
        
        # Test prompts for different types of functions
        prompts = [
            "Write a Python function to calculate the factorial of a number",
            "Create a function that checks if a string is a palindrome",
            "Generate a function to find the maximum value in a list",
            "Write a function that converts Celsius to Fahrenheit"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. Prompt: {prompt}")
            print("-" * 60)
            
            try:
                response = constrained_llm.generate_with_constraints(
                    prompt=prompt,
                    fsm=python_fsm,
                    guidance_prompt="Generate only valid Python function code with proper structure: def function_name(parameters): body with return statement"
                )
                
                print(f"✅ Generated Function:")
                print("```python")
                print(response.text)
                print("```")
                print(f"📊 Tokens used: {response.tokens_used}")
                
                # Validate the function structure
                python_fsm.reset()
                is_valid = python_fsm.transition(response.text.strip())
                validation_status = "✅ VALID" if is_valid and python_fsm.is_final_state() else "❌ INVALID"
                print(f"🔍 Structure Validation: {validation_status}")
                print(f"📍 Final State: {python_fsm.current_state}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        print("\n" + "=" * 60)
        print("Python function constraint example completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        print("Using mock example instead...\n")
        demo_python_function_fsm()


def demo_python_function_fsm():
    """Demonstrate Python function FSM without API calls."""
    print("Python Function FSM Demo (Without API)")
    print("-" * 40)
    
    # Create Python function FSM
    python_fsm = create_python_function_fsm()
    
    # Test cases
    test_functions = [
        # Valid functions
        ('''def add(a, b):
    """Add two numbers"""
    return a + b''', True),
        
        ('''def greet(name):
    return f"Hello, {name}!"''', True),
        
        # Invalid functions
        ("function add(a, b): return a + b", False),  # Missing 'def'
        ("def add(a, b) return a + b", False),        # Missing ':'
        ("def (a, b): return a + b", False),          # Missing function name
    ]
    
    print("Testing Python function validation with FSM:")
    print()
    
    for i, (code, expected) in enumerate(test_functions, 1):
        python_fsm.reset()
        
        # Process the code line by line for more accurate state transitions
        lines = code.strip().split('\n')
        result = True
        
        for line in lines:
            if not python_fsm.transition(line.strip()):
                result = False
                break
        
        is_final = python_fsm.is_final_state()
        is_valid = result and is_final
        
        status = "✅ VALID" if is_valid else "❌ INVALID"
        expectation = "✓" if is_valid == expected else "✗"
        
        print(f"{expectation} {status}: Function {i}")
        print("```python")
        print(code)
        print("```")
        print(f"   Final state: {python_fsm.current_state}")
        print(f"   Is final: {is_final}")
        print(f"   State history: {' -> '.join(python_fsm.history)}")
        print()


if __name__ == "__main__":
    main()
