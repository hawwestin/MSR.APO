import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import numpy as np

from Operations.operation_template import OperationTemplate
from tabpicture import TabPicture


class UOPOperation(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Uniwersalna operacja jednopunktowa", tab)

    def control_plugin(self):
        def uop():
            self.tab.vision.uop(2, 0)
            self.refresh()

        button = ttk.Button(self.plugins, text="uop", command=uop)
        button.pack(side=tk.LEFT, padx=2)


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
