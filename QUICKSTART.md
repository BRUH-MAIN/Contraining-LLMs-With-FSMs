# Quick Start Guide

## 🚀 HTTP Status Code Constraints for LLMs

### Files Overview:
- `main.py` - Full LLM integration demo
- `demo.py` - Constraint validation demo (no API calls)
- `src/fsm/constraints.py` - HTTP status code constraints
- `src/fsm/state_machine.py` - FSM implementation  
- `src/llm/groq_client.py` - Groq API client

### Quick Commands:

```bash
# Install dependencies
pip install groq python-dotenv

# Test constraints (no API key needed)
python demo.py

# Test with LLM (requires GROQ_API_KEY in .env)
python main.py --example server  # 5xx codes
python main.py --example client  # 4xx codes
python main.py --example all     # All examples
```

### HTTP Code Examples:
- **Server Errors (5xx)**: 500, 502, 503, 504
- **Client Errors (4xx)**: 400, 401, 403, 404
- **Success (2xx)**: 200, 201, 202
- **Redirects (3xx)**: 301, 302, 304

### Environment Setup:
1. Copy `.env.example` to `.env`
2. Add your GROQ_API_KEY to `.env`
3. Run demos with `python main.py`

### Key Features:
✅ Clean, simple codebase  
✅ HTTP status code validation  
✅ LLM constraint enforcement  
✅ Easy to extend and modify
