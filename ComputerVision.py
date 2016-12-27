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
        tk.Frame.__init__(self, master=parent)
        self.controller = controller
        self.path = None
        self.cvImage = None
        self.tkImage = None
        self.id = None
        # Panele
        self.panel = None
        self.canvas = None
        self.toolbar = None
        # self.panel = tk.Label(parent)
        # self.panel.pack()
        self.f = Figure()
        self.a = f.add_subplot(111)


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
        print(MainGui.cwt)


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
        # global a
        # global f


        self.a.clear()
        # f.clear()
        histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])
        self.a.plot(histr)

        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(f, self.master)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        else:
            self.canvas.show()
            self.toolbar.update()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
            self.toolbar.update()
        else:
            self.toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
        if self.panel is None:
            self.panel = ttk.Label(self.master, image=self.tkImage)
            # self.panelA.image = self.image.tkImage
            self.panel.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panel.configure(image=self.tkImage)
            self.panel.image = self.tkImage
