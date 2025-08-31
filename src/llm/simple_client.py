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
    
    def generate_with_fsm(self, prompt: str, fsm, verbose: bool = True) -> str:
        """Generate text constrained by FSM with detailed logging."""
        # Reset FSM
        fsm.reset()
        
        if verbose:
            print(f"\n🤖 LLM Generation Process")
            print(f"📝 Original prompt: {prompt}")
        
        # Create a prompt that asks for HTTP status code
        http_prompt = f"""
{prompt}

Please respond with only a 3-digit HTTP status code number. 
Examples: 200, 404, 500, 301

Response:"""
        
        if verbose:
            print(f"📋 Enhanced prompt sent to LLM:")
            print(f"   {http_prompt.strip()}")
        
        # Generate response
        response = self.generate_simple(http_prompt, max_tokens=10, temperature=0.1)
        
        if verbose:
            print(f"\n🎯 Raw LLM Response:")
            print(f"   '{response}'")
        
        # Extract 3-digit number from response
        http_code = self.extract_http_code(response)
        
        if verbose:
            print(f"\n🔍 Extracted HTTP Code: {http_code if http_code else 'None found'}")
        
        if http_code:
            if verbose:
                print(f"\n🧪 Testing '{http_code}' with FSM...")
            
            # Test with FSM step by step
            fsm.reset()
            is_valid = self._test_code_with_detailed_fsm(http_code, fsm, verbose)
            
            if is_valid:
                if verbose:
                    print(f"✅ LLM output '{http_code}' is valid!")
                return http_code
            else:
                if verbose:
                    print(f"❌ LLM output '{http_code}' rejected by FSM")
                    print(f"🔧 Generating FSM-compliant code...")
                # FSM rejected it, try to generate a valid one
                return self.generate_valid_code_with_fsm(fsm, verbose)
        else:
            if verbose:
                print(f"❌ No valid HTTP code found in LLM response")
                print(f"🔧 Generating FSM-compliant code...")
            # No valid code found, generate one with FSM
            return self.generate_valid_code_with_fsm(fsm, verbose)
    
    def extract_http_code(self, text: str) -> Optional[str]:
        """Extract HTTP status code from text."""
        # Look for 3-digit numbers
        matches = re.findall(r'\b\d{3}\b', text)
        if matches:
            # Return the first 3-digit number found
            return matches[0]
        return None
    
    def _test_code_with_detailed_fsm(self, code: str, fsm, verbose: bool = True) -> bool:
        """Test a code with FSM and show detailed step-by-step process."""
        if not code or len(code) != 3:
            if verbose:
                print(f"   ❌ Invalid format: '{code}' (must be 3 digits)")
            return False
        
        if verbose:
            print(f"   🔄 Processing '{code}' digit by digit:")
        
        # Process each digit
        for i, digit in enumerate(code):
            current_state = fsm.state
            possibilities = fsm.get_current_possibilities()
            
            if verbose:
                print(f"      Step {i+1}: Processing digit '{digit}'")
                print(f"      Current state: {current_state}")
                print(f"      Valid possibilities: {possibilities}")
            
            success = fsm.process_digit(digit)
            
            if success:
                if verbose:
                    print(f"      ✅ Accepted '{digit}' -> New state: {fsm.state}")
            else:
                if verbose:
                    print(f"      ❌ Rejected '{digit}' (not in valid possibilities)")
                    print(f"      FSM validation failed at digit {i+1}")
                return False
        
        # Check if we reached a valid final state
        is_complete = fsm.is_complete()
        is_valid_code = int(code) in fsm.VALID_CODES if code.isdigit() else False
        
        if verbose:
            print(f"   📊 Final validation:")
            print(f"      Complete path: {' -> '.join(fsm.path)}")
            print(f"      FSM complete: {is_complete}")
            print(f"      Valid HTTP code: {is_valid_code}")
        
        return is_complete and is_valid_code

    def generate_valid_code_with_fsm(self, fsm, verbose: bool = True) -> str:
        """Generate a valid HTTP code using FSM guidance with detailed logging."""
        fsm.reset()
        
        if verbose:
            print(f"\n🔧 FSM-Guided Generation Process:")
            print(f"   Starting from state: {fsm.state}")
        
        # Build the code digit by digit
        result_code = ""
        
        for position in range(3):
            possibilities = fsm.get_current_possibilities()
            
            if not possibilities:
                if verbose:
                    print(f"   ❌ No valid transitions available at position {position}")
                break
            
            if verbose:
                print(f"\n   Step {position + 1}: Choosing digit for position {position + 1}")
                print(f"   Current state: {fsm.state}")
                print(f"   Valid possibilities: {possibilities}")
            
            # For simplicity, pick the first valid possibility
            # In a more sophisticated implementation, we could:
            # 1. Ask LLM to choose from possibilities
            # 2. Use probabilities based on context
            # 3. Apply domain-specific logic
            
            if position == 0:
                # First digit: prefer common HTTP code ranges
                if "4" in possibilities:  # Client errors are common
                    chosen_digit = "4"
                    reason = "client error codes are common"
                elif "2" in possibilities:  # Success codes are common
                    chosen_digit = "2"
                    reason = "success codes are common"
                elif "5" in possibilities:  # Server errors
                    chosen_digit = "5"
                    reason = "server error codes"
                else:
                    chosen_digit = possibilities[0]
                    reason = "first available option"
            else:
                # For second and third digits, choose based on common codes
                if result_code == "4" and position == 1:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                    reason = "forming '40x' pattern"
                elif result_code == "40" and position == 2:
                    chosen_digit = "4" if "4" in possibilities else possibilities[0]
                    reason = "completing '404' (Not Found)"
                elif result_code == "2" and position == 1:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                    reason = "forming '20x' pattern"
                elif result_code == "20" and position == 2:
                    chosen_digit = "0" if "0" in possibilities else possibilities[0]
                    reason = "completing '200' (OK)"
                else:
                    chosen_digit = possibilities[0]
                    reason = "first available option"
            
            if verbose:
                print(f"   🎯 Chosen: '{chosen_digit}' ({reason})")
            
            # Process the chosen digit
            if fsm.process_digit(chosen_digit):
                result_code += chosen_digit
                if verbose:
                    print(f"   ✅ FSM accepted '{chosen_digit}' -> New state: {fsm.state}")
                    print(f"   Current code: '{result_code}'")
            else:
                if verbose:
                    print(f"   ❌ FSM rejected '{chosen_digit}' (unexpected error)")
                break
        
        # Ensure we have a valid 3-digit code
        if len(result_code) == 3 and fsm.is_complete():
            final_code = int(result_code)
            is_valid = final_code in fsm.VALID_CODES
            
            if verbose:
                print(f"\n   📊 Generation Summary:")
                print(f"   Generated code: '{result_code}'")
                print(f"   FSM path: {' -> '.join(fsm.path)}")
                print(f"   Valid HTTP code: {is_valid}")
                
            if is_valid:
                return result_code
        
        if verbose:
            print(f"   ⚠️  Generation failed, using fallback")
        
        # Fallback to a known valid code
        return "200"
