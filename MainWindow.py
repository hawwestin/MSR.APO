# coding=utf-8
#my py
import MainGui
import tkinter as tk
from imgtree import *
from menubar import *


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master
        # init a CV instance
        MainGui.image = Vision()

        self.master.title("APO")
        mainmenu(self.master)
        self.imgtree = img_tree(master)
