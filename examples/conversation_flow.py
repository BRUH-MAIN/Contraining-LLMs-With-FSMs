"""
Example 3: Conversation Flow Constraint
========================================

This example demonstrates how to constrain LLM outputs to follow
a structured conversation flow using FSM.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.fsm import FSMBuilder, State, StateType, FiniteStateMachine, Transition, ContentConstraints
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig


def create_customer_service_fsm():
    """Create an FSM for customer service conversation flow."""
    fsm = FiniteStateMachine("greeting")
    
    # States
    fsm.add_state(State("greeting", StateType.INITIAL))
    fsm.add_state(State("problem_identification", StateType.INTERMEDIATE))
    fsm.add_state(State("solution_offering", StateType.INTERMEDIATE))
    fsm.add_state(State("confirmation", StateType.INTERMEDIATE))
    fsm.add_state(State("closure", StateType.FINAL))
    fsm.add_state(State("escalation", StateType.FINAL))
    
    # Transitions
    fsm.add_transition(Transition(
        "greeting", "problem_identification",
        lambda x: any(word in x.lower() for word in ["issue", "problem", "help", "trouble", "question"]),
        "Identify customer problem"
    ))
    
    fsm.add_transition(Transition(
        "problem_identification", "solution_offering",
        lambda x: any(word in x.lower() for word in ["solution", "fix", "resolve", "try", "suggest"]),
        "Offer solution"
    ))
    
    fsm.add_transition(Transition(
        "solution_offering", "confirmation",
        lambda x: any(word in x.lower() for word in ["work", "help", "solved", "fixed", "better"]),
        "Confirm solution effectiveness"
    ))
    
    fsm.add_transition(Transition(
        "confirmation", "closure",
        lambda x: any(word in x.lower() for word in ["thank", "satisfied", "resolved", "complete"]),
        "Close conversation positively"
    ))
    
    fsm.add_transition(Transition(
        "solution_offering", "escalation",
        lambda x: any(word in x.lower() for word in ["manager", "escalate", "supervisor", "not working"]),
        "Escalate to supervisor"
    ))
    
    fsm.add_transition(Transition(
        "problem_identification", "escalation",
        lambda x: any(word in x.lower() for word in ["complex", "urgent", "manager", "supervisor"]),
        "Escalate complex issue"
    ))
    
    return fsm


def main():
    """Demonstrate conversation flow constraint."""
    print("Conversation Flow Constraint Example")
    print("=" * 40)
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY environment variable not set!")
        print("   Set it with: export GROQ_API_KEY='your-api-key'")
        print("   Using mock example instead...\n")
        
        # Mock example without actual API call
        demo_conversation_fsm()
        return
    
    try:
        # Initialize Groq client
        client = GroqClient()
        
        # Configure constrained LLM
        config = ConstrainedLLMConfig(
            max_tokens=150,
            temperature=0.6,  # Moderate temperature for natural conversation
            max_retries=3
        )
        
        constrained_llm = ConstrainedLLM(client, config)
        
        # Create conversation FSM
        conversation_fsm = create_customer_service_fsm()
        
        # Simulate a conversation flow
        conversation_steps = [
            ("greeting", "Hello, I'm having trouble with my account login"),
            ("problem_identification", "I can help you with that login issue"),
            ("solution_offering", "Please try resetting your password using the forgot password link"),
            ("confirmation", "Yes, that worked perfectly! Thank you for your help"),
            ("closure", "Great! Is there anything else I can help you with today?")
        ]
        
        print("Simulating Customer Service Conversation:")
        print("=" * 45)
        
        for step, user_input in conversation_steps:
            print(f"\n🔄 Current FSM State: {conversation_fsm.current_state}")
            print(f"👤 Customer: {user_input}")
            
            # Transition FSM based on user input
            conversation_fsm.transition(user_input)
            print(f"🤖 New FSM State: {conversation_fsm.current_state}")
            
            # Generate constrained response
            prompt = f"As a customer service representative, respond to: '{user_input}'. Current conversation state: {conversation_fsm.current_state}"
            
            try:
                response = constrained_llm.generate_with_constraints(
                    prompt=prompt,
                    fsm=conversation_fsm,
                    guidance_prompt=f"Respond as a helpful customer service agent. Current state: {conversation_fsm.current_state}"
                )
                
                print(f"🎧 Agent: {response.text}")
                print(f"📊 Tokens: {response.tokens_used}")
                
            except Exception as e:
                print(f"❌ Error generating response: {str(e)}")
        
        print(f"\n✅ Conversation completed in state: {conversation_fsm.current_state}")
        print(f"🎯 Is final state: {conversation_fsm.is_final_state()}")
        
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        print("Using mock example instead...\n")
        demo_conversation_fsm()


def demo_conversation_fsm():
    """Demonstrate conversation FSM without API calls."""
    print("Conversation FSM Demo (Without API)")
    print("-" * 35)
    
    # Create conversation FSM
    conversation_fsm = create_customer_service_fsm()
    
    # Test conversation flow
    conversation_flow = [
        "Hello, I need help with my order",
        "I can help you with that order issue",
        "Let me suggest checking your email for tracking information",
        "That worked great, I found the tracking info!",
        "Wonderful! Thank you for choosing our service"
    ]
    
    print("Testing conversation flow with FSM:")
    print()
    
    for i, message in enumerate(conversation_flow):
        print(f"Step {i+1}: '{message}'")
        print(f"   Before: {conversation_fsm.current_state}")
        
        success = conversation_fsm.transition(message)
        
        print(f"   After: {conversation_fsm.current_state}")
        print(f"   Transition: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"   Is final: {conversation_fsm.is_final_state()}")
        print()
    
    print("Conversation History:")
    for i, state in enumerate(conversation_fsm.history):
        print(f"  {i}: {state}")


if __name__ == "__main__":
    main()
