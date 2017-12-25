import tkinter as tk
import os

import matplotlib

from gui.operations.filters import filter, smoothing
from gui.operations.OperationsArithmetic import logic_operations
from gui.operations.OperationsArithmetic import arithmertic_operations
from .operations.OperationsLinear import adap_prog, histEq, red_poz_sza, binary_operation, UOP, two_arg_threshold
from gui.operations.filters import hough
from gui.operations.filters import morphology

import app_config
from .operations.computer_vision import *
from .tabpicture import TabPicture

matplotlib.use("TkAgg")
LARGE_FONT = app_config.LARGE_FONT
NORM_FONT = app_config.NORM_FONT
SMALL_FONT = app_config.SMALL_FONT


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
            return tab.vision.color
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
        path = filedialog.askopenfilename()
        if len(path) > 0:
            name = tk.StringVar()
            name.set(os.path.split(path)[1])
            tab_frame = self.main_window.new_tab(name.get())
            tab_pic = TabPicture(tab_frame, self.main_window, name)
            tab_pic.vision.color = color
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
        tab_pic.vision.color = tab.vision.color
        tab_pic.open_image(tab.vision.path)
        tab_pic.refresh()

    def open_color_image(self):
        self._open_img(True)

    def open_grey_image(self):
        self._open_img(False)

    def reload_image(self):
        tab = self._current_tab()
        if tab.vision.path is None:
            tab.vision.path = filedialog.askopenfilename()

        tab.open_image(tab.vision.path)
        tab.refresh()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Info")
        # popup.geometry("240x180")
        label = tk.Label(popup, text=msg, font=NORM_FONT, justify=tk.CENTER)
        label.pack(pady=20, padx=20)
        b1 = tk.Button(popup, text="ok", command=popup.destroy)
        b1.pack(side=tk.BOTTOM, pady=20)
        popup.mainloop()

    def img_list(self):
        print(self.main_window.notebook.index("current"))
        print(self.main_window.notebook.index("end"))
        print(self.main_window.notebook.tab(self.main_window.notebook.index("current")))
        print(self.main_window.notebook.tabs())
        print(self.main_window.notebook.select())

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016-2018\nVersion {}".format(app_config.__VERSION__))
        # simpledialog.SimpleDialog(master=self.main_window, text="APO Made by\nMichał Robaszewski\n2016/2017")

    def hist_equ(self):
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
        tab_pic = TabPicture(tab_frame, self.main_window, name)
        tab_pic.vision.color = False
        tab_pic.vision.new_rand_img()
        tab_pic.vision.path = path
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
        if tab.vision.color and not color:
            """
            color to gray
            """
            tab.vision.color_convert(False)
            self.main_window.update_status("Image was convert to Gray")
        elif not tab.vision.color and color:
            """
            gray to color
            """
            tab.vision.color_convert(True)
            self.main_window.update_status("Image was convert to RGB")
        else:
            self.main_window.update_status("Color was not changed")

        tab.refresh()
