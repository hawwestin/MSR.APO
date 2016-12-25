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

from ComputerVision import *

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


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

    def show_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac

        :return:
        """
        # plt.imshow(self.image, cmap='Greys', interpolation='bicubic')
        # plt.show()
        # if the panels are None, initialize them
        if MainGui.panelA is None:
            MainGui.panelA = tk.Label(image=MainGui.gallery[MainGui.cwi].tkImage)
            # self.panelA.image = self.image.tkImage
            MainGui.panelA.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            MainGui.panelA.configure(image=MainGui.gallery[MainGui.cwi].tkImage)
            # self.panelA.image = self.image.tkImage

    def load_image(self):
        # open a file chooser dialog and allow the user to select an input
        # image
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
        # todo path do obrazka powinien byc storowany by moc go zapisac
        path = filedialog.askopenfilename()
        # self.statusbar()


        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk and init CV
            # nowy obiekt ? okno ? jak wiele okien ?
            MainGui.statusmsg.configure(text=os.path.splitext(path)[0])
            index = MainGui.add_img(Vision(self, self.tkController))

            # teraz Open po dodaniu
            MainGui.gallery[index].open_color_img(path)
            self.show_img()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Info")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(pady=20, padx=20)
        B1 = ttk.Button(popup, text="ok", command=popup.destroy)
        B1.pack(side=tk.BOTTOM, pady=20)
        popup.mainloop()


    def imgList(self):
        self.popupmsg(sorted(MainGui.gallery))

    def inHist(self):
        MainGui.gallery[MainGui.cwi].load_hist()

    def outHist(self):
        MainGui.gallery[MainGui.cwi].show_hist()

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016/2017")

