# coding=utf-8
#my py
import main_gui
import tkinter as tk
from imgtree import *
from menubar import *
from tkinter import ttk

from style import StyleGuide


class MainWindow(tk.Tk):
    # parameters that you want to send through the Frame class.
    def __init__(self, *args, **kwargs):
        """
        Self its TK and Controler -> parent is a Frame
        :param args:
        :param kwargs:
        """

        tk.Tk.__init__(self, *args, **kwargs)

        self.style = StyleGuide(self)

        self.body = tk.Frame(self)
        self.body.pack()

        self.title("APO")
        self.command = MenuCmd(self.body, self)
        self.main_menu = MainMenu(self.body, self)

        self.statusbar()

        # self.imgtree = img_tree(container, self)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side="top", fill="both", expand=True)
        # self.notebook.style.configure(bg='grey')


    def new_tab(self, name):
        frame = ttk.Frame(self.notebook)
        frame.pack(fill=BOTH, expand=1)
        self.notebook.add(frame, text=name)
        return frame

    def rename_tab(self, name):
        tab = self.notebook.index("current")
        self.notebook.tab(tab, text=name)

    def statusbar(self):
        main_gui.status_message = Label(self, text=main_gui.status_message, bd=1, relief=SUNKEN, anchor=W)
        main_gui.status_message.pack(side=BOTTOM, fill=X)

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
        main_gui.gallery[id].__del__()
        main_gui.gallery.pop(id)
        # todo to zamyka tylko kartę potrzeba sksaować również obiekt by zwolnic pamiec

