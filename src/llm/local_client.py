"""
Local Gemma Client for LaTeX Math FSM-constrained generation.
============================================================

A client that uses local Hugging Face Transformers models to generate valid LaTeX mathematical expressions token-by-token.
"""

import re
import torch
from typing import Optional, List, Dict, Any
import warnings

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    AutoTokenizer = None
    AutoModelForCausalLM = None
    GenerationConfig = None
    TRANSFORMERS_AVAILABLE = False


class LocalGemmaClient:
    """Local Gemma client for FSM-constrained generation using Hugging Face Transformers."""
    
    def __init__(self, model_name: str = "google/gemma-3-270m", device: Optional[str] = None):
        """Initialize the local Gemma client.
        
        Args:
            model_name: Hugging Face model identifier
            device: Device to run the model on ('cuda', 'cpu', 'auto')
        """
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Transformers package not available. Install with: pip install transformers torch accelerate")
        
        self.model_name = model_name
        self.device = device or self._get_best_device()
        
        print(f"🤗 Loading {model_name} on {self.device}...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
            use_fast=True,
            token=True  # Use HF token if available
        )
        
        # Ensure pad token is set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  # Use float32 for stability
            device_map=None,  # Don't use auto device mapping
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            token=True  # Use HF token if available
        )
        
        # Always move to the specified device
        self.model = self.model.to(self.device)
        
        self.model.eval()
        
        # Generation config
        self.generation_config = GenerationConfig(
            max_new_tokens=50,
            temperature=0.3,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.1,
            no_repeat_ngram_size=3
        )
        
        print(f"✅ Model loaded successfully!")
    
    def _get_best_device(self) -> str:
        """Get the best available device for inference."""
        # Use CPU by default to avoid CUDA assertion errors
        # CUDA can be unstable with some models/configurations
        if torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def generate_simple(
        self,
        prompt: str,
        max_tokens: int = 50,
        temperature: float = 0.3
    ) -> str:
        """Generate simple text response using the local model."""
        try:
            # Format prompt for Gemma
            formatted_prompt = self._format_prompt_for_gemma(prompt)
            
            # Tokenize input
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Update generation config
            generation_config = GenerationConfig(
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1,
                no_repeat_ngram_size=3
            )
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    generation_config=generation_config,
                    attention_mask=inputs.attention_mask
                )
            
            # Decode response (remove input tokens)
            input_length = inputs.input_ids.shape[1]
            generated_tokens = outputs[0][input_length:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            return response.strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate text with local model: {str(e)}")
    
    def _format_prompt_for_gemma(self, prompt: str) -> str:
        """Format prompt appropriately for Gemma model."""
        # Use Gemma's instruction format
        formatted_prompt = f"<bos><start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
        return formatted_prompt
    
    def generate_with_latex_fsm(self, prompt: str, fsm, verbose: bool = True) -> str:
        """Generate LaTeX math expressions constrained by FSM with detailed logging."""
        # Reset FSM
        fsm.reset()
        
        if verbose:
            print(f"\n🧮 Local Gemma LaTeX Generation Process")
            print(f"📝 Original prompt: {prompt}")
        
        # Create a prompt that forces simple LaTeX math expression generation
        latex_prompt = f"""
Generate a simple LaTeX math expression for: {prompt}

Rules:
1. Use ONLY inline math format: $expression$
2. Keep expressions simple and complete
3. No text, no explanations, ONLY the math expression
4. Examples: $ax^3 + bx^2 + cx + d$, $\\frac{{x}}{{y}}$, $\\alpha^2$

Expression:"""
        
        if verbose:
            print(f"📋 Enhanced prompt sent to local model:")
            print(f"   {latex_prompt.strip()}")
        
        # Generate response
        response = self.generate_simple(latex_prompt, max_tokens=30, temperature=0.1)
        
        if verbose:
            print(f"\n🎯 Raw Local Model Response:")
            print(f"   '{response}'")
        
        # Extract LaTeX expression from response
        latex_expr = self.extract_latex_expression(response)
        
        if verbose:
            print(f"\n🔍 Extracted LaTeX Expression: {latex_expr if latex_expr else 'None found'}")
        
        if latex_expr:
            if verbose:
                print(f"\n🧪 Testing '{latex_expr}' with LaTeX FSM...")
            
            # Test with FSM step by step
            fsm.reset()
            is_valid = self._test_latex_with_detailed_fsm(latex_expr, fsm, verbose)
            
            if is_valid:
                if verbose:
                    print(f"✅ Local model output '{latex_expr}' is valid!")
                return latex_expr
            else:
                if verbose:
                    print(f"❌ Local model output '{latex_expr}' rejected by FSM")
                    print(f"🔧 Generating FSM-compliant expression...")
                # FSM rejected it, try to generate a valid one
                return self.generate_valid_latex_with_fsm(fsm, prompt, verbose)
        else:
            if verbose:
                print(f"❌ No valid LaTeX expression found in local model response")
                print(f"🔧 Generating FSM-compliant expression...")
            # No valid expression found, generate one with FSM
            return self.generate_valid_latex_with_fsm(fsm, prompt, verbose)
    
    def extract_latex_expression(self, text: str) -> Optional[str]:
        """Extract LaTeX mathematical expression from text."""
        
        # Clean the text first
        text = text.strip()
        
        # Try inline math first: $...$
        inline_matches = re.findall(r'\$([^$]+)\$', text)
        if inline_matches:
            # Take the first complete match
            expr = inline_matches[0].strip()
            if expr:  # Make sure it's not empty
                return f"${expr}$"
        
        # Try display math: $$...$$
        display_matches = re.findall(r'\$\$([^$]+)\$\$', text)
        if display_matches:
            expr = display_matches[0].strip()
            if expr:
                return f"${expr}$"  # Convert to inline math
        
        # Try to find incomplete expressions and fix them
        incomplete_matches = re.findall(r'\$\$?\s*([^$]*(?:\\\w+[^$]*)*)', text)
        if incomplete_matches:
            expr = incomplete_matches[0].strip()
            # If it looks like a math expression, wrap it
            if re.search(r'[a-zA-Z]|\\\w+|\d|[+\-*/^_{}()]', expr):
                return f"${expr}$"
        
        # If text starts with $ but is incomplete, try to extract what we can
        if text.startswith('$'):
            # Extract everything after the first $
            remaining = text[1:].strip()
            # Remove any trailing incomplete parts
            remaining = re.sub(r'[^a-zA-Z0-9+\-*/^_{}()\\\s]*$', '', remaining)
            if remaining and len(remaining) > 0:
                return f"${remaining}$"
        
        return None
    
    def _test_latex_with_detailed_fsm(self, latex_expr: str, fsm, verbose: bool) -> bool:
        """Test LaTeX expression with FSM and show detailed steps."""
        try:
            if verbose:
                print(f"   🔄 Processing '{latex_expr}' token by token:")
            
            # Tokenize the expression
            tokens = fsm.tokenize(latex_expr)
            
            if verbose:
                print(f"   📝 Tokens: {tokens}")
            
            for i, token in enumerate(tokens):
                if verbose:
                    possibilities = fsm.get_current_possibilities()
                    print(f"      Step {i+1}: Processing token '{token}'")
                    print(f"      Current state: {fsm.state}")
                    print(f"      Valid possibilities: {possibilities[:10]}{'...' if len(possibilities) > 10 else ''}")
                
                if not fsm.process_token(token):
                    if verbose:
                        print(f"      ❌ FSM rejected token '{token}'")
                    return False
                
                if verbose:
                    print(f"      ✅ FSM accepted '{token}' -> New state: {fsm.state}")
            
            # Check if expression is complete
            is_complete = fsm.is_complete()
            
            if verbose:
                print(f"\n   📊 Validation Summary:")
                print(f"   Processed tokens: {len(tokens)}")
                print(f"   FSM path: {' -> '.join(fsm.path)}")
                print(f"   Final state: {fsm.state}")
                print(f"   Complete expression: {is_complete}")
            
            return is_complete
            
        except Exception as e:
            if verbose:
                print(f"   ❌ Error during FSM processing: {str(e)}")
            return False
    
    def generate_valid_latex_with_fsm(self, fsm, prompt: str, verbose: bool) -> str:
        """Generate a valid LaTeX expression using FSM step by step."""
        if verbose:
            print(f"\n   🔧 FSM-guided LaTeX generation (local model):")
        
        # Reset FSM
        fsm.reset()
        result_expr = ""
        max_tokens = 20
        
        for position in range(max_tokens):
            # Get valid possibilities from FSM
            possibilities = fsm.get_current_possibilities()
            
            if not possibilities:
                if verbose:
                    print(f"   🛑 No more valid tokens available")
                break
            
            if verbose:
                print(f"   Step {position + 1}: State '{fsm.state}'")
                print(f"   Available tokens: {possibilities[:10]}{'...' if len(possibilities) > 10 else ''}")
            
            # Choose token based on prompt content and FSM state
            chosen_token = self._choose_latex_token(prompt, possibilities, fsm.state, result_expr, verbose)
            
            if chosen_token is None:
                if verbose:
                    print(f"   🎯 Choosing to end generation")
                break
            
            # Process the chosen token
            if fsm.process_token(chosen_token):
                result_expr += chosen_token
                if verbose:
                    print(f"   ✅ FSM accepted '{chosen_token}' -> New state: {fsm.state}")
                    print(f"   Current expression: '{result_expr}'")
                
                # Check if we have a complete expression
                if fsm.is_complete():
                    if verbose:
                        print(f"   🎉 Complete valid expression generated!")
                    break
            else:
                if verbose:
                    print(f"   ❌ FSM rejected '{chosen_token}' (unexpected error)")
                break
        
        # Validate final result
        if fsm.is_complete():
            if verbose:
                print(f"\n   📊 Generation Summary:")
                print(f"   Generated expression: '{result_expr}'")
                print(f"   FSM path: {' -> '.join(fsm.path)}")
                print(f"   Valid LaTeX expression: True")
            return result_expr
        
        if verbose:
            print(f"   ⚠️  Generation incomplete, using fallback")
        
        # Fallback to a simple valid expression
        return "$x$"
    
    def _choose_latex_token(self, prompt: str, possibilities: list, state: str, current_expr: str, verbose: bool) -> Optional[str]:
        """Choose the most appropriate LaTeX token based on context."""
        prompt_lower = prompt.lower()
        
        # End conditions
        if "$" in possibilities and len(current_expr) > 3:
            # Simple heuristic: end after generating some content
            if any(char in current_expr for char in "xyzabc123"):
                if verbose:
                    print(f"   🎯 Chosen: '$' (completing expression)")
                return "$"
        
        # Content-based choices
        if "fraction" in prompt_lower and "\\frac" in possibilities:
            if verbose:
                print(f"   🎯 Chosen: '\\frac' (prompt mentions fraction)")
            return "\\frac"
        elif "square" in prompt_lower and "^" in possibilities:
            if verbose:
                print(f"   🎯 Chosen: '^' (prompt mentions square)")
            return "^"
        elif "subscript" in prompt_lower and "_" in possibilities:
            if verbose:
                print(f"   🎯 Chosen: '_' (prompt mentions subscript)")
            return "_"
        elif "alpha" in prompt_lower and "\\alpha" in possibilities:
            if verbose:
                print(f"   🎯 Chosen: '\\alpha' (prompt mentions alpha)")
            return "\\alpha"
        elif "beta" in prompt_lower and "\\beta" in possibilities:
            if verbose:
                print(f"   🎯 Chosen: '\\beta' (prompt mentions beta)")
            return "\\beta"
        
        # State-based choices
        if state == "start":
            for token in ["$"]:
                if token in possibilities:
                    if verbose:
                        print(f"   🎯 Chosen: '{token}' (starting math mode)")
                    return token
        elif state == "math_mode":
            # Prefer variables for basic expressions
            for token in ["x", "y", "z", "a", "b", "1", "2", "+"]:
                if token in possibilities:
                    if verbose:
                        print(f"   🎯 Chosen: '{token}' (basic math content)")
                    return token
        elif state in ["superscript", "subscript"]:
            for token in ["2", "i", "n", "1", "{"]:
                if token in possibilities:
                    if verbose:
                        print(f"   🎯 Chosen: '{token}' (simple {state} content)")
                    return token
        elif state == "fraction_num":
            if "{" in possibilities:
                if verbose:
                    print(f"   🎯 Chosen: '{{' (opening fraction numerator)")
                return "{"
        elif state == "content":
            for token in ["a", "b", "x", "y", "1", "2", "}"]:
                if token in possibilities:
                    if verbose:
                        print(f"   🎯 Chosen: '{token}' (content inside braces)")
                    return token
        
        # Fallback: first available token
        if possibilities:
            if verbose:
                print(f"   🎯 Chosen: '{possibilities[0]}' (first available)")
            return possibilities[0]
        
        return None

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "model_type": "local_transformers",
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad),
            "torch_dtype": str(self.model.dtype),
            "device_map": getattr(self.model, "hf_device_map", None)
        }
