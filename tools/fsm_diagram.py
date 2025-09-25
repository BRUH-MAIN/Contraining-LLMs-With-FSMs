#!/usr/bin/env python3
"""
LaTeX Math FSM State Diagram Generator
====================================

This script generates visual state machine diagrams for the LaTeX Math FSM.
It creates both a detailed flowchart and a simplified overview diagram.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import networkx as nx
from matplotlib.patches import Rectangle

def create_detailed_fsm_diagram():
    """Create detailed FSM diagram with all states and transitions."""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors for different state types
    colors = {
        'start': '#4CAF50',      # Green
        'math': '#2196F3',       # Blue  
        'command': '#FF9800',    # Orange
        'content': '#9C27B0',    # Purple
        'special': '#F44336',    # Red
        'end': '#4CAF50'         # Green
    }
    
    # State definitions with positions and types
    states = {
        'start': (2, 6, 'start'),
        'math_mode': (6, 6, 'math'),
        'command': (4, 9, 'command'),
        'brace_open': (8, 9, 'content'),
        'content': (10, 9, 'content'),
        'superscript': (4, 3, 'special'),
        'subscript': (4, 1, 'special'),
        'fraction_num': (8, 3, 'special'),
        'fraction_den': (8, 1, 'special'),
        'end_state': (14, 6, 'end')
    }
    
    # Draw states
    state_boxes = {}
    for state_name, (x, y, state_type) in states.items():
        # Create rounded rectangle
        box = FancyBboxPatch(
            (x-0.8, y-0.4), 1.6, 0.8,
            boxstyle="round,pad=0.1",
            facecolor=colors[state_type],
            edgecolor='black',
            linewidth=2,
            alpha=0.8
        )
        ax.add_patch(box)
        state_boxes[state_name] = (x, y)
        
        # Add state name
        ax.text(x, y, state_name.replace('_', '\n'), 
               ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Define transitions with labels
    transitions = [
        # From start
        ('start', 'math_mode', '$, $$, \\[', 0.2),
        
        # From math_mode
        ('math_mode', 'command', '\\command', 0.3),
        ('math_mode', 'superscript', '^', 0.2),
        ('math_mode', 'subscript', '_', 0.2),
        ('math_mode', 'content', '{', 0.3),
        ('math_mode', 'end_state', '$, $$, \\]', 0.2),
        
        # From command
        ('command', 'brace_open', '{', 0.2),
        
        # From brace_open
        ('brace_open', 'content', 'content', 0.2),
        ('brace_open', 'math_mode', '}', -0.3),
        
        # From content
        ('content', 'content', 'nested {}', 0.0),
        ('content', 'math_mode', '}', -0.4),
        
        # From superscript
        ('superscript', 'content', '{', 0.3),
        ('superscript', 'math_mode', 'var/num', -0.2),
        
        # From subscript  
        ('subscript', 'content', '{', 0.3),
        ('subscript', 'math_mode', 'var/num', -0.2),
        
        # Special fraction handling
        ('math_mode', 'fraction_num', '\\frac', 0.0),
        ('fraction_num', 'content', '{', 0.2),
        ('content', 'fraction_den', '} (after frac)', 0.0),
        ('fraction_den', 'content', '{', 0.2),
    ]
    
    # Draw transitions
    for from_state, to_state, label, curve in transitions:
        if from_state in state_boxes and to_state in state_boxes:
            x1, y1 = state_boxes[from_state]
            x2, y2 = state_boxes[to_state]
            
            # Create curved arrow
            if curve != 0:
                mid_x = (x1 + x2) / 2 + curve
                mid_y = (y1 + y2) / 2 + curve
                
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=1.5, color='black',
                                         connectionstyle=f"arc3,rad={curve}"))
                
                # Add label at midpoint
                ax.text(mid_x, mid_y, label, ha='center', va='center', 
                       fontsize=8, bbox=dict(boxstyle="round,pad=0.2", 
                                           facecolor='white', alpha=0.8))
            else:
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
                
                # Add label at midpoint
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(mid_x, mid_y, label, ha='center', va='center', 
                       fontsize=8, bbox=dict(boxstyle="round,pad=0.2", 
                                           facecolor='white', alpha=0.8))
    
    # Add title and legend
    ax.text(8, 11.5, 'LaTeX Math FSM - Detailed State Diagram', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Create legend
    legend_elements = [
        patches.Patch(color=colors['start'], label='Start/End States'),
        patches.Patch(color=colors['math'], label='Math Mode'),
        patches.Patch(color=colors['command'], label='Command Processing'),
        patches.Patch(color=colors['content'], label='Content/Braces'),
        patches.Patch(color=colors['special'], label='Special Constructs')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('latex_fsm_detailed.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_simplified_fsm_diagram():
    """Create simplified FSM diagram focusing on main flow."""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Simplified states
    states = {
        'START': (2, 4, '#4CAF50'),
        'MATH_MODE': (6, 4, '#2196F3'),
        'COMMAND': (6, 6, '#FF9800'),
        'CONTENT': (10, 4, '#9C27B0'),
        'SCRIPT': (6, 2, '#F44336'),
        'END': (12, 4, '#4CAF50')
    }
    
    # Draw simplified states
    for state_name, (x, y, color) in states.items():
        circle = plt.Circle((x, y), 0.8, facecolor=color, edgecolor='black', 
                           linewidth=2, alpha=0.8)
        ax.add_patch(circle)
        ax.text(x, y, state_name, ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white')
    
    # Simplified transitions
    transitions = [
        ('START', 'MATH_MODE', '$'),
        ('MATH_MODE', 'COMMAND', '\\cmd'),
        ('MATH_MODE', 'CONTENT', '{'),
        ('MATH_MODE', 'SCRIPT', '^/_'),
        ('MATH_MODE', 'END', '$'),
        ('COMMAND', 'CONTENT', '{'),
        ('CONTENT', 'MATH_MODE', '}'),
        ('SCRIPT', 'MATH_MODE', 'expr'),
        ('SCRIPT', 'CONTENT', '{'),
    ]
    
    # Draw simplified transitions
    for from_state, to_state, label in transitions:
        if from_state in states and to_state in states:
            x1, y1, _ = states[from_state]
            x2, y2, _ = states[to_state]
            
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
            
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y, label, ha='center', va='center', 
                   fontsize=9, bbox=dict(boxstyle="round,pad=0.2", 
                                       facecolor='yellow', alpha=0.7))
    
    ax.text(7, 7.5, 'LaTeX Math FSM - Simplified Overview', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('latex_fsm_simplified.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_example_trace_diagram():
    """Create example trace diagram showing FSM processing a LaTeX expression."""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Example: $\frac{x^2}{y+1}$
    expression = "$\\frac{x^2}{y+1}$"
    tokens = ["$", "\\frac", "{", "x", "^", "2", "}", "{", "y", "+", "1", "}", "$"]
    states = ["start", "math_mode", "fraction_num", "content", "content", "superscript", 
             "math_mode", "fraction_den", "content", "content", "content", "content", "math_mode", "end_state"]
    
    ax.text(8, 9.5, f'Example Trace: {expression}', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Draw trace
    y_pos = 8
    for i, (token, state) in enumerate(zip(tokens, states)):
        x_pos = 1 + i * 1.1
        
        # Token box
        token_box = FancyBboxPatch(
            (x_pos-0.3, y_pos-0.2), 0.6, 0.4,
            boxstyle="round,pad=0.05",
            facecolor='lightblue',
            edgecolor='black'
        )
        ax.add_patch(token_box)
        ax.text(x_pos, y_pos, token, ha='center', va='center', fontsize=8)
        
        # State box
        state_color = {
            'start': '#4CAF50', 'math_mode': '#2196F3', 'fraction_num': '#FF9800',
            'content': '#9C27B0', 'superscript': '#F44336', 'fraction_den': '#FF5722',
            'end_state': '#4CAF50'
        }.get(state, '#gray')
        
        state_box = FancyBboxPatch(
            (x_pos-0.4, y_pos-1.2), 0.8, 0.4,
            boxstyle="round,pad=0.05",
            facecolor=state_color,
            edgecolor='black',
            alpha=0.8
        )
        ax.add_patch(state_box)
        ax.text(x_pos, y_pos-1, state.replace('_', '\n'), ha='center', va='center', 
               fontsize=7, color='white', fontweight='bold')
        
        # Arrow
        if i < len(tokens) - 1:
            ax.annotate('', xy=(x_pos+0.5, y_pos-1), xytext=(x_pos+0.3, y_pos-1),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    
    # Add labels
    ax.text(0.5, y_pos, 'Token:', ha='right', va='center', fontweight='bold')
    ax.text(0.5, y_pos-1, 'State:', ha='right', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('latex_fsm_trace.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Generate all FSM diagrams."""
    print("🎨 Generating LaTeX Math FSM Diagrams...")
    
    print("📊 Creating detailed state diagram...")
    create_detailed_fsm_diagram()
    
    print("🔍 Creating simplified overview...")
    create_simplified_fsm_diagram()
    
    print("📝 Creating example trace diagram...")
    create_example_trace_diagram()
    
    print("✅ All diagrams generated successfully!")
    print("📁 Files created:")
    print("   - latex_fsm_detailed.png")
    print("   - latex_fsm_simplified.png") 
    print("   - latex_fsm_trace.png")

if __name__ == "__main__":
    main()