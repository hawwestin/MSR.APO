import utils
import tkinter as tk
import cv2
from tkinter import ttk
from computer_vision import Vision
from tabpicture import TabPicture


def rps(tab: TabPicture):
    """
    Tab numer with Image to load and wher save to
    """
    popup = tk.Toplevel()
    popup.wm_title("Redukcja poziomow szarosci")
    popup.geometry("1024x768")

    container = tk.Frame(master=popup)
    container.grid()
    # tk.Grid.rowconfigure(popup, 0, weight=1)
    # tk.Grid.columnconfigure(popup, 0, weight=1)

    # TODO jezeli wybrana to opcje z kolorowego obrazka powinna byc informacja ze nastapi konwersja na szary .
    # jezeli ktos sie nie zgodzi to zamyka okno.

    huk = Vision(parent=container, controller=popup)
    huk.frame_for_Canvas = tk.Frame(master=popup)
    huk.frame_for_Canvas.grid(row=4, column=5, columnspan=5, rowspan=2, sticky='nsew', padx=10)

    labelframe = tk.LabelFrame(popup, text="Original", labelanchor='nw')
    labelframe.grid(row=4, column=0, columnspan=4, sticky='nsew', ipadx=0, ipady=0)

    labelframe_tmp = tk.LabelFrame(popup, text="Equalised", labelanchor='nw')
    labelframe_tmp.grid(row=5, column=0, columnspan=4, sticky='nsew')

    ###
    # Init Panel of Vision Huk .
    ###
    huk.panel = tk.Label(labelframe)
    huk.panel.grid(sticky='nsew')
    huk.panel_tmp = tk.Label(labelframe_tmp)
    huk.panel_tmp.grid(sticky='nsew')

    huk.cvImage = tab.vision.cvImage
    huk.tkImage = tab.vision.tkImage
    huk.set_panel_img()

    label = ttk.Label(popup, text="Redukcja poziomów szarości", font=utils.NORM_FONT)
    label.grid(row=2, column=5, sticky='nsew')

    B1 = ttk.Button(popup, text="Wyjdź", command=popup.destroy)
    B1.grid(row=1, column=0, sticky='nsew')
    B2 = ttk.Button(popup, text="Zatwierdz zmiany", command=lambda: utils.confirm(tab, huk))
    B2.grid(row=1, column=1, sticky='nsew')
    B3 = ttk.Button(popup, text="Zapisz i wyjdz", command=lambda: utils.confirm(tab, huk, popup))
    B3.grid(row=1, column=2, sticky='nsew')
    B4 = ttk.Button(popup, text="Cofnij", command=lambda: utils.cofnij(tab, huk))
    B4.grid(row=1, column=3, sticky='nsew')

    B5 = ttk.Button(popup, text="odświerz histogram", command=lambda: huk.set_hist(tmp=1))
    B5.grid(row=0, column=0, sticky='nsew')

    slider = tk.Frame(popup)
    slider.grid(row=2, column=0, columnspan=4, sticky='nsew')

    sl = tk.Scale(slider, orient=tk.HORIZONTAL, from_=1, to=255, length=300)
    sl.configure(command=lambda x: huk.rps(int(x)))
    sl.pack(expand=1)

    popup.mainloop()
