"""
LaTeX Math FSM
==============

A finite state machine for validating LaTeX mathematical expressions token-by-token.

Usage:
    >>> from src.fsm import LaTeXMathFSM
    >>> from src.llm import SimpleGroqClient
    >>> 
    >>> # Create FSM
    >>> fsm = LaTeXMathFSM()
    >>> 
    >>> # Test with LaTeX expression
    >>> result = fsm.process_input("$x^2$")
    >>> print(f"Valid: {result}")
"""

from .fsm import LaTeXMathFSM
from .llm import SimpleGroqClient

__all__ = ['LaTeXMathFSM', 'SimpleGroqClient']
__version__ = "0.3.0"
