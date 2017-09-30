from tabpicture import TabPicture

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


def close_img(tab_id):
    """

    :param tab_id: img index in gallery , Key to pop
    :return:
    """
    global gallery
    gallery.pop(tab_id, None)


def confirm(tab: TabPicture, huk, window=None):
    """
    akcja dla operacji wywoływanych z Menu do nadpisanai obrazka przechowywanego
    na wynikowy z operacji
    :param tab:
    :param huk:
    :param window:
    :return:
    """
    tab.vision.cvImage = huk.cvImage_tmp
    tab.vision.tkImage = huk.tkImage_tmp
    tab.set_panel_img()
    tab.panel.pack(side="left",
                   padx=10,
                   pady=10)

    if tab.histCanvas is not None:
        tab.set_hist()
        tab.set_hist_geometry()
    if window is not None:
        window.destroy()


def cofnij(tab: TabPicture, huk):
    """
    reset image stored in gallery to image with operation was initialize.
    :param tab:
    :param huk:
    :return:
    """
    tab.vision.cvImage = huk.cvImage
    tab.vision.tkImage = huk.tkImage
    tab.set_panel_img()
    tab.panel.pack(side="left",
                   padx=10,
                   pady=10)

    if tab.histCanvas is not None:
        tab.set_hist()
        tab.set_hist_geometry()
