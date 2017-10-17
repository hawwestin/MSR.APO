import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from computer_vision import Vision
from histogram import Histogram
from utils import resolution
from tabpicture import TabPicture


class OperationTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry(resolution)

        self.tab = tab
        self.size = (300, 700)
        # self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.image)

        self.body = tk.Frame(master=self.window)

        self.body.pack(fill=tk.BOTH, expand=True)

        self.buttons = tk.Frame(master=self.body)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        self.plugins = tk.Frame(master=self.body)
        self.plugins.pack(after=self.buttons, side=tk.TOP, fill=tk.X)

        self.panels = tk.Frame(master=self.body)
        self.panels.pack(after=self.plugins, side=tk.TOP, fill=tk.BOTH, expand=True)

        ###############
        # Panels
        ###############
        lf_original = tk.LabelFrame(master=self.panels, text='Original')
        lf_original.pack(side=tk.LEFT)
        self.panel = tk.Label(master=lf_original, image=self.tab.vision.tkImage)
        self.panel.pack()

        lf_equalised = tk.LabelFrame(master=self.panels, text='Equalised')
        lf_equalised.pack(side=tk.LEFT, after=lf_original)
        self.panel_tmp = tk.Label(master=lf_equalised)
        self.panel_tmp.pack()

        self.panel_hist = tk.Frame(master=self.panels)
        self.panel_hist.pack(side=tk.RIGHT)
        self.histogram = Histogram(self.panel_hist)

        self.widget_buttons()

        self.control_plugin()
        self.refresh()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab.vision.cvImage.undo()
            self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.image)
            self.refresh()

        def redo():
            self.tab.vision.cvImage.redo()
            self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.image)
            self.refresh()

        def confirm():
            self.tab.persist_tmp()
            self.refresh()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)

        b_exit = ttk.Button(self.buttons, text="Exit", command=self.window.destroy)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh(self):
        self.set_panel_img()
        self.histogram(self.tab.vision.cvImage_tmp.image)

    def set_panel_img(self):
        self.tab.vision.tkImage = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)
        self.panel.configure(image=self.tab.vision.tkImage)
        self.panel.image = self.tab.vision.tkImage
        if self.tab.vision.tkImage_tmp is not None:
            self.tab.vision.tkImage_tmp = Vision.resize_tk_image(self.tab.vision.cvImage_tmp.image, self.size)
            self.panel_tmp.configure(image=self.tab.vision.tkImage_tmp)
            self.panel_tmp.image = self.tab.vision.tkImage_tmp

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass
