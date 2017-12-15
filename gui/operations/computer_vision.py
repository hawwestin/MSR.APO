import copy
from pprint import pprint
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
from cv2 import *
from matplotlib import pyplot as plt

from gui.operations.repeater import Repeater

colors = {"COLOR": 1,
          "GREY": 0}

supported_ext = [
    ".jpg",
    ".png"
]

"""
https://docs.opencv.org/3.3.0/d2/de8/group__core__array.html#ga209f2f4869e304c82d07739337eae7c5
"""
borderType = {
    "CONSTANT": cv2.BORDER_CONSTANT,
    "ISOLATED": cv2.BORDER_ISOLATED,
    "REFLECT": cv2.BORDER_REFLECT,
    "REFLECT101": cv2.BORDER_REFLECT101,
    "REPLICATE": cv2.BORDER_REPLICATE
}


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

    def negation2(self):
        hist, bins = np.histogram(self.cvImage.image.flatten(), 256, [0, 256])
        cdf_m = (255 - bins)
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        # LUT Table cdf
        self.cvImage.image = cdf[self.cvImage.image]

    def negation(self):
        self.cvImage.image = cv2.bitwise_not(self.cvImage.image)

    def negation3(self):
        """
        error in curent params
        error: (-215) type == CV_32F || type == CV_64F in function cv::invert
        :return:
        """
        cv2.invert(self.cvImage.image, self.cvImage.image)

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

    def img_paste(self, **kwargs):
        """
        Place given source on current version in cvImage.image and store new image cvImage_tmp.image
        Target is default cvImage_tmp
        :param source: Image which will be placed , Must by already cut to target size.
        :param img_place: left top corner of source image on target image
        :return:
        """
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(kwargs.get('img_place'), self.cvImage.image.shape, kwargs.get('source').shape)
        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]] = self._mask_to_size(self.cvImage_tmp.image, kwargs.get('source'),
                                                                          kwargs.get('img_place'))

    def ar_add(self, **kwargs):
        """
        Arytmethic add of two images . Source on top of internal cvImage.image
        :param source:
        :param place:
        :param weight:
        :return:
        """
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(kwargs.get('img_place'), self.cvImage.image.shape, kwargs.get('source').shape)
        self.img_paste(source=cv2.addWeighted(self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]],
                                              kwargs.get('weight')[0],
                                              self._mask_to_size(self.cvImage_tmp.image,
                                                                 kwargs.get('source'),
                                                                 kwargs.get('img_place')),
                                              kwargs.get('weight')[1],
                                              0),
                       img_place=kwargs.get('img_place'))

    def image_cut(self, **kwargs):
        """
        Cut piece of self.cvImage on given place.
        :param rect_place: tuple of top left x, y on target img
        :return:
        """
        self.cvImage_tmp.image = self.cvImage.image[int(kwargs.get('rect_place')[1]):int(kwargs.get('rect_place')[3]),
                                 int(kwargs.get('rect_place')[0]):int(kwargs.get('rect_place')[2])]

    def ar_diff(self, **kwargs):
        """
        Arithmetic subtraction of source image on given place.
        :param source: Image to be added on top of current self.cvImage
        :param img_place: tuple of top left x, y on target img
        :return:
        """
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        y, x = self._target_place(kwargs.get('img_place'), self.cvImage.image.shape, kwargs.get('source').shape)
        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]] -= self._mask_to_size(self.cvImage_tmp.image, kwargs.get('source'),
                                                                           kwargs.get('img_place'))

    def logic_and(self, target, source, place):
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_and(target[y[0]:y[1], x[0]:x[1]],
                        self._mask_to_size(target, source, place),
                        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(source=self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], img_place=place)

    def logic_or(self, target, source, place):
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_or(target[y[0]:y[1], x[0]:x[1]],
                       self._mask_to_size(target, source, place),
                       self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(source=self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], img_place=place)

    def logic_xor(self, target, source, place):
        """
        Logic operation Xor on given images.
        :param target: Image on which should by applied change
        :param source: Image which will be aplied on target image.
        :param place: Left top corner where source Image will be placed on target.
        :param preview: Bool Flag
        :return:
        """
        self.cvImage_tmp.image = copy.copy(target)
        y, x = self._target_place(place, target.shape, source.shape)
        cv2.bitwise_xor(target[y[0]:y[1], x[0]:x[1]],
                        self._mask_to_size(target, source, place),
                        self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]])
        self.img_paste(source=self.cvImage_tmp.image[y[0]:y[1], x[0]:x[1]], img_place=place)

    def filter(self, kernel, border_type):
        """
        Apply given kernel on current cvImage.image and store new in cvImage_tmp.image.

        :param kernel: numpy array
        :param preview: bool flag
        :param border_type:
        :return:
        """
        self.cvImage_tmp.image = cv2.filter2D(self.cvImage.image, -1, kernel, self.cvImage_tmp.image,
                                              borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def blur(self, kernel, border_type):
        self.cvImage_tmp.image = cv2.blur(src=self.cvImage.image, ksize=kernel,
                                          borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def preview(self, img=None):
        """
        Display current tmp image.

        Linux 4.4 with openCv 3.1 have broken cv2.imshow function.
        For different platform support matplotlib imshow is used.
        :return:
        """
        # cv2.startWindowThread()
        # cv2.namedWindow('preview', cv2.WINDOW_NORMAL)
        # cv2.imshow('preview', self.cvImage_tmp.image)
        if img is None:
            plt.imshow(self.cvImage_tmp.image,
                       cmap='gray',
                       interpolation='none')
            # ,
            # vmin=0,
            # vmax=255)
        else:
            plt.imshow(img,
                       cmap='gray',
                       interpolation='none',
                       vmin=0,
                       vmax=255)
        plt.show()

    def houghProbabilistic(self, threshold1=50, threshold2=150, threshold3=200, apertureSize=3, color=(0, 255, 0),
                           thickness=2):
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        edges = cv2.Canny(self.cvImage_tmp.image, threshold1, threshold2, apertureSize=apertureSize)
        # todo rho and theta as method params.
        lines = cv2.HoughLinesP(image=edges,
                                rho=1,
                                theta=np.pi / 180,
                                threshold=threshold3,
                                minLineLength=20,
                                maxLineGap=10)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(self.cvImage_tmp.image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return len(lines), self.cvImage_tmp.image

    def hough(self, threshold1=50, threshold2=150, threshold3=200, apertureSize=3, color=(0, 255, 0), thickness=2):
        self.cvImage_tmp.image = copy.copy(self.cvImage.image)
        edges = cv2.Canny(self.cvImage_tmp.image, threshold1, threshold2, apertureSize=apertureSize)
        # todo rho and theta as method params.

        lines = cv2.HoughLines(image=edges,
                               rho=1,
                               theta=np.pi / 180,
                               threshold=threshold3)

        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + self.cvImage_tmp.image.shape[1] * 1.5 * (-b))
            y1 = int(y0 + self.cvImage_tmp.image.shape[0] * 1.5 * a)
            x2 = int(x0 - self.cvImage_tmp.image.shape[1] * 1.5 * (-b))
            y2 = int(y0 - self.cvImage_tmp.image.shape[0] * 1.5 * a)
            print("rho {}, theta {}, a {}, b {}, x0 {}, y0 {}, x1 {}, x2 {}, y1 {}, y2 {}".format(rho, theta, a, b, x0,
                                                                                                  y0, x1, x2, y1, y2))
            cv2.line(self.cvImage_tmp.image, (x1, y1), (x2, y2), color, thickness=thickness)

        return len(lines), self.cvImage_tmp.image

    def hough_accumulator(self):
        # Rho and Theta ranges
        thetas = np.deg2rad(np.arange(-90.0, 90.0))
        width, height = self.cvImage.image.shape
        diag_len = np.ceil(np.sqrt(width * width + height * height))  # max_dist
        rhos = np.linspace(-diag_len, diag_len, diag_len * 2.0)

        # Cache some resuable values
        cos_t = np.cos(thetas)
        sin_t = np.sin(thetas)
        num_thetas = len(thetas)

        # Hough accumulator array of theta vs rho
        accumulator = np.zeros((int(2 * diag_len), int(num_thetas)), dtype=np.uint64)
        y_idxs, x_idxs = np.nonzero(self.cvImage.image)  # (row, col) indexes to edges

        # Vote in the hough accumulator
        for i in range(len(x_idxs)):
            # todo add progress bar for impatient users!
            for t_idx in range(num_thetas):
                # Calculate rho. diag_len is added for a positive index
                rho = round(x_idxs[i] * cos_t[t_idx] + y_idxs[i] * sin_t[t_idx]) + diag_len
                accumulator[int(rho), int(t_idx)] += 1

        self.preview(accumulator)

        return thetas, rhos

    def erode(self, kernel, border_type, iterations=1):
        self.cvImage_tmp.image = cv2.erode(self.cvImage.image, kernel, iterations=iterations,
                                           borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def dilate(self, kernel, border_type, iterations=1):
        self.cvImage_tmp.image = cv2.dilate(self.cvImage.image, kernel, iterations=iterations,
                                            borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def opening(self, kernel, border_type, iterations=1):
        self.cvImage_tmp.image = cv2.morphologyEx(self.cvImage.image, cv2.MORPH_OPEN, kernel, iterations=iterations,
                                                  borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def closing(self, kernel, border_type, iterations=1):
        self.cvImage_tmp.image = cv2.morphologyEx(self.cvImage.image, cv2.MORPH_CLOSE, kernel, iterations=iterations,
                                                  borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def GRADIENT(self, kernel, border_type, iterations=1):
        """
        a morphological gradient
            dst=morph_grad(src,element)=dilate(src,element)−erode(src,element)
        :param kernel:
        :param border_type:
        :param iterations:
        :return:
        """
        self.cvImage_tmp.image = cv2.morphologyEx(self.cvImage.image, cv2.MORPH_GRADIENT, kernel, iterations=iterations,
                                                  borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def TOPHAT(self, kernel, border_type, iterations=1):
        """
        "top hat"
            dst=tophat(src,element)=src−open(src,element)
        :param kernel:
        :param border_type:
        :param iterations:
        :return:
        """
        self.cvImage_tmp.image = cv2.morphologyEx(self.cvImage.image, cv2.MORPH_TOPHAT, kernel, iterations=iterations,
                                                  borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def BLACKHAT(self, kernel, border_type, iterations=1):
        """
        "black hat"
            dst=blackhat(src,element)=close(src,element)−src
        :param kernel:
        :param border_type:
        :param iterations:
        :return:
        """
        self.cvImage_tmp.image = cv2.morphologyEx(self.cvImage.image, cv2.MORPH_BLACKHAT, kernel, iterations=iterations,
                                                  borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))

    def skeleton(self, kernel, border_type, iterations=1):
        """
        Best work after image threshold.
            cv2.threshold(img,127,255,0)

        :return:
        """
        img = copy.copy(self.cvImage.image)
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)

        element = cv2.getStructuringElement(cv2.MORPH_CROSS, kernel.shape)
        done = False

        while (not done):
            eroded = cv2.erode(img, element, borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))
            temp = cv2.dilate(eroded, element, borderType=borderType.get(border_type, cv2.BORDER_DEFAULT))
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True

        self.cvImage_tmp.image = skel
