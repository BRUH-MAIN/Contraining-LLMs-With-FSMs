# Development Tools and Utilities

This directory contains utility tools for the LaTeX Math FSM project.

## Available Tools

### 🎨 `fsm_diagram.py`
Generate static state machine diagrams.

```bash
# Generate all diagrams
python tools/fsm_diagram.py
```

**Outputs:**
- `assets/latex_fsm_detailed.png` - Comprehensive state diagram
- `assets/latex_fsm_simplified.png` - High-level overview
- `assets/latex_fsm_trace.png` - Example processing trace

### 📊 `fsm_visualizer.py`
Interactive visualization components for Streamlit.

**Components:**
- `create_interactive_fsm_diagram()` - Interactive state diagram
- `create_token_flow_visualization()` - Token processing flow
- `create_state_statistics_chart()` - Usage statistics
- `render_fsm_trace_table()` - Detailed processing table
- `create_transition_matrix_heatmap()` - State transition matrix

**Usage in Streamlit:**
```python
from tools.fsm_visualizer import create_interactive_fsm_diagram
fig = create_interactive_fsm_diagram()
st.plotly_chart(fig)
```

## Dependencies

These tools require additional packages:
- `matplotlib` - Static diagram generation
- `plotly` - Interactive visualizations  
- `networkx` - Graph operations
- `pandas` - Data manipulation

Install with:
```bash
uv add matplotlib plotly networkx pandas
```

## Development Workflow

### Updating Diagrams
1. Modify FSM structure in `src/fsm/latex_math_fsm.py`
2. Update diagram generation in `tools/fsm_diagram.py`
3. Regenerate assets: `python tools/fsm_diagram.py`
4. Update interactive components in `tools/fsm_visualizer.py`
5. Test in Streamlit: `streamlit run streamlit_app.py`

### Adding New Visualizations
1. Create new function in `fsm_visualizer.py`
2. Add unique Streamlit key for plotly charts
3. Import and use in `streamlit_app.py`
4. Test all tabs work correctly

## Customization

### Colors and Styling
State colors are defined in both files:
- 🟢 Start/End: `#4CAF50`
- 🔵 Math Mode: `#2196F3`  
- 🟠 Commands: `#FF9800`
- 🟣 Content: `#9C27B0`
- 🔴 Special: `#F44336`

### Layout and Positioning  
Modify state positions in `fsm_diagram.py`:
```python
states = {
    'start': (x, y, color),
    # ... other states
}
```

## Future Tools

Planned additions:
- [ ] **Performance Profiler**: Analyze FSM processing speed
- [ ] **Command Coverage Analyzer**: Track LaTeX command usage
- [ ] **Export Utilities**: Save results in various formats
- [ ] **Batch Processor**: Process multiple LaTeX files
- [ ] **Validation Reporter**: Generate validation reports

## Contributing

When adding new tools:
1. Follow existing code structure
2. Add comprehensive docstrings
3. Include usage examples
4. Update this README
5. Test with different inputs

---

*Tools make development faster and visualization clearer!* 🛠️