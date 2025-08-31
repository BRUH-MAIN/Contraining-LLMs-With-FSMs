"""
Finite State Machine implementation for constraining LLM outputs.
"""
from enum import Enum
from typing import Dict, Set, Optional, List, Callable, Any
import re


class StateType(Enum):
    """Types of states in the FSM."""
    INITIAL = "initial"
    INTERMEDIATE = "intermediate"
    FINAL = "final"
    ERROR = "error"


class State:
    """Represents a state in the finite state machine."""
    
    def __init__(
        self, 
        name: str, 
        state_type: StateType = StateType.INTERMEDIATE,
        validators: Optional[List[Callable[[str], bool]]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.state_type = state_type
        self.validators = validators or []
        self.constraints = constraints or {}
        
    def validate(self, input_text: str) -> bool:
        """Validate input text against state constraints."""
        return all(validator(input_text) for validator in self.validators)
    
    def __str__(self) -> str:
        return f"State({self.name}, {self.state_type.value})"
    
    def __repr__(self) -> str:
        return self.__str__()


class Transition:
    """Represents a transition between states."""
    
    def __init__(
        self,
        from_state: str,
        to_state: str,
        condition: Callable[[str], bool],
        description: Optional[str] = None
    ):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.description = description or f"{from_state} -> {to_state}"
    
    def can_transition(self, input_text: str) -> bool:
        """Check if transition condition is met."""
        return self.condition(input_text)
    
    def __str__(self) -> str:
        return f"Transition({self.from_state} -> {self.to_state})"


class FiniteStateMachine:
    """Finite State Machine for constraining LLM outputs."""
    
    def __init__(self, initial_state: str):
        self.states: Dict[str, State] = {}
        self.transitions: List[Transition] = []
        self.current_state = initial_state
        self.initial_state = initial_state
        self.history: List[str] = [initial_state]
        
    def add_state(self, state: State) -> None:
        """Add a state to the FSM."""
        self.states[state.name] = state
    
    def add_transition(self, transition: Transition) -> None:
        """Add a transition to the FSM."""
        self.transitions.append(transition)
    
    def get_valid_transitions(self, input_text: str) -> List[Transition]:
        """Get all valid transitions from current state given input."""
        valid_transitions = []
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.can_transition(input_text)):
                valid_transitions.append(transition)
        return valid_transitions
    
    def transition(self, input_text: str) -> bool:
        """Attempt to transition based on input text."""
        valid_transitions = self.get_valid_transitions(input_text)
        
        if not valid_transitions:
            return False
        
        # Take the first valid transition (can be modified for priority)
        transition = valid_transitions[0]
        
        # Validate against target state
        target_state = self.states.get(transition.to_state)
        if target_state and target_state.validate(input_text):
            self.current_state = transition.to_state
            self.history.append(self.current_state)
            return True
        
        return False
    
    def is_final_state(self) -> bool:
        """Check if current state is a final state."""
        current = self.states.get(self.current_state)
        return current and current.state_type == StateType.FINAL
    
    def is_error_state(self) -> bool:
        """Check if current state is an error state."""
        current = self.states.get(self.current_state)
        return current and current.state_type == StateType.ERROR
    
    def reset(self) -> None:
        """Reset FSM to initial state."""
        self.current_state = self.initial_state
        self.history = [self.initial_state]
    
    def get_allowed_patterns(self) -> List[str]:
        """Get patterns that are allowed from current state."""
        patterns = []
        for transition in self.transitions:
            if transition.from_state == self.current_state:
                patterns.append(transition.description)
        return patterns
    
    def __str__(self) -> str:
        return f"FSM(current={self.current_state}, states={len(self.states)})"
