import copy
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
from cv2 import *

from gui.operations.repeater import Repeater

colors = {"COLOR": 1,
          "GREY": 0}

supported_ext = [
    ".jpg",
    ".png"
]


class MemoImageData(Repeater):
    @property
    def image(self):
        return self.current()

    @image.setter
    def image(self, value):
        self.update(value)

    @property
    def tk_image(self):
        return ImageTk.PhotoImage(Image.fromarray(self.image))


class SingleImageData:
    def __init__(self):
        self._item = None

    @property
    def image(self):
        return self._item

    @image.setter
    def image(self, value):
        self._item = value

    @property
    def tk_image(self):
        return ImageTk.PhotoImage(Image.fromarray(self.image))


class Vision:
    """
    Przechowuje instancje otwartego pliku i pozwala wykonywac na nim operacje

    """

    def __init__(self):
        self.path = None
        self.color = None

        # Actual
        self.cvImage = MemoImageData()
        # temp
        self.cvImage_tmp = SingleImageData()

    def open_image(self, path):
        self.path = path
        if self.color is cv2.IMREAD_COLOR:
            self.cvImage.image = cv2.imread(self.path, cv2.IMREAD_COLOR)
            self.cvImage.image = cv2.cvtColor(self.cvImage.image, cv2.COLOR_BGR2RGB)
        else:
            self.cvImage.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

    def color_convertion(self, img):
        """
        chalupnicza nie wydajna metoda do conversji obrazow

        :param img:
        :return:
        """
        # Rearrang the color channel
        b, g, r = cv2.split(img)
        return cv2.merge((r, g, b))

    def global_prog(self, thresh, thresholdType=cv2.THRESH_BINARY):
        ret, self.cvImage_tmp.image = cv2.threshold(self.cvImage.image, thresh, 255, thresholdType)

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
        self.cvImage_tmp.image = cv2.adaptiveThreshold(self.cvImage.image, 255,
                                                       adaptiveMethod,
                                                       thresholdType,
                                                       blockSize,
                                                       C)

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
        self.cvImage_tmp.image = cdf[self.cvImage.image]

    def negation(self):
        # cv2.invert(self.cvImage, self.cvImage_tmp)

        hist, bins = np.histogram(self.cvImage.image.flatten(), 256, [0, 256])
        # cdf = hist.cumsum()
        cdf_m = (255 - bins)
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage.image = cdf[self.cvImage.image]

    def hist_rand(self):
        hist, bins = np.histogram(self.cvImage.image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.mean())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        self.cvImage_tmp.image = cdf[self.cvImage.image]

        return cv2.calcHist([self.cvImage_tmp.image], [0], None, [256], [0, 256])

    def hist_num(self):
        hist, bins = np.histogram(self.cvImage.image.flatten(), 256, [0, 256])

        cdf = hist.cumsum()
        # cdf_normalized = cdf * hist.max() / cdf.max()

        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage_tmp.image = cdf[self.cvImage.image]

    def hist_eq(self):
        self.cvImage_tmp.image = cv2.equalizeHist(self.cvImage.image)

    def hist_CLAHE(self, x=8, y=8):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(x, y))
        self.cvImage_tmp.image = clahe.apply(self.cvImage.image)

    def save(self, path=None):
        if path is not None:
            cv2.imwrite(path, self.cvImage.image)
        elif self.path is not None:
            cv2.imwrite(self.path, self.cvImage.image)
        else:
            self.path = filedialog.asksaveasfilename()
            cv2.imwrite(self.path, self.cvImage.image)

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

    def new_rand_img(self):
        image = np.random.randint(0, 256, 120000).reshape(300, 400)
        self.cvImage.image = image.astype('uint8')

    def uop(self, gamma: float, brightness: int, contrast: float):
        invGamma = 1.0 / gamma

        # table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        lut = []
        for x in range(256):
            v = contrast * (((x / 255.0) ** invGamma) * 255) + brightness
            if v < 0:
                lut.append(0)
            elif v > 255:
                lut.append(255)
            else:
                lut.append(v)
        lut = np.array(lut).astype('uint8')
        cv2.LUT(self.cvImage.image, lut, self.cvImage_tmp.image)
        return lut

    def tone_curve(self, lut):
        self.cvImage_tmp.image = cv2.LUT(self.cvImage.image, np.array(lut).astype("uint8"))

    def image_stretching(self, p1, p2):
        lut = []
        for p in range(256):
            if p1 < p <= p2:
                lut.append((p - p1) * (256 / (p2 - p1)))
            elif p <= p1 or p > p2:
                lut.append(0)
        lut = np.array(lut)
        lut = np.ma.filled(lut, 0).astype('uint8')
        self.cvImage_tmp.image = lut[self.cvImage.image]
        return lut

    def progowanie_z_zachowaniem_poziomow(self, p1, p2):
        lut = []
        for p in range(256):
            if p1 < p <= p2:
                lut.append(p)
            elif p <= p1 or p > p2:
                lut.append(0)
        lut = np.array(lut)
        lut = np.ma.filled(lut, 0).astype('uint8')
        self.cvImage_tmp.image = lut[self.cvImage.image]
        return lut

    def _mask_to_size(self, target, source, place: tuple):
        """
        Cut source to borders of img_bg
        :param target:
        :param source:
        :param place: tuple of top left x, y on target img_bg
        :return:
        """
        place_x = int(place[0])
        place_y = int(place[1])

        # img size , height and width
        img_y, img_x = source.shape
        if place_x < 0:
            source = source[0:img_y, np.abs(place_x):img_x]
        if place_y < 0:
            source = source[np.abs(place_y):img_y, 0:img_x]

        if place_x + img_x > target.shape[1]:
            source = source[0:img_y, 0:img_x - (place_x + img_x - target.shape[1])]
        if place_y + img_y > target.shape[0]:
            source = source[0:img_y - (place_y + img_y - target.shape[0]), 0:img_x]
        return source

    def _target_place(self, place: tuple, target_shape: tuple, source_shape: tuple):
        """
        Calculate valid shape on target
        :param place: tuple of top left x, y on target img
        :param source_shape: tuple (width, height) of target image.
        :param target_shape: tuple (width, height) of source image.
        :return: tuple y, x
        """
        place_x = int(place[0])
        place_y = int(place[1])
        img_y, img_x = source_shape
        x1 = place_x if place_x > 0 else 0
        x2 = place_x + img_x if place_x + img_x <= target_shape[1] else target_shape[1]
        y1 = place_y if place_y > 0 else 0
        y2 = place_y + img_y if place_y + img_y <= target_shape[0] else target_shape[0]

        return (y1, y2), (x1, x2)

    def img_paste(self, source, place, preview=True):
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(place, self.cvImage.image.shape, source.shape)
        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]] = self._mask_to_size(self.cvImage_tmp.image, source, place)
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def ar_add(self, source, place, weight, preview=True):
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(place, self.cvImage.image.shape, source.shape)
        self.img_paste(cv2.addWeighted(self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]],
                                       weight[0],
                                       self._mask_to_size(self.cvImage_tmp.image,
                                                          source,
                                                          place),
                                       weight[1],
                                       0),
                       place,
                       preview=False)
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)
        pass

    def image_cut(self, place, preview=True):
        """
        Cut piece of self.cvImage on given place.
        :param place: tuple of top left x, y on target img
        :param preview: Flag for additional preview window
        :return:
        """
        self.cvImage_tmp.image = self.cvImage.image[int(place[1]):int(place[3]), int(place[0]):int(place[2])]
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def ar_diff(self, source, place, preview=True):
        """
        Arithmetic subtraction of source image on given place.
        :param source: Image to be added on top of current self.cvImage
        :param place: tuple of top left x, y on target img
        :param preview: Flag for additional preview window
        :return:
        """
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(place, self.cvImage.image.shape, source.shape)
        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]] -= self._mask_to_size(self.cvImage_tmp.image, source, place)
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def logic_and(self, target, source, place, preview=True):
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_and(target[y[0]:y[1], x[0]:x[1]],
                        self._mask_to_size(target, source, place),
                        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], place, preview=False)

        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def logic_or(self, target, source, place, preview=True):
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_or(target[y[0]:y[1], x[0]:x[1]],
                       self._mask_to_size(target, source, place),
                       self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], place, preview=False)

        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def logic_xor(self, target, source, place, preview=True):
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_xor(target[y[0]:y[1], x[0]:x[1]],
                        self._mask_to_size(target, source, place),
                        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], place, preview=False)

        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def filter(self, kernel, preview=True):
        self.cvImage_tmp.image = cv2.filter2D(self.cvImage.image, -1, kernel, self.cvImage_tmp.image)
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)