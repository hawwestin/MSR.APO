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

    # TODO jezeli wybrana to opcje z kolorowego obrazka powinna byc informacja ze nastapi konwersja na szary .
    # jezeli ktos sie nie zgodzi to zamyka okno.

    huk = Vision(parent=container, controller=popup)
    labelframe = tk.LabelFrame(popup, text="Original", labelanchor='nw')
    labelframe.pack(fill="both", expand="yes", side=tk.LEFT)

    labelframe_tmp = tk.LabelFrame(popup, text="Equalised", labelanchor='nw')
    labelframe_tmp.pack(fill="both", expand="yes", side=tk.LEFT)

    huk.panel = tk.Label(labelframe)
    huk.panel.pack(side=tk.TOP)
    huk.panel_tmp = tk.Label(labelframe_tmp)
    huk.panel_tmp.pack(side=tk.TOP)

    # huk.open_grey_scale_img(gallery[tab_id].path)
    huk.cvImage = gallery[tab_id].cvImage
    huk.tkImage = gallery[tab_id].tkImage

    # huk.load_hist()

    # img = cv2.imread('wiki.jpg', 0)

    # huk.cvImage_tmp = cv2.equalizeHist(huk.cvImage)

    # res = np.hstack((huk.cvImage, huk.cvImage_tmp))  # stacking images side-by-side
    # cv2.imwrite('res.png', res)
    # cv2.imwrite('HE.png', huk.cvImage_tmp)
    # huk.assign_tkimage_tmp()
    #
    # huk.show_both_img()
    # huk.load_hist_tmp()

    def confirm(flag=None):
        gallery[tab_id].cvImage = huk.cvImage_tmp
        gallery[tab_id].tkImage = huk.tkImage_tmp
        gallery[tab_id].show_img()
        if gallery[tab_id].histCanvas is not None:
            gallery[tab_id].set_hist()
            gallery[tab_id].load_hist_geometry().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        if flag is not None:
            popup.destroy()

    def cofnij():
        gallery[tab_id].cvImage = huk.cvImage
        gallery[tab_id].tkImage = huk.tkImage
        gallery[tab_id].show_img()
        if gallery[tab_id].histCanvas is not None:
            gallery[tab_id].set_hist()
            gallery[tab_id].load_hist_geometry().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    label = ttk.Label(container, text="Equalisation Method", font=NORM_FONT)
    label.pack(side=tk.TOP, pady=20, padx=20)

    B1 = ttk.Button(container, text="Wyjdź", command=popup.destroy)
    B1.pack(side=tk.BOTTOM, padx=2)
    B2 = ttk.Button(container, text="Zatwierdz zmiany", command=confirm)
    B2.pack(side=tk.BOTTOM, padx=2)
    B3 = ttk.Button(container, text="Zapisz i wyjdz", command=lambda: confirm(1))
    B3.pack(side=tk.BOTTOM, padx=2)
    B7 = ttk.Button(container, text="Cofnij", command=cofnij)
    B7.pack(side=tk.BOTTOM, padx=2)

    B4 = ttk.Button(container, text="Hist EQ", command=huk.hist_eq)
    B4.pack(side=tk.LEFT, padx=2)
    B5 = ttk.Button(container, text="Hist num", command=huk.hist_num)
    B5.pack(side=tk.LEFT, padx=2)
    B6 = ttk.Button(container, text="Hist Clahe", command=huk.hist_CLAHE)
    B6.pack(side=tk.LEFT, padx=2)

    popup.mainloop()
