

from ComputerVision import Vision
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


def add_img(img):
    """

    :param img:  Vision(frame, controller, path)
    :return:
    """
    global cwt
    global gallery

    # frame = Vision(frame, controller, path)

    if gallery.__len__() is 0:
        cwt = 0
    else:
        cwt = sorted(gallery)[-1] + 1
    # print("\nitem : %d" % cwi)
    gallery[cwt] = img

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
