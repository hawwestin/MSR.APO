import MainGui
import tkinter as tk
from tkinter import ttk
from ComputerVision import Vision

def Hist_Equalization(tab_id):
    """
    """
    # Tab numer with Image to load and wher save to

    popup = tk.Toplevel()
    popup.wm_title("Histogram Equalization")
    popup.geometry("1024x720")

    container = tk.Frame(master=popup)
    # container.pack()
    container.grid()
    # tk.Grid.rowconfigure(popup, 0, weight=1)
    # tk.Grid.columnconfigure(popup, 0, weight=1)

    # TODO jezeli wybrana to opcje z kolorowego obrazka powinna byc informacja ze nastapi konwersja na szary .
    # jezeli ktos sie nie zgodzi to zamyka okno.

    huk = Vision(parent=container, controller=popup)
    huk.frame_for_Canvas = tk.Frame(master=popup)
    huk.frame_for_Canvas.grid(row=4, column=5, columnspan=5, rowspan=2, sticky='nsew', padx=10)

    labelframe = tk.LabelFrame(popup, text="Original", labelanchor='nw')
    # labelframe.pack(fill="both", expand="yes", side=tk.LEFT)
    labelframe.grid(row=4, column=0, columnspan=4, sticky='nsew', ipadx=0, ipady=0)

    labelframe_tmp = tk.LabelFrame(popup, text="Equalised", labelanchor='nw')
    # labelframe_tmp.pack(fill="both", expand="yes", side=tk.LEFT)
    labelframe_tmp.grid(row=5, column=0,columnspan=4, sticky='nsew')

    huk.panel = tk.Label(labelframe)
    huk.panel.grid(sticky='nsew')
    huk.panel_tmp = tk.Label(labelframe_tmp)
    huk.panel_tmp.grid(sticky='nsew')

    # huk.open_grey_scale_img(gallery[tab_id].path)
    huk.cvImage = MainGui.gallery[tab_id].cvImage
    huk.tkImage = MainGui.gallery[tab_id].tkImage
    huk.set_panel_img()

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

    label = ttk.Label(popup, text="Equalisation Method", font=MainGui.NORM_FONT)
    # label.pack(side=tk.TOP, pady=20, padx=20)
    label.grid(row=0, column=5, sticky='nsew')

    B1 = ttk.Button(popup, text="Wyjdź", command=popup.destroy)
    # B1.pack(side=tk.BOTTOM, padx=2)
    B1.grid(row=1, column=0, sticky='nsew')
    B2 = ttk.Button(popup, text="Zatwierdz zmiany", command=lambda: MainGui.confirm(tab_id, huk))
    # B2.pack(side=tk.BOTTOM, padx=2)
    B2.grid(row=1, column=1, sticky='nsew')
    B3 = ttk.Button(popup, text="Zapisz i wyjdz", command=lambda: MainGui.confirm(tab_id, huk, popup))
    # B3.pack(side=tk.BOTTOM, padx=2)
    B3.grid(row=1, column=2, sticky='nsew')
    B7 = ttk.Button(popup, text="Cofnij", command=lambda: MainGui.cofnij(tab_id, huk))
    # B7.pack(side=tk.BOTTOM, padx=2)
    B7.grid(row=1, column=3, sticky='nsew')

    def he():
        huk.hist_eq()
        # w, h = labelframe.winfo_width(), labelframe.winfo_height()
        # print(w, h)
        # w, h = labelframe_tmp.winfo_width(), labelframe_tmp.winfo_height()
        # print(w, h)
        # huk.set_geometry_hist_frame().grid(row=5, column=5)

    def hn():
        huk.hist_num()
        # huk.set_geometry_hist_frame().grid(row=4, column=2)

    B4 = ttk.Button(popup, text="Hist EQ", command=huk.hist_eq)
    # B4.pack(side=tk.LEFT, padx=2)
    B4.grid(row=0, column=0, sticky='nsew')
    B5 = ttk.Button(popup, text="Hist num", command=huk.hist_num)
    # B5.pack(side=tk.LEFT, padx=2)
    B5.grid(row=0, column=1, sticky='nsew')
    B6 = ttk.Button(popup, text="Sąsiedztwa 3x3", command=lambda: huk.hist_CLAHE(3, 3))
    # B6.pack(side=tk.LEFT, padx=2)
    B6.grid(row=0, column=2, sticky='nsew')
    B8 = ttk.Button(popup, text="Sąsiedztwa 8x8", command=lambda: huk.hist_CLAHE(8, 8))
    # B6.pack(side=tk.LEFT, padx=2)
    B8.grid(row=0, column=3, sticky='nsew')

    # w, h = labelframe.winfo_width(), labelframe.winfo_height()
    # print("w i h", w,h)
    # huk.resize(w, h)

    # labelframe.bind("<Configure>", huk.resize_event)

    popup.mainloop()
