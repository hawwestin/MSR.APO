import tkinter as tk
from tkinter.ttk import *
from tkinter.tix import *
import MainGui


class img_tree(tk.Frame):
    def __init__(self, parent, controller):
        """

        :param parent: a Frame Instance (a controler)
        :param controller: is a TK instance (self)
        """
        self.controller = controller
        tk.Frame.__init__(self, parent)
        # self.tw = HList()

    def show_frame(self, cont):
        frame = MainGui.frames[cont]
        frame.tkraise()



