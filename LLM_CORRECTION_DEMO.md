# LLM Output Validation and Correction Demo

## Overview

This enhanced version of the HTTP Status Code FSM project now demonstrates **detailed LLM output validation and correction**, showing exactly how the FSM acts as a "smart filter" to ensure only valid HTTP status codes are generated.

## Key Features Added

### 🔍 **Detailed LLM Output Inspection**
- **Raw LLM Response Logging**: Shows exactly what the LLM originally generated
- **Code Extraction Process**: Demonstrates how HTTP codes are extracted from natural language responses
- **Step-by-Step Validation**: Each digit is validated against FSM rules with detailed logging

### 🔧 **Correction Process Visualization**
- **Invalid Code Detection**: Shows when and why LLM outputs are rejected
- **FSM-Guided Generation**: Demonstrates how valid alternatives are generated
- **Reasoning Display**: Each choice is explained (e.g., "client error codes are common")

### 📊 **Comprehensive Logging**
- **State Transitions**: Shows FSM state changes for each digit
- **Valid Possibilities**: Displays allowed tokens at each step
- **Validation Results**: Clear success/failure indicators
- **Path Tracking**: Complete FSM traversal path

## Demo Files

### 1. `demo_correction.py` - **LLM Correction Showcase**
```bash
python3 demo_correction.py
```

**What it demonstrates:**
- Simulates various LLM responses (valid, invalid, malformed)
- Shows extraction of HTTP codes from natural language
- Validates each code digit-by-digit with detailed FSM logging
- Generates corrected alternatives for invalid outputs

**Example Output:**
```
🧪 Testing '999' with FSM...
   🔄 Processing '999' digit by digit:
      Step 1: Processing digit '9'
      Current state: start
      Valid possibilities: ['1', '2', '3', '4', '5']
      ❌ Rejected '9' (not in valid possibilities)
      FSM validation failed at digit 1

❌ Result: LLM output '999' is invalid
🔧 Generating FSM-corrected code...
🎯 Final Corrected Result: 404
```

### 2. `demo_simple.py` - **Basic FSM Validation**
```bash
python3 demo_simple.py
```

**What it demonstrates:**
- Core FSM functionality with step-by-step processing
- Valid vs invalid HTTP code examples
- State transition visualization

### 3. `main.py` - **Full LLM Integration** (requires GROQ_API_KEY)
```bash
python3 main.py
```

**What it demonstrates:**
- Real LLM API integration with FSM constraints
- End-to-end correction workflow
- Multiple test scenarios

## Key Workflow Demonstrated

### ✅ **Valid LLM Output Flow:**
1. **LLM generates**: "The status code is 200"
2. **Extract code**: "200"
3. **FSM validates**: ✅ Each digit (2→0→0) passes validation
4. **Result**: Original output accepted

### ❌ **Invalid LLM Output Flow:**
1. **LLM generates**: "Error code: 999"
2. **Extract code**: "999"
3. **FSM validates**: ❌ First digit "9" rejected (not in [1,2,3,4,5])
4. **FSM corrects**: Generates valid alternative "404"
5. **Result**: Corrected output provided

### 🚫 **No Code Found Flow:**
1. **LLM generates**: "abc123"
2. **Extract code**: None found
3. **FSM generates**: Creates valid code "404" from scratch
4. **Result**: FSM-guided output provided

## Implementation Highlights

### Enhanced `SimpleGroqClient` Methods:

- **`generate_with_fsm(verbose=True)`**: Shows complete correction process
- **`_test_code_with_detailed_fsm()`**: Step-by-step FSM validation with logging
- **`generate_valid_code_with_fsm()`**: FSM-guided generation with reasoning

### Detailed Logging Features:

- **Prompt Enhancement**: Shows how prompts are modified for better LLM compliance
- **Extraction Process**: Reveals regex-based code extraction from natural language
- **State Transitions**: Visualizes FSM state changes for each digit
- **Decision Reasoning**: Explains why specific digits are chosen during correction

## Real-World Applications

This demonstration shows how FSM-constrained generation can be applied to:

1. **API Response Generation**: Ensuring valid HTTP status codes
2. **Structured Data Creation**: Validating format compliance
3. **Error Correction**: Automatically fixing malformed outputs
4. **Quality Assurance**: Guaranteeing syntactic correctness

## Testing Different Scenarios

The demos test various challenging scenarios:

- ✅ **Valid embedded codes**: "The status code is 200"
- ❌ **Invalid embedded codes**: "Error code: 999"
- 🚫 **No codes found**: "abc123"
- 📏 **Wrong length**: "12" or "1234"
- 🔢 **Invalid ranges**: "600" (starts with 6)

## Running the Demos

```bash
# No API key required - shows correction process
python3 demo_correction.py

# Basic FSM validation
python3 demo_simple.py

# Full LLM integration (requires GROQ_API_KEY)
export GROQ_API_KEY="your_key_here"
python3 main.py
```

## Key Insights Demonstrated

1. **🎯 Precision Control**: FSM ensures 100% valid outputs
2. **🔧 Automatic Correction**: Invalid LLM outputs are automatically fixed
3. **📊 Transparency**: Every decision is logged and explained
4. **⚡ Efficiency**: Fast validation and correction process
5. **🔄 Reliability**: Fallback mechanisms ensure robust operation

This implementation successfully demonstrates the core concept from your reference text: **using FSMs as deterministic gatekeepers to constrain probabilistic LLM outputs**, with complete visibility into the correction process.
