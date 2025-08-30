"""
Example 2: Email Format Constraint
===================================

This example demonstrates how to constrain LLM outputs to generate
valid email addresses using FSM.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.fsm import FSMBuilder, State, StateType, TextConstraints, StructuralConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def create_email_fsm():
    """Create an enhanced FSM for email validation."""
    fsm = FSMBuilder.create_email_fsm()
    
    # Add additional constraints
    username_state = fsm.states.get("username")
    if username_state:
        username_state.validators.extend([
            TextConstraints.min_length(3),
            TextConstraints.max_length(30)
        ])
    
    # Add domain constraints
    domain_state = fsm.states.get("domain")
    if domain_state:
        domain_state.validators.extend([
            TextConstraints.min_length(3),
            TextConstraints.max_length(50)
        ])
    
    return fsm


def main():
    """Demonstrate email-constrained LLM generation."""
    print("Email Format Constraint Example")
    print("=" * 40)
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY environment variable not set!")
        print("   Set it with: export GROQ_API_KEY='your-api-key'")
        print("   Using mock example instead...\n")
        
        # Mock example without actual API call
        demo_email_fsm()
        return
    
    try:
        # Initialize Groq client
        client = GroqClient()
        
        # Configure constrained LLM
        config = ConstrainedLLMConfig(
            max_tokens=100,
            temperature=0.2,  # Very low temperature for precise format
            max_retries=5
        )
        
        constrained_llm = ConstrainedLLM(client, config)
        
        # Create email FSM
        email_fsm = create_email_fsm()
        
        # Test prompts
        prompts = [
            "Generate a professional email address for John Doe",
            "Create an email address for a marketing manager at TechCorp",
            "Provide an email for a student named Alice Smith",
            "Generate a customer service email for ABC Company"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. Prompt: {prompt}")
            print("-" * 50)
            
            try:
                response = constrained_llm.generate_with_constraints(
                    prompt=prompt,
                    fsm=email_fsm,
                    guidance_prompt="Generate only valid email addresses in the format user@domain.com"
                )
                
                print(f"✅ Generated Email: {response.text}")
                print(f"📊 Tokens used: {response.tokens_used}")
                
                # Validate the email format
                email_fsm.reset()
                is_valid = email_fsm.transition(response.text.strip())
                validation_status = "✅ VALID" if is_valid and email_fsm.is_final_state() else "❌ INVALID"
                print(f"🔍 Validation: {validation_status}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        print("\n" + "=" * 50)
        print("Email constraint example completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        print("Using mock example instead...\n")
        demo_email_fsm()


def demo_email_fsm():
    """Demonstrate email FSM without API calls."""
    print("Email FSM Demo (Without API)")
    print("-" * 30)
    
    # Create email FSM
    email_fsm = create_email_fsm()
    
    # Test cases
    test_cases = [
        ("john.doe@example.com", True),
        ("alice_smith@company.org", True),
        ("user123@domain.co.uk", True),
        ("invalid-email", False),
        ("@domain.com", False),
        ("user@", False),
        ("user@domain", False),
        ("a@b.c", True),  # Minimal valid email
        ("very.long.username@very.long.domain.com", True)
    ]
    
    print("Testing email validation with FSM:")
    print()
    
    for email, expected in test_cases:
        email_fsm.reset()
        result = email_fsm.transition(email)
        is_final = email_fsm.is_final_state()
        is_valid = result and is_final
        
        status = "✅ VALID" if is_valid else "❌ INVALID"
        expectation = "✓" if is_valid == expected else "✗"
        
        print(f"{expectation} {status}: '{email}'")
        print(f"   Current state: {email_fsm.current_state}")
        print(f"   Is final: {is_final}")
        print()


if __name__ == "__main__":
    main()
