import MainGui
import tkinter as tk
from tkinter import ttk
from ComputerVision import Vision

def progowanie(tab_id):
    """
    Tab numer with Image to load and wher save to
    """
    popup = tk.Toplevel()
    popup.wm_title("Progowanie")
    popup.geometry("800x400")

    container = tk.Frame(master=popup)
    container.grid()
    # tk.Grid.rowconfigure(popup, 0, weight=1)
    # tk.Grid.columnconfigure(popup, 0, weight=1)

    # TODO jezeli wybrana to opcje z kolorowego obrazka powinna byc informacja ze nastapi konwersja na szary .
    # jezeli ktos sie nie zgodzi to zamyka okno.

    huk = Vision(parent=container, controller=popup)
    huk.fCanvas = tk.Frame(master=popup)
    huk.fCanvas.grid(row=4, column=5, columnspan=5, rowspan=2, sticky='nsew', padx=10)

    labelframe = tk.LabelFrame(popup, text="Original", labelanchor='nw')
    labelframe.grid(row=4, column=0, columnspan=4, sticky='nsew', ipadx=0, ipady=0)

    labelframe_tmp = tk.LabelFrame(popup, text="Equalised", labelanchor='nw')
    labelframe_tmp.grid(row=4, column=5,columnspan=4, sticky='nsew')

    ###
    # Init Panel of Vision Huk .
    ###
    huk.panel = tk.Label(labelframe)
    huk.panel.grid(sticky='nsew')
    huk.panel_tmp = tk.Label(labelframe_tmp)
    huk.panel_tmp.grid(sticky='nsew')

    huk.cvImage = MainGui.gallery[tab_id].cvImage
    huk.tkImage = MainGui.gallery[tab_id].tkImage
    huk.set_panel_img()

    label = ttk.Label(popup, text="Progowanie", font=MainGui.NORM_FONT)
    label.grid(row=1, column=5, sticky='nsew')

    B1 = ttk.Button(popup, text="Wyjdź", command=popup.destroy)
    B1.grid(row=1, column=0, sticky='nsew')
    B2 = ttk.Button(popup, text="Zatwierdz zmiany", command=lambda: MainGui.confirm(tab_id, huk))
    B2.grid(row=1, column=1, sticky='nsew')
    B3 = ttk.Button(popup, text="Zapisz i wyjdz", command=lambda: MainGui.confirm(tab_id, huk, popup))
    B3.grid(row=1, column=2, sticky='nsew')
    B4 = ttk.Button(popup, text="Cofnij", command=lambda: MainGui.cofnij(tab_id, huk))
    B4.grid(row=1, column=3, sticky='nsew')

    slider = tk.Frame(popup)
    slider.grid(row=2, column=0, columnspan=4, sticky='nsew')

    sl = tk.Scale(slider, orient=tk.HORIZONTAL, to=255, length=300)
    sl.configure(command=lambda x: huk.global_prog(float(x)))
    sl.pack(expand=1)

    # B4 = ttk.Button(popup, text="Hist EQ", command=huk.hist_eq)
    # B4.grid(row=0, column=0, sticky='nsew')
    # B5 = ttk.Button(popup, text="Hist num", command=huk.hist_num)
    # B5.grid(row=0, column=1, sticky='nsew')
    # B6 = ttk.Button(popup, text="Sąsiedztwa 3x3", command=lambda: huk.hist_CLAHE(3, 3))
    # B6.grid(row=0, column=2, sticky='nsew')
    # B8 = ttk.Button(popup, text="Sąsiedztwa 8x8", command=lambda: huk.hist_CLAHE(8, 8))
    # B8.grid(row=0, column=3, sticky='nsew')

    popup.mainloop()
