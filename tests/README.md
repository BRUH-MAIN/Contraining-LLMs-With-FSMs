# Test files for LaTeX Math FSM

This directory will contain test files for the project.

## Planned Test Structure

```
tests/
├── test_fsm.py           # FSM core functionality tests
├── test_llm_clients.py   # LLM integration tests  
├── test_integration.py   # End-to-end integration tests
├── test_visualization.py # Visualization component tests
└── fixtures/            # Test data and fixtures
    ├── valid_latex.json     # Valid LaTeX expressions
    ├── invalid_latex.json   # Invalid expressions for error testing
    └── expected_results.json # Expected FSM processing results
```

## Test Categories

### FSM Core Tests (`test_fsm.py`)
- Token processing validation
- State transition correctness
- Depth tracking accuracy
- Command recognition
- Error handling

### LLM Integration Tests (`test_llm_clients.py`)
- Client initialization
- API communication
- Response parsing
- FSM constraint enforcement
- Fallback mechanisms

### Integration Tests (`test_integration.py`)
- End-to-end LaTeX generation
- Web interface functionality
- Visualization accuracy
- Performance benchmarks

## Contributing Tests

When adding new features, please include:
1. Unit tests for core functionality
2. Integration tests for LLM interactions
3. Edge case testing
4. Performance regression tests

Run tests with:
```bash
python -m pytest tests/
```

## Test Data

Test fixtures should include:
- **Simple expressions**: `$x^2$`, `$a + b$`
- **Complex expressions**: `$\sum_{i=1}^n \frac{x_i^2}{\sigma^2}$`
- **Invalid expressions**: `$x^$`, `$\unknown{x}$`
- **Edge cases**: Empty braces, nested structures

## Mock Data

For LLM testing without API calls:
- Mock responses for various prompts
- Simulated API failures
- Rate limiting scenarios
- Different model behaviors

---

*Tests help ensure reliability and prevent regressions!* 🧪