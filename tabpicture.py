import tkinter as tk
from queue import LifoQueue
from tkinter import ttk

import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import utils
from computer_vision import Vision
from repeater import Repeater

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

        # tk.StrinVar()
        self.name = name

        self.vision = Vision(tab_frame, main_window)

        TabPicture.gallery[self.id] = self

        self.panel = None
        self.panel_tmp = None
        self.display = tk.Canvas(tab_frame, bd=0, highlightthickness=0)
        self.frame_for_Canvas = tk.Frame(master=tab_frame)
        self.histCanvas = None
        self.toolbar = None
        self.f = Figure()
        self.fig_subplot = self.f.add_subplot(111)

    def __len__(self):
        return TabPicture.gallery.__len__()

    def __del__(self):
        TabPicture.gallery.pop(self.id, None)

    def persist_tmp(self):
        self.vision.cvImage.update(self.vision.cvImage_tmp)
        self.vision.tkImage = self.vision.cvImage.tk_image
        self.set_panel_img()

    def confirm(self, huk: Vision, window=None):
        """
        akcja dla operacji wywoływanych z Menu do nadpisanai obrazka przechowywanego
        na wynikowy z operacji
        :param huk:
        :param window:
        :return:
        """
        self.vision.cvImage.update(huk.cvImage_tmp)
        self.vision.tkImage = self.vision.cvImage.tk_image
        self.set_panel_img()
        self.panel.pack(side="left",
                        padx=10,
                        pady=10)

        if self.histCanvas is not None:
            self.set_hist()
        if window is not None:
            window.destroy()

    def cofnij(self, huk: Vision):
        """
        reset image stored in gallery to image with operation was initialize.
        :param tab:
        :param huk:
        :return:
        """
        self.vision.cvImage.update(huk.cvImage.current())
        self.vision.tkImage = self.vision.cvImage.tk_image
        self.set_panel_img()
        self.panel.pack(side="left",
                        padx=10,
                        pady=10)

        if self.histCanvas is not None:
            self.set_hist()

    def match(self, what):
        '''
        Determine if this note matches the filter text.
        Return true if it matches, False otherwise.

        Search is case sensitive and matches both name and id.
        :param what:
        :return:
        '''
        return what == self.id or what in self.name.get()

    def search(self, finder):
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
            utils.status_message.set("nie podano pliku")

    def set_hist(self):
        self.fig_subplot.clear()
        # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])

        self.fig_subplot.hist(self.vision.cvImage.current().ravel(), bins=256, range=[0.0, 256.0])
        self.fig_subplot.set_xlim([0, 256])

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.f, self.frame_for_Canvas)
        self.histCanvas.show()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas, self.frame_for_Canvas)
        self.toolbar.update()

        self.histCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_for_Canvas.pack(side=tk.RIGHT, expand=True)

    def show_hist(self):
        """
        Wyswietlenie histogramu dla danego okna. zachowanie Mathplota
        zostawic . wyswietlanie dodatkowych ekranow z wykozystaniem tego

        :return:
        """
        # todo wyczyszczenie grafu przed zaladowaniem kolejnego , jak zaladowac kilka instancji do kilku obrazkow ?
        plt.hist(self.vision.cvImage.current().ravel(), 256, [0, 255])
        plt.show()

    def close_hist(self):
        self.fig_subplot.clear()
        self.frame_for_Canvas.destroy()

    def set_panel_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac
        """
        if self.panel is None:
            self.panel = ttk.Label(self.tab_frame, image=self.vision.tkImage)
            self.panel.pack(side="left", padx=10, pady=10)
        self.panel.configure(image=self.vision.tkImage)
        self.panel.image = self.vision.tkImage

        self.set_hist()

    def popup_image(self):
        plt.imshow(self.vision.tkImage, cmap='Greys', interpolation='bicubic')
        plt.show()


class TabColorPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 1


class TabGreyPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 0
