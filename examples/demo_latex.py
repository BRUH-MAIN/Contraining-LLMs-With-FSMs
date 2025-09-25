"""
LaTeX Math FSM Demo
==================

This demo shows how the LaTeX Math FSM processes mathematical expressions token by token.
Similar to the HTTP FSM demo but for LaTeX mathematical syntax validation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import LaTeXMathFSM


def demo_latex_fsm_step_by_step():
    """Demonstrate the LaTeX Math FSM step by step."""
    print("🧮 LaTeX Math FSM Demo")
    print("=" * 35)
    
    fsm = LaTeXMathFSM()
    
    # Test cases - various LaTeX math expressions
    test_cases = [
        "$x^2$",                           # Simple inline math
        "$\\frac{a}{b}$",                  # Fraction
        "$x_{i}$",                         # Subscript
        "$\\sum_{i=1}^{n} x_i$",          # Summation with limits
        "$\\sqrt{x^2 + y^2}$",            # Square root
        "$$\\int_0^1 x dx$$",             # Display mode integral
        "$\\alpha + \\beta$",             # Greek letters
        "$f(x) = x^2 + 2x + 1$",          # Function definition
        "$\\frac{\\sin(x)}{\\cos(x)}$",   # Trigonometric fraction
        "$x^{2^3}$",                      # Nested superscript
        "$x + y$",                        # Invalid - no math delimiters
        "$\\frac{a$",                     # Invalid - incomplete fraction
        "$x^$",                           # Invalid - incomplete superscript
    ]
    
    for test_case in test_cases:
        print(f"\n📝 Testing: '{test_case}'")
        fsm.reset()
        
        # Tokenize and show tokens
        tokens = fsm.tokenize(test_case)
        print(f"   Tokens: {tokens}")
        
        # Process step by step
        valid = True
        for i, token in enumerate(tokens):
            old_state = fsm.state
            success = fsm.process_token(token)
            new_state = fsm.state
            
            status = "✅" if success else "❌"
            print(f"   Step {i+1}: '{token}' | {old_state} → {new_state} {status}")
            
            if not success:
                valid = False
                break
        
        # Final validation
        is_complete = fsm.is_complete()
        final_status = "✅ VALID" if valid and is_complete else "❌ INVALID"
        
        print(f"   Result: {final_status}")
        print(f"   Final State: {fsm.state}")
        print(f"   Complete: {is_complete}")
        print(f"   State Info: {fsm.get_state_info()}")


def demo_latex_fsm_possibilities():
    """Demonstrate valid next token possibilities."""
    print("\n\n🎯 LaTeX Math FSM - Valid Next Tokens Demo")
    print("=" * 50)
    
    fsm = LaTeXMathFSM()
    
    # Test partial expressions
    partial_expressions = [
        "",                    # Start state
        "$",                   # Just entered math mode
        "$x",                  # Variable in math mode
        "$x^",                 # After superscript
        "$\\f",                # Incomplete command
        "$\\frac",             # Complete frac command
        "$\\frac{",            # Opening fraction numerator
        "$\\frac{a",           # Content in numerator
        "$\\frac{a}",          # Closed numerator
        "$\\frac{a}{",         # Opening denominator
        "$\\frac{a}{b",        # Content in denominator
    ]
    
    for expr in partial_expressions:
        print(f"\n📝 Partial expression: '{expr}'")
        fsm.reset()
        
        if expr:  # Not empty
            tokens = fsm.tokenize(expr)
            for token in tokens:
                fsm.process_token(token)
        
        possibilities = fsm.get_current_possibilities()
        print(f"   Current state: {fsm.state}")
        print(f"   Valid next tokens: {possibilities[:15]}...")  # Show first 15
        print(f"   Total possibilities: {len(possibilities)}")


def demo_latex_fsm_validation():
    """Demonstrate validation of complete expressions."""
    print("\n\n✅ LaTeX Math FSM - Complete Validation Demo")
    print("=" * 55)
    
    fsm = LaTeXMathFSM()
    
    expressions = [
        # Valid expressions
        ("$x$", True),
        ("$x + y$", True),
        ("$x^2$", True),
        ("$x_{i}$", True),
        ("$\\frac{a}{b}$", True),
        ("$\\sqrt{x}$", True),
        ("$$x = y$$", True),
        ("$\\alpha + \\beta$", True),
        ("$f(x) = x^2$", True),
        ("$x^{2+3}$", True),
        
        # Invalid expressions
        ("x + y", False),           # No math delimiters
        ("$x +", False),            # Incomplete
        ("$x^$", False),            # Incomplete superscript
        ("$\\frac{a$", False),      # Incomplete fraction
        ("$x + y$$", False),        # Mismatched delimiters
        ("$\\unknown{x}$", False),  # Unknown command
    ]
    
    print("Testing complete expressions:")
    for expr, expected in expressions:
        fsm.reset()
        result = fsm.process_input(expr)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{expr}' → {result} (expected: {expected})")


if __name__ == "__main__":
    demo_latex_fsm_step_by_step()
    demo_latex_fsm_possibilities()
    demo_latex_fsm_validation()
