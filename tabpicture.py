import tkinter as tk
import cv2
import os

import main_gui
from computer_vision import Vision


class TabPicture:
    gallery = {}

    def __init__(self, tab_frame, main_window, name):
        self.tab_frame = tab_frame
        self.main_window = main_window

        self.id = tab_frame._w

        # tk.StrinVar()
        self.name = name
        # ImageTK.PhotoImage
        self.tkImage = None

        self.vision = Vision(tab_frame, main_window)

        TabPicture.gallery[self.id] = self

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
            main_gui.status_message.set("nie podano pliku")


class TabColorPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 1


class TabGreyPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)
        self.vision.color = 0
