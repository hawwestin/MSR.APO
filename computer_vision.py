import copy
from tkinter import filedialog

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

    def _mask_to_size(self, img_bg, img_fg, place):
        print("{} {}".format(place[0], place[1]))
        print("{} {}".format(np.abs(place[0]), abs(place[1])))

        place_x = int(place[0])
        place_y = int(place[1])

        # img size , height and width
        img_y, img_x = img_fg.shape
        if place_x < 0:
            img_fg = img_fg[0:img_y, np.abs(place_x):img_x]
        if place_y < 0:
            img_fg = img_fg[np.abs(place_y):img_y, 0:img_x]

        if place_x + img_x > img_bg.shape[1]:
            img_fg = img_fg[0:img_y, 0:img_x - (place_x + img_x - img_bg.shape[1])]
        if place_y + img_y > img_bg.shape[0]:
            img_fg = img_fg[0:img_y - (place_y + img_y - img_bg.shape[0]), 0:img_x]

        x1 = place_x if place_x > 0 else 0
        x2 = place_x + img_x if place_x + img_x <= self.cvImage.image.shape[1] else self.cvImage.image.shape[1]
        y1 = place_y if place_y > 0 else 0
        y2 = place_y + img_y if place_y + img_y <= self.cvImage.image.shape[0] else self.cvImage.image.shape[0]

        img_bg[y1:y2, x1:x2] = img_fg

        return img_bg

    def ar_add(self, img, place, preview=True):
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        self.cvImage_tmp.image = self._mask_to_size(self.cvImage_tmp.image, img, place)
        # img = cv2.addWeighted(self.cvImage.image, 0.7, img, 0.3, 0)
        # cv2.imshow('1', img)
        if preview:
            cv2.imshow('preview', self.cvImage_tmp.image)

    def ar_sub(self):
        pass

    def ar_diff(self):
        pass

    def logic_and(self, img, place):
        # img_bg = np.zeros(self.cvImage.image.shape, np.uint8)
        # rows, cols = img_bg.shape
        rows, cols = self.cvImage.image.shape
        roi = self.cvImage.image[0:rows, 0:cols]
        # Now create a mask of logo and create its inverse mask also
        # try:
        #     img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # except Exception as e:
        #     print(e)
        img2gray = img
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img, img, mask=mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg, img2_fg)
        self.cvImage.image[place[0]:rows, place[0]:cols] = dst
        cv2.imshow('res', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        pass

    def logic_or(self):
        pass

    def logic_xor(self):
        pass
