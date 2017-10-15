from repeater import Repeater

from cv2 import *
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk

colors = {"COLOR": 1,
          "GREY": 0}

supported_ext = [
    ".jpg",
    ".png"
]


class ImageData(Repeater):
    def calculate_hist(self):
        return cv2.calcHist([self.current()], [0], None, [256], [0, 256])
    pass


class Vision:
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.path = None
        self.color = None

        # Actual
        self.cvImage = ImageData()
        self.tkImage = None
        # temp
        self.size = None
        self.cvImage_tmp = None
        self.tkImage_tmp = None
        self.id = None
        # ToDO po tym resize nie widac histogramu po prawej stronie.
        # parent.bind("<Configure>", self.resize)
        # Bad Idea Dont do that again
        # self.fCanvas.bind("<Configure>", self.resize)

    def open_image(self, path):
        self.path = path
        if self.color is cv2.IMREAD_COLOR:
            self.cvImage.update(cv2.imread(self.path, cv2.IMREAD_COLOR))
            self.cvImage.update(cv2.cvtColor(self.cvImage.current(), cv2.COLOR_BGR2RGB))
        else:
            self.cvImage.update(cv2.imread(self.path, cv2.IMREAD_GRAYSCALE))

        self.tkImage = self.prepare_tk_image(self.cvImage.current())

    def prepare_tk_image(self, image):
        return Vision.resize_tk_image(image, self.size)

    ################################

    # def show(self):
    #     plt.imshow(self.cvImage, cmap='Greys', interpolation='bicubic')
    #     plt.show()

    def color_convertion(self, img):
        """
        chalupnicza nie wydajna metoda do conversji obrazow

        :param img:
        :return:
        """
        # Rearrang the color channel
        b, g, r = cv2.split(img)  # not optimal TODO change to numpay array
        return cv2.merge((r, g, b))

    def resize(self, width, height):
        """
        Resize
        :param width:
        :param height:
        :return:
        """
        # TODO store the original value to save image in original size.
        size = (width, height)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage.current())
        resized = image.resize(size, Image.ANTIALIAS)
        self.tkImage = ImageTk.PhotoImage(resized)

    def resize_event(self, event):
        # TODO store the original value to save image in original size.
        size = (event.width, event.height)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage)
        resized = image.resize_event(size, Image.ANTIALIAS)
        self.tkImage = ImageTk.PhotoImage(resized)
        #         For Canvas
        # self.display.delete("IMG")
        # self.display.create_image(0, 0, image=self.tkImage, anchor='nw', tags="IMG")
        #

    def resize_event_tmp(self, event):
        # TODO store the original value to save image in original size.
        size = (event.width - 20, event.height - 25)
        # image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB)
        # cv2.COLOR_BGR2RGB)
        print(size)
        image = Image.fromarray(self.cvImage_tmp)
        resized = image.resize_event(size, Image.ANTIALIAS)
        self.tkImage_tmp = ImageTk.PhotoImage(resized)
        #         For Canvas
        # self.display.delete("IMG")
        # self.display.create_image(0, 0, image=self.tkImage, anchor='nw', tags="IMG")

    def global_prog(self, thresh, thresholdType=cv2.THRESH_BINARY):
        ret, self.cvImage_tmp = cv2.threshold(self.cvImage.current(), thresh, 255, thresholdType)
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def adaptive_prog(self, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=11,
                      C=2):
        """
        Adaptive Thresholding

        :param adaptiveMethod: cv2.ADAPTIVE_THRESH_GAUSSIAN_C or cv2.ADAPTIVE_THRESH_MEAN_C,
        :param thresholdType: types are :
                            cv2.THRESH_BINARY
                            cv2.THRESH_BINARY_INV
                            cv2.THRESH_TRUNC
                            cv2.THRESH_TOZERO
                            cv2.THRESH_TOZERO_INV

        :param blockSize: It decides the size of neighbourhood area.
        :param C: It is just a constant which is subtracted from the mean or weighted mean calculated.
        :return:
        """
        self.cvImage_tmp = cv2.adaptiveThreshold(self.cvImage.current(), 255,
                                                 adaptiveMethod,
                                                 thresholdType,
                                                 blockSize,
                                                 C)
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def color_picker(self):
        # Create a black image, a window
        def nothing(x):
            pass

        img = np.zeros((300, 512, 3), np.uint8)
        cv2.namedWindow('image')

        # create trackbars for color change
        cv2.createTrackbar('R', 'image', 0, 255, nothing)
        cv2.createTrackbar('G', 'image', 0, 255, nothing)
        cv2.createTrackbar('B', 'image', 0, 255, nothing)

        # create switch for ON/OFF functionality
        # switch = '0 : OFF \n1 : ON'
        # cv2.createTrackbar(switch, 'image', 0, 1, nothing)

        while (1):
            cv2.imshow('image', img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

            # get current positions of four trackbars
            r = cv2.getTrackbarPos('R', 'image')
            g = cv2.getTrackbarPos('G', 'image')
            b = cv2.getTrackbarPos('B', 'image')
            # s = cv2.getTrackbarPos(switch, 'image')

            # if s == 0:
            # img[:] = 0
            # else:
            img[:] = [b, g, r]

        cv2.destroyAllWindows()

    def rps(self, num):
        # redukcja poziomow szarosci
        bins = np.arange(0, 256, num)
        l_bins = []
        for i in range(num):
            l_bins.append(bins)

        cdf_m = [list(a) for a in zip(*l_bins)]
        cdf_m = np.array(cdf_m).ravel()
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage_tmp = cdf[self.cvImage.current()]
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def negation(self):
        # cv2.invert(self.cvImage, self.cvImage_tmp)

        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])
        # cdf = hist.cumsum()
        cdf_m = (255 - bins)
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # print("cdf Lut: ", cdf)
        # LUT Table cdf
        self.cvImage.update(cdf[self.cvImage.current()])
        self.tkImage = self.prepare_tk_image(self.cvImage.current())

    def hist_rand(self):
        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.mean())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')

        self.cvImage_tmp = cdf[self.cvImage.current()]
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def calculate_hist(self):
        return cv2.calcHist([self.cvImage_tmp], [0], None, [256], [0, 256])

    def hist_num(self):
        hist, bins = np.histogram(self.cvImage.current().flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        # cdf_normalized = cdf * hist.max() / cdf.max()

        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage_tmp = cdf[self.cvImage.current()]

        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def hist_eq(self):
        self.cvImage_tmp = cv2.equalizeHist(self.cvImage.current())
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def hist_CLAHE(self, x=8, y=8):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(x, y))
        self.cvImage_tmp = clahe.apply(self.cvImage.current())
        self.tkImage_tmp = self.prepare_tk_image(self.cvImage_tmp)

    def save(self, path=None):
        if path is None:
            cv2.imwrite(self.path, self.cvImage.current())
        else:
            cv2.imwrite(path, self.cvImage.current())

    @staticmethod
    def resize_tk_image(image, size=None):
        inner_image = ImageTk.PhotoImage(Image.fromarray(image))
        if size is None:
            return inner_image
        org_size = inner_image._PhotoImage__size
        if org_size[0] > size[0] or org_size[1] > size[1]:
            proportion_x = size[0] / org_size[0]
            proportion_y = size[1] / org_size[1]
            prop = proportion_x if proportion_x < proportion_y else proportion_y
            size = tuple([int(org_size[0] * prop), int(org_size[1] * prop)])
        else:
            size = org_size
        image = Image.fromarray(image)
        resize = image.resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(resize)
