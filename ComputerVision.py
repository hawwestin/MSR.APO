import MainGui
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style
# old
import cv2
import tkinter as tk
import numpy as np
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt

f = Figure()
a = f.add_subplot(111)


class Vision(tk.Frame):
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.path = None
        self.cvImage = None
        self.tkImage = None


    def open_color_img(self, path):
        # 0 - gray , 1 color
        # todo kopia dla obrazkow szarych
        self.path = path
        self.cvImage = cv2.imread(self.path, cv2.IMREAD_COLOR)
        # cv2.cvtColor(self.tkImage, cv2.COLOR_BGR2RGB, self.cvImage)
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        # TODO sa problemy przy otwieraniu obrazkow o jakims rozszerzeniu. gify i svg .
        image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tkImage = ImageTk.PhotoImage(image)



    def show(self):
        plt.imshow(self.cvImage, cmap='Greys', interpolation='bicubic')
        plt.show()

    def show_hist(self):
        """
                Wyswietlenie histogramu dla danego okna. zachowanie Mathplota
                zostawic . wyswietlanie dodatkowych ekranow z wykozystaniem tego

                :return:
                """
        # todo wyczyszczenie grafu przed zaladowaniem kolejnego , jak zaladowac kilka instancji do kilku obrazkow ?
        plt.hist(self.cvImage.ravel(), 256, [0, 255])
        plt.show()
        print(MainGui.cwi)


    def color_convertion(self, img):
        """
        chalupnicza nie wydajna metoda do conversji obrazow

        :param img:
        :return:
        """
        # Rearrang the color channel
        b, g, r = cv2.split(img) # not optimal TODO change to numpay array
        return cv2.merge((r, g, b))

    def load_hist(self):
        # todo how to close histogram ?
        global a
        global f

        print(MainGui.cwi)

        a.clear()
        # f.clear()
        histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])
        a.plot(histr)

        if MainGui.canvas is None:
            MainGui.canvas = FigureCanvasTkAgg(f, self.controller)
            MainGui.canvas.show()
            MainGui.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        else:
            MainGui.canvas.show()
            MainGui.toolbar.update()

        if MainGui.toolbar is None:
            MainGui.toolbar = NavigationToolbar2TkAgg(MainGui.canvas, self.controller)
            MainGui.toolbar.update()
        else:
            MainGui.toolbar.update()

        MainGui.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
