# HTTP Status Code FSM - Quick Start

## Overview

This project demonstrates a **simplified digit-by-digit finite state machine (FSM)** for constraining HTTP status codes. The FSM processes each digit individually and transitions through states:

1. **start** → **first_digit** (accepts 1, 2, 3, 4, 5)
2. **first_digit** → **second_digit** (accepts 0-9)
3. **second_digit** → **third_digit** (accepts valid digits based on first two)

## Key Features

- ✅ **Digit-by-digit processing**: FSM moves state by state for each digit
- ✅ **Real-time validation**: Only valid HTTP codes can complete the FSM path
- ✅ **Simple architecture**: Streamlined codebase focused on core FSM concepts
- ✅ **LLM integration**: Generate valid HTTP codes using Groq API

## Quick Demo

```bash
# Run the simple FSM demo
python3 demo_simple.py

# Run the full demo with LLM integration (requires GROQ_API_KEY)
python3 main.py
```

## Example Output

```
📝 Testing: '404'
   Step 1: Processing digit '4'
   Current state: start
   Valid possibilities: ['1', '2', '3', '4', '5']
   ✅ Accepted '4' -> New state: first_digit
   
   Step 2: Processing digit '0'
   Current state: first_digit
   Valid possibilities: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   ✅ Accepted '0' -> New state: second_digit
   
   Step 3: Processing digit '4'
   Current state: second_digit
   Valid possibilities: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   ✅ Accepted '4' -> New state: third_digit
   
   Final result: ✅ Valid
   FSM path: start -> first_digit -> second_digit -> third_digit
```

## Code Structure

```
src/
├── fsm/
│   ├── __init__.py
│   └── http_fsm.py          # Simple digit-by-digit FSM
└── llm/
    ├── __init__.py
    └── simple_client.py     # Simplified Groq client
```

## Usage with LLM

```python
from src.fsm import HTTPCodeFSM
from src.llm import SimpleGroqClient

# Create FSM
fsm = HTTPCodeFSM()

# Create LLM client (requires GROQ_API_KEY environment variable)
client = SimpleGroqClient()

# Generate HTTP code with FSM constraints
result = client.generate_with_fsm("Give me a server error code", fsm)
print(f"Generated: {result}")  # e.g., "500"
```

## Setup

1. Install dependencies:
```bash
pip install groq python-dotenv
```

2. Set up environment:
```bash
# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
```

3. Run demos:
```bash
python3 demo_simple.py  # FSM-only demo
python3 main.py         # Full demo with LLM
```

## How the FSM Works

The FSM processes HTTP status codes digit by digit:

1. **State: start** 
   - Accepts: 1, 2, 3, 4, 5 (valid HTTP first digits)
   - Transitions to: first_digit

2. **State: first_digit**
   - Accepts: 0-9 (any second digit)
   - Transitions to: second_digit

3. **State: second_digit**
   - Accepts: only digits that form valid HTTP codes
   - Transitions to: third_digit

4. **State: third_digit**
   - Final state - validates complete 3-digit code

## Valid HTTP Codes Supported

- **1xx**: 100, 101, 102, 103
- **2xx**: 200, 201, 202, 203, 204, 205, 206, 207, 208, 226
- **3xx**: 300, 301, 302, 303, 304, 305, 307, 308
- **4xx**: 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451
- **5xx**: 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
