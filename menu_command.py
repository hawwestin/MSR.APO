import matplotlib
import tkinter as tk


import utils

matplotlib.use("TkAgg")

from tkinter import filedialog
from tkinter import simpledialog
import os
from OperationsLinear import adap_prog, histEq, red_poz_sza, prog, UOP, stretching, prog_zach
from OperationsArithmetic.insert_img import InsertImage
from OperationsArithmetic.subtraction import Substraction
from tabpicture import TabColorPicture, TabGreyPicture, TabPicture
from computer_vision import *

LARGE_FONT = utils.LARGE_FONT
NORM_FONT = utils.NORM_FONT
SMALL_FONT = utils.SMALL_FONT


class MenuCmd:
    """
    Class to communicate Main Menu with tab windows to perform desired actions on images inside.

    """

    def __init__(self, main_window: tk.Tk):
        self.main_window = main_window

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
        print(tab_id)
        return TabPicture.gallery.get(tab_id, None)

    def _open_img(self, color=True):
        """
        Init new tab of color or gray image.

        In future create dict of supported images.
        :param color: bool
        :return:
        """
        path = filedialog.askopenfilename()
        if len(path) > 0:
            name = tk.StringVar()
            name.set(os.path.split(path)[1])
            tab_frame = self.main_window.new_tab(name.get())
            if color is True:
                tab_pic = TabColorPicture(tab_frame, self.main_window, name)
            else:
                tab_pic = TabGreyPicture(tab_frame, self.main_window, name)

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
        if tab.vision.color == 1:
            tab_pic = TabColorPicture(tab_frame, self.main_window, name)
        else:
            tab_pic = TabGreyPicture(tab_frame, self.main_window, name)

        tab_pic.open_image(tab.vision.path)
        tab_pic.refresh()


    def open_color_image(self):
        self._open_img(True)

    def open_grey_image(self):
        self._open_img(False)

    def load_image(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            tab = self._current_tab()
            tab.vision.path = path
            if tab.vision.color == 1:
                self._open_img(color=True)
            else:
                self._open_img(color=False)
            self.main_window.rename_tab(os.path.splitext(path)[0])

            tab.refresh()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Info")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=msg, font=NORM_FONT, justify=tk.CENTER)
        label.pack(pady=20, padx=20)
        B1 = ttk.Button(popup, text="ok", command=popup.destroy)
        B1.pack(side=tk.BOTTOM, pady=20)
        popup.mainloop()

    def imgList(self):
        print(self.main_window.notebook.index("current"))
        print(self.main_window.notebook.index("end"))
        print(self.main_window.notebook.tab(self.main_window.notebook.index("current")))
        print(self.main_window.notebook.tabs())
        print(self.main_window.notebook.select())

    def inHist(self):
        tab = self._current_tab()
        tab.histogram(tab.vision.cvImage.image)

    def outHist(self):
        self._current_tab().show_hist()

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016/2017")

    def picker(self):
        tab_id = self.main_window.notebook.select()
        print(tab_id)
        # id = self.main_window.notebook.index("current")
        TabPicture.gallery[tab_id].vision.color_picker()

    def hist_Equ(self):
        tab = self._current_tab()
        histEq.OperationHistEQ(tab)

    def save(self):
        tab = self._current_tab()
        tab.vision.save()

    def save_as(self):
        tab = self._current_tab()
        path = filedialog.asksaveasfilename()
        tab.vision.save(path)

    def negation(self):
        tab = self._current_tab()
        tab.vision.negation()
        tab.refresh()

    def light_threshold(self):
        """
        Progowanie
        :return:
        """
        tab = self._current_tab()
        prog.OperationLightThreshold(tab)

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
        tab.vision.tkImage = Vision.resize_tk_image(tab.vision.cvImage.image, tab.size)
        tab.refresh()

    def redo_image(self):
        tab = self._current_tab()
        tab.vision.cvImage.redo(self.main_window.status_message)
        tab.vision.tkImage = Vision.resize_tk_image(tab.vision.cvImage.image, tab.size)
        tab.refresh()

    def new_img(self):
        path = filedialog.asksaveasfilename()
        name = tk.StringVar()
        name.set("New.jpg")
        tab_frame = self.main_window.new_tab(name.get())
        tab_pic = TabGreyPicture(tab_frame, self.main_window, name)
        tab_pic.vision.new_rand_img()
        tab_pic.vision.path = path
        # tab_pic.open_image(path)
        tab_pic.refresh()

    def stretching(self):
        tab = self._current_tab()
        stretching.OperationStretching(tab)

    def progowanie_z_zachowaniem(self):
        tab = self._current_tab()
        prog_zach.OperationLightThresholdKeepingValue(tab)

    def add_img(self):
        tab = self._current_tab()
        InsertImage(tab)

    def sub_img(self):
        tab = self._current_tab()
        Substraction(tab)

