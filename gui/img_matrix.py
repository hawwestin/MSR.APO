import tkinter as tk
from cv2 import *
import cv2
import numpy as np

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


class ImgMatrix:
    def __init__(self, parent: tk.Frame):
        self.image = None

        self._frame = parent
        self._canvas = None
        self.toolbar = None
        self.fig = Figure(tight_layout=True)
        self.fig_subplot = self.fig.add_subplot(111)

    def __call__(self, image, *args, **kwargs):
        self.image = image
        self.fig_subplot.clear()

        x, y = self.image.shape[:2]

        for i in range(x):
            for j in range(y):
                c = self.image[i, j]
                self.fig_subplot.text(j, i, str(c), va='center', ha='center')

        self.fig_subplot.set_xlim(0, y)
        self.fig_subplot.set_ylim(0, y)
        self.fig_subplot.set_xticks(np.arange(x))
        self.fig_subplot.set_yticks(np.arange(y))
        self.fig_subplot.grid()
        # self.fig_subplot.set_xlim([-1, 256])

        if self._canvas is None:
            self._canvas = FigureCanvasTkAgg(self.fig, self._frame)
        self._canvas.show()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self._canvas, self._frame)
        self.toolbar.update()

        self._canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
