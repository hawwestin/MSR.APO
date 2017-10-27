import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import numpy as np

from OperationsLinear.operation_template import OperationTemplate
from tabpicture import TabPicture


class UOPOperation(OperationTemplate):
    bins = list(range(0, 256))

    def __init__(self, tab: TabPicture):
        self.fig = Figure()
        self.fig_subplot = self.fig.add_subplot(111)
        self.lut_canvas = None
        self.draw = False
        self.lut = np.array(UOPOperation.bins)
        self.lut_pos_label = None
        self.gamma = tk.DoubleVar()
        self.gamma.set(1)
        self.contrast = tk.DoubleVar()
        self.contrast.set(1)
        self.brightness = tk.IntVar()
        self.brightness.set(0)
        super().__init__("Uniwersalna operacja jednopunktowa", tab)

    def reset(self):
        self.lut = np.array(UOPOperation.bins)
        self.lut = self.tab.vision.uop(self.gamma.get(), self.brightness.get(), self.contrast.get())
        self.lut_line(self.lut)
        self.tab.vision.tone_curve(self.lut)
        self.refresh()

    def control_plugin(self):
        def draw(flag):
            self.draw = flag
            if flag is False:
                self.tab.vision.tone_curve(self.lut)
                self.refresh()

        menu = tk.Frame(self.plugins)
        menu.pack(side=tk.LEFT, padx=2, anchor='nw')
        _width = 17

        b_reset = ttk.Button(menu, text="Redraw from Lut", command=self.reset, width=_width)
        b_reset.pack(side=tk.TOP, padx=2, anchor='nw')

        gamma_l = tk.Label(menu, text="gamma")
        gamma_l.pack(side=tk.TOP)
        gamma_e = tk.Entry(menu, textvariable=self.gamma, width=_width)
        gamma_e.pack(side=tk.TOP)
        brightness_l = tk.Label(menu, text="brigtness")
        brightness_l.pack(side=tk.TOP)
        brightness_e = tk.Entry(menu, textvariable=self.brightness, width=_width)
        brightness_e.pack(side=tk.TOP)
        contrast_l = tk.Label(menu, text="contrast")
        contrast_l.pack(side=tk.TOP)
        contrast_e = tk.Entry(menu, textvariable=self.contrast, width=_width)
        contrast_e .pack(side=tk.TOP)

        self.lut_pos_label = tk.Label(master=self.plugins)
        self.lut_pos_label.pack(side=tk.TOP, anchor='n')

        self.lut_line(self.lut)
        self.fig.tight_layout()
        self.fig.canvas.mpl_connect('button_press_event', lambda x: draw(True))
        self.fig.canvas.mpl_connect('button_release_event', lambda x: draw(False))
        self.fig.canvas.mpl_connect('motion_notify_event', self._mouse_brush)

    def _mouse_brush(self, event):
        if event.xdata is not None:
            self.lut_pos_label.config(text="{}:{}".format(int(event.xdata), int(self.lut[int(event.xdata)])))
            if self.draw and event.xdata < 256:
                self.lut[int(event.xdata)] = event.ydata
                self.lut_line(self.lut)

    def lut_line(self, lut):
        self.fig_subplot.clear()
        self.fig_subplot.plot(UOPOperation.bins, lut)
        self.fig_subplot.set_xlim([0, 256])
        self.fig_subplot.set_ylim([0, 255])
        if self.lut_canvas is None:
            self.lut_canvas = FigureCanvasTkAgg(self.fig, self.plugins)
            self.lut_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.lut_canvas.show()


class tmp:
    def __init__(self):
        popup = tk.Tk()
        LabelFrame = tk.Frame(popup)

        w, h = LabelFrame.winfo_width(), LabelFrame.winfo_height()
        print(w, h)

        f = Figure()
        fig_subplot = f.add_subplot(111)
        uop_line = np.arange(0, 255)
        # cdf = [list(a) for a in zip(source_x, output_y)]

        fig_subplot.plot(uop_line, color='b')

        canvas = tk.Canvas(LabelFrame, width=255, height=255)

        histCanvas = FigureCanvasTkAgg(f, LabelFrame)
        histCanvas.show()
        histCanvas.get_tk_widget().pack(side=tk.TOP,
                                        fill=tk.BOTH,
                                        expand=True)
        histCanvas.get_tk_widget().bind("<Key>", key)
        histCanvas.get_tk_widget().bind("<Button-1>", callback)
        # histCanvas.get_tk_widget().pack()

        w, h = LabelFrame.winfo_width(), LabelFrame.winfo_height()
        print("after hist: ", w, h)

        popup.mainloop()

    def key(self, event):
        print("pressed", repr(event.char))

    def callback(self, event):
        global uop_line
        global histCanvas
        uop_line[event.x] = 255 - event.y
        fig_subplot.plot(uop_line, color='b')
        histCanvas.show()
        print("clicked at", event.x, event.y)
        # print(uop_line)
