from matplotlib import pyplot as plt
from tkinter import filedialog
import numpy as np
import cv2
# Panel is a box to display an image
# panelA = None
# panelB = None
# images = None
status_message = None

# canvas = None
# toolbar = None

gallery = {}

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def add_img(tab, img):
    """

    :param tab:  value of tkController.notebook.select() for that new tab. its frame._w
    :param img:  Vision(frame, controller, path)
    :return:
    """
    global gallery
    gallery[tab] = img

def close_img(img):
    """

    :param img: img index in gallery , Key to pop
    :return:
    """
    global gallery
    gallery.pop(img)
    # item = sorted(self.gallery)[-1] + 1
    # print("\nitem after close : %d"% item)


def get_path():
    # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
    # todo path do obrazka powinien byc storowany by moc go zapisac
    return filedialog.askopenfilename()


def confirm(tab_id, huk, window=None):
    global gallery

    gallery[tab_id].cvImage = huk.cvImage_tmp
    gallery[tab_id].tkImage = huk.tkImage_tmp
    gallery[tab_id].set_panel_img()
    gallery[tab_id].panel.pack(side="left",
                               padx=10,
                               pady=10)

    if gallery[tab_id].histCanvas is not None:
        gallery[tab_id].set_hist()
        gallery[tab_id].set_hist_geometry()
    if window is not None:
        window.destroy()


def cofnij(tab_id, huk):
    global gallery

    gallery[tab_id].cvImage = huk.cvImage
    gallery[tab_id].tkImage = huk.tkImage
    gallery[tab_id].set_panel_img()
    gallery[tab_id].panel.pack(side="left",
                               padx=10,
                               pady=10)

    if gallery[tab_id].histCanvas is not None:
        gallery[tab_id].set_hist()
        gallery[tab_id].set_hist_geometry()


