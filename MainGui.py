

from ComputerVision import Vision
# Panel is a box to display an image
panelA = None
panelB = None
# images = None
statusmsg = None

canvas = None
toolbar = None
gallery = {}
#current working image
cwi = None


def add_img(img):
    """

    :param img:  Vision(frame, controller, path)
    :return:
    """
    global cwi
    global gallery

    # frame = Vision(frame, controller, path)

    if gallery.__len__() is 0:
        cwi = 0
    else:
        cwi = sorted(gallery)[-1] + 1
    # print("\nitem : %d" % cwi)
    gallery[cwi] = img

    return cwi


def close_img(img):
    """

    :param img: img index in gallery , Key to pop
    :return:
    """
    global gallery
    gallery.pop(img)
    # item = sorted(self.gallery)[-1] + 1
    # print("\nitem after close : %d"% item)
