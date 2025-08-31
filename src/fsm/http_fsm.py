"""
HTTP Status Code Finite State Machine
====================================

A simple FSM that processes HTTP status codes digit by digit.
Each digit moves the FSM to the next state.

States:
- start: Initial state
- first_digit: After processing first digit (1-5)
- second_digit: After processing second digit (0-9)
- third_digit: Final state after processing third digit (0-9)
"""

from typing import List, Optional


class HTTPCodeFSM:
    """Finite State Machine for HTTP status codes."""
    
    # Valid HTTP status codes
    VALID_CODES = {
        # 1xx Informational
        100, 101, 102, 103,
        
        # 2xx Success  
        200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
        
        # 3xx Redirection
        300, 301, 302, 303, 304, 305, 307, 308,
        
        # 4xx Client Error
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
        410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
        422, 423, 424, 425, 426, 428, 429, 431, 451,
        
        # 5xx Server Error
        500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
    }
    
    def __init__(self):
        """Initialize the FSM."""
        self.reset()
    
    def reset(self):
        """Reset FSM to initial state."""
        self.state = "start"
        self.current_code = ""
        self.path = ["start"]
    
    def get_valid_first_digits(self) -> List[str]:
        """Get valid first digits (1-5)."""
        return ["1", "2", "3", "4", "5"]
    
    def get_valid_second_digits(self, first_digit: str) -> List[str]:
        """Get valid second digits based on first digit."""
        if first_digit in ["1", "2", "3", "4", "5"]:
            return [str(i) for i in range(10)]  # 0-9
        return []
    
    def get_valid_third_digits(self, first_two: str) -> List[str]:
        """Get valid third digits based on first two digits."""
        valid_thirds = []
        for code in self.VALID_CODES:
            if str(code).startswith(first_two):
                third_digit = str(code)[2]
                if third_digit not in valid_thirds:
                    valid_thirds.append(third_digit)
        return sorted(valid_thirds)
    
    def process_digit(self, digit: str) -> bool:
        """Process a single digit through the FSM."""
        if not digit.isdigit():
            return False
        
        if self.state == "start":
            if digit in self.get_valid_first_digits():
                self.state = "first_digit"
                self.current_code = digit
                self.path.append("first_digit")
                return True
            return False
        
        elif self.state == "first_digit":
            if digit in self.get_valid_second_digits(self.current_code):
                self.state = "second_digit"
                self.current_code += digit
                self.path.append("second_digit")
                return True
            return False
        
        elif self.state == "second_digit":
            if digit in self.get_valid_third_digits(self.current_code):
                self.state = "third_digit"
                self.current_code += digit
                self.path.append("third_digit")
                return True
            return False
        
        return False
    
    def process_input(self, input_str: str) -> bool:
        """Process complete input string digit by digit."""
        input_str = input_str.strip()
        
        # Must be exactly 3 digits
        if len(input_str) != 3 or not input_str.isdigit():
            return False
        
        # Process each digit
        for digit in input_str:
            if not self.process_digit(digit):
                return False
        
        # Check if final code is valid and we're in final state
        if self.state == "third_digit" and len(self.current_code) == 3:
            code = int(self.current_code)
            return code in self.VALID_CODES
        
        return False
    
    def is_complete(self) -> bool:
        """Check if FSM is in final state."""
        return self.state == "third_digit"
    
    def get_current_possibilities(self) -> List[str]:
        """Get valid next digits based on current state."""
        if self.state == "start":
            return self.get_valid_first_digits()
        elif self.state == "first_digit":
            return self.get_valid_second_digits(self.current_code)
        elif self.state == "second_digit":
            return self.get_valid_third_digits(self.current_code)
        else:
            return []
    
    def get_state_info(self) -> dict:
        """Get current state information."""
        return {
            "state": self.state,
            "current_code": self.current_code,
            "path": self.path.copy(),
            "next_possibilities": self.get_current_possibilities(),
            "is_complete": self.is_complete()
        }
    
    def generate_valid_completion(self) -> Optional[str]:
        """Generate a valid completion from current state."""
        if self.state == "start":
            # Return a common HTTP code
            return "200"
        elif self.state == "first_digit":
            # Complete with common second and third digits
            possibilities = self.get_valid_second_digits(self.current_code)
            if possibilities:
                # Try to find a common completion
                for second in ["0", "1", "2", "3", "4"]:
                    if second in possibilities:
                        test_code = self.current_code + second
                        thirds = self.get_valid_third_digits(test_code)
                        if thirds:
                            return test_code + thirds[0]
        elif self.state == "second_digit":
            # Complete with valid third digit
            thirds = self.get_valid_third_digits(self.current_code)
            if thirds:
                return self.current_code + thirds[0]
        
        return None
    
    def __str__(self) -> str:
        """String representation of FSM."""
        return f"HTTPCodeFSM(state={self.state}, code='{self.current_code}')"
