import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
# tk
import tkinter as tk
# from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# my py
import os
import MainGui
import histEq
import prog
import adap_prog
import Red_poz_sza

from ComputerVision import *

LARGE_FONT = MainGui.LARGE_FONT
NORM_FONT = MainGui.NORM_FONT
SMALL_FONT = MainGui.SMALL_FONT


class MenuCmd(tk.Frame):
    def __init__(self, parentFrame, tkController):
        tk.Frame.__init__(self, parentFrame)
        # just self
        # self.parentFrame = parentFrame
        self.tkController = tkController

    @staticmethod
    def client_exit():
        exit()

    def treelist(self):
        """
        Lista obrazkowu przechowywana w tree liscie plikow po lewej stronie ekranu
        z mozliwoscia rozszerzenia .
        :return:
        """
        # todo https://docs.python.org/3.5/library/tkinter.ttk.html?highlight=ttk#treeview
        self.not_implemented()


    def open_color_image(self):
        # open a file chooser dialog and allow the user to select an input
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie

        path = filedialog.askopenfilename()
        if len(path) > 0:
            tab = self.tkController.new_tab(os.path.splitext(path)[0])

            MainGui.add_img(tab._w, Vision(tab, self.tkController))

            MainGui.gallery[tab._w].open_color_img(path)
            MainGui.gallery[tab._w].set_panel_img()
            # MainGui.gallery[tab._w].panel.pack(side="left",
            #                                    padx=10,
            #                                    pady=10)


    def open_grey_image(self):
        # open a file chooser dialog and allow the user to select an input
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
        path = filedialog.askopenfilename()
        if len(path) > 0:
            tab = self.tkController.new_tab(os.path.splitext(path)[0])

            MainGui.add_img(tab._w, Vision(tab, self.tkController))

            MainGui.gallery[tab._w].open_grey_scale_img(path)
            MainGui.gallery[tab._w].set_panel_img()
            # MainGui.gallery[tab._w].panel.pack(side="left",
            #                                    padx=10,
            #                                    pady=10)



    def load_image(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            tab_id = self.tkController.notebook.select()
            # MainGui.statusmsg.configure(text=os.path.splitext(path)[0])
            self.tkController.rename_tab(os.path.splitext(path)[0])

            MainGui.gallery[tab_id].open_color_img(path)
            MainGui.gallery[tab_id].set_panel_img()
            # MainGui.gallery[tab._w].panel.pack(side="left",
            #                                    padx=10,
            #                                    pady=10)
            if MainGui.gallery[tab_id].histCanvas is not None:
                MainGui.gallery[tab_id].set_hist()
                MainGui.gallery[tab_id].set_hist_geometry()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Info")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=msg, font=NORM_FONT, justify=tk.CENTER)
        label.pack(pady=20, padx=20)
        B1 = ttk.Button(popup, text="ok", command=popup.destroy)
        B1.pack(side=tk.BOTTOM, pady=20)
        popup.mainloop()


    def imgList(self):
        print(self.tkController.notebook.index("current"))
        print(self.tkController.notebook.index("end"))
        print(self.tkController.notebook.tab(self.tkController.notebook.index("current")))
        print(self.tkController.notebook.tabs())
        print(self.tkController.notebook.select())

    def inHist(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].set_hist()
        MainGui.gallery[tab_id].set_hist_geometry()

    def outHist(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].show_hist()

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016/2017")

    def picker(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].color_picker()

    def hist_Equ(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        histEq.Hist_Equalization(tab_id)


    def save(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].save()

    def save_as(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        title = filedialog.asksaveasfilename()
        # TODO jakis dialog box do podania ścieżki.
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].save(title)

    def clear_hist(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].close_hist()

    def negacja(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        MainGui.gallery[tab_id].negation()
        MainGui.gallery[tab_id].set_panel_img()
        if MainGui.gallery[tab_id].histCanvas is not None:
            MainGui.gallery[tab_id].set_hist()

    def progowanie(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        prog.progowanie(tab_id)

    def adap_progowanie(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        adap_prog.progowanie(tab_id)

    def redukcja_p_s(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        Red_poz_sza.rps(tab_id)
        # MainGui.gallery[tab_id].rps()
        # MainGui.gallery[tab_id].set_panel_img()
        # if MainGui.gallery[tab_id].histCanvas is not None:
        #     MainGui.gallery[tab_id].set_hist()