"""
LaTeX Math FSM Integration Demo
==============================

Demonstrates how the LaTeX Math FSM can be integrated with LLM clients
to constrain mathematical expression generation, similar to HTTP code validation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import LaTeXMathFSM


class LaTeXMathConstrainedGenerator:
    """LLM client that generates LaTeX math expressions constrained by FSM."""
    
    def __init__(self):
        self.fsm = LaTeXMathFSM()
        
    def generate_constrained_latex(self, prompt: str, max_tokens: int = 20) -> str:
        """
        Simulate constrained generation where each token must be valid according to FSM.
        
        In a real implementation, this would:
        1. Get valid next tokens from FSM
        2. Constrain LLM token generation to only those valid tokens
        3. Update FSM state with chosen token
        4. Repeat until complete expression
        """
        print(f"🎯 Generating LaTeX for: '{prompt}'")
        print("=" * 50)
        
        # Reset FSM
        self.fsm.reset()
        generated = ""
        
        # Start with math delimiter
        token = "$"  # Could be chosen based on prompt
        generated += token
        self.fsm.process_token(token)
        print(f"Step 1: Added '{token}' | State: {self.fsm.state}")
        
        # Simulate token-by-token generation
        for step in range(2, max_tokens + 1):
            # Get valid next tokens
            valid_tokens = self.fsm.get_current_possibilities()
            
            if not valid_tokens:
                print(f"   No valid tokens available. Stopping.")
                break
                
            # Simulate LLM choosing from valid tokens based on prompt
            next_token = self._simulate_llm_choice(prompt, valid_tokens, generated)
            
            if next_token is None:
                print(f"   LLM chose to stop generation.")
                break
                
            # Update FSM
            if self.fsm.process_token(next_token):
                generated += next_token
                print(f"Step {step}: Added '{next_token}' | State: {self.fsm.state}")
                
                # Check if we have a complete expression
                if self.fsm.is_complete():
                    print(f"   ✅ Complete valid expression generated!")
                    break
            else:
                print(f"   ❌ Token '{next_token}' was invalid!")
                break
        
        print(f"\n🎯 Final Result: '{generated}'")
        print(f"   Valid: {self.fsm.is_complete()}")
        print(f"   Final State: {self.fsm.state}")
        
        return generated
    
    def _simulate_llm_choice(self, prompt: str, valid_tokens: list, current: str) -> str:
        """
        Simulate LLM choosing next token based on prompt and current generation.
        In reality, this would use the actual LLM with constrained decoding.
        """
        # Simple heuristics based on prompt content
        prompt_lower = prompt.lower()
        
        # If we need to end math mode
        if "$" in valid_tokens and len(current) > 3:
            # Simple heuristic: end after generating some content
            if any(char in current for char in "xyzabc123"):
                return "$"
        
        # Generate based on prompt keywords
        if "fraction" in prompt_lower and "\\frac" in valid_tokens:
            return "\\frac"
        elif "square" in prompt_lower and "^" in valid_tokens:
            return "^"
        elif "subscript" in prompt_lower and "_" in valid_tokens:
            return "_"
        elif "alpha" in prompt_lower and "\\alpha" in valid_tokens:
            return "\\alpha"
        elif "sum" in prompt_lower and "\\sum" in valid_tokens:
            return "\\sum"
        elif "integral" in prompt_lower and "\\int" in valid_tokens:
            return "\\int"
        
        # Default choices based on state
        if self.fsm.state == "math_mode":
            # Prefer common math tokens
            for token in ["x", "y", "z", "a", "b", "c", "1", "2", "3", "+", "-", "="]:
                if token in valid_tokens:
                    return token
        elif self.fsm.state in ["superscript", "subscript"]:
            # Prefer simple expressions for super/subscripts
            for token in ["2", "i", "n", "{"]:
                if token in valid_tokens:
                    return token
        elif self.fsm.state == "fraction_num":
            return "{"
        elif self.fsm.state == "content":
            # Content inside braces
            for token in ["a", "b", "x", "y", "1", "2", "}"]:
                if token in valid_tokens:
                    return token
        
        # Fallback: return first valid token
        return valid_tokens[0] if valid_tokens else None


def demo_constrained_generation():
    """Demonstrate constrained LaTeX generation."""
    print("🧮 LaTeX Math Constrained Generation Demo")
    print("=" * 45)
    
    generator = LaTeXMathConstrainedGenerator()
    
    # Test prompts
    prompts = [
        "Generate a simple variable x",
        "Create a fraction with numerator a and denominator b", 
        "Show x squared",
        "Generate alpha plus beta",
        "Create a summation expression",
    ]
    
    for prompt in prompts:
        print(f"\n" + "="*60)
        generator.generate_constrained_latex(prompt)


def demo_step_by_step_constraint():
    """Show step-by-step how FSM constrains token generation."""
    print("\n\n🔒 Step-by-Step Token Constraint Demo")
    print("=" * 45)
    
    fsm = LaTeXMathFSM()
    
    # Build expression step by step
    target_expression = "$\\frac{x}{y}$"
    tokens = fsm.tokenize(target_expression)
    
    print(f"Target expression: '{target_expression}'")
    print(f"Tokens: {tokens}")
    print()
    
    for i, token in enumerate(tokens):
        print(f"Step {i+1}: About to process '{token}'")
        print(f"   Current state: {fsm.state}")
        
        # Show what tokens are valid before processing
        valid_next = fsm.get_current_possibilities()
        print(f"   Valid next tokens: {valid_next[:10]}...")  # Show first 10
        
        # Check if our target token is valid
        is_valid = token in valid_next
        status = "✅" if is_valid else "❌"
        print(f"   Target token '{token}' is valid: {status}")
        
        # Process the token
        success = fsm.process_token(token)
        print(f"   Processing result: {'✅' if success else '❌'}")
        print(f"   New state: {fsm.state}")
        print()


if __name__ == "__main__":
    demo_constrained_generation()
    demo_step_by_step_constraint()
