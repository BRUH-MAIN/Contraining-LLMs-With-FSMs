"""
LaTeX Math Finite State Machine
==============================

A finite state machine that processes LaTeX mathematical expressions token by token.
Each token moves the FSM through appropriate states to validate mathematical syntax.

States:
- start: Initial state
- math_mode: Inside mathematical expression ($ ... $ or \[ ... \])
- command: After backslash (\)
- command_name: Reading command name (e.g., "frac", "sum")
- brace_open: After opening brace {
- content: Reading content inside braces
- superscript: After ^ symbol
- subscript: After _ symbol
- fraction_num: Reading fraction numerator
- fraction_den: Reading fraction denominator
- matrix_mode: Inside matrix environment
- end_state: Valid complete expression
"""

from typing import List, Dict, Set
import re


class LaTeXMathFSM:
    """Finite State Machine for LaTeX mathematical expressions."""
    
    # Valid LaTeX math commands
    VALID_COMMANDS = {
        # Basic math operations
        "frac", "sqrt", "sum", "int", "lim", "prod",
        
        # Greek letters
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
        "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
        "tau", "upsilon", "phi", "chi", "psi", "omega",
        "Alpha", "Beta", "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi",
        "Sigma", "Upsilon", "Phi", "Psi", "Omega",
        
        # Mathematical operators
        "cdot", "times", "div", "pm", "mp", "ast", "star", "circ",
        "bullet", "cap", "cup", "sqcap", "sqcup", "vee", "wedge",
        
        # Relations
        "leq", "geq", "neq", "equiv", "approx", "sim", "simeq", "cong",
        "propto", "parallel", "perp", "subset", "supset", "subseteq", "supseteq",
        "in", "ni", "notin",
        
        # Arrows
        "rightarrow", "leftarrow", "leftrightarrow", "Rightarrow", "Leftarrow",
        "Leftrightarrow", "mapsto", "longmapsto",
        
        # Delimiters
        "left", "right", "big", "Big", "bigg", "Bigg",
        
        # Functions
        "sin", "cos", "tan", "sec", "csc", "cot", "sinh", "cosh", "tanh",
        "arcsin", "arccos", "arctan", "ln", "log", "exp", "det", "dim",
        "ker", "hom", "deg", "gcd",
        
        # Environments
        "begin", "end", "matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix",
        "array", "align", "equation", "split",
        
        # Text formatting
        "text", "mathbf", "mathit", "mathcal", "mathbb", "mathfrak",
        "mathrm", "boldsymbol",
        
        # Spacing
        "quad", "qquad", ",", ";", ":", "!", "enspace", "thinspace",
        
        # Special symbols
        "infty", "nabla", "partial", "emptyset", "exists", "forall",
        "therefore", "because", "dots", "ldots", "cdots", "vdots", "ddots"
    }
    
    # Valid brackets and delimiters
    VALID_DELIMITERS = {
        "(", ")", "[", "]", "{", "}", "|", "\\|", "\\{", "\\}",
        "\\langle", "\\rangle", "\\lceil", "\\rceil", "\\lfloor", "\\rfloor"
    }
    
    # Valid single characters
    VALID_NUMBERS = set("0123456789")
    VALID_VARIABLES = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    VALID_OPERATORS = {"+", "-", "=", "<", ">", "*", "/", "!", "?", ".", ",", ";", ":", "'"}
    
    # Math mode delimiters
    MATH_DELIMITERS = {
        "inline": {"$": "$"},
        "display": {"\\[": "\\]", "$$": "$$"},
        "equation": {"\\begin{equation}": "\\end{equation}"},
        "align": {"\\begin{align}": "\\end{align}"}
    }
    
    def __init__(self):
        """Initialize the FSM."""
        self.reset()
    
    def reset(self):
        """Reset FSM to initial state."""
        self.state = "start"
        self.current_expression = ""
        self.path = ["start"]
        self.brace_depth = 0
        self.bracket_depth = 0
        self.paren_depth = 0
        self.math_mode_type = None
        self.command_buffer = ""
        self.environment_stack = []
        
    def tokenize(self, latex_str: str) -> List[str]:
        """Tokenize LaTeX string into meaningful tokens."""
        tokens = []
        i = 0
        
        while i < len(latex_str):
            char = latex_str[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle backslash commands
            if char == '\\':
                # Look ahead for command
                j = i + 1
                if j < len(latex_str) and latex_str[j].isalpha():
                    # Read command name
                    while j < len(latex_str) and latex_str[j].isalpha():
                        j += 1
                    tokens.append(latex_str[i:j])
                    i = j
                elif j < len(latex_str):
                    # Single character after backslash
                    tokens.append(latex_str[i:j+1])
                    i = j + 1
                else:
                    tokens.append(char)
                    i += 1
            
            # Handle multi-character delimiters
            elif char == '$' and i + 1 < len(latex_str) and latex_str[i + 1] == '$':
                tokens.append("$$")
                i += 2
            elif char == '\\' and i + 1 < len(latex_str) and latex_str[i + 1] == '[':
                tokens.append("\\[")
                i += 2
            elif char == '\\' and i + 1 < len(latex_str) and latex_str[i + 1] == ']':
                tokens.append("\\]")
                i += 2
            
            # Single characters
            else:
                tokens.append(char)
                i += 1
        
        return tokens
    
    def is_valid_command(self, command: str) -> bool:
        """Check if command is valid (without backslash)."""
        return command in self.VALID_COMMANDS
    
    def is_math_delimiter(self, token: str) -> bool:
        """Check if token is a math mode delimiter."""
        for delim_type, delims in self.MATH_DELIMITERS.items():
            if token in delims.keys() or token in delims.values():
                return True
        return False
    
    def get_valid_commands(self) -> List[str]:
        """Get list of valid commands with backslash prefix."""
        return [f"\\{cmd}" for cmd in self.VALID_COMMANDS]
    
    def get_valid_variables(self) -> List[str]:
        """Get valid single variable characters."""
        return list(self.VALID_VARIABLES)
    
    def get_valid_numbers(self) -> List[str]:
        """Get valid single digit characters."""
        return list(self.VALID_NUMBERS)
    
    def get_valid_operators(self) -> List[str]:
        """Get valid operator characters."""
        return list(self.VALID_OPERATORS)
    
    def get_valid_delimiters(self) -> List[str]:
        """Get valid delimiter tokens."""
        return list(self.VALID_DELIMITERS)
    
    def process_token(self, token: str) -> bool:
        """Process a single token through the FSM."""
        if self.state == "start":
            return self._process_start_state(token)
        elif self.state == "math_mode":
            return self._process_math_mode(token)
        elif self.state == "command":
            return self._process_command_state(token)
        elif self.state == "brace_open":
            return self._process_brace_open_state(token)
        elif self.state == "content":
            return self._process_content_state(token)
        elif self.state == "superscript":
            return self._process_superscript_state(token)
        elif self.state == "subscript":
            return self._process_subscript_state(token)
        elif self.state == "fraction_num":
            return self._process_fraction_num_state(token)
        elif self.state == "fraction_den":
            return self._process_fraction_den_state(token)
        else:
            return False
    
    def _process_start_state(self, token: str) -> bool:
        """Process token in start state."""
        if token == "$":
            self.state = "math_mode"
            self.math_mode_type = "inline"
            self._add_to_path("math_mode")
            return True
        elif token == "$$":
            self.state = "math_mode"
            self.math_mode_type = "display"
            self._add_to_path("math_mode")
            return True
        elif token == "\\[":
            self.state = "math_mode"
            self.math_mode_type = "display"
            self._add_to_path("math_mode")
            return True
        return False
    
    def _process_math_mode(self, token: str) -> bool:
        """Process token in math mode."""
        # Check for end of math mode
        if self._is_math_mode_end(token):
            self.state = "end_state"
            self._add_to_path("end_state")
            return True
        
        # Commands
        if token.startswith("\\") and len(token) > 1:
            command_name = token[1:]
            if self.is_valid_command(command_name):
                if command_name == "frac":
                    self.state = "fraction_num"
                    self._add_to_path("fraction_num")
                elif command_name in ["begin"]:
                    self.state = "command"
                    self.command_buffer = command_name
                    self._add_to_path("command")
                else:
                    # Stay in math mode for most commands
                    pass
                return True
        
        # Variables, numbers, operators
        if (token in self.VALID_VARIABLES or 
            token in self.VALID_NUMBERS or 
            token in self.VALID_OPERATORS):
            return True
        
        # Superscript and subscript
        if token == "^":
            self.state = "superscript"
            self._add_to_path("superscript")
            return True
        elif token == "_":
            self.state = "subscript"
            self._add_to_path("subscript")
            return True
        
        # Braces
        if token == "{":
            self.brace_depth += 1
            self.state = "content"
            self._add_to_path("content")
            return True
        elif token == "}":
            if self.brace_depth > 0:
                self.brace_depth -= 1
                return True
        
        # Parentheses and brackets
        if token in ["(", "[", "|"]:
            if token == "(":
                self.paren_depth += 1
            elif token == "[":
                self.bracket_depth += 1
            return True
        elif token in [")", "]", "|"]:
            if token == ")" and self.paren_depth > 0:
                self.paren_depth -= 1
                return True
            elif token == "]" and self.bracket_depth > 0:
                self.bracket_depth -= 1
                return True
            elif token == "|":
                return True
        
        return False
    
    def _process_command_state(self, token: str) -> bool:
        """Process token in command state."""
        # This state is for handling complex commands like \begin{matrix}
        if token == "{":
            self.brace_depth += 1
            self.state = "brace_open"
            self._add_to_path("brace_open")
            return True
        return False
    
    def _process_brace_open_state(self, token: str) -> bool:
        """Process token in brace open state."""
        if token == "}":
            self.brace_depth -= 1
            self.state = "math_mode"
            self._add_to_path("math_mode")
            return True
        else:
            self.state = "content"
            self._add_to_path("content")
            return self._process_content_state(token)
    
    def _process_content_state(self, token: str) -> bool:
        """Process token in content state."""
        if token == "}":
            self.brace_depth -= 1
            if self.brace_depth == 0:
                self.state = "math_mode"
                self._add_to_path("math_mode")
            return True
        elif token == "{":
            self.brace_depth += 1
            return True
        else:
            # Allow most content inside braces
            return (token in self.VALID_VARIABLES or 
                   token in self.VALID_NUMBERS or 
                   token in self.VALID_OPERATORS or
                   token.startswith("\\"))
    
    def _process_superscript_state(self, token: str) -> bool:
        """Process token in superscript state."""
        if token == "{":
            self.brace_depth += 1
            self.state = "content"
            self._add_to_path("content")
            return True
        elif (token in self.VALID_VARIABLES or 
              token in self.VALID_NUMBERS):
            self.state = "math_mode"
            self._add_to_path("math_mode")
            return True
        return False
    
    def _process_subscript_state(self, token: str) -> bool:
        """Process token in subscript state."""
        if token == "{":
            self.brace_depth += 1
            self.state = "content"
            self._add_to_path("content")
            return True
        elif (token in self.VALID_VARIABLES or 
              token in self.VALID_NUMBERS):
            self.state = "math_mode"
            self._add_to_path("math_mode")
            return True
        return False
    
    def _process_fraction_num_state(self, token: str) -> bool:
        """Process token in fraction numerator state."""
        if token == "{":
            self.brace_depth += 1
            self.state = "content"
            self._add_to_path("content")
            return True
        return False
    
    def _process_fraction_den_state(self, token: str) -> bool:
        """Process token in fraction denominator state."""
        if token == "{":
            self.brace_depth += 1
            self.state = "content"
            self._add_to_path("content")
            return True
        return False
    
    def _is_math_mode_end(self, token: str) -> bool:
        """Check if token ends current math mode."""
        if self.math_mode_type == "inline" and token == "$":
            return True
        elif self.math_mode_type == "display" and token in ["$$", "\\]"]:
            return True
        return False
    
    def _add_to_path(self, state: str):
        """Add state to path history."""
        self.path.append(state)
    
    def process_input(self, latex_str: str) -> bool:
        """Process complete LaTeX string."""
        tokens = self.tokenize(latex_str)
        
        for token in tokens:
            if not self.process_token(token):
                return False
        
        return self.is_complete()
    
    def is_complete(self) -> bool:
        """Check if FSM is in a valid final state."""
        return (self.state == "end_state" and 
                self.brace_depth == 0 and 
                self.bracket_depth == 0 and 
                self.paren_depth == 0)
    
    def get_current_possibilities(self) -> List[str]:
        """Get valid next tokens based on current state."""
        possibilities = []
        
        if self.state == "start":
            possibilities.extend(["$", "$$", "\\["])
            
        elif self.state == "math_mode":
            possibilities.extend(self.get_valid_variables())
            possibilities.extend(self.get_valid_numbers())
            possibilities.extend(self.get_valid_operators())
            possibilities.extend(self.get_valid_commands())
            possibilities.extend(["^", "_", "{", "}", "(", ")", "[", "]"])
            
            # Add math mode end delimiters
            if self.math_mode_type == "inline":
                possibilities.append("$")
            elif self.math_mode_type == "display":
                possibilities.extend(["$$", "\\]"])
                
        elif self.state in ["superscript", "subscript"]:
            possibilities.extend(self.get_valid_variables())
            possibilities.extend(self.get_valid_numbers())
            possibilities.append("{")
            
        elif self.state == "command":
            possibilities.append("{")
            
        elif self.state in ["brace_open", "content"]:
            possibilities.extend(self.get_valid_variables())
            possibilities.extend(self.get_valid_numbers())
            possibilities.extend(self.get_valid_operators())
            possibilities.extend(self.get_valid_commands())
            possibilities.extend(["{", "}", "^", "_"])
            
        elif self.state == "fraction_num":
            possibilities.append("{")
            
        elif self.state == "fraction_den":
            possibilities.append("{")
        
        return possibilities
    
    def get_state_info(self) -> Dict:
        """Get current state information."""
        return {
            "state": self.state,
            "path": self.path,
            "brace_depth": self.brace_depth,
            "bracket_depth": self.bracket_depth,
            "paren_depth": self.paren_depth,
            "math_mode_type": self.math_mode_type,
            "is_complete": self.is_complete(),
            "valid_next_tokens": self.get_current_possibilities()[:10]  # Limit for readability
        }
