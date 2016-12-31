from matplotlib import pyplot as plt
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from ComputerVision import Vision
import numpy as np
import cv2
# Panel is a box to display an image
panelA = None
panelB = None
# images = None
statusmsg = None

canvas = None
toolbar = None
gallery = {}
#current working tab
cwt = None

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def add_img(tab, img):
    """

    :param img:  Vision(frame, controller, path)
    :return:
    """
    global cwt
    global gallery

    # frame = Vision(frame, controller, path)

    # if gallery.__len__() is 0:
    #     cwt = 0
    # else:
    #     cwt = sorted(gallery)[-1] + 1
    # # print("\nitem : %d" % cwi)

    gallery[tab] = img

    # zapychacz
    cwt = 0
    return cwt

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


def Hist_Equalization(tab_id):
    """
    """
    # Tab numer with Image to load and wher save to
    global gallery

    popup = tk.Toplevel()
    popup.wm_title("Histogram Equalization")
    # popup.geometry("240x180")

    container = tk.Frame(master=popup)
    container.pack()

    huk = Vision(parent=container, controller=popup)

    # huk.tkImage = gallery[tab_id].tkImage
    # huk.cvImage = gallery[tab_id].cvImage
    huk.open_grey_scale_img(gallery[tab_id].path)
    # huk.assign_tkimage()
    # huk.show()
    huk.show_img()
    huk.load_hist()

    # img = cv2.imread('wiki.jpg', 0)
    huk.cvImage_tmp = cv2.equalizeHist(huk.cvImage)
    res = np.hstack((huk.cvImage, huk.cvImage_tmp))  # stacking images side-by-side
    cv2.imwrite('res.png', res)

    huk.show_tmp_img()

    label = ttk.Label(container, text="aaa", font=NORM_FONT)
    label.pack(pady=20, padx=20)
    B1 = ttk.Button(container, text="Odrzuć zmiany", command=popup.destroy)
    B1.pack(side=tk.BOTTOM, pady=20)
    popup.mainloop()
