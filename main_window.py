# coding=utf-8
# my py
import main_gui
import tkinter as tk
from menubar import MainMenu
from tkinter import ttk
from menu_command import MenuCmd
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

        main_gui.status_message = tk.StringVar()
        main_gui.status_message.set('')
        self.status_bar = tk.Label(self, textvariable=main_gui.status_message, bd=1, relief=tk.SUNKEN,
                                   anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side="top", fill="both", expand=True)

    def new_tab(self, tab_name):
        """
        Create a new frame and add it to notebook collection.

        Identification of selected notebook tab is made by frame variable _w
        with is unique assigned opn Frame.__init__
        :param tab_name:
        :return:
        """
        frame = ttk.Frame(self.notebook)
        frame.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(frame, text=tab_name)
        print("new tab id " + frame._w)
        return frame

    def rename_tab(self, name):
        tab = self.notebook.index("current")
        if isinstance(name, tk.StringVar):
            self.notebook.tab(tab, text=name.get())
        else:
            self.notebook.tab(tab, text=name)

    def tabs(self):
        print(self.notebook.tabs())

    def tab_index(self):
        '''
        Diagnostic method to adjust tab selection in
        :return:
        '''
        print("end " + str(self.notebook.index("end")))
        print("current " + str(self.notebook.index("current")))
        print("tab id " + str(self.notebook.select()))
        print("tab data " + str(self.notebook.tab(self.notebook.index("current"))))

    def close_Current_tab(self):
        id = self.notebook.index("current")
        self.notebook.forget("current")
        print(id)
        # main_gui.gallery[id].__del__()
        main_gui.gallery.pop(id)
        # todo to zamyka tylko kartę potrzeba sksaować również obiekt by zwolnic pamiec

    def update_status(self, text):
        main_gui.status_message.set(text)
        self.update_idletasks()
