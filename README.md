# Constraining LLMs with Finite State Machines

A Python library for constraining Large Language Model outputs using Finite State Machines (FSMs) with Groq API integration.

## 🎯 Overview

This project demonstrates how to use Finite State Machines to constrain and structure LLM outputs, ensuring they follow specific patterns, formats, or conversation flows. It provides a flexible framework for creating custom constraints and integrates with the Groq API for fast LLM inference.

## 🚀 Features

- **Finite State Machine Framework**: Define complex state transitions and constraints
- **Groq API Integration**: Fast LLM inference with constraint enforcement
- **Pre-built FSM Templates**: JSON, Email, Conversation flows, and Code generation
- **Flexible Constraint System**: Text, structural, and content-based validation
- **Streaming Support**: Real-time constraint validation during generation
- **Extensible Architecture**: Easy to create custom FSMs and constraints

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Contraining-LLMs-With-FSMs.git
cd Contraining-LLMs-With-FSMs
```

2. Install dependencies:
```bash
# Using pip
pip install groq pydantic python-dotenv

# Or install from requirements
pip install -r requirements.txt
```

3. Set up your Groq API key:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

## 🏃‍♂️ Quick Start

### Basic Usage

```python
from src.fsm import FiniteStateMachine, State, StateType, FSMBuilder
from src.llm import GroqClient, ConstrainedLLM

# Create a JSON structure FSM
json_fsm = FSMBuilder.create_json_fsm()

# Initialize Groq client
client = GroqClient()
constrained_llm = ConstrainedLLM(client)

# Generate constrained output
response = constrained_llm.generate_with_constraints(
    prompt="Create a JSON object for a person with name and age",
    fsm=json_fsm,
    guidance_prompt="Generate only valid JSON format"
)

print(response.text)  # Guaranteed to be valid JSON
```

### Run Examples

```bash
# Run all demonstrations
python main.py

# Run specific examples
python main.py --example json
python main.py --example email
python main.py --example conversation
python main.py --example code
python main.py --example all

# Run with custom API key
python main.py --api-key YOUR_GROQ_API_KEY
```

## 🧩 Components

### 1. Finite State Machine (FSM)

Create custom state machines to define valid output structures:

```python
from src.fsm import FiniteStateMachine, State, StateType, Transition

# Create FSM
fsm = FiniteStateMachine("start")

# Add states
fsm.add_state(State("start", StateType.INITIAL))
fsm.add_state(State("processing", StateType.INTERMEDIATE))
fsm.add_state(State("end", StateType.FINAL))

# Add transitions
fsm.add_transition(Transition(
    "start", "processing",
    lambda x: "begin" in x.lower(),
    "Start processing"
))
```

### 2. Constraints

Apply various types of constraints to your states:

```python
from src.fsm import TextConstraints, StructuralConstraints, ContentConstraints

# Text constraints
max_length = TextConstraints.max_length(100)
valid_email = TextConstraints.valid_email()

# Structural constraints  
balanced_brackets = StructuralConstraints.has_balanced_brackets()
word_count = StructuralConstraints.word_count(10, 50)

# Content constraints
requires_keywords = ContentConstraints.requires_keywords(["python", "code"])
positive_sentiment = ContentConstraints.sentiment_positive()
```

### 3. LLM Integration

Constrain LLM outputs using your FSMs:

```python
from src.llm import GroqClient, ConstrainedLLM, ConstrainedLLMConfig

# Configure the LLM
config = ConstrainedLLMConfig(
    max_tokens=512,
    temperature=0.3,
    max_retries=3
)

client = GroqClient()
constrained_llm = ConstrainedLLM(client, config)

# Generate with constraints
response = constrained_llm.generate_with_constraints(
    prompt="Your prompt here",
    fsm=your_fsm,
    guidance_prompt="Additional guidance"
)
```

## 📁 Project Structure

```
Contraining-LLMs-With-FSMs/
├── src/
│   ├── fsm/
│   │   ├── __init__.py
│   │   ├── state_machine.py    # Core FSM implementation
│   │   └── constraints.py      # Constraint functions
│   └── llm/
│       ├── __init__.py
│       └── groq_client.py      # Groq API integration
├── examples/
│   ├── json_constraint.py      # JSON structure example
│   ├── email_constraint.py     # Email format example
│   ├── conversation_flow.py    # Conversation flow example
│   └── code_generation.py     # Code generation example
├── tests/
│   ├── test_fsm.py            # FSM tests
│   └── test_llm.py            # LLM integration tests
├── main.py                    # Main demonstration script
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## 💡 Examples

### 1. JSON Structure Constraint

Force the LLM to generate valid JSON:

```python
from src.fsm import FSMBuilder

json_fsm = FSMBuilder.create_json_fsm()
# Use with constrained_llm.generate_with_constraints()
```

### 2. Email Format Constraint

Ensure generated emails are properly formatted:

```python
from src.fsm import FSMBuilder

email_fsm = FSMBuilder.create_email_fsm()
# Validates user@domain.tld format
```

### 3. Conversation Flow

Control conversation structure:

```python
from src.fsm import FSMBuilder

conversation_fsm = FSMBuilder.create_conversation_fsm()
# Enforces greeting -> question -> answer -> conclusion flow
```

### 4. Custom FSM

Create your own constraints:

```python
from src.fsm import FiniteStateMachine, State, StateType, Transition

# Custom phone number FSM
phone_fsm = FiniteStateMachine("start")
phone_fsm.add_state(State("start", StateType.INITIAL))
phone_fsm.add_state(State("area_code", StateType.INTERMEDIATE))
phone_fsm.add_state(State("number", StateType.FINAL))

phone_fsm.add_transition(Transition(
    "start", "area_code",
    lambda x: x.startswith("(") and ")" in x,
    "Area code in parentheses"
))

phone_fsm.add_transition(Transition(
    "area_code", "number",
    lambda x: x.count("-") >= 1,
    "Phone number with dashes"
))
```

## 🧪 Testing

Run the test suite:

```bash
# Run FSM tests
python tests/test_fsm.py

# Run LLM tests  
python tests/test_llm.py

# Run all tests
python -m pytest tests/ -v
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_DEFAULT_MODEL`: Default model to use (optional)

### Configuration Options

```python
from src.llm import ConstrainedLLMConfig

config = ConstrainedLLMConfig(
    max_tokens=512,        # Maximum tokens to generate
    temperature=0.7,       # Generation temperature (0.0-2.0)
    max_retries=3,         # Maximum retry attempts
    model="llama3-8b-8192" # Groq model to use
)
```

## 🔄 How It Works

1. **FSM Definition**: Create states and transitions that define valid output patterns
2. **Constraint Application**: Add validators to states for content validation
3. **LLM Guidance**: System prompts guide the LLM toward valid outputs
4. **Validation**: Generated text is validated against FSM constraints
5. **Retry Logic**: Invalid outputs trigger retries with additional guidance

## 🚀 Use Cases

- **Structured Data Generation**: JSON, XML, CSV formats
- **Format Validation**: Email addresses, phone numbers, URLs
- **Conversation Management**: Customer service, chatbots, interviews
- **Code Generation**: Functions, classes, documentation
- **Content Moderation**: Filtering inappropriate content
- **Multi-step Processes**: Guided workflows and forms

## 🛠️ Extending the Framework

### Creating Custom Constraints

```python
from src.fsm import TextConstraints

# Custom constraint function
def custom_constraint(text: str) -> bool:
    return "custom_rule" in text.lower()

# Add to state
state.validators.append(custom_constraint)
```

### Adding New FSM Templates

```python
from src.fsm import FSMBuilder

class CustomFSMBuilder(FSMBuilder):
    @staticmethod
    def create_custom_fsm():
        fsm = FiniteStateMachine("start")
        # Add your states and transitions
        return fsm
```

## 📝 API Reference

### FSM Classes

- `FiniteStateMachine`: Core state machine implementation
- `State`: Individual states with validation
- `Transition`: State transitions with conditions
- `FSMBuilder`: Pre-built FSM templates

### Constraint Classes

- `TextConstraints`: Length, pattern, format validation
- `StructuralConstraints`: Brackets, sentences, paragraphs
- `ContentConstraints`: Keywords, sentiment, requirements
- `CompositeConstraints`: Combining multiple constraints

### LLM Classes

- `GroqClient`: Groq API wrapper
- `ConstrainedLLM`: FSM-constrained generation
- `ConstrainedLLMConfig`: Configuration options
- `LLMResponse`: Response data structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest tests/`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast LLM inference
- [Pydantic](https://pydantic.dev/) for data validation
- Finite State Machine theory and applications

## 📞 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/Contraining-LLMs-With-FSMs/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/Contraining-LLMs-With-FSMs/discussions)

---

⭐ If you find this project useful, please consider giving it a star on GitHub!
