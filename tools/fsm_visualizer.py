"""
Interactive FSM Visualizer for Streamlit
=======================================

This module provides interactive visualization components for the LaTeX Math FSM
that can be integrated into the Streamlit app.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Tuple, Optional

def create_interactive_fsm_diagram():
    """Create an interactive FSM diagram using Plotly."""
    
    # Define state positions for the graph
    states = {
        'START': (1, 3, '#4CAF50'),
        'MATH_MODE': (3, 3, '#2196F3'), 
        'COMMAND': (3, 4.5, '#FF9800'),
        'BRACE_OPEN': (4.5, 4.5, '#9C27B0'),
        'CONTENT': (6, 3, '#9C27B0'),
        'SUPERSCRIPT': (3, 1.5, '#F44336'),
        'SUBSCRIPT': (3, 0.5, '#F44336'),
        'FRACTION_NUM': (4.5, 1.5, '#FF5722'),
        'FRACTION_DEN': (4.5, 0.5, '#FF5722'),
        'END_STATE': (8, 3, '#4CAF50')
    }
    
    # Create the plot
    fig = go.Figure()
    
    # Add states as circles
    for state, (x, y, color) in states.items():
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=30, color=color, line=dict(width=2, color='black')),
            text=state.replace('_', '<br>'),
            textposition='middle center',
            textfont=dict(color='white', size=10),
            name=state,
            hovertemplate=f'<b>{state}</b><br>Click to see transitions<extra></extra>'
        ))
    
    # Define transitions
    transitions = [
        ('START', 'MATH_MODE', '$'),
        ('MATH_MODE', 'COMMAND', '\\cmd'),
        ('MATH_MODE', 'SUPERSCRIPT', '^'),
        ('MATH_MODE', 'SUBSCRIPT', '_'),
        ('MATH_MODE', 'CONTENT', '{'),
        ('MATH_MODE', 'END_STATE', '$'),
        ('COMMAND', 'BRACE_OPEN', '{'),
        ('BRACE_OPEN', 'CONTENT', 'content'),
        ('CONTENT', 'MATH_MODE', '}'),
        ('SUPERSCRIPT', 'MATH_MODE', 'expr'),
        ('SUPERSCRIPT', 'CONTENT', '{'),
        ('SUBSCRIPT', 'MATH_MODE', 'expr'),
        ('SUBSCRIPT', 'CONTENT', '{'),
        ('MATH_MODE', 'FRACTION_NUM', '\\frac'),
        ('FRACTION_NUM', 'CONTENT', '{'),
        ('CONTENT', 'FRACTION_DEN', '} (frac)'),
        ('FRACTION_DEN', 'CONTENT', '{'),
    ]
    
    # Add transition arrows
    for from_state, to_state, label in transitions:
        if from_state in states and to_state in states:
            x0, y0, _ = states[from_state]
            x1, y1, _ = states[to_state]
            
            # Add arrow
            fig.add_annotation(
                x=x1, y=y1,
                ax=x0, ay=y0,
                xref='x', yref='y',
                axref='x', ayref='y',
                text='',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='gray'
            )
            
            # Add label
            mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
            fig.add_trace(go.Scatter(
                x=[mid_x], y=[mid_y],
                mode='text',
                text=label,
                textfont=dict(size=8),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Update layout
    fig.update_layout(
        title='LaTeX Math FSM - Interactive State Diagram',
        showlegend=False,
        width=1000, height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_token_flow_visualization(tokens: List[str], states: List[str]):
    """Create a visualization of token processing flow."""
    
    if not tokens or not states:
        return go.Figure()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Token Sequence', 'State Transitions'),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Token sequence
    fig.add_trace(
        go.Scatter(
            x=list(range(len(tokens))),
            y=[1] * len(tokens),
            mode='markers+text',
            marker=dict(size=20, color='lightblue', line=dict(width=2, color='blue')),
            text=tokens,
            textposition='middle center',
            name='Tokens',
            hovertemplate='Token %{x}: %{text}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # State sequence
    state_colors = {
        'start': '#4CAF50', 'math_mode': '#2196F3', 'command': '#FF9800',
        'content': '#9C27B0', 'superscript': '#F44336', 'subscript': '#F44336',
        'fraction_num': '#FF5722', 'fraction_den': '#FF5722', 'end_state': '#4CAF50'
    }
    
    colors = [state_colors.get(state, '#gray') for state in states]
    
    fig.add_trace(
        go.Scatter(
            x=list(range(len(states))),
            y=[1] * len(states),
            mode='markers+text',
            marker=dict(size=25, color=colors, line=dict(width=2, color='black')),
            text=[state.replace('_', '<br>') for state in states],
            textposition='middle center',
            textfont=dict(color='white', size=8),
            name='States',
            hovertemplate='Step %{x}: %{text}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add arrows between states
    for i in range(len(states) - 1):
        fig.add_annotation(
            x=i+1, y=1,
            ax=i, ay=1,
            xref='x2', yref='y2',
            axref='x2', ayref='y2',
            text='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='red'
        )
    
    # Update layout
    fig.update_layout(
        title=f'Processing Flow: {len(tokens)} tokens → {len(states)} states',
        showlegend=False,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    
    return fig

def create_state_statistics_chart(fsm_path: List[str]):
    """Create a chart showing state usage statistics."""
    
    if not fsm_path:
        return go.Figure()
    
    # Count state occurrences
    state_counts = {}
    for state in fsm_path:
        state_counts[state] = state_counts.get(state, 0) + 1
    
    # Create bar chart
    states = list(state_counts.keys())
    counts = list(state_counts.values())
    
    colors = ['#4CAF50' if state in ['start', 'end_state'] 
             else '#2196F3' if state == 'math_mode'
             else '#FF9800' if 'command' in state or 'fraction' in state
             else '#9C27B0' if 'content' in state or 'brace' in state
             else '#F44336' for state in states]
    
    fig = go.Figure(data=[
        go.Bar(x=states, y=counts, marker_color=colors, 
               hovertemplate='State: %{x}<br>Visits: %{y}<extra></extra>')
    ])
    
    fig.update_layout(
        title='State Usage Frequency',
        xaxis_title='FSM States',
        yaxis_title='Number of Visits',
        height=300
    )
    
    return fig

def render_fsm_trace_table(tokens: List[str], states: List[str], 
                          possibilities: List[List[str]] = None):
    """Render a detailed trace table of FSM processing."""
    
    if not tokens or not states:
        st.warning("No trace data available")
        return
    
    # Create trace data
    trace_data = []
    for i, (token, state) in enumerate(zip(tokens, states)):
        possible = possibilities[i][:5] if possibilities and i < len(possibilities) else []
        trace_data.append({
            'Step': i + 1,
            'Token': token,
            'State': state,
            'Possibilities': ', '.join(possible) + ('...' if len(possible) == 5 else ''),
            'Valid': '✅'
        })
    
    # Convert to DataFrame and display
    df = pd.DataFrame(trace_data)
    
    st.subheader("🔍 Detailed Processing Trace")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            'Step': st.column_config.NumberColumn('Step', width='small'),
            'Token': st.column_config.TextColumn('Token', width='small'),
            'State': st.column_config.TextColumn('State', width='medium'),
            'Possibilities': st.column_config.TextColumn('Next Possibilities', width='large'),
            'Valid': st.column_config.TextColumn('✓', width='small')
        }
    )

def render_fsm_complexity_metrics(fsm):
    """Render complexity metrics for the FSM."""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Total States",
            value=10,
            help="Number of distinct states in the FSM"
        )
    
    with col2:
        st.metric(
            label="📝 Valid Commands", 
            value=len(fsm.VALID_COMMANDS),
            help="Number of supported LaTeX commands"
        )
    
    with col3:
        st.metric(
            label="🔤 Variables",
            value=len(fsm.VALID_VARIABLES),
            help="Supported variable characters (a-z, A-Z)"
        )
    
    with col4:
        st.metric(
            label="⚡ Operators",
            value=len(fsm.VALID_OPERATORS),
            help="Supported mathematical operators"
        )

def render_state_description(selected_state: str):
    """Render detailed description of a selected state."""
    
    state_descriptions = {
        'START': {
            'description': 'Initial state when FSM is created or reset',
            'valid_inputs': ['$', '$$', '\\['],
            'transitions': ['MATH_MODE'],
            'color': '#4CAF50'
        },
        'MATH_MODE': {
            'description': 'Core state for processing mathematical content',
            'valid_inputs': ['variables', 'numbers', 'operators', 'commands', '^', '_', '{', '}'],
            'transitions': ['COMMAND', 'SUPERSCRIPT', 'SUBSCRIPT', 'CONTENT', 'END_STATE'],
            'color': '#2196F3'
        },
        'COMMAND': {
            'description': 'Processing LaTeX commands that require arguments',
            'valid_inputs': ['{'],
            'transitions': ['BRACE_OPEN'],
            'color': '#FF9800'
        },
        'CONTENT': {
            'description': 'Processing content inside braces {}',
            'valid_inputs': ['variables', 'numbers', 'operators', 'commands', '{', '}'],
            'transitions': ['CONTENT', 'MATH_MODE'],
            'color': '#9C27B0'
        },
        'SUPERSCRIPT': {
            'description': 'Processing superscript expressions (after ^)',
            'valid_inputs': ['single char', '{'],
            'transitions': ['MATH_MODE', 'CONTENT'],
            'color': '#F44336'
        },
        'SUBSCRIPT': {
            'description': 'Processing subscript expressions (after _)',
            'valid_inputs': ['single char', '{'],
            'transitions': ['MATH_MODE', 'CONTENT'],
            'color': '#F44336'
        },
        'END_STATE': {
            'description': 'Valid final state - complete LaTeX expression',
            'valid_inputs': [],
            'transitions': [],
            'color': '#4CAF50'
        }
    }
    
    if selected_state in state_descriptions:
        info = state_descriptions[selected_state]
        
        st.markdown(f"""
        <div style="border-left: 4px solid {info['color']}; padding-left: 20px; margin: 10px 0;">
            <h4 style="color: {info['color']}; margin-top: 0;">{selected_state}</h4>
            <p><strong>Description:</strong> {info['description']}</p>
            <p><strong>Valid Inputs:</strong> {', '.join(info['valid_inputs']) if info['valid_inputs'] else 'None (terminal state)'}</p>
            <p><strong>Possible Transitions:</strong> {', '.join(info['transitions']) if info['transitions'] else 'None (terminal state)'}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"State '{selected_state}' not found in descriptions.")

def create_transition_matrix_heatmap(fsm):
    """Create a heatmap showing state transition patterns."""
    
    # Define all states
    all_states = ['START', 'MATH_MODE', 'COMMAND', 'BRACE_OPEN', 'CONTENT', 
                 'SUPERSCRIPT', 'SUBSCRIPT', 'FRACTION_NUM', 'FRACTION_DEN', 'END_STATE']
    
    # Create transition matrix (simplified)
    transitions = {
        ('START', 'MATH_MODE'): 1,
        ('MATH_MODE', 'COMMAND'): 1,
        ('MATH_MODE', 'SUPERSCRIPT'): 1,
        ('MATH_MODE', 'SUBSCRIPT'): 1,
        ('MATH_MODE', 'CONTENT'): 1,
        ('MATH_MODE', 'END_STATE'): 1,
        ('MATH_MODE', 'MATH_MODE'): 1,
        ('COMMAND', 'BRACE_OPEN'): 1,
        ('BRACE_OPEN', 'CONTENT'): 1,
        ('CONTENT', 'MATH_MODE'): 1,
        ('CONTENT', 'CONTENT'): 1,
        ('SUPERSCRIPT', 'MATH_MODE'): 1,
        ('SUPERSCRIPT', 'CONTENT'): 1,
        ('SUBSCRIPT', 'MATH_MODE'): 1,
        ('SUBSCRIPT', 'CONTENT'): 1,
    }
    
    # Create matrix
    matrix = [[0 for _ in all_states] for _ in all_states]
    for i, from_state in enumerate(all_states):
        for j, to_state in enumerate(all_states):
            if (from_state, to_state) in transitions:
                matrix[i][j] = transitions[(from_state, to_state)]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=all_states,
        y=all_states,
        colorscale='Blues',
        hoverongaps=False,
        hovertemplate='From: %{y}<br>To: %{x}<br>Transitions: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='State Transition Matrix',
        xaxis_title='To State',
        yaxis_title='From State',
        height=500
    )
    
    return fig