import tkinter as tk
import cv2
import os

from computer_vision import Vision

# Store the next available id for all new images
last_id = 0


class TabPicture:
    all_pictures = []

    def __init__(self, tab_frame, main_window, name):
        global last_id
        self.id = last_id
        last_id += 1
        self.name = name
        self.path = ""
        self.vision = Vision(tab_frame, main_window)

        TabPicture.all_pictures.append(self)

    def match(self, what):
        '''
        Determine if this note matches the filter text.
        Return true if it matches, False otherwise.

        Search is case sensitive and matches both name and id.
        :param what:
        :return:
        '''
        return what in self.id or what in self.name.get()

    def search(self, finder):
        '''
        Find vison object in visions list
        :param finder:
        :return:
        '''
        return [tab for tab in TabPicture.all_pictures if tab.match(finder)]

    def open_image(self, path):
        '''
        Save copy of opened image for further usage.
        :param path:
        :return:
        '''
        self.path = path
        if len(path) > 0:
            self.vision.path = self.path #todo refactor vision to drop that internal value.

    def save(self, path=None):
        if path is None:
            cv2.imwrite(self.path, self.vision.cvImage)
        else:
            cv2.imwrite(path, self.vision.cvImage)


class TabColorPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)

    def open_image(self, path):
        super().open_image(path)

        self.vision.open_image(color=True)

        # self.cvImage = cv2.imread(self.path, cv2.IMREAD_COLOR)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # image = Image.fromarray(image)
        # self.tkImage = ImageTk.PhotoImage(image)


class TabGreyPicture(TabPicture):
    def __init__(self, tab_frame, main_window, name):
        super().__init__(tab_frame, main_window, name)

    def open_image(self, path):
        super().open_image(path)
        self.vision.open_image(color=False)
