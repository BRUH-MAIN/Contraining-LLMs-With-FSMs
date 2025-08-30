"""
Example 1: JSON Structure Constraint
=====================================

This example demonstrates how to constrain LLM outputs to follow
valid JSON structure using FSM.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.fsm import FSMBuilder, State, StateType, TextConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def create_json_response_fsm():
    """Create an FSM for JSON object responses."""
    fsm = FSMBuilder.create_json_fsm()
    
    # Add additional constraints to JSON values
    value_state = fsm.states.get("value")
    if value_state:
        value_state.validators.extend([
            TextConstraints.max_length(100),  # Limit value length
            TextConstraints.no_profanity()    # Filter profanity
        ])
    
    return fsm


def main():
    """Demonstrate JSON-constrained LLM generation."""
    print("JSON Structure Constraint Example")
    print("=" * 40)
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY environment variable not set!")
        print("   Set it with: export GROQ_API_KEY='your-api-key'")
        print("   Using mock example instead...\n")
        
        # Mock example without actual API call
        demo_json_fsm()
        return
    
    try:
        # Initialize Groq client
        client = GroqClient()
        
        # Configure constrained LLM
        config = ConstrainedLLMConfig(
            max_tokens=200,
            temperature=0.3,  # Lower temperature for more structured output
            max_retries=3
        )
        
        constrained_llm = ConstrainedLLM(client, config)
        
        # Create JSON FSM
        json_fsm = create_json_response_fsm()
        
        # Test prompts
        prompts = [
            "Create a JSON object describing a person with name and age",
            "Generate a JSON object for a book with title, author, and year",
            "Make a JSON object for a product with name, price, and category"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. Prompt: {prompt}")
            print("-" * 50)
            
            try:
                response = constrained_llm.generate_with_constraints(
                    prompt=prompt,
                    fsm=json_fsm,
                    guidance_prompt="Generate only valid JSON objects with proper structure."
                )
                
                print(f"✅ Generated JSON:")
                print(response.text)
                print(f"📊 Tokens used: {response.tokens_used}")
                print(f"🎯 Model: {response.model}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        print("\n" + "=" * 50)
        print("JSON constraint example completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        print("Using mock example instead...\n")
        demo_json_fsm()


def demo_json_fsm():
    """Demonstrate JSON FSM without API calls."""
    print("JSON FSM Demo (Without API)")
    print("-" * 30)
    
    # Create JSON FSM
    json_fsm = create_json_response_fsm()
    
    # Test cases
    test_cases = [
        ('{"name": "John"', True),
        ('{"name": "John", "age": 30}', True),
        ('{"invalid json', False),
        ('not json at all', False),
        ('{"name": "Alice", "city": "NYC"}', True)
    ]
    
    print("Testing JSON validation with FSM:")
    print()
    
    for text, expected in test_cases:
        json_fsm.reset()
        result = json_fsm.transition(text)
        status = "✅ VALID" if result else "❌ INVALID"
        expectation = "✓" if result == expected else "✗"
        
        print(f"{expectation} {status}: '{text[:30]}{'...' if len(text) > 30 else ''}'")
        print(f"   Current state: {json_fsm.current_state}")
        print(f"   Final state: {json_fsm.is_final_state()}")
        print()


if __name__ == "__main__":
    main()
