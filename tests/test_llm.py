"""
Test cases for LLM integration (mock tests without API calls).
"""
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.fsm import FSMBuilder
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig, LLMResponse


def test_llm_config():
    """Test LLM configuration."""
    print("Testing LLM Configuration...")
    
    # Default config
    config = ConstrainedLLMConfig()
    assert config.max_tokens == 512
    assert config.temperature == 0.7
    assert config.max_retries == 3
    
    # Custom config
    config = ConstrainedLLMConfig(
        max_tokens=256,
        temperature=0.5,
        max_retries=5
    )
    assert config.max_tokens == 256
    assert config.temperature == 0.5
    assert config.max_retries == 5
    
    print("✅ LLM Configuration test passed")


def test_llm_response():
    """Test LLM response object."""
    print("Testing LLM Response...")
    
    response = LLMResponse(
        text="Generated text",
        model="test-model",
        tokens_used=50,
        finish_reason="stop",
        metadata={"test": "data"}
    )
    
    assert response.text == "Generated text"
    assert response.model == "test-model"
    assert response.tokens_used == 50
    assert response.finish_reason == "stop"
    assert response.metadata["test"] == "data"
    
    print("✅ LLM Response test passed")


def test_constrained_llm_validation():
    """Test FSM validation in constrained LLM."""
    print("Testing Constrained LLM Validation...")
    
    # Create mock client
    mock_client = Mock()
    mock_response = LLMResponse(
        text='{"name": "John", "age": 30}',
        model="test-model",
        tokens_used=25,
        finish_reason="stop",
        metadata={}
    )
    mock_client.generate.return_value = mock_response
    
    # Create constrained LLM
    config = ConstrainedLLMConfig(max_retries=1)
    constrained_llm = ConstrainedLLM(mock_client, config)
    
    # Create JSON FSM
    json_fsm = FSMBuilder.create_json_fsm()
    
    # Test validation method
    valid_json = '{"name": "John", "age": 30}'
    invalid_json = '{"invalid": json'
    
    assert constrained_llm._validate_response_with_fsm(valid_json, json_fsm)
    assert not constrained_llm._validate_response_with_fsm(invalid_json, json_fsm)
    
    print("✅ Constrained LLM Validation test passed")


def test_system_prompt_building():
    """Test system prompt building."""
    print("Testing System Prompt Building...")
    
    # Create mock client and constrained LLM
    mock_client = Mock()
    constrained_llm = ConstrainedLLM(mock_client)
    
    # Create FSM
    json_fsm = FSMBuilder.create_json_fsm()
    
    # Test system prompt building
    system_prompt = constrained_llm._build_system_prompt(
        json_fsm, 
        "Generate valid JSON"
    )
    
    assert "Generate valid JSON" in system_prompt
    assert "Current state:" in system_prompt
    assert "structural constraints" in system_prompt
    
    print("✅ System Prompt Building test passed")


def test_constraint_feedback():
    """Test constraint feedback generation."""
    print("Testing Constraint Feedback...")
    
    # Create mock client and constrained LLM
    mock_client = Mock()
    constrained_llm = ConstrainedLLM(mock_client)
    
    # Create FSM
    json_fsm = FSMBuilder.create_json_fsm()
    
    # Test feedback generation
    original_prompt = "Generate JSON"
    failed_response = "invalid json"
    
    feedback_prompt = constrained_llm._add_constraint_feedback(
        original_prompt,
        failed_response,
        json_fsm
    )
    
    assert original_prompt in feedback_prompt
    assert "Previous attempt failed" in feedback_prompt
    assert "Current FSM state" in feedback_prompt
    
    print("✅ Constraint Feedback test passed")


@patch('src.llm.groq_client.GROQ_AVAILABLE', False)
def test_groq_unavailable():
    """Test behavior when Groq is not available."""
    print("Testing Groq Unavailable...")
    
    try:
        client = GroqClient()
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "Groq package not available" in str(e)
    
    print("✅ Groq Unavailable test passed")


def run_all_tests():
    """Run all LLM test cases."""
    print("🧪 Running LLM Tests")
    print("=" * 20)
    
    try:
        test_llm_config()
        test_llm_response()
        test_constrained_llm_validation()
        test_system_prompt_building()
        test_constraint_feedback()
        test_groq_unavailable()
        
        print("\n✅ All LLM tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
