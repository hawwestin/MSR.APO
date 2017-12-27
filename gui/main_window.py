# coding=utf-8
# my py
import tkinter as tk
from tkinter import ttk

from .menu_command import MenuCmd

from gui.menu_bar import MainMenu
from gui.style import StyleGuide
from gui.tabpicture import TabPicture
import app_config


class MainWindow(tk.Tk):
    # parameters that you want to send through the Frame class.
    def __init__(self, *args, **kwargs):
        """
        Main Window of application. Holds TabPicture instances in tk.notebook
        :param args:
        :param kwargs:
        """
        tk.Tk.__init__(self, *args, **kwargs)

        self.style = StyleGuide(self)

        self.body = tk.Frame(self)
        self.body.pack()
        self.status_message = tk.StringVar()

        self.title("APO")
        self.command = MenuCmd(self)
        self.main_menu = MainMenu(self.body, self)

        self.status_message.set('*')
        self.status_bar = tk.Label(self, textvariable=self.status_message, bd=1, relief=tk.SUNKEN,
                                   anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bind('<Configure>', self.resize)

    def new_tab(self, tab_name):
        """
        Create a new frame and add it to notebook collection.

        Identification of selected notebook tab is made by frame variable _w
        with is unique assigned opn Frame.__init__
        :param tab_name:
        :return:
        """
        frame = tk.Frame(self.notebook)
        frame.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(frame, text=tab_name)
        # print("new tab id " + frame._w)
        return frame

    def rename_tab(self, name):
        tab = self.notebook.index("current")
        if isinstance(name, tk.StringVar):
            self.notebook.tab(tab, text=name.get())
        else:
            self.notebook.tab(tab, text=name)

    def close_Current_tab(self):
        id = self.notebook.select()
        del TabPicture.gallery[id]
        TabPicture.gallery.pop(id, None)
        self.notebook.forget("current")

    def update_status(self, text):
        self.status_message.set(text)
        self.update_idletasks()

    def resize(self, _):
        app_config.main_window_resolution = self.winfo_geometry()
