"""
Unified LLM Client for LaTeX Math FSM-constrained generation.
============================================================

A unified client that supports both Groq API and local Hugging Face models for generating 
valid LaTeX mathematical expressions token-by-token with FSM constraints.
"""

import os
from typing import Optional, Dict, Any, Union, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .simple_client import SimpleGroqClient
    from .local_client import LocalGemmaClient

try:
    from .simple_client import SimpleGroqClient, GROQ_AVAILABLE
except ImportError:
    SimpleGroqClient = None
    GROQ_AVAILABLE = False

try:
    from .local_client import LocalGemmaClient, TRANSFORMERS_AVAILABLE
except ImportError:
    LocalGemmaClient = None
    TRANSFORMERS_AVAILABLE = False


class ModelType(Enum):
    """Enumeration of supported model types."""
    GROQ = "groq"
    LOCAL_GEMMA = "local_gemma"


class UnifiedLLMClient:
    """Unified LLM client supporting both Groq and local models."""
    
    def __init__(
        self, 
        model_type: Union[ModelType, str] = ModelType.GROQ,
        groq_api_key: Optional[str] = None,
        local_model_name: str = "google/gemma-3-270m",
        device: Optional[str] = None,
        auto_fallback: bool = True
    ):
        """Initialize the unified LLM client.
        
        Args:
            model_type: Type of model to use (GROQ or LOCAL_GEMMA)
            groq_api_key: API key for Groq (if None, uses environment variable)
            local_model_name: Hugging Face model name for local models
            device: Device for local models ('cuda', 'cpu', 'auto')
            auto_fallback: Whether to automatically fallback to alternative model on failure
        """
        self.model_type = ModelType(model_type) if isinstance(model_type, str) else model_type
        self.auto_fallback = auto_fallback
        self.client = None
        self.fallback_client = None
        
        print(f"🚀 Initializing Unified LLM Client with {self.model_type.value} model...")
        
        # Initialize primary client
        if self.model_type == ModelType.GROQ:
            self.client = self._init_groq_client(groq_api_key)
            if auto_fallback and TRANSFORMERS_AVAILABLE:
                try:
                    self.fallback_client = self._init_local_client(local_model_name, device)
                    print("📋 Local model fallback available")
                except Exception as e:
                    print(f"⚠️  Local model fallback failed to initialize: {e}")
        
        elif self.model_type == ModelType.LOCAL_GEMMA:
            self.client = self._init_local_client(local_model_name, device)
            if auto_fallback and GROQ_AVAILABLE:
                try:
                    self.fallback_client = self._init_groq_client(groq_api_key)
                    print("📋 Groq API fallback available")
                except Exception as e:
                    print(f"⚠️  Groq API fallback failed to initialize: {e}")
        
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
        
        if self.client is None:
            raise RuntimeError(f"Failed to initialize {self.model_type.value} client")
        
        print(f"✅ Unified LLM Client initialized successfully!")
    
    def _init_groq_client(self, api_key: Optional[str]):
        """Initialize Groq client."""
        if not GROQ_AVAILABLE:
            print("❌ Groq package not available")
            return None
        
        try:
            return SimpleGroqClient(api_key=api_key)
        except Exception as e:
            print(f"❌ Failed to initialize Groq client: {e}")
            return None
    
    def _init_local_client(self, model_name: str, device: Optional[str]):
        """Initialize local model client."""
        if not TRANSFORMERS_AVAILABLE:
            print("❌ Transformers package not available")
            return None
        
        try:
            return LocalGemmaClient(model_name=model_name, device=device)
        except Exception as e:
            print(f"❌ Failed to initialize local client: {e}")
            return None
    
    def generate_simple(
        self,
        prompt: str,
        max_tokens: int = 50,
        temperature: float = 0.3
    ) -> str:
        """Generate simple text response using the primary or fallback client."""
        try:
            return self.client.generate_simple(prompt, max_tokens, temperature)
        except Exception as e:
            print(f"⚠️  Primary client failed: {e}")
            
            if self.auto_fallback and self.fallback_client:
                print(f"🔄 Attempting fallback...")
                try:
                    return self.fallback_client.generate_simple(prompt, max_tokens, temperature)
                except Exception as fallback_e:
                    print(f"❌ Fallback also failed: {fallback_e}")
                    raise RuntimeError(f"Both primary and fallback clients failed. Primary: {e}, Fallback: {fallback_e}")
            
            raise RuntimeError(f"Primary client failed: {e}")
    
    def generate_with_latex_fsm(self, prompt: str, fsm, verbose: bool = True) -> str:
        """Generate LaTeX math expressions constrained by FSM using primary or fallback client."""
        client_name = f"{self.model_type.value} client"
        
        try:
            if verbose:
                print(f"🎯 Using {client_name} for LaTeX FSM generation")
            
            return self.client.generate_with_latex_fsm(prompt, fsm, verbose)
        
        except Exception as e:
            if verbose:
                print(f"⚠️  {client_name} failed: {e}")
            
            if self.auto_fallback and self.fallback_client:
                fallback_name = "Groq API" if self.model_type == ModelType.LOCAL_GEMMA else "local model"
                
                if verbose:
                    print(f"🔄 Attempting fallback to {fallback_name}...")
                
                try:
                    return self.fallback_client.generate_with_latex_fsm(prompt, fsm, verbose)
                except Exception as fallback_e:
                    if verbose:
                        print(f"❌ Fallback to {fallback_name} also failed: {fallback_e}")
                    raise RuntimeError(f"Both primary and fallback clients failed. Primary ({client_name}): {e}, Fallback ({fallback_name}): {fallback_e}")
            
            raise RuntimeError(f"{client_name} failed: {e}")
    
    def extract_latex_expression(self, text: str) -> Optional[str]:
        """Extract LaTeX mathematical expression from text."""
        # Delegate to the primary client if it has this method
        if hasattr(self.client, 'extract_latex_expression'):
            return self.client.extract_latex_expression(text)
        
        # Fallback to manual extraction if client doesn't have the method
        import re
        
        # Try inline math first: $...$
        inline_matches = re.findall(r'\$([^$]+)\$', text)
        if inline_matches:
            return f"${inline_matches[0]}$"
        
        # Try display math: $$...$$
        display_matches = re.findall(r'\$\$([^$]+)\$\$', text)
        if display_matches:
            return f"$${display_matches[0]}$$"
        
        # Try LaTeX blocks: \[...\]
        block_matches = re.findall(r'\\\\?\[([^\\]+)\\\\?\]', text)
        if block_matches:
            return f"\\[{block_matches[0]}\\]"
        
        return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        info = {
            "primary_model_type": self.model_type.value,
            "auto_fallback": self.auto_fallback,
            "fallback_available": self.fallback_client is not None
        }
        
        # Add primary client info
        if hasattr(self.client, 'get_model_info'):
            info["primary_model"] = self.client.get_model_info()
        elif hasattr(self.client, 'default_model'):
            info["primary_model"] = {
                "model_name": self.client.default_model,
                "model_type": "groq_api"
            }
        
        # Add fallback client info
        if self.fallback_client:
            if hasattr(self.fallback_client, 'get_model_info'):
                info["fallback_model"] = self.fallback_client.get_model_info()
            elif hasattr(self.fallback_client, 'default_model'):
                info["fallback_model"] = {
                    "model_name": self.fallback_client.default_model,
                    "model_type": "groq_api"
                }
        
        return info
    
    def switch_model(self, new_model_type: Union[ModelType, str]) -> bool:
        """Switch to a different model type.
        
        Args:
            new_model_type: New model type to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        new_type = ModelType(new_model_type) if isinstance(new_model_type, str) else new_model_type
        
        if new_type == self.model_type:
            print(f"Already using {new_type.value} model")
            return True
        
        # Check if we can switch to the requested type
        if new_type == ModelType.GROQ and not GROQ_AVAILABLE:
            print("❌ Cannot switch to Groq: package not available")
            return False
        
        if new_type == ModelType.LOCAL_GEMMA and not TRANSFORMERS_AVAILABLE:
            print("❌ Cannot switch to local model: transformers package not available")
            return False
        
        # If we have a fallback client of the requested type, switch to it
        if self.fallback_client:
            if ((new_type == ModelType.GROQ and hasattr(self.fallback_client, 'default_model')) or
                (new_type == ModelType.LOCAL_GEMMA and hasattr(self.fallback_client, 'model_name'))):
                
                print(f"🔄 Switching from {self.model_type.value} to {new_type.value}")
                
                # Swap primary and fallback
                self.client, self.fallback_client = self.fallback_client, self.client
                self.model_type = new_type
                
                print(f"✅ Successfully switched to {new_type.value} model")
                return True
        
        print(f"❌ Cannot switch to {new_type.value}: no available client")
        return False
    
    @classmethod
    def create_auto(cls, prefer_local: bool = False, **kwargs) -> 'UnifiedLLMClient':
        """Create a client with automatic model selection based on availability.
        
        Args:
            prefer_local: Whether to prefer local models over API-based ones
            **kwargs: Additional arguments for client initialization
            
        Returns:
            Initialized UnifiedLLMClient
        """
        # Determine preferred order
        if prefer_local:
            model_types = [ModelType.LOCAL_GEMMA, ModelType.GROQ]
        else:
            model_types = [ModelType.GROQ, ModelType.LOCAL_GEMMA]
        
        last_error = None
        
        for model_type in model_types:
            try:
                print(f"🔍 Trying {model_type.value} model...")
                return cls(model_type=model_type, **kwargs)
            except Exception as e:
                last_error = e
                print(f"❌ {model_type.value} failed: {e}")
        
        raise RuntimeError(f"No available models could be initialized. Last error: {last_error}")


# Convenience functions for backward compatibility
def create_groq_client(api_key: Optional[str] = None, **kwargs) -> UnifiedLLMClient:
    """Create a Groq-based unified client."""
    return UnifiedLLMClient(model_type=ModelType.GROQ, groq_api_key=api_key, **kwargs)


def create_local_client(model_name: str = "google/gemma-2-2b-it", device: Optional[str] = None, **kwargs) -> UnifiedLLMClient:
    """Create a local model-based unified client."""
    return UnifiedLLMClient(model_type=ModelType.LOCAL_GEMMA, local_model_name=model_name, device=device, **kwargs)


def create_auto_client(prefer_local: bool = False, **kwargs) -> UnifiedLLMClient:
    """Create a client with automatic model selection."""
    return UnifiedLLMClient.create_auto(prefer_local=prefer_local, **kwargs)
