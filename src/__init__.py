"""
HTTP Status Code Constraints for LLMs
====================================

A simple demonstration of constraining LLM outputs to valid HTTP status codes.

Main Components:
- FSM: Finite State Machine implementation with HTTP constraints
- LLM: Groq API client with constraint enforcement

Usage:
    >>> from src.fsm import FiniteStateMachine, State, StateType, HTTPConstraints
    >>> from src.llm import GroqClient, ConstrainedLLM
    >>> 
    >>> # Create FSM with HTTP constraints
    >>> fsm = FiniteStateMachine("start")
    >>> # Add states and transitions...
    >>> 
    >>> # Create constrained LLM
    >>> client = GroqClient()
    >>> constrained_llm = ConstrainedLLM(client)
    >>> response = constrained_llm.generate_with_constraints("prompt", fsm)
"""

from .fsm import (
    FiniteStateMachine,
    State,
    Transition,
    StateType,
    FSMBuilder,
    HTTPConstraints
)

from .llm import (
    GroqClient,
    ConstrainedLLM,
    ConstrainedLLMConfig,
    LLMResponse
)

__version__ = "0.1.0"
__author__ = "HTTP-Status-Code-Constraints Project"
__description__ = "Constraining LLMs to generate valid HTTP status codes using FSMs"

__all__ = [
    # FSM components
    'FiniteStateMachine',
    'State',
    'Transition',
    'StateType',
    'FSMBuilder',
    'HTTPConstraints',
    
    # LLM components
    'GroqClient',
    'ConstrainedLLM',
    'ConstrainedLLMConfig',
    'LLMResponse',
    
    # Metadata
    '__version__',
    '__author__',
    '__description__'
]
