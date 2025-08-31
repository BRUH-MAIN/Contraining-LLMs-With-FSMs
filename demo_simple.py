"""
Simple Demo of HTTP Status Code FSM
==================================

This demo shows how the FSM processes HTTP status codes digit by digit.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.fsm import HTTPCodeFSM


def demo_fsm_step_by_step():
    """Demonstrate the FSM step by step."""
    print("🚀 HTTP Status Code FSM Demo")
    print("=" * 35)
    
    fsm = HTTPCodeFSM()
    
    # Test cases
    test_cases = ["404", "200", "500", "301", "123", "999", "4"]
    
    for test_case in test_cases:
        print(f"\n📝 Testing: '{test_case}'")
        fsm.reset()
        
        # Process digit by digit
        for i, digit in enumerate(test_case):
            print(f"   Step {i+1}: Processing digit '{digit}'")
            print(f"   Current state: {fsm.state}")
            print(f"   Valid possibilities: {fsm.get_current_possibilities()}")
            
            success = fsm.process_digit(digit)
            
            if success:
                print(f"   ✅ Accepted '{digit}' -> New state: {fsm.state}")
            else:
                print(f"   ❌ Rejected '{digit}'")
                break
        
        # Final result  
        if fsm.is_complete():
            code = int(fsm.current_code)
            is_valid = code in fsm.VALID_CODES
            print(f"   Final result: {'✅ Valid' if is_valid else '❌ Invalid'}")
        else:
            print(f"   Final result: ❌ Invalid (incomplete)")
        print(f"   FSM path: {' -> '.join(fsm.path)}")


def demo_possibilities():
    """Show what digits are possible at each state."""
    print("\n\n🔍 FSM State Possibilities")
    print("=" * 30)
    
    fsm = HTTPCodeFSM()
    
    # Show possibilities for each state
    print("\n🟢 Starting state:")
    print(f"   Valid first digits: {fsm.get_valid_first_digits()}")
    
    print("\n🟡 After first digit '4':")
    fsm.process_digit("4")
    print(f"   Valid second digits: {fsm.get_current_possibilities()}")
    
    print("\n🟡 After '40':")
    fsm.process_digit("0")
    print(f"   Valid third digits: {fsm.get_current_possibilities()}")
    
    # Reset and try another path
    fsm.reset()
    print("\n🟡 After first digit '2':")
    fsm.process_digit("2")
    print(f"   Valid second digits: {fsm.get_current_possibilities()}")
    
    print("\n🟡 After '20':")
    fsm.process_digit("0")
    print(f"   Valid third digits: {fsm.get_current_possibilities()}")


def main():
    """Run the demo."""
    demo_fsm_step_by_step()
    demo_possibilities()


if __name__ == "__main__":
    main()
