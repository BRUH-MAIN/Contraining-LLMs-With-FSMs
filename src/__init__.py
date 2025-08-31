"""
Simple HTTP Status Code FSM
==========================

A simplified implementation of constraining HTTP status codes digit by digit.

Usage:
    >>> from src.fsm import HTTPCodeFSM
    >>> from src.llm import SimpleGroqClient
    >>> 
    >>> # Create FSM
    >>> fsm = HTTPCodeFSM()
    >>> 
    >>> # Test with HTTP code
    >>> result = fsm.process_input("404")
    >>> print(f"Valid: {result}")
"""

from .fsm import HTTPCodeFSM
from .llm import SimpleGroqClient

__all__ = ['HTTPCodeFSM', 'SimpleGroqClient']
__version__ = "0.2.0"
