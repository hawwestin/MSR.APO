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

# f = Figure()
# a = f.add_subplot(111)


class Vision(tk.Frame):
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller
        self.path = None
        # Actual
        self.cvImage = None
        self.tkImage = None
        # temp
        self.cvImage_tmp = None
        self.tkImage_tmp = None
        self.id = None
        # Panele
        self.panel = None
        self.panel_tmp = None
        self.histCanvas = None
        self.toolbar = None
        # self.panel = tk.Label(parent)
        # self.panel.pack()
        self.f = Figure()
        self.a = self.f.add_subplot(111)

    def __del__(self):
        self.destroy()

    def open_color_img(self, path):
        # 0 - gray , 1 color
        self.path = path
        self.cvImage = cv2.imread(self.path, cv2.IMREAD_COLOR)
        # cv2.cvtColor(self.tkImage, cv2.COLOR_BGR2RGB, self.cvImage)
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        # TODO sa problemy przy otwieraniu obrazkow o jakims rozszerzeniu. gify i svg .
        image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tkImage = ImageTk.PhotoImage(image)

    def open_grey_scale_img(self, path):
        # 0 - gray , 1 color
        self.path = path
        self.cvImage = cv2.imread(self.path, 0)
        # TODO sa problemy przy otwieraniu obrazkow o jakims rozszerzeniu. gify i svg .
        image = cv2.cvtColor(self.cvImage, cv2.COLOR_GRAY2RGB)
        image = Image.fromarray(image)
        self.tkImage = ImageTk.PhotoImage(image)


    def assign_tkimage(self):
        image = cv2.cvtColor(self.cvImage, cv2.COLOR_GRAY2RGB)
                             # cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tkImage = ImageTk.PhotoImage(image)

    def assign_tkimage_tmp(self):
        image = cv2.cvtColor(self.cvImage_tmp, cv2.COLOR_GRAY2RGB)
                             # cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tkImage_tmp = ImageTk.PhotoImage(image)


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

    def close_hist(self):
        self.a.clear()
        # self.f.clear()

    def load_hist(self):
        # todo how to close histogram ?

        self.close_hist()
        # self.a.clear()
        # self.f.clear()
        # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])
        # TODO przerobic na bar plot

        self.a.hist(self.cvImage.ravel(), bins=256, range=[0.0, 256.0])
        self.a.set_xlim([0, 256])

        # self.a.hist(histr)

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.f, self.master)
            self.histCanvas.show()
            self.histCanvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        else:
            # self.canvas = FigureCanvasTkAgg(self.f, self.master)
            self.histCanvas.show()
            self.toolbar.update()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas, self.master)
            self.toolbar.update()
        else:
            self.toolbar.update()

        self.histCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def load_hist_tmp(self):
        # todo how to close histogram ?
        self.close_hist()

        self.a.clear()
        # f.clear()
        # histr = cv2.calcHist([self.cvImage_tmp], [0], None, [256], [0, 256])
        # self.a.plot(histr)

        self.a.hist(self.cvImage_tmp.ravel(), bins=256, range=[0, 256])
        self.a.set_xlim([0, 256])

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.f, self.master)
            self.histCanvas.show()
            self.histCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        else:
            self.histCanvas.show()
            self.toolbar.update()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas, self.master)
            self.toolbar.update()
        else:
            self.toolbar.update()

        # self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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
            # self.panel.configure(image=self.tkImage)
            # self.panel.image = self.tkImage
            self.panel.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panel.configure(image=self.tkImage)
            self.panel.image = self.tkImage

    def show_both_img(self):
        if self.panel_tmp is None or self.panel is None:
            self.panel_tmp = ttk.Label(self.master, image=self.tkImage_tmp)
            self.panel_tmp.image = self.tkImage_tmp
            self.panel_tmp.pack(side="left", padx=10, pady=10)

            self.panel = ttk.Label(self.master, image=self.tkImage)
            self.panel.image = self.tkImage
            self.panel.pack(side="left", padx=10, pady=10)

        # otherwise, update the image panels
        else:
            # update the pannels
            self.panel_tmp.configure(image=self.tkImage_tmp)
            self.panel.configure(image=self.tkImage)
            self.panel_tmp.image = self.tkImage_tmp
            self.panel.image = self.tkImage
        # self.panel.image = self.tkImage_tmp

    def color_picker(self):
        # Create a black image, a window
        def nothing(x):
            pass

        img = np.zeros((300, 512, 3), np.uint8)
        cv2.namedWindow('image')

        # create trackbars for color change
        cv2.createTrackbar('R', 'image', 0, 255, nothing)
        cv2.createTrackbar('G', 'image', 0, 255, nothing)
        cv2.createTrackbar('B', 'image', 0, 255, nothing)

        # create switch for ON/OFF functionality
        # switch = '0 : OFF \n1 : ON'
        # cv2.createTrackbar(switch, 'image', 0, 1, nothing)

        while (1):
            cv2.imshow('image', img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

            # get current positions of four trackbars
            r = cv2.getTrackbarPos('R', 'image')
            g = cv2.getTrackbarPos('G', 'image')
            b = cv2.getTrackbarPos('B', 'image')
            # s = cv2.getTrackbarPos(switch, 'image')

            # if s == 0:
                # img[:] = 0
            # else:
            img[:] = [b, g, r]

        cv2.destroyAllWindows()

    def hist_num(self):
        hist, bins = np.histogram(self.cvImage.flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        # cdf_normalized = cdf * hist.max() / cdf.max()

        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')

        self.cvImage_tmp = cdf[self.cvImage]

        self.assign_tkimage_tmp()
        self.show_both_img()
        self.load_hist_tmp()


        # plt.imshow(huk.cvImage_tmp)

        # self.show_both_img()

        # plt.plot(cdf_normalized, color='b')
        # plt.hist(self.cvImage.flatten(), 256, [0, 256], color='r')
        # plt.xlim([0, 256])
        # plt.legend(('cdf', 'histogram'), loc='upper left')
        # plt.show()

    def hist_eq(self):
        self.cvImage_tmp = cv2.equalizeHist(self.cvImage)

        self.assign_tkimage_tmp()
        self.show_both_img()
        self.load_hist_tmp()

    def hist_CLAHE(self):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3, 3))
        self.cvImage_tmp = clahe.apply(self.cvImage)

        self.assign_tkimage_tmp()
        self.show_both_img()
        self.load_hist_tmp()

    def save(self, path=None):
        if path is None:
            cv2.imwrite(self.path, self.cvImage)
        else:
            cv2.imwrite(path, self.cvImage)
