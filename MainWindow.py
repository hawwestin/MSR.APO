# coding=utf-8
#my py
import MainGui
import tkinter as tk
from imgtree import *
from menubar import *


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(tk.Tk):



    # parameters that you want to send through the Frame class.
    def __init__(self, *args, **kwargs):
        """
        Self its TK and Controler -> parent is a Frame
        :param args:
        :param kwargs:
        """
        # reference to the master widget, which is the tk window
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.title("APO")
        mainmenu(container, self)

        # self.imgtree = img_tree(container, self)

    def __del__(self):
        self.destroy()
