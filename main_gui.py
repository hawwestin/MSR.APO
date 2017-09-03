status_message = None

gallery = {}

LARGE_FONT = ("Verdana", 12)
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
    # print(gallery.keys())


def close_img(tab_id):
    """

    :param tab_id: img index in gallery , Key to pop
    :return:
    """
    global gallery
    gallery.pop(tab_id, None)


def confirm(tab_id, huk, window=None):
    """
    akcja dla operacji wywoływanych z Menu do nadpisanai obrazka przechowywanego
    na wynikowy z operacji
    :param tab_id:
    :param huk:
    :param window:
    :return:
    """
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
    """
    reset image stored in gallery to image with operation was initialize.
    :param tab_id:
    :param huk:
    :return:
    """
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
