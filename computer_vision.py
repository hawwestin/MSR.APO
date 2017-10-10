import matplotlib

from repeater import Repeater

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style
from cv2 import *
import cv2
import tkinter as tk
import numpy as np
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt

colors = {"COLOR": 1,
          "GREY": 0}

supported_ext = [
    ".jpg",
    ".png"
]


class ImageData(Repeater):

    @property
    def tk_image(self):
        """
        Return tkImage of current cvImage
        :param image:
        :return:
        """
        # todo add resize on image to keep same size after image enchantments operations.
        return ImageTk.PhotoImage(Image.fromarray(self.item))


class Vision:
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.path = None
        self.color = None

        # Actual
        self.cvImage = ImageData()
        self.tkImage = None
        # temp
        self.cvImage_tmp = None
        self.tkImage_tmp = None
        self.id = None
        # Panele
        self.panel = None
        self.panel_tmp = None
        self.display = tk.Canvas(parent, bd=0, highlightthickness=0)
        self.frame_for_Canvas = tk.Frame(master=parent)
        self.histCanvas = None
        self.toolbar = None
        # self.panel = tk.Label(parent)
        # self.panel.pack()
        self.f = Figure()
        self.fig_subplot = self.f.add_subplot(111)
        # ToDO po tym resize nie widac histogramu po prawej stronie.
        # parent.bind("<Configure>", self.resize)
        # Bad Idea Dont do that again
        # self.fCanvas.bind("<Configure>", self.resize)

    def open_image(self, path):
        self.path = path
        if self.color is cv2.IMREAD_COLOR:
            self.cvImage.update(cv2.imread(self.path, cv2.IMREAD_COLOR))
            self.cvImage.update(cv2.cvtColor(self.cvImage.current(), cv2.COLOR_BGR2RGB))
        else:
            self.cvImage.update(cv2.imread(self.path, cv2.IMREAD_GRAYSCALE))

        self.tkImage = self.cvImage.tk_image

    def assign_tkimage(self, image):
        # todo move this to tabpic
        # if self.color is cv2.IMREAD_COLOR:
        #     image = cv2.cvtColor(self.cvImage, cv2.COLOR_RGB2BGR)
        # else:
        #     image = cv2.cvtColor(self.cvImage, cv2.COLOR_GRAY2BGR)
        return ImageTk.PhotoImage(Image.fromarray(image))

    ################################

    # def show(self):
    #     plt.imshow(self.cvImage, cmap='Greys', interpolation='bicubic')
    #     plt.show()

    def color_convertion(self, img):
        """
        chalupnicza nie wydajna metoda do conversji obrazow

        :param img:
        :return:
        """
        # Rearrang the color channel
        b, g, r = cv2.split(img)  # not optimal TODO change to numpay array
        return cv2.merge((r, g, b))

    def close_hist(self):
        self.fig_subplot.clear()
        # self.f.clear()

    def set_hist_geometry(self):
        # self.histCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # self.histCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_for_Canvas.pack(side=tk.RIGHT, expand=True)

    def set_hist(self, tmp=None):
        # todo how close histogram ?

        if tmp is None:
            source = self.cvImage.current()
            self.close_hist()
            # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])

            self.fig_subplot.hist(source.ravel(), bins=256, range=[0.0, 256.0])
            self.fig_subplot.set_xlim([0, 256])

        else:
            self.close_hist()
            # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])

            self.fig_subplot.hist(self.cvImage_tmp.ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
            self.fig_subplot.hist(self.cvImage.current().ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
            self.fig_subplot.set_xlim([0, 256])

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.f, self.frame_for_Canvas)
            self.histCanvas.show()
        else:
            self.histCanvas.show()
            ###################
            #     ToolBAR
            ###################
        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas,
                                                   self.frame_for_Canvas)
            self.toolbar.update()
        else:
            self.toolbar.update()

        self.histCanvas.get_tk_widget().pack(side=tk.TOP,
                                             fill=tk.BOTH,
                                             expand=True)

    def set_panel_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac
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
            self.panel.configure(image=self.tkImage)
            self.panel.image = self.tkImage

        if self.panel_tmp is None and self.tkImage_tmp is not None:
            self.panel_tmp = ttk.Label(self.master, image=self.tkImage_tmp)
            # self.panel.configure(image=self.tkImage)
            # self.panel.image = self.tkImage
            self.panel_tmp.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        elif self.panel_tmp is not None:
            self.panel_tmp.configure(image=self.tkImage_tmp)
            self.panel_tmp.image = self.tkImage_tmp

    def show_both_img(self):
        if self.panel_tmp is None or self.panel is None:
            self.panel_tmp = ttk.Label(self.master, image=self.tkImage_tmp)
            self.panel_tmp.image = self.tkImage_tmp
            self.panel_tmp.pack(side="left", padx=10, pady=10)

            self.panel = ttk.Label(self.master, image=self.tkImage)
            self.panel.image = self.tkImage
            self.panel.pack(side="left")

        # otherwise, update the image panels
        else:
            # update the pannels
            self.panel_tmp.configure(image=self.tkImage_tmp)
            self.panel.configure(image=self.tkImage)
            self.panel_tmp.image = self.tkImage_tmp
            self.panel.image = self.tkImage
            # self.panel.image = self.tkImage_tmp

    def resize(self, width, height):
        """
        Resize
        :param width:
        :param height:
        :return:
        """
        # TODO store the original value to save image in original size.
        size = (width, height)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage.current())
        resized = image.resize(size, Image.ANTIALIAS)
        self.tkImage = ImageTk.PhotoImage(resized)

    def resize_event(self, event):
        # TODO store the original value to save image in original size.
        size = (event.width, event.height)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage)
        resized = image.resize_event(size, Image.ANTIALIAS)
        self.tkImage = ImageTk.PhotoImage(resized)
        #         For Canvas
        # self.display.delete("IMG")
        # self.display.create_image(0, 0, image=self.tkImage, anchor='nw', tags="IMG")
        #

    def resize_event_tmp(self, event):
        # TODO store the original value to save image in original size.
        size = (event.width - 20, event.height - 25)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage_tmp)
        resized = image.resize_event(size, Image.ANTIALIAS)
        self.tkImage_tmp = ImageTk.PhotoImage(resized)
        #         For Canvas
        # self.display.delete("IMG")
        # self.display.create_image(0, 0, image=self.tkImage, anchor='nw', tags="IMG")

    def global_prog(self, thresh, thresholdType=cv2.THRESH_BINARY):
        ret, self.cvImage_tmp = cv2.threshold(self.cvImage.current(), thresh, 255, thresholdType)
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)
        self.show_both_img()
        # self.set_hist(tmp=1)

    def adaptive_prog(self, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=11,
                      C=2):
        """
        Adaptive Thresholding

        :param adaptiveMethod: cv2.ADAPTIVE_THRESH_GAUSSIAN_C or cv2.ADAPTIVE_THRESH_MEAN_C,
        :param thresholdType: types are :
                            cv2.THRESH_BINARY
                            cv2.THRESH_BINARY_INV
                            cv2.THRESH_TRUNC
                            cv2.THRESH_TOZERO
                            cv2.THRESH_TOZERO_INV

        :param blockSize: It decides the size of neighbourhood area.
        :param C: It is just a constant which is subtracted from the mean or weighted mean calculated.
        :return:
        """
        self.cvImage_tmp = cv2.adaptiveThreshold(self.cvImage.current(), 255,
                                                 adaptiveMethod,
                                                 thresholdType,
                                                 blockSize,
                                                 C)
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)
        self.show_both_img()

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

    def rps(self, num):
        # redukcja poziomow szarosci
        bins = np.arange(0, 256, num)
        l_bins = []
        for i in range(num):
            l_bins.append(bins)

        cdf_m = [list(a) for a in zip(*l_bins)]
        cdf_m = np.array(cdf_m).ravel()
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage_tmp = cdf[self.cvImage.current()]
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)

    def negation(self):
        # cv2.invert(self.cvImage, self.cvImage_tmp)

        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])
        # cdf = hist.cumsum()
        cdf_m = (255 - bins)
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # print("cdf Lut: ", cdf)
        # LUT Table cdf
        self.cvImage.update(cdf[self.cvImage.current()])
        self.tkImage = self.cvImage.tk_image

    def hist_rand(self):
        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.mean())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')

        self.cvImage_tmp = cdf[self.cvImage.current()]
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)

    def hist_num(self):
        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        # cdf_normalized = cdf * hist.max() / cdf.max()

        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage_tmp = cdf[self.cvImage.current()]

        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)
        # TODO zmieniac tylko _tmp obraz nie potrzeba przeladowywac orginalnego jezeli go nie modyfikujemy.
        # self.show_both_img()
        # self.set_hist(tmp=1)

        # plt.plot(cdf_normalized, color='b')
        # plt.hist(self.cvImage.flatten(), 256, [0, 256], color='r')
        # plt.xlim([0, 256])
        # plt.legend(('cdf', 'histogram'), loc='upper left')
        # plt.show()

    def hist_eq(self):
        self.cvImage_tmp = cv2.equalizeHist(self.cvImage.current())
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)

    def hist_CLAHE(self, x=8, y=8):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(x, y))
        self.cvImage_tmp = clahe.apply(self.cvImage.current())
        self.tkImage_tmp = self.assign_tkimage(self.cvImage_tmp)

    def save(self, path=None):
        if path is None:
            cv2.imwrite(self.path, self.cvImage.current())
        else:
            cv2.imwrite(path, self.cvImage.current())
