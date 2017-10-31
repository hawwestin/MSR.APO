import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt

import utils
from computer_vision import Vision
from histogram import Histogram

matplotlib.use("TkAgg")


class TabPicture:
    """
    Kompozycja obiektów Vision przechowujących obrazy do operacji.

    In feature main control of tkinter tab displaying images and other data.
    """
    gallery = {}

    def __init__(self, tab_frame: tk.Frame, main_window: tk.Tk, name: tk.StringVar):
        self.tab_frame = tab_frame
        self.main_window = main_window

        """
        Master Key must match menu_command _current tab politics
        """
        self.id = tab_frame._w
        TabPicture.gallery[self.id] = self

        self.name = name

        self.vision = Vision()
        self.size = (500, 600)

        self.tkImage = None

        self.panel = None
        self.panel = ttk.Label(self.tab_frame)
        self.panel.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.panel_hist = tk.Frame(master=tab_frame)
        self.panel_hist.pack(side=tk.RIGHT, expand=True, after=self.panel)
        self.histogram = Histogram(self.panel_hist)

    def __len__(self):
        return TabPicture.gallery.__len__()

    def __del__(self):
        TabPicture.gallery.pop(self.id, None)

    def persist_tmp(self):
        self.vision.cvImage.image = self.vision.cvImage_tmp.image
        self.refresh()

    def match(self, what):
        '''
        Determine if this note matches the filter text.
        Return true if it matches, False otherwise.

        Search is case sensitive and matches both name and id.
        :param what:
        :return:
        '''
        return what == self.id or what in self.name.get()


    @staticmethod
    def search(finder):
        '''
        Find vison object in visions list
        :param finder:
        :return:
        '''
        return [TabPicture.gallery[tab] for tab in TabPicture.gallery.keys()
                if TabPicture.gallery[tab].match(finder)]

    def __contains__(self, item):
        """
        Implement Container abstract method to check if object is in our list.
        :param item:
        :return:
        """
        return len(self.search(item)) > 0

    def open_image(self, path):
        '''
        Save copy of opened image for further usage.
        :param path: image path
        :return:
        '''
        if len(path) > 0:
            self.vision.open_image(path)
        else:
            self.main_window.status_message.set("nie podano pliku")

    def show_hist(self):
        """
        Wyswietlenie histogramu dla danego okna. zachowanie Mathplota
        zostawic . wyswietlanie dodatkowych ekranow z wykozystaniem tego

        :return:
        """
        # wyczyszczenie grafu przed zaladowaniem kolejnego , jak zaladowac kilka instancji do kilku obrazkow ?
        plt.hist(self.vision.cvImage.image.ravel(), 256, [0, 255])
        plt.show()

    def refresh(self):
        self.set_panel_img()
        self.histogram(image=self.vision.cvImage.image)

    def set_panel_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac
        """
        self.tkImage = Vision.resize_tk_image(self.vision.cvImage.image, self.size)
        self.panel.configure(image=self.tkImage)
        self.panel.image = self.tkImage

    def popup_image(self):
        plt.imshow(self.tkImage, cmap='Greys', interpolation='bicubic')
        plt.show()


class TabColorPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 1


class TabGreyPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 0
