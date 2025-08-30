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
        
    def generate_with_constraints(
        self,
        prompt: str,
        fsm,  # FiniteStateMachine instance
        guidance_prompt: Optional[str] = None
    ) -> LLMResponse:
        """Generate text that satisfies FSM constraints."""
        
        # Build guidance system prompt
        system_prompt = self._build_system_prompt(fsm, guidance_prompt)
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.generate(
                    prompt=prompt,
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    system_prompt=system_prompt,
                    stop_sequences=self.config.stop_sequences
                )
                
                # Check if response satisfies FSM constraints
                if self._validate_response_with_fsm(response.text, fsm):
                    return response
                else:
                    # Add feedback for next attempt
                    prompt = self._add_constraint_feedback(prompt, response.text, fsm)
                    
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise RuntimeError(f"Failed to generate constrained text after {self.config.max_retries} attempts: {str(e)}")
                
                # Wait before retry
                import time
                time.sleep(self.config.retry_delay)
        
        raise RuntimeError("Failed to generate text satisfying FSM constraints")
    
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
