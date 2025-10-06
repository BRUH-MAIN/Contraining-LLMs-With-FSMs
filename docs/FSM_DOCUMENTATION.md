# LaTeX Math FSM - State Machine Documentation

## Overview
The LaTeX Math Finite State Machine (FSM) processes LaTeX mathematical expressions token-by-token to ensure syntactic validity. It handles complex mathematical constructs including fractions, superscripts, subscripts, commands, and nested braces.

## States

### 1. **START** 🏁
- **Description**: Initial state when FSM is created or reset
- **Valid Inputs**: Math mode delimiters
- **Transitions**: 
  - `$` → MATH_MODE (inline math)
  - `$$` → MATH_MODE (display math)
  - `\[` → MATH_MODE (display math)

### 2. **MATH_MODE** 🧮
- **Description**: Core state for processing mathematical content
- **Valid Inputs**: Variables, numbers, operators, commands, delimiters
- **Transitions**:
  - `\command` → COMMAND (for commands like \frac, \sum)
  - `^` → SUPERSCRIPT
  - `_` → SUBSCRIPT
  - `{` → CONTENT (entering braced content)
  - `}` → MATH_MODE (closing braces, if depth > 0)
  - Variables (a-z, A-Z) → MATH_MODE (stay)
  - Numbers (0-9) → MATH_MODE (stay)
  - Operators (+, -, =, etc.) → MATH_MODE (stay)
  - `$`, `$$`, `\]` → END_STATE (end math mode)

### 3. **COMMAND** ⚡
- **Description**: Processing LaTeX commands that require arguments
- **Valid Inputs**: Opening brace for command arguments
- **Transitions**:
  - `{` → BRACE_OPEN

### 4. **BRACE_OPEN** 📂
- **Description**: Just opened a brace, determining content type
- **Valid Inputs**: Any valid content or immediate brace closure
- **Transitions**:
  - `}` → MATH_MODE (empty braces)
  - Any other content → CONTENT

### 5. **CONTENT** 📝
- **Description**: Processing content inside braces {}
- **Valid Inputs**: Variables, numbers, operators, nested braces, commands
- **Transitions**:
  - `}` → MATH_MODE (if brace_depth becomes 0)
  - `}` → CONTENT (if brace_depth > 0, stay in nested content)
  - `{` → CONTENT (nested braces, increment depth)
  - Variables/Numbers/Operators/Commands → CONTENT (stay)

### 6. **SUPERSCRIPT** ⬆️
- **Description**: Processing superscript expressions (after ^)
- **Valid Inputs**: Single character or braced content
- **Transitions**:
  - `{` → CONTENT (complex superscript)
  - Single variable/number → MATH_MODE (simple superscript)

### 7. **SUBSCRIPT** ⬇️
- **Description**: Processing subscript expressions (after _)
- **Valid Inputs**: Single character or braced content  
- **Transitions**:
  - `{` → CONTENT (complex subscript)
  - Single variable/number → MATH_MODE (simple subscript)

### 8. **FRACTION_NUM** 🔢
- **Description**: Expecting numerator for \frac command
- **Valid Inputs**: Opening brace for numerator
- **Transitions**:
  - `{` → CONTENT (numerator content)

### 9. **FRACTION_DEN** 🔢
- **Description**: Expecting denominator for \frac command  
- **Valid Inputs**: Opening brace for denominator
- **Transitions**:
  - `{` → CONTENT (denominator content)

### 10. **END_STATE** 🎯
- **Description**: Valid final state - complete LaTeX expression
- **Valid Inputs**: None (terminal state)
- **Transitions**: None

## State Transition Rules

### Depth Tracking
The FSM maintains three depth counters:
- `brace_depth`: Tracks nested `{}`
- `bracket_depth`: Tracks nested `[]`  
- `paren_depth`: Tracks nested `()`

### Special Command Handling
- `\frac{}{}`: START → MATH_MODE → FRACTION_NUM → CONTENT → FRACTION_DEN → CONTENT → MATH_MODE
- `x^2`: MATH_MODE → SUPERSCRIPT → MATH_MODE
- `x_{i+1}`: MATH_MODE → SUBSCRIPT → CONTENT → MATH_MODE

## Valid Tokens

### Commands (200+ supported)
```
\frac, \sqrt, \sum, \int, \alpha, \beta, \gamma, \sin, \cos, \ln, \log,
\leq, \geq, \neq, \rightarrow, \leftarrow, \infty, \partial, \nabla, etc.
```

### Variables
```
a-z, A-Z (single characters)
```

### Numbers  
```
0-9 (single digits)
```

### Operators
```
+, -, *, /, =, <, >, !, ?, ., ,, ;, :, '
```

### Delimiters
```
(, ), [, ], {, }, |, \{, \}, \langle, \rangle, \lceil, \rceil, etc.
```

## Example Processing Traces

### Simple Expression: `$x^2$`
```
Token: $     | State: start → math_mode
Token: x     | State: math_mode → math_mode  
Token: ^     | State: math_mode → superscript
Token: 2     | State: superscript → math_mode
Token: $     | State: math_mode → end_state
```

### Complex Expression: `$\frac{x+1}{y^2}$`
```
Token: $      | State: start → math_mode
Token: \frac  | State: math_mode → fraction_num
Token: {      | State: fraction_num → content (depth=1)
Token: x      | State: content → content
Token: +      | State: content → content
Token: 1      | State: content → content  
Token: }      | State: content → fraction_den (depth=0)
Token: {      | State: fraction_den → content (depth=1)
Token: y      | State: content → content
Token: ^      | State: content → superscript
Token: 2      | State: superscript → content
Token: }      | State: content → math_mode (depth=0)
Token: $      | State: math_mode → end_state
```

## Validation Rules

### Complete Expression Requirements
1. Must start and end in valid states (START → END_STATE)
2. All braces must be balanced (brace_depth = 0)
3. All brackets must be balanced (bracket_depth = 0)
4. All parentheses must be balanced (paren_depth = 0)
5. Must have proper math mode delimiters

### Error Conditions
- Invalid tokens for current state
- Unbalanced delimiters
- Incomplete expressions (not reaching END_STATE)
- Unknown LaTeX commands
- Invalid character sequences

## Integration with LLM

### Generation Flow
1. **Free Generation**: LLM generates LaTeX expression naturally
2. **Extraction**: Extract LaTeX from LLM response using regex
3. **Validation**: Process extracted expression through FSM
4. **Accept/Retry**: If valid, return; if invalid, guide LLM to generate valid expression

### Token-by-Token Guidance
```python
# Get valid next tokens based on current FSM state
valid_tokens = fsm.get_current_possibilities()

# Guide LLM to choose only valid tokens
# (Implementation varies by LLM API)
```

This FSM design ensures that only syntactically correct LaTeX mathematical expressions can be generated, providing robust constraint satisfaction for mathematical content generation.