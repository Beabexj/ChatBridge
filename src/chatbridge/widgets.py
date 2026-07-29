import tkinter as tk
from tkinter import ttk

def create_labeled_combobox(parent, label_text, values, default_value=None):
    """Create a frame containing a label and a combobox."""
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, pady=5)
    
    label = ttk.Label(frame, text=label_text, width=20)
    label.pack(side=tk.LEFT)
    
    combobox = ttk.Combobox(frame, values=values, state="readonly")
    if default_value is not None:
        combobox.set(default_value)
    combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X)
    
    return frame, combobox

def create_labeled_checkbox(parent, label_text, default_value=False):
    """Create a frame containing a label and a checkbox."""
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, pady=5)
    
    label = ttk.Label(frame, text=label_text, width=20)
    label.pack(side=tk.LEFT)
    
    var = tk.BooleanVar(value=default_value)
    checkbox = ttk.Checkbutton(frame, variable=var)
    checkbox.pack(side=tk.RIGHT, anchor=tk.E)
    
    return frame, var
