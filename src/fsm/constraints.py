"""
HTTP Status Code Constraints for FSM states.
"""
import re
from typing import Callable


class HTTPConstraints:
    """Collection of HTTP status code constraints for FSM states."""
    
    # Standard HTTP status codes
    VALID_HTTP_CODES = {
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
    
    @staticmethod
    def valid_http_status_code() -> Callable[[str], bool]:
        """Constraint for valid HTTP status code (3-digit number)."""
        def validator(text: str) -> bool:
            text = text.strip()
            # Check if it's a 3-digit number
            if not re.match(r'^\d{3}$', text):
                return False
            code = int(text)
            return code in HTTPConstraints.VALID_HTTP_CODES
        return validator
    
    @staticmethod
    def server_error_codes() -> Callable[[str], bool]:
        """Constraint for server error codes (5xx)."""
        def validator(text: str) -> bool:
            text = text.strip()
            if not re.match(r'^\d{3}$', text):
                return False
            code = int(text)
            return 500 <= code <= 599 and code in HTTPConstraints.VALID_HTTP_CODES
        return validator
    
    @staticmethod
    def client_error_codes() -> Callable[[str], bool]:
        """Constraint for client error codes (4xx)."""
        def validator(text: str) -> bool:
            text = text.strip()
            if not re.match(r'^\d{3}$', text):
                return False
            code = int(text)
            return 400 <= code <= 499 and code in HTTPConstraints.VALID_HTTP_CODES
        return validator
    
    @staticmethod
    def success_codes() -> Callable[[str], bool]:
        """Constraint for success codes (2xx)."""
        def validator(text: str) -> bool:
            text = text.strip()
            if not re.match(r'^\d{3}$', text):
                return False
            code = int(text)
            return 200 <= code <= 299 and code in HTTPConstraints.VALID_HTTP_CODES
        return validator
    
    @staticmethod
    def specific_codes(*codes) -> Callable[[str], bool]:
        """Constraint for specific HTTP status codes."""
        def validator(text: str) -> bool:
            text = text.strip()
            if not re.match(r'^\d{3}$', text):
                return False
            code = int(text)
            return code in codes
        return validator
