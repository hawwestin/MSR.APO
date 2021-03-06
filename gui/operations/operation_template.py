import tkinter as tk
from tkinter import ttk

from gui.histogram import Histogram
from gui.operations.computer_vision import Vision
from gui.tabpicture import TabPicture
import app_config


class OperationTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry(app_config.operations_window_resolution)

        self.tab = tab
        self.size = (300, 700)
        self.tkImage = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)
        self.tkImage_tmp = None

        self.body = tk.Frame(master=self.window)

        self.body.pack(fill=tk.BOTH, expand=True)

        self.buttons = tk.Frame(master=self.body)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        self.plugins = tk.Frame(master=self.body)
        self.plugins.pack(after=self.buttons, side=tk.TOP, fill=tk.X)

        self.panels = tk.Frame(master=self.body)
        self.panels.pack(after=self.plugins, side=tk.TOP, fill=tk.BOTH, expand=True)

        self.status_message = tk.StringVar()
        self.status_message.set('*')
        self.status_bar = tk.Label(self.body, textvariable=self.status_message, bd=1, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        ###############
        # Panels
        ###############
        self.outer_pan = tk.PanedWindow(self.panels,
                                        handlesize=10,
                                        showhandle=True,
                                        handlepad=12,
                                        sashwidth=3)
        self.outer_pan.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_pan = tk.PanedWindow(self.outer_pan,
                                       handlesize=10,
                                       showhandle=True,
                                       handlepad=12,
                                       sashwidth=3,
                                       orient=tk.VERTICAL)
        self.left_pan.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.outer_pan.add(self.left_pan, minsize=100)



        lf_original = tk.LabelFrame(master=self.panels, text='Original')
        lf_original.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.left_pan.add(lf_original, minsize=100)
        self.panel = tk.Label(master=lf_original, image=self.tkImage)
        self.panel.pack()

        lf_equalised = tk.LabelFrame(master=self.panels, text='Equalised')
        lf_equalised.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.left_pan.add(lf_equalised, minsize=100)
        self.panel_tmp = tk.Label(master=lf_equalised)
        self.panel_tmp.pack()

        self.panel_hist = tk.Frame(master=self.panels)
        self.panel_hist.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.outer_pan.add(self.panel_hist, minsize=100)
        self.histogram = Histogram(self.panel_hist)

        self.widget_buttons()

        self.control_plugin()
        self.refresh()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab.vision.cvImage.undo(self.status_message)
            self.refresh()

        def redo():
            self.tab.vision.cvImage.redo(self.status_message)
            self.refresh()

        def confirm():
            self.operation_command(True)

        def preview():
            self.operation_command()
            self.tab.vision.preview()

        def _exit():
            self.tab.vision.cvImage_tmp.image = None
            self.window.destroy()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)
        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)
        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)
        b_confirm = ttk.Button(self.buttons, text="Update", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)
        b_preview = ttk.Button(self.buttons, text="Preview", command=preview)
        b_preview.pack(side=tk.LEFT, padx=2, after=b_confirm)
        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh(self):
        self.set_panel_img()
        self.histogram(self.tab.vision.cvImage_tmp.image)

    def set_panel_img(self):
        self.tkImage = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)
        self.panel.configure(image=self.tkImage)
        self.panel.image = self.tkImage
        if self.tab.vision.cvImage_tmp.image is not None:
            self.tkImage_tmp = Vision.resize_tk_image(self.tab.vision.cvImage_tmp.image, self.size)
            self.panel_tmp.configure(image=self.tkImage_tmp)
            self.panel_tmp.image = self.tkImage_tmp

    def control_plugin(self):
        """
        Mock method for gui widgets to be filled by concrete operation.
        :return:
        """
        pass

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        pass
