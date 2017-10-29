import tkinter as tk
from tkinter import ttk


class ScrolledCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        vscrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        hscrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        self.xview_moveto(0)
        self.yview_moveto(0)

        self.configure(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)

        vscrollbar.config(command=self.yview)
        hscrollbar.config(command=self.xview)
