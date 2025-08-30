"""
Finite State Machine implementation for constraining LLM outputs.
"""
from enum import Enum
from typing import Dict, Set, Optional, List, Callable, Any
from abc import ABC, abstractmethod
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


class FSMBuilder:
    """Builder class for creating FSMs with common patterns."""
    
    @staticmethod
    def create_json_fsm() -> FiniteStateMachine:
        """Create an FSM for valid JSON structure."""
        fsm = FiniteStateMachine("start")
        
        # States
        fsm.add_state(State("start", StateType.INITIAL))
        fsm.add_state(State("object_start", StateType.INTERMEDIATE))
        fsm.add_state(State("key", StateType.INTERMEDIATE))
        fsm.add_state(State("colon", StateType.INTERMEDIATE))
        fsm.add_state(State("value", StateType.INTERMEDIATE))
        fsm.add_state(State("comma", StateType.INTERMEDIATE))
        fsm.add_state(State("object_end", StateType.FINAL))
        fsm.add_state(State("error", StateType.ERROR))
        
        # Transitions
        fsm.add_transition(Transition(
            "start", "object_start",
            lambda x: x.strip().startswith("{"),
            "Start with opening brace"
        ))
        
        fsm.add_transition(Transition(
            "object_start", "key",
            lambda x: '"' in x and not x.strip().endswith("}"),
            "Add quoted key"
        ))
        
        fsm.add_transition(Transition(
            "key", "colon",
            lambda x: ":" in x,
            "Add colon after key"
        ))
        
        fsm.add_transition(Transition(
            "colon", "value",
            lambda x: any(char in x for char in ['"', '{', '[', 't', 'f', 'n']) or x.strip()[-1].isdigit(),
            "Add value"
        ))
        
        fsm.add_transition(Transition(
            "value", "comma",
            lambda x: "," in x,
            "Add comma for next item"
        ))
        
        fsm.add_transition(Transition(
            "comma", "key",
            lambda x: '"' in x,
            "Add next key"
        ))
        
        fsm.add_transition(Transition(
            "value", "object_end",
            lambda x: x.strip().endswith("}"),
            "Close object"
        ))
        
        fsm.add_transition(Transition(
            "object_start", "object_end",
            lambda x: x.strip().endswith("}"),
            "Empty object"
        ))
        
        return fsm
    
    @staticmethod
    def create_email_fsm() -> FiniteStateMachine:
        """Create an FSM for email format validation."""
        fsm = FiniteStateMachine("start")
        
        # States
        fsm.add_state(State("start", StateType.INITIAL))
        fsm.add_state(State("username", StateType.INTERMEDIATE))
        fsm.add_state(State("at_symbol", StateType.INTERMEDIATE))
        fsm.add_state(State("domain", StateType.INTERMEDIATE))
        fsm.add_state(State("dot", StateType.INTERMEDIATE))
        fsm.add_state(State("tld", StateType.FINAL))
        fsm.add_state(State("error", StateType.ERROR))
        
        # Transitions
        fsm.add_transition(Transition(
            "start", "username",
            lambda x: re.match(r'^[a-zA-Z0-9._-]+', x.strip()),
            "Valid username characters"
        ))
        
        fsm.add_transition(Transition(
            "username", "at_symbol",
            lambda x: "@" in x,
            "At symbol"
        ))
        
        fsm.add_transition(Transition(
            "at_symbol", "domain",
            lambda x: re.search(r'@([a-zA-Z0-9.-]+)', x),
            "Domain name"
        ))
        
        fsm.add_transition(Transition(
            "domain", "dot",
            lambda x: "." in x.split("@")[-1],
            "Dot in domain"
        ))
        
        fsm.add_transition(Transition(
            "dot", "tld",
            lambda x: re.search(r'\.([a-zA-Z]{2,})$', x),
            "Top-level domain"
        ))
        
        return fsm
    
    @staticmethod
    def create_conversation_fsm() -> FiniteStateMachine:
        """Create an FSM for structured conversation flow."""
        fsm = FiniteStateMachine("greeting")
        
        # States
        fsm.add_state(State("greeting", StateType.INITIAL))
        fsm.add_state(State("question", StateType.INTERMEDIATE))
        fsm.add_state(State("answer", StateType.INTERMEDIATE))
        fsm.add_state(State("clarification", StateType.INTERMEDIATE))
        fsm.add_state(State("conclusion", StateType.FINAL))
        fsm.add_state(State("error", StateType.ERROR))
        
        # Transitions
        greeting_keywords = ["hello", "hi", "hey", "greetings"]
        question_keywords = ["what", "how", "why", "when", "where", "?"]
        answer_keywords = ["the answer", "it is", "here", "because"]
        clarify_keywords = ["clarify", "explain", "elaborate", "could you"]
        conclude_keywords = ["thank you", "goodbye", "bye", "thanks"]
        
        fsm.add_transition(Transition(
            "greeting", "question",
            lambda x: any(keyword in x.lower() for keyword in question_keywords),
            "Ask a question"
        ))
        
        fsm.add_transition(Transition(
            "question", "answer",
            lambda x: any(keyword in x.lower() for keyword in answer_keywords),
            "Provide an answer"
        ))
        
        fsm.add_transition(Transition(
            "answer", "clarification",
            lambda x: any(keyword in x.lower() for keyword in clarify_keywords),
            "Request clarification"
        ))
        
        fsm.add_transition(Transition(
            "clarification", "answer",
            lambda x: any(keyword in x.lower() for keyword in answer_keywords),
            "Provide clarified answer"
        ))
        
        fsm.add_transition(Transition(
            "answer", "conclusion",
            lambda x: any(keyword in x.lower() for keyword in conclude_keywords),
            "Conclude conversation"
        ))
        
        fsm.add_transition(Transition(
            "answer", "question",
            lambda x: any(keyword in x.lower() for keyword in question_keywords),
            "Ask follow-up question"
        ))
        
        return fsm
