"""
Constraining LLMs with Finite State Machines
============================================

A Python library for constraining Large Language Model outputs using
Finite State Machines (FSMs) with Groq API integration.

Main Components:
- FSM: Finite State Machine implementation with constraints
- LLM: Groq API client with constraint enforcement
- Examples: Practical usage examples

Usage:
    >>> from src.fsm import FiniteStateMachine, State, StateType
    >>> from src.llm import GroqClient, ConstrainedLLM
    >>> 
    >>> # Create FSM
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
    TextConstraints,
    StructuralConstraints,
    ContentConstraints,
    CompositeConstraints
)

from .llm import (
    GroqClient,
    ConstrainedLLM,
    ConstrainedLLMConfig,
    LLMResponse
)

__version__ = "0.1.0"
__author__ = "FSM-LLM Project"
__description__ = "Constraining Large Language Models using Finite State Machines"

__all__ = [
    # FSM components
    'FiniteStateMachine',
    'State',
    'Transition',
    'StateType',
    'FSMBuilder',
    'TextConstraints',
    'StructuralConstraints',
    'ContentConstraints',
    'CompositeConstraints',
    
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
