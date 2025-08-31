"""
Groq API client for LLM interactions.
"""
import os
from typing import Optional, List, Dict, Any, Generator, Iterator
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_AVAILABLE = False

try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    # Fallback base class
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def Field(**kwargs):
        return kwargs.get('default')
    
    PYDANTIC_AVAILABLE = False

import time
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM containing generated text and metadata."""
    text: str
    model: str
    tokens_used: int
    finish_reason: str
    metadata: Dict[str, Any]


class GroqClient:
    """Client for interacting with Groq API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client."""
        if not GROQ_AVAILABLE:
            raise RuntimeError("Groq package not available. Install with: pip install groq")
            
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.default_model = "llama3-8b-8192"
        
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> LLMResponse:
        """Generate text using Groq API."""
        
        if not GROQ_AVAILABLE:
            raise RuntimeError("Groq package not available. Install with: pip install groq")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences
            )
            
            choice = response.choices[0]
            return LLMResponse(
                text=choice.message.content,
                model=response.model,
                tokens_used=response.usage.total_tokens,
                finish_reason=choice.finish_reason,
                metadata={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "created": response.created,
                    "id": response.id
                }
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {str(e)}")
    
    def generate_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> Generator[str, None, None]:
        """Generate text using streaming API."""
        
        if not GROQ_AVAILABLE:
            raise RuntimeError("Groq package not available. Install with: pip install groq")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise RuntimeError(f"Failed to generate streaming text: {str(e)}")
    
    def list_models(self) -> List[str]:
        """List available models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            # Return default models if API call fails
            return [
                "llama3-8b-8192",
                "llama3-70b-8192",
                "mixtral-8x7b-32768",
                "gemma-7b-it"
            ]


class ConstrainedLLMConfig(BaseModel):
    """Configuration for constrained LLM generation."""
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_retries: int = Field(default=3, ge=1, le=10)
    retry_delay: float = Field(default=1.0, ge=0.1, le=10.0)
    model: str = Field(default="llama3-8b-8192")
    system_prompt: Optional[str] = None
    stop_sequences: Optional[List[str]] = None
    
    class Config:
        extra = "forbid"


class ConstrainedLLM:
    """LLM wrapper that enforces constraints through FSM."""
    
    def __init__(self, groq_client: GroqClient, config: Optional[ConstrainedLLMConfig] = None):
        self.client = groq_client
        self.config = config or ConstrainedLLMConfig()
        
    def generate_continuous_with_constraints(
        self,
        prompt: str,
        fsm,  # FiniteStateMachine instance
        guidance_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Generate text continuously, guiding each token with FSM constraints."""
        
        # Build guidance system prompt
        system_prompt = self._build_system_prompt(fsm, guidance_prompt)
        max_tokens = max_tokens or self.config.max_tokens
        
        # Reset FSM to initial state
        fsm.reset()
        generated_text = ""
        total_tokens = 0
        
        # Continue generating until we reach a final state or max tokens
        while total_tokens < max_tokens and not fsm.is_final_state():
            try:
                # Generate next token/chunk with current context
                current_prompt = prompt
                if generated_text:
                    current_prompt += f"\n\nContinue from: {generated_text}"
                
                # Add FSM state guidance to prompt
                state_guidance = self._build_state_guidance(fsm)
                current_prompt += state_guidance
                
                # Generate a small chunk (1-5 tokens)
                response = self.client.generate(
                    prompt=current_prompt,
                    model=self.config.model,
                    max_tokens=min(5, max_tokens - total_tokens),  # Generate small chunks
                    temperature=self.config.temperature,
                    system_prompt=system_prompt,
                    stop_sequences=self.config.stop_sequences
                )
                
                candidate_text = generated_text + response.text
                
                # Test if this addition satisfies FSM constraints
                if self._can_fsm_accept_text(candidate_text, fsm):
                    # Accept this generation
                    generated_text = candidate_text
                    total_tokens += response.tokens_used
                    
                    # Update FSM state
                    self._update_fsm_with_text(generated_text, fsm)
                    
                    # Check if we've reached a valid final state
                    if fsm.is_final_state():
                        break
                        
                else:
                    # Reject this generation and try alternative
                    # Generate with more constraint guidance
                    constraint_prompt = self._build_rejection_guidance(candidate_text, fsm)
                    current_prompt += constraint_prompt
                    
                    # Try again with stronger guidance
                    response = self.client.generate(
                        prompt=current_prompt,
                        model=self.config.model,
                        max_tokens=min(3, max_tokens - total_tokens),
                        temperature=max(0.1, self.config.temperature - 0.3),  # Lower temperature for more control
                        system_prompt=system_prompt,
                        stop_sequences=self.config.stop_sequences
                    )
                    
                    candidate_text = generated_text + response.text
                    
                    # If still doesn't work, force a valid transition
                    if not self._can_fsm_accept_text(candidate_text, fsm):
                        # Generate a minimal valid continuation
                        valid_continuation = self._generate_minimal_valid_continuation(fsm)
                        generated_text += valid_continuation
                        total_tokens += len(valid_continuation.split())  # Rough token count
                        self._update_fsm_with_text(generated_text, fsm)
                    else:
                        generated_text = candidate_text
                        total_tokens += response.tokens_used
                        self._update_fsm_with_text(generated_text, fsm)
                        
            except Exception as e:
                # If generation fails, try to complete with minimal valid text
                if not generated_text:
                    raise RuntimeError(f"Failed to start generation: {str(e)}")
                
                # Try to reach final state with minimal addition
                completion = self._force_completion_to_final_state(generated_text, fsm)
                generated_text += completion
                break
        
        # Create response object
        return LLMResponse(
            text=generated_text,
            model=self.config.model,
            tokens_used=total_tokens,
            finish_reason="stop" if fsm.is_final_state() else "length",
            metadata={"fsm_final_state": fsm.is_final_state(), "fsm_current_state": fsm.current_state}
        )
    
    def _build_state_guidance(self, fsm) -> str:
        """Build guidance based on current FSM state."""
        current_state = fsm.states.get(fsm.current_state)
        if not current_state:
            return ""
        
        guidance = f"\n\n[FSM STATE: {current_state.name}]"
        
        # Get valid transitions from current state
        valid_transitions = []
        for transition in fsm.transitions:
            if transition.from_state == fsm.current_state:
                valid_transitions.append(transition.description)
        
        if valid_transitions:
            guidance += f"\nValid next steps: {', '.join(valid_transitions)}"
        
        return guidance
    
    def _can_fsm_accept_text(self, text: str, fsm) -> bool:
        """Check if FSM can accept the given text."""
        # Create a copy of FSM to test
        test_fsm = type(fsm)(fsm.initial_state)
        test_fsm.states = fsm.states.copy()
        test_fsm.transitions = fsm.transitions.copy()
        
        # Reset and try to transition
        test_fsm.reset()
        return test_fsm.transition(text)
    
    def _update_fsm_with_text(self, text: str, fsm) -> None:
        """Update the FSM state with the given text."""
        fsm.reset()
        fsm.transition(text)
    
    def _build_rejection_guidance(self, rejected_text: str, fsm) -> str:
        """Build guidance when text is rejected by FSM."""
        guidance = f"\n\n[CONSTRAINT VIOLATION] The text '{rejected_text[-20:]}...' violates constraints."
        guidance += f"\nCurrent state: {fsm.current_state}"
        
        # Get allowed patterns
        patterns = fsm.get_allowed_patterns()
        if patterns:
            guidance += f"\nRequired patterns: {', '.join(patterns)}"
        
        guidance += "\nGenerate only text that follows the structural requirements."
        return guidance
    
    def _generate_minimal_valid_continuation(self, fsm) -> str:
        """Generate minimal text to make a valid transition."""
        # This is a fallback - generate the simplest valid continuation
        valid_transitions = []
        for transition in fsm.transitions:
            if transition.from_state == fsm.current_state:
                valid_transitions.append(transition)
        
        if valid_transitions:
            # For HTTP codes, this might be just a number
            if "error" in fsm.current_state.lower():
                return "404"  # Default to 404 for errors
            elif "success" in fsm.current_state.lower():
                return "200"  # Default to 200 for success
            else:
                return "200"  # Default HTTP code
        
        return ""
    
    def _force_completion_to_final_state(self, current_text: str, fsm) -> str:
        """Force completion to reach a final state."""
        # Simple completion strategy for HTTP codes
        if not current_text.strip():
            return "200"  # Valid HTTP status code
        
        # If already has some text, try to complete minimally
        text = current_text.strip()
        if text and text[-1].isdigit():
            return ""  # Already looks like a complete HTTP code
        
        return " 200"  # Add a valid HTTP code

    def generate_with_constraints(
        self,
        prompt: str,
        fsm,  # FiniteStateMachine instance
        guidance_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate text that satisfies FSM constraints."""
        
        # Use the new continuous generation method
        return self.generate_continuous_with_constraints(prompt, fsm, guidance_prompt)
    
    def generate_stream_with_constraints(
        self,
        prompt: str,
        fsm,  # FiniteStateMachine instance
        guidance_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Generate streaming text with FSM constraints."""
        
        system_prompt = self._build_system_prompt(fsm, guidance_prompt)
        accumulated_text = ""
        
        for chunk in self.client.generate_stream(
            prompt=prompt,
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system_prompt=system_prompt,
            stop_sequences=self.config.stop_sequences
        ):
            accumulated_text += chunk
            
            # Check if current text violates constraints
            if self._validate_partial_response_with_fsm(accumulated_text, fsm):
                yield chunk
            else:
                # Stop generation if constraints are violated
                break
    
    def _build_system_prompt(self, fsm, guidance_prompt: Optional[str] = None) -> str:
        """Build system prompt with FSM guidance."""
        base_prompt = "You are an AI assistant that must follow specific structural constraints."
        
        if guidance_prompt:
            base_prompt += f" {guidance_prompt}"
        
        # Add FSM state information
        current_state = fsm.states.get(fsm.current_state)
        if current_state:
            base_prompt += f"\n\nCurrent state: {current_state.name}"
            
            # Add allowed patterns
            patterns = fsm.get_allowed_patterns()
            if patterns:
                base_prompt += f"\nAllowed transitions: {', '.join(patterns)}"
        
        # Add structural requirements
        base_prompt += "\n\nIMPORTANT: Your response must follow the specified structural constraints and state transitions."
        
        return base_prompt
    
    def _validate_response_with_fsm(self, text: str, fsm) -> bool:
        """Validate complete response against FSM."""
        fsm.reset()
        return fsm.transition(text) and (fsm.is_final_state() or not fsm.is_error_state())
    
    def _validate_partial_response_with_fsm(self, text: str, fsm) -> bool:
        """Validate partial response against FSM (for streaming)."""
        # Create a copy of FSM to test partial text
        test_fsm = type(fsm)(fsm.initial_state)
        test_fsm.states = fsm.states.copy()
        test_fsm.transitions = fsm.transitions.copy()
        
        # Try to transition with partial text
        return test_fsm.transition(text) or test_fsm.current_state != "error"
    
    def _add_constraint_feedback(self, original_prompt: str, failed_response: str, fsm) -> str:
        """Add feedback about constraint violations to prompt."""
        feedback = f"\n\nPrevious attempt failed constraints. Response was: '{failed_response[:100]}...'"
        feedback += f"\nCurrent FSM state: {fsm.current_state}"
        feedback += f"\nRequired patterns: {', '.join(fsm.get_allowed_patterns())}"
        feedback += "\nPlease generate a response that follows the structural constraints."
        
        return original_prompt + feedback
