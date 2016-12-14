import cv2
from tkinter import *
import numpy as np
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt




class Vision:
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self, ):
        self.cvImage = None
        self.tkImage = None


    def open_img(self, path):
        # 0 - gray , 1 color
        self.cvImage = cv2.imread(path, 1)
        # cv2.cvtColor(self.tkImage, cv2.COLOR_BGR2RGB, self.cvImage)
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.tkImage = ImageTk.PhotoImage(image)



    def show(self):
        img = cv2.imread('Auto_3.jpg', cv2.IMREAD_COLOR)

        # img = cv2.cv2.imread('Auto_3.jpg',cv2.cv2.IMREAD_COLOR)
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        plt.imshow(img, cmap='Greys', interpolation='bicubic')
        plt.show()

    def show_hist(self):
        """
                Wyswietlenie histogramu dla danego okna. zachowanie Mathplota
                zostawic . wyswietlanie dodatkowych ekranow z wykozystaniem tego

                :return:
                """
        plt.hist(self.cvImage.ravel(), 256, [0, 256])
        plt.show()


    def color_convertion(self, img):
        """
        chalupnicza nie wydajna metoda do conversji obrazow

        :param img:
        :return:
        """
        # Rearrang the color channel
        b, g, r = cv2.split(img) # not optimal TODO change to numpay array
        return cv2.merge((r, g, b))