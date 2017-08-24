from tkinter import ttk
import sys


class StyleGuide(ttk.Style):
    def __init__(self, master):
        _bgcolor = 'wheat'  # RGV value #f5deb3
        _fgcolor = '#000000'  # Closest X11 color: 'black'
        _compcolor = '#b2c9f4'  # Closest X11 color: 'SlateGray2'
        _ana1color = '#eaf4b2'  # Closest X11 color: '{pale goldenrod}'
        _ana2color = '#f4bcb2'  # Closest X11 color: 'RosyBrown2'
        font10 = "-family {DejaVu Sans} -size 14 -weight normal -slant roman -underline 0 -overstrike 0"

        self.style = ttk.Style(master)
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        # self.style.configure('.', font=font10)
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=[('selected', _compcolor), ('active', _ana2color)])

    def get_style(self):
        return self.style


