# Shell Scripts and Automation

This directory contains shell scripts for project automation and convenience.

## Available Scripts

### 🚀 `run_app.sh`
Smart Streamlit app launcher that automatically detects the best Python environment.

**Usage:**
```bash
./scripts/run_app.sh
```

**Features:**
- Auto-detects `uv`, virtual environments, or system Python
- Provides helpful error messages
- Cross-platform compatibility
- Environment validation

**Decision Logic:**
1. **uv** (preferred): Uses `uv run streamlit run streamlit_app.py`
2. **Virtual environment**: Uses `./.venv/bin/python -m streamlit run streamlit_app.py`
3. **System Python**: Uses `python -m streamlit run streamlit_app.py`
4. **Error handling**: Provides setup instructions if no environment found

## Future Scripts

Planned additions:

### 📊 `generate_diagrams.sh`
```bash
#!/bin/bash
# Generate all project diagrams
python tools/fsm_diagram.py
echo "✅ Static diagrams generated in assets/"
```

### 🧪 `run_tests.sh`
```bash
#!/bin/bash
# Run comprehensive test suite
python -m pytest tests/ -v
python examples/demo_latex.py --test-mode
echo "✅ All tests completed"
```

### 📦 `setup_dev.sh`
```bash
#!/bin/bash
# Set up development environment
if command -v uv &> /dev/null; then
    uv sync --dev
else
    pip install -r requirements.txt
fi
pre-commit install
echo "✅ Development environment ready"
```

### 🏗️ `build_docs.sh`
```bash
#!/bin/bash
# Generate documentation
python tools/fsm_diagram.py
sphinx-build -b html docs/ docs/_build/
echo "✅ Documentation built"
```

### 🧹 `cleanup.sh`
```bash
#!/bin/bash
# Clean up temporary files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
rm -f *.log
echo "✅ Cleanup completed"
```

## Script Guidelines

### Writing New Scripts
1. **Shebang**: Always start with `#!/bin/bash`
2. **Error Handling**: Use `set -e` for error exit
3. **Help Text**: Provide usage information
4. **Cross-platform**: Consider macOS, Linux, Windows (Git Bash)
5. **Permissions**: Make scripts executable with `chmod +x`

### Template for New Scripts
```bash
#!/bin/bash

# Script Name: [Brief Description]
# Usage: ./scripts/script_name.sh [options]

set -e  # Exit on any error

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Description of what this script does.

OPTIONS:
    -h, --help    Show this help message
    -v, --verbose Enable verbose output

Examples:
    $0              # Basic usage
    $0 -v           # Verbose mode

EOF
}

# Parse command line arguments
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# Main script logic
echo "🧮 LaTeX Math FSM - [Script Purpose]"

if [ "$VERBOSE" = true ]; then
    echo "Running in verbose mode..."
fi

# Script functionality here

echo "✅ Script completed successfully!"
```

### Best Practices
- **Error Messages**: Clear, actionable error messages
- **Progress Indicators**: Use emojis and clear status messages
- **Environment Checks**: Verify prerequisites before running
- **Logging**: Option for verbose output
- **Cleanup**: Clean up temporary files on exit

## Platform Support

### Linux/macOS
All scripts work natively.

### Windows
Use Git Bash or WSL for script execution:
```bash
# In Git Bash or WSL
./scripts/run_app.sh
```

### Docker (Future)
Planned Docker support:
```bash
# Future Docker integration
./scripts/docker_run.sh
```

## Permissions

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

Or individually:
```bash
chmod +x scripts/run_app.sh
```

## Integration with Development Workflow

### Pre-commit Hooks
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: run-tests
        name: Run Tests
        entry: ./scripts/run_tests.sh
        language: script
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: ./scripts/run_tests.sh

- name: Generate Diagrams
  run: ./scripts/generate_diagrams.sh
```

### Makefile Integration
```makefile
# Makefile
.PHONY: run test docs clean

run:
	./scripts/run_app.sh

test:
	./scripts/run_tests.sh

docs:
	./scripts/build_docs.sh

clean:
	./scripts/cleanup.sh
```

---

*Scripts automate common tasks and make development more efficient!* 🚀