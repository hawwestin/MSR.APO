import matplotlib

import utils

matplotlib.use("TkAgg")
# from tkinter import *
from tkinter import filedialog
import os
from Operations import adap_prog, histEq, red_poz_sza, prog
from tabpicture import TabColorPicture, TabGreyPicture, TabPicture
from computer_vision import *

LARGE_FONT = utils.LARGE_FONT
NORM_FONT = utils.NORM_FONT
SMALL_FONT = utils.SMALL_FONT


class MenuCmd:
    """
    Class to communicate Main Menu with tab windows to perform desired actions on images inside.

    """

    def __init__(self, tk_controller: tk.Tk):
        self.tkController = tk_controller

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
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        return TabPicture.gallery.get(tab_id, None)

    def _open_img(self, color=True):
        """
        Init new tab of color or gray image.

        In future create dict of supported images.
        :param color: bool
        :return:
        """
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
        path = filedialog.askopenfilename()
        if len(path) > 0:
            name = tk.StringVar()
            name.set(os.path.split(path)[1])
            tab_frame = self.tkController.new_tab(name.get())
            if color is True:
                tab_pic = TabColorPicture(tab_frame, self.tkController, name)
            else:
                tab_pic = TabGreyPicture(tab_frame, self.tkController, name)

            tab_pic.open_image(path)
            tab_pic.set_panel_img()

    def duplicate(self):
        """
        Create duplicate image of current selected Tab.
        Method load image from HDD not copying current state of image.
        :return:
        """
        tab = self._current_tab()

        name = tk.StringVar(value=tab.name.get())
        tab_frame = self.tkController.new_tab(name.get())
        if tab.vision.color == 1:
            tab_pic = TabColorPicture(tab_frame, self.tkController, name)
        else:
            tab_pic = TabGreyPicture(tab_frame, self.tkController, name)

        tab_pic.open_image(tab.vision.path)
        tab_pic.set_panel_img()


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

            tab_id = self.tkController.notebook.select()
            self.tkController.rename_tab(os.path.splitext(path)[0])

            tab.set_panel_img()
            # utils.gallery[tab_id].set_panel_img()
            tab.set_hist()

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
        print(self.tkController.notebook.index("current"))
        print(self.tkController.notebook.index("end"))
        print(self.tkController.notebook.tab(self.tkController.notebook.index("current")))
        print(self.tkController.notebook.tabs())
        print(self.tkController.notebook.select())

    def inHist(self):
        tab = self._current_tab()
        tab.set_hist()

    def outHist(self):
        self._current_tab().show_hist()

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016/2017")

    def picker(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        TabPicture.gallery[tab_id].vision.color_picker()

    def hist_Equ(self):
        tab = self._current_tab()
        histEq.OperationHistEQ(tab)

    def save(self):
        tab = self._current_tab()
        tab.vision.save()

    def save_as(self):
        tab = self._current_tab()
        title = filedialog.asksaveasfilename()
        # TODO jakis dialog box do podania ścieżki.
        tab.vision.save(title)

    def negation(self):
        tab = self._current_tab()
        tab.vision.negation()
        tab.set_panel_img()

    def light_levelling(self):
        """
        Progowanie
        :return:
        """
        tab = self._current_tab()
        prog.progowanie(tab)

    def adaptive_light_levelling(self):
        tab = self._current_tab()
        adap_prog.progowanie(tab)

    def redukcja_p_s(self):
        tab = self._current_tab()
        red_poz_sza.rps(tab)
        # MainGui.gallery[tab_id].rps()
        # MainGui.gallery[tab_id].set_panel_img()
        # if MainGui.gallery[tab_id].histCanvas is not None:
        #     MainGui.gallery[tab_id].set_hist()

    def undo_image(self):
        tab = self._current_tab()
        tab.vision.cvImage.undo()
        tab.vision.tkImage = tab.vision.cvImage.tk_image
        tab.set_panel_img()

    def redo_image(self):
        tab = self._current_tab()
        tab.vision.cvImage.redo()
        tab.vision.tkImage = tab.vision.cvImage.tk_image
        tab.set_panel_img()

