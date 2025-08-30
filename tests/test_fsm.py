"""
Test cases for FSM functionality.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.fsm import (
    FiniteStateMachine, State, StateType, Transition, FSMBuilder,
    TextConstraints, StructuralConstraints
)


def test_basic_fsm():
    """Test basic FSM functionality."""
    print("Testing Basic FSM...")
    
    # Create simple FSM
    fsm = FiniteStateMachine("start")
    fsm.add_state(State("start", StateType.INITIAL))
    fsm.add_state(State("middle", StateType.INTERMEDIATE))
    fsm.add_state(State("end", StateType.FINAL))
    
    # Add transitions
    fsm.add_transition(Transition(
        "start", "middle",
        lambda x: "go" in x.lower(),
        "Go to middle"
    ))
    
    fsm.add_transition(Transition(
        "middle", "end",
        lambda x: "finish" in x.lower(),
        "Go to end"
    ))
    
    # Test transitions
    assert fsm.current_state == "start"
    assert fsm.transition("let's go")
    assert fsm.current_state == "middle"
    assert fsm.transition("finish now")
    assert fsm.current_state == "end"
    assert fsm.is_final_state()
    
    print("✅ Basic FSM test passed")


def test_json_fsm():
    """Test JSON FSM."""
    print("Testing JSON FSM...")
    
    json_fsm = FSMBuilder.create_json_fsm()
    
    # Valid JSON
    json_fsm.reset()
    assert json_fsm.transition('{"name": "John", "age": 30}')
    
    # Invalid JSON
    json_fsm.reset()
    assert not json_fsm.transition('invalid json')
    
    print("✅ JSON FSM test passed")


def test_email_fsm():
    """Test email FSM."""
    print("Testing Email FSM...")
    
    email_fsm = FSMBuilder.create_email_fsm()
    
    # Valid email
    email_fsm.reset()
    result = email_fsm.transition("user@domain.com")
    assert result and email_fsm.is_final_state()
    
    # Invalid email
    email_fsm.reset()
    result = email_fsm.transition("invalid.email")
    assert not (result and email_fsm.is_final_state())
    
    print("✅ Email FSM test passed")


def test_constraints():
    """Test constraint functions."""
    print("Testing Constraints...")
    
    # Text constraints
    max_len = TextConstraints.max_length(5)
    assert max_len("short")
    assert not max_len("very long text")
    
    # Email validation
    email_validator = TextConstraints.valid_email()
    assert email_validator("test@example.com")
    assert not email_validator("invalid-email")
    
    # Structural constraints
    balanced = StructuralConstraints.has_balanced_brackets()
    assert balanced("(hello [world])")
    assert not balanced("(unbalanced")
    
    print("✅ Constraints test passed")


def test_state_history():
    """Test FSM state history tracking."""
    print("Testing State History...")
    
    fsm = FiniteStateMachine("a")
    fsm.add_state(State("a", StateType.INITIAL))
    fsm.add_state(State("b", StateType.INTERMEDIATE))
    fsm.add_state(State("c", StateType.FINAL))
    
    fsm.add_transition(Transition("a", "b", lambda x: "1" in x, "a to b"))
    fsm.add_transition(Transition("b", "c", lambda x: "2" in x, "b to c"))
    
    assert fsm.history == ["a"]
    fsm.transition("1")
    assert fsm.history == ["a", "b"]
    fsm.transition("2")
    assert fsm.history == ["a", "b", "c"]
    
    print("✅ State history test passed")


def run_all_tests():
    """Run all test cases."""
    print("🧪 Running FSM Tests")
    print("=" * 20)
    
    try:
        test_basic_fsm()
        test_json_fsm()
        test_email_fsm()
        test_constraints()
        test_state_history()
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
