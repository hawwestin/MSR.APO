import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt

from gui.histogram import Histogram
from gui.operations.computer_vision import Vision
from gui.image_frame import ImageFrame
import app_config

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
        ###############
        # vars
        ###############
        self.id = tab_frame._w
        TabPicture.gallery[self.id] = self
        self.name = name
        self.tkImage = None
        res = int(app_config.main_window_resolution[:int(app_config.main_window_resolution.index('x'))])/2

        ###############
        # Panels
        ###############
        self.pann = tk.PanedWindow(self.tab_frame, handlesize=10, showhandle=True, handlepad=12, sashwidth=3)
        self.pann.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.pann)
        self.image_frame.pack(expand=True, fill=tk.BOTH)
        self.pann.add(self.image_frame, width=res, minsize=100)
        self.panel_hist = tk.Frame(self.pann)
        self.panel_hist.pack(expand=True, fill=tk.BOTH)
        self.pann.add(self.panel_hist, width=res, minsize=100)

        ###############
        # Class
        ###############
        self.vision = Vision()
        self.histogram = Histogram(self.panel_hist)
        self.image_canvas = ImageFrame(self.image_frame)

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
        self.histogram(image=self.vision.cvImage.image)
        self.set_panel_img()
        self.main_window.main_menu.color_mode()

    def set_panel_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac
        """
        self.image_canvas(self.vision.cvImage.image)

    def popup_image(self):
        plt.imshow(self.tkImage, cmap='Greys', interpolation='bicubic')
        plt.show()
