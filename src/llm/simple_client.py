"""
Simple Groq Client for FSM-constrained generation.
=================================================

A simplified client that works with the HTTP FSM to generate
valid HTTP status codes digit by digit.
"""

import os
import re
from typing import Optional

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_AVAILABLE = False


class SimpleGroqClient:
    """Simple Groq client for FSM-constrained generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client."""
        if not GROQ_AVAILABLE:
            raise RuntimeError("Groq package not available. Install with: pip install groq")
            
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.default_model = "llama3-8b-8192"
    
    def generate_simple(
        self,
        prompt: str,
        max_tokens: int = 50,
        temperature: float = 0.3
    ) -> str:
        """Generate simple text response."""
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {str(e)}")
    
    def generate_with_fsm(self, prompt: str, fsm) -> str:
        """Generate text constrained by FSM."""
        # Reset FSM
        fsm.reset()
        
        # Create a prompt that asks for HTTP status code
        http_prompt = f"""
{prompt}

Please respond with only a 3-digit HTTP status code number. 
Examples: 200, 404, 500, 301

Response:"""
        
        # Generate response
        response = self.generate_simple(http_prompt, max_tokens=10, temperature=0.1)
        
        # Extract 3-digit number from response
        http_code = self.extract_http_code(response)
        
        if http_code:
            # Test with FSM
            if fsm.process_input(http_code):
                return http_code
            else:
                # FSM rejected it, try to generate a valid one
                return self.generate_valid_code_with_fsm(fsm)
        else:
            # No valid code found, generate one with FSM
            return self.generate_valid_code_with_fsm(fsm)
    
    def extract_http_code(self, text: str) -> Optional[str]:
        """Extract HTTP status code from text."""
        # Look for 3-digit numbers
        matches = re.findall(r'\b\d{3}\b', text)
        if matches:
            # Return the first 3-digit number found
            return matches[0]
        return None
    
    def generate_valid_code_with_fsm(self, fsm) -> str:
        """Generate a valid HTTP code using FSM guidance."""
        fsm.reset()
        
        # Build the code digit by digit
        result_code = ""
        
        for position in range(3):
            possibilities = fsm.get_current_possibilities()
            
            if not possibilities:
                # FSM has no valid transitions, fallback
                break
            
            # For simplicity, pick the first valid possibility
            # In a more sophisticated implementation, we could:
            # 1. Ask LLM to choose from possibilities
            # 2. Use probabilities based on context
            # 3. Apply domain-specific logic
            
            if position == 0:
                # First digit: prefer common HTTP code ranges
                if "4" in possibilities:  # Client errors are common
                    chosen_digit = "4"
                elif "2" in possibilities:  # Success codes are common
                    chosen_digit = "2"
                elif "5" in possibilities:  # Server errors
                    chosen_digit = "5"
                else:
                    chosen_digit = possibilities[0]
            else:
                # For second and third digits, choose based on common codes
                if result_code == "4" and position == 1:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                elif result_code == "40" and position == 2:
                    chosen_digit = "4" if "4" in possibilities else possibilities[0]
                elif result_code == "2" and position == 1:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                elif result_code == "20" and position == 2:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                else:
                    chosen_digit = possibilities[0]
            
            # Process the chosen digit
            if fsm.process_digit(chosen_digit):
                result_code += chosen_digit
            else:
                # This shouldn't happen if FSM is correct, but fallback
                break
        
        # Ensure we have a valid 3-digit code
        if len(result_code) == 3 and fsm.is_complete():
            return result_code
        else:
            # Fallback to a known valid code
            return "200"
