import tkinter as tk
import matplotlib
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from gui.operations.computer_vision import MemoImageData


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

        self._start = 0
        self._stop = 0

        # self.fig.canvas.mpl_connect('button_press_event', self.start_rect_tracker)
        # self.fig.canvas.mpl_connect('button_release_event', self.stop_rect_tracker)

    def __call__(self, image: MemoImageData, *args, **kwargs):
        self.image = image
        # FIXME With no clearing subplot ram is rising in usages!!!
        # if not image.color:
        self.fig_subplot.imshow(self.image.image,
                                cmap='gray',  # todo new params
                                interpolation='none',
                                vmin=0,
                                vmax=255,
                                aspect='equal')
        # else:
        #     self.fig_subplot.imshow(self.image.image,
        #                             cmap='hsv',  # todo new params
        #                             interpolation='none',
        #                             vmin=0,
        #                             vmax=255,
        #                             aspect='equal')
        self.toolbar.draw()

    def start_rect_tracker(self, event):
        if event.xdata is not None and event.ydata is not None:
            self._start = int(event.xdata)
            print('you pressed', event.button, event.xdata, event.ydata)

    def stop_rect_tracker(self, event):
        if event.xdata is not None and event.ydata is not None:
            self._stop = int(event.xdata)
            print('you pressed', event.button, event.xdata, event.ydata)

            self.fig_subplot.add_patch(patches.Rectangle((50, 50),
                                                         50,
                                                         50
                                                         ))
