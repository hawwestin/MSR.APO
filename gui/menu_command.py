import copy
import logging
import tkinter as tk
import os
from tkinter import filedialog

import matplotlib

from gui.operations.filters import filter, smoothing
from gui.operations.OperationsArithmetic import logic_operations
from gui.operations.OperationsArithmetic import arithmertic_operations
from .operations.OperationsLinear import adap_prog, histEq, red_poz_sza, binary_operation, UOP, two_arg_threshold
from gui.operations.filters import hough
from gui.operations.filters import morphology

import app_config
from .operations.computer_vision import Vision
from .tabpicture import TabPicture
import gui.utilities

matplotlib.use("TkAgg")
LARGE_FONT = app_config.LARGE_FONT
NORM_FONT = app_config.NORM_FONT
SMALL_FONT = app_config.SMALL_FONT
SUPPORTED_FILES = [('jpg', '*.jpg'), ('png', '*.png'), ('bmp', '*.bmp')]


class MenuCmd:
    """
    Class to communicate Main Menu with tab windows to perform desired actions on images inside.

    """

    def __init__(self, main_window):
        self.main_window = main_window

    def color_mode(self) -> bool:
        """
        
        :return: True If Img is in Color 
        """
        tab = self._current_tab()
        if tab is not None:
            return tab.vision.cvImage.color
        else:
            return False

    @staticmethod
    def client_exit():
        exit()

    def _current_tab(self) -> TabPicture:
        """
        Fetch TabPicture object of current selected tab.
        TabPicture dict gallery must have matching keys with value returned by
         ttk.notebook.select() function.
        :return: TabPicture object of current selected tab
        """
        tab_id = self.main_window.notebook.select()
        return TabPicture.gallery.get(tab_id, None)

    def _open_img(self, color=True):
        """
        Init new tab of color or gray image.

        In future create dict of supported images.
        :param color: bool
        :return:
        """
        if app_config.image_path is not None:
            path = filedialog.askopenfilename(initialdir=app_config.image_path, filetypes=SUPPORTED_FILES)
        else:
            path = filedialog.askopenfilename(filetypes=SUPPORTED_FILES)
        if len(path) > 0:
            name = tk.StringVar()
            name.set(os.path.split(path)[1])
            app_config.image_path = os.path.split(path)[0]
            tab_frame = self.main_window.new_tab(name.get())
            tab_pic = TabPicture(tab_frame, self.main_window, name)
            tab_pic.vision.cvImage.color = color
            tab_pic.vision.cvImage.path = path
            tab_pic.open_image(path)
            tab_pic.refresh()

    def duplicate(self):
        """
        Create duplicate image of current selected Tab.
        Method load image from HDD not copying current state of image.
        :return:
        """
        tab = self._current_tab()

        name = tk.StringVar(value=tab.name.get())
        tab_frame = self.main_window.new_tab(name.get())
        tab_pic = TabPicture(tab_frame, self.main_window, name)
        tab_pic.vision.cvImage = tab.vision.cvImage.duplicate()
        tab_pic.vision.cvImage_tmp = tab.vision.cvImage_tmp.duplicate()
        # tab_pic.open_image(tab.vision.cvImage.path)
        tab_pic.refresh()

    def open_color_image(self):
        self._open_img(True)

    def open_grey_image(self):
        self._open_img(False)

    def reload_image(self):
        tab = self._current_tab()
        if tab.vision.cvImage.path is None:
            tab.vision.cvImage.path = filedialog.askopenfilename(initialdir=app_config.image_path,
                                                                 filetypes=SUPPORTED_FILES)

        tab.open_image(tab.vision.cvImage.path)
        tab.refresh()

    def refresh_image(self):
        tab = self._current_tab()
        tab.refresh()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def info(self):
        msg = "APO\n\nAutor\nMichał Robaszewski\n\nProwadzący\ndr inż. Marek Doros\n\nAlgorytmu przetwarzania obrazów " \
              "2016-2018\n\nWersja programu {}".format(app_config.__VERSION__)
        gui.utilities.popup_message_box(msg)
        # simpledialog.SimpleDialog(master=self.main_window, text="APO Made by\nMichał Robaszewski\n2016/2017")

    def hist_equ(self):
        tab = self._current_tab()
        histEq.OperationHistEQ(tab)

    def save(self):
        tab = self._current_tab()
        tab.vision.save()

    def save_as(self):
        tab = self._current_tab()
        path = filedialog.asksaveasfilename(initialdir=app_config.image_path)
        if path != '':
            tab.vision.save(path)

    def negation(self):
        tab = self._current_tab()
        try:
            tab.vision.negation()
        except Exception as ex:
            logging.exception(ex)
            self.main_window.update_status("Operation have Failed check given options!")
        tab.refresh()

    def light_threshold(self):
        """
        Progowanie
        :return:
        """
        tab = self._current_tab()
        binary_operation.OperationLightThreshold(tab)

    def adaptive_light_threshold(self):
        tab = self._current_tab()
        adap_prog.OperationAdaptiveThreshold(tab)

    def redukcja_p_s(self):
        tab = self._current_tab()
        red_poz_sza.OperationLightLeveling(tab)

    def uop(self):
        tab = self._current_tab()
        UOP.UOPOperation(tab)

    def undo_image(self):
        tab = self._current_tab()
        tab.vision.cvImage.undo(self.main_window.status_message)
        # tab.vision.tkImage = tab.vision.cvImage.tk_image
        tab.refresh()

    def redo_image(self):
        tab = self._current_tab()
        tab.vision.cvImage.redo(self.main_window.status_message)
        # tab.vision.tkImage = tab.vision.cvImage.tk_image
        # tab.vision.tkImage = Vision.resize_tk_image(tab.vision.cvImage.image, tab.size)
        tab.refresh()

    def new_img(self):
        # path = filedialog.asksaveasfilename()
        name = tk.StringVar()
        name.set("New.jpg")
        tab_frame = self.main_window.new_tab(name.get())
        tab_pic = TabPicture(tab_frame, self.main_window, name)
        tab_pic.vision.cvImage.color = False
        tab_pic.vision.new_rand_img()
        # tab_pic.vision.path = path
        # tab_pic.open_image(path)
        tab_pic.refresh()

    def progowanie_z_zachowaniem(self):
        tab = self._current_tab()
        two_arg_threshold.TwoArgLightThreshold(tab)

    def logic_all(self):
        tab = self._current_tab()
        logic_operations.LogicOperations(tab)

    def filter(self):
        tab = self._current_tab()
        filter.Filter(tab)

    def smooth(self):
        tab = self._current_tab()
        smoothing.Smoothing(tab)

    def arithmetics(self):
        tab = self._current_tab()
        arithmertic_operations.ArithmeticOperations(tab)

    def hough(self):
        tab = self._current_tab()
        hough.Hough(tab)

    def morphologic(self):
        tab = self._current_tab()
        morphology.Morphology(tab)

    def gray_2_rgb(self):
        self._color_convert(True)

    def rgb_2_gray(self):
        self._color_convert(False)

    def _color_convert(self, color):
        tab = self._current_tab()
        if tab.vision.cvImage.color and not color:
            """
            color to gray
            """
            tab.vision.color_convert(False)
            self.main_window.update_status("Image was convert to Gray")
        elif not tab.vision.cvImage.color and color:
            """
            gray to color
            """
            tab.vision.color_convert(True)
            self.main_window.update_status("Image was convert to RGB")
        else:
            self.main_window.update_status("Color was not changed")

        self.main_window.main_menu.color_mode()
        tab.refresh()
