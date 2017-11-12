import tkinter as tk
from cv2 import *
import cv2

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


class Histogram:
    def __init__(self, parent: tk.Frame):
        self.image = None

        self.hist_frame = parent
        self.hist_frame.pack(side=tk.RIGHT, expand=True)
        self.histCanvas = None
        self.toolbar = None
        self.fig = Figure()
        self.fig_subplot = self.fig.add_subplot(111)

        self.hist_pos_label = tk.Label(master=self.hist_frame)
        self.hist_pos_label.pack(side=tk.TOP)

    def _on_plot_hover(self, event):
        if event.xdata is not None:
            if event.xdata <= 256:
                x = int(event.xdata)
                y = int(self.calculate_hist()[int(event.xdata)])
                self.hist_pos_label.config(text="{}:{}".format(x, y))

    def __call__(self, image, *args, **kwargs):
        self.image = image
        self.fig_subplot.clear()

        self.fig_subplot.bar(range(0, 256), self.calculate_hist(), width=1)
        # self.fig_subplot.hist(self.image.current().ravel(), bins=256, range=[0.0, 256.0])
        self.fig_subplot.set_xlim([-1, 256])

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.fig, self.hist_frame)
        self.histCanvas.show()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas, self.hist_frame)
        self.toolbar.update()

        self.histCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig.canvas.mpl_connect('motion_notify_event', self._on_plot_hover)

    def calculate_hist(self):
        return cv2.calcHist([self.image], [0], None, [256], [0, 256])

