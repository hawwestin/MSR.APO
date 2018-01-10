import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class ImageFrame:
    def __init__(self, parent: tk.Frame):
        self.image = None

        self._frame = parent
        self.image_canvas = None
        self.toolbar = None

        self.fig = Figure(tight_layout=True)
        self.fig_subplot = self.fig.add_subplot(111)

        self.fig_subplot.clear()

        if self.image_canvas is None:
            self.image_canvas = FigureCanvasTkAgg(self.fig, self._frame)
        self.image_canvas.show()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.image_canvas, self._frame)
        self.toolbar.update()

        self.image_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def __call__(self, image, *args, **kwargs):
        self.image = image
        # FIXME With no clearing subplot ram is rising in usages!!!
        self.fig_subplot.imshow(self.image,
                                cmap='gray', #todo new params
                                interpolation='none',
                                vmin=0,
                                vmax=255,
                                aspect='equal')
        self.toolbar.draw()

