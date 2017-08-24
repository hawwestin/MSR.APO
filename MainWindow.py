# coding=utf-8
#my py
import MainGui
import tkinter as tk
from imgtree import *
from menubar import *
from tkinter import ttk

from style import StyleGuide


class Window(tk.Tk):
    # parameters that you want to send through the Frame class.
    def __init__(self, *args, **kwargs):
        """
        Self its TK and Controler -> parent is a Frame
        :param args:
        :param kwargs:
        """

        tk.Tk.__init__(self, *args, **kwargs)

        self.style = StyleGuide(self)

        container = tk.Frame(self)
        container.pack()
        # container.configure(background='grey')

        self.title("APO")
        mainmenu(container, self)

        self.statusbar()

        # self.imgtree = img_tree(container, self)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side="top", fill="both", expand=True)
        # self.notebook.style.configure(bg='grey')

    # def __del__(self):
    #     self.destroy()

    # def tabs(self):
        # notebook = ttk.Notebook(self)

    def new_tab(self, name):
        frame = ttk.Frame(self.notebook)
        frame.pack(fill=BOTH, expand=1)
        self.notebook.add(frame, text=name)
        return frame

    def rename_tab(self, name):
        tab = self.notebook.index("current")
        self.notebook.tab(tab, text=name)

    def statusbar(self):
        MainGui.statusmsg = Label(self, text=MainGui.statusmsg, bd=1, relief=SUNKEN, anchor=W)
        MainGui.statusmsg.pack(side=BOTTOM, fill=X)

    def tags(self):
        print(self.notebook.tabs())

    def tab_index(self):
        print(self.notebook.index("end"))
        print(self.notebook.index("current"))
        print(self.notebook.tab(self.notebook.index("current")))

    def close_Current_tab(self):
        id = self.notebook.index("current")
        self.notebook.forget("current")
        print(id)
        MainGui.gallery[id].__del__()
        MainGui.gallery.pop(id)
        # todo to zamyka tylko kartę potrzeba sksaować również obiekt by zwolnic pamiec

