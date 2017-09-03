import matplotlib

import main_gui

matplotlib.use("TkAgg")
# from tkinter import *
from tkinter import filedialog
import os
from Operations import adap_prog, histEq, red_poz_sza, prog
from tabpicture import TabColorPicture, TabGreyPicture
from computer_vision import *

LARGE_FONT = main_gui.LARGE_FONT
NORM_FONT = main_gui.NORM_FONT
SMALL_FONT = main_gui.SMALL_FONT


class MenuCmd(tk.Frame):
    """
    Class to communicate Main Menu with tab windows to perform desired actions on images inside.



    """

    def __init__(self, parentFrame, tkController):
        tk.Frame.__init__(self, parentFrame)
        self.tkController = tkController

    @staticmethod
    def client_exit():
        exit()

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
                pic = TabColorPicture(tab_frame, self.tkController, name)
            else:
                pic = TabGreyPicture(tab_frame, self.tkController, name)

            pic.open_image(path)
            main_gui.add_img(tab_frame._w, pic.vision)

            pic.vision.set_panel_img()

    def open_color_image(self):
        self._open_img(True)

    def open_grey_image(self):
        self._open_img(False)

    def load_image(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            tab_id = self.tkController.notebook.select()
            print(tab_id)
            main_gui.gallery[tab_id].path = path
            if main_gui.gallery[tab_id].color == 1:
                self._open_img(color=True)
            else:
                self._open_img(color=False)

            tab_id = self.tkController.notebook.select()
            self.tkController.rename_tab(os.path.splitext(path)[0])

            main_gui.gallery[tab_id].set_panel_img()

            if main_gui.gallery[tab_id].histCanvas is not None:
                main_gui.gallery[tab_id].set_hist()
                main_gui.gallery[tab_id].set_hist_geometry()


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
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].set_hist()
        main_gui.gallery[tab_id].set_hist_geometry()

    def outHist(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].show_hist()

    def info(self):
        self.popupmsg("APO Made by\nMichał Robaszewski\n2016/2017")

    def picker(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].color_picker()

    def hist_Equ(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        histEq.Hist_Equalization(tab_id)

    def save(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)

        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].save()

    def save_as(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        title = filedialog.asksaveasfilename()
        # TODO jakis dialog box do podania ścieżki.
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].save(title)

    def clear_hist(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].close_hist()

    def negacja(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        main_gui.gallery[tab_id].negation()
        main_gui.gallery[tab_id].set_panel_img()
        if main_gui.gallery[tab_id].histCanvas is not None:
            main_gui.gallery[tab_id].set_hist()

    def progowanie(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        prog.progowanie(tab_id)

    def adap_progowanie(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # tab_id = self.tkController.notebook.index("current")
        adap_prog.progowanie(tab_id)

    def redukcja_p_s(self):
        tab_id = self.tkController.notebook.select()
        print(tab_id)
        # id = self.tkController.notebook.index("current")
        red_poz_sza.rps(tab_id)
        # MainGui.gallery[tab_id].rps()
        # MainGui.gallery[tab_id].set_panel_img()
        # if MainGui.gallery[tab_id].histCanvas is not None:
        #     MainGui.gallery[tab_id].set_hist()
