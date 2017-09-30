import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import utils
from computer_vision import Vision

matplotlib.use("TkAgg")


class TabPicture:
    """
    Kompozycja obiektów Vision przechowujących obrazy do operacji.

    In feature main control of tkinter tab displaying images and other data.
    """
    gallery = {}

    def __init__(self, tab_frame, main_window, name):
        self.tab_frame = tab_frame
        self.main_window = main_window

        """
        Master Key must match menu_command _current tab politics
        """
        self.id = tab_frame._w

        # tk.StrinVar()
        self.name = name
        # ImageTK.PhotoImage
        self.tkImage = None

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

    def set_hist(self, tmp=None):
        # todo how close histogram ?

        if tmp is None:
            source = self.vision.cvImage
            self.close_hist()
            # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])

            self.fig_subplot.hist(source.ravel(), bins=256, range=[0.0, 256.0])
            self.fig_subplot.set_xlim([0, 256])

        else:
            self.close_hist()
            # histr = cv2.calcHist([self.cvImage], [0], None, [256], [0, 256])

            self.fig_subplot.hist(self.vision.cvImage_tmp.ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
            self.fig_subplot.hist(self.vision.cvImage.ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
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

    def set_hist_geometry(self):
        # self.histCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # self.histCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_for_Canvas.pack(side=tk.RIGHT, expand=True)

    def show_hist(self):
        """
        Wyswietlenie histogramu dla danego okna. zachowanie Mathplota
        zostawic . wyswietlanie dodatkowych ekranow z wykozystaniem tego

        :return:
        """
        # todo wyczyszczenie grafu przed zaladowaniem kolejnego , jak zaladowac kilka instancji do kilku obrazkow ?
        plt.hist(self.vision.cvImage.ravel(), 256, [0, 255])
        plt.show()

    def close_hist(self):
        self.fig_subplot.clear()

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
            self.panel = ttk.Label(self.tab_frame, image=self.vision.tkImage)
            # self.panel.configure(image=self.tkImage)
            # self.panel.image = self.tkImage
            self.panel.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            self.panel.configure(image=self.vision.tkImage)
            self.panel.image = self.vision.tkImage

        if self.panel_tmp is None and self.vision.tkImage_tmp is not None:
            self.panel_tmp = ttk.Label(self.tab_frame, image=self.vision.tkImage_tmp)
            # self.panel.configure(image=self.tkImage)
            # self.panel.image = self.tkImage
            self.panel_tmp.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        elif self.panel_tmp is not None:
            self.panel_tmp.configure(image=self.vision.tkImage_tmp)
            self.panel_tmp.image = self.vision.tkImage_tmp

    def show_both_img(self):
        if self.panel_tmp is None or self.panel is None:
            self.panel_tmp = ttk.Label(self.tab_frame,
                                       image=self.vision.tkImage_tmp)
            self.panel_tmp.image = self.vision.tkImage_tmp
            self.panel_tmp.pack(side="left", padx=10, pady=10)

            self.panel = ttk.Label(self.tab_frame, image=self.vision.tkImage)
            self.panel.image = self.vision.tkImage
            self.panel.pack(side="left")

        # otherwise, update the image panels
        else:
            # update the pannels
            self.panel_tmp.configure(image=self.vision.tkImage_tmp)
            self.panel.configure(image=self.vision.tkImage)
            self.panel_tmp.image = self.vision.tkImage_tmp
            self.panel.image = self.vision.tkImage
            # self.panel.image = self.tkImage_tmp



class TabColorPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 1


class TabGreyPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 0
