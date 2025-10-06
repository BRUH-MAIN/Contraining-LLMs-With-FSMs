# Contributing to LaTeX Math FSM

Thank you for your interest in contributing to the LaTeX Math FSM project! This document outlines how you can help improve this project.

## 🌟 Ways to Contribute

### 1. Bug Reports
- Use the [GitHub Issues](https://github.com/BRUH-MAIN/Contraining-LLMs-With-FSMs/issues) page
- Include detailed descriptions and steps to reproduce
- Provide sample LaTeX expressions that cause issues

### 2. Feature Requests
- Suggest new LaTeX commands to support
- Propose improvements to the FSM architecture
- Request new LLM integrations

### 3. Code Contributions
- Fix bugs or add new features
- Improve documentation
- Add tests
- Optimize performance

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup Process
```bash
# Fork and clone the repository
git clone https://github.com/your-username/Contraining-LLMs-With-FSMs.git
cd Contraining-LLMs-With-FSMs

# Install development dependencies
uv sync --dev
# or
pip install -r requirements.txt

# Create a new branch for your feature
git checkout -b feature/your-feature-name
```

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Write descriptive docstrings using Google style
- Keep functions focused and modular

### FSM Development Rules
1. **State Validation**: All state transitions must be explicitly defined
2. **Token Processing**: Validate each token before processing
3. **Depth Tracking**: Maintain proper nesting for braces/brackets
4. **Error Handling**: Provide graceful failure for invalid tokens
5. **Documentation**: Update state diagrams when adding new states

### Testing
- Write tests for new features
- Ensure existing tests pass
- Test with various LaTeX expressions
- Validate both positive and negative cases

```bash
# Run tests (when implemented)
python -m pytest tests/

# Test specific functionality
python examples/demo_latex.py
```

## 🎯 Priority Areas

### High Priority
- [ ] **Extended LaTeX Commands**: Add support for more mathematical packages
- [ ] **Test Coverage**: Comprehensive test suite for FSM functionality
- [ ] **Performance Optimization**: Faster token processing
- [ ] **Error Messages**: Better error reporting and suggestions

### Medium Priority
- [ ] **Semantic Validation**: Check mathematical correctness, not just syntax
- [ ] **Visual Editor**: Drag-and-drop LaTeX construction interface
- [ ] **More LLM Integrations**: Support for additional LLM providers
- [ ] **Mobile Interface**: Responsive design improvements

### Low Priority
- [ ] **API Service**: RESTful API for external integrations
- [ ] **Plugin System**: Extensible architecture for custom commands
- [ ] **Export Features**: Save diagrams and results in various formats

## 📝 Pull Request Process

### Before Submitting
1. **Test Thoroughly**: Ensure your changes work correctly
2. **Update Documentation**: Include relevant documentation updates
3. **Check Style**: Follow the coding guidelines
4. **Small Commits**: Make atomic commits with clear messages

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] I have tested these changes locally
- [ ] I have added/updated tests as needed
- [ ] All existing tests pass

## Documentation
- [ ] I have updated relevant documentation
- [ ] I have added docstrings to new functions
- [ ] I have updated type hints

## LaTeX Commands (if applicable)
List any new LaTeX commands added:
- `\newcommand`
- `\anothercommand`
```

### Review Process
1. **Automated Checks**: Ensure all CI checks pass
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Merge**: Once approved, your PR will be merged

## 🏗️ Architecture Guidelines

### Adding New LaTeX Commands
```python
# In src/fsm/latex_math_fsm.py
VALID_COMMANDS = {
    # Add your new command here
    "newcommand",
    # ... existing commands
}
```

### Extending FSM States
```python
def process_token(self, token: str) -> bool:
    if self.state == "new_state":
        # Handle new state logic
        if token in valid_tokens:
            self.state = "next_state"
            return True
    return False
```

### Adding LLM Clients
```python
# Create new file in src/llm/
class NewLLMClient:
    def generate_with_latex_fsm(self, prompt: str, fsm) -> str:
        # Implementation specific to your LLM provider
        return generated_latex
```

## 🧪 Testing Guidelines

### FSM Testing
```python
from src.fsm import LaTeXMathFSM

def test_new_command():
    fsm = LaTeXMathFSM()
    result = fsm.process_input("$\\newcommand{test}$")
    assert result == True
```

### LLM Integration Testing
```python
from src.llm import SimpleGroqClient
from src.fsm import LaTeXMathFSM

def test_generation():
    client = SimpleGroqClient()
    fsm = LaTeXMathFSM()
    result = client.generate_with_latex_fsm("test prompt", fsm)
    assert fsm.process_input(result)
```

## 📚 Documentation Standards

### Code Documentation
- Use Google-style docstrings
- Include parameter types and descriptions
- Provide usage examples
- Document complex algorithms

### README Updates
- Update feature lists for new capabilities
- Add usage examples for new functionality
- Keep installation instructions current

### Diagram Updates
- Update state diagrams when adding new states
- Regenerate PNG files with `python tools/fsm_diagram.py`
- Update Mermaid diagrams in documentation

## 🎨 Visual Assets

### Generating Diagrams
```bash
# Generate static diagrams
python tools/fsm_diagram.py

# Update interactive visualizations
# Edit tools/fsm_visualizer.py and test in Streamlit
```

### Asset Guidelines
- Keep diagrams clear and professional
- Use consistent color schemes
- Ensure diagrams are readable at different sizes

## 🐛 Bug Report Template

When reporting bugs, please include:

```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- Operating system:
- LaTeX expression that caused the issue:

## Additional Context
Screenshots, error messages, etc.
```

## 💡 Feature Request Template

For feature requests, please provide:

```markdown
## Feature Description
Clear description of the desired feature

## Use Case
Why is this feature needed?

## Proposed Implementation
Ideas for how it could be implemented

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

## 🎖️ Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes for significant contributions
- Hall of Fame (if we create one)

## 📞 Getting Help

- **Questions**: Use [GitHub Discussions](https://github.com/BRUH-MAIN/Contraining-LLMs-With-FSMs/discussions)
- **Issues**: Use [GitHub Issues](https://github.com/BRUH-MAIN/Contraining-LLMs-With-FSMs/issues)
- **Direct Contact**: [Your email if you want to provide it]

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make LaTeX Math FSM better! 🧮✨