import copy
import tkinter as tk
from tkinter import ttk

import app_config
from gui.histogram import Histogram
from gui.operations import computer_vision
from gui.tabpicture import TabPicture
from gui.image_frame import ImageFrame


class MatLibTemplate:
    """
    Dictionary to hold all valid filter operations with kernel
    """
    Kernel_Size = {
        "3x3": (3, 3),
        "2x2": (2, 2),
        "3x5": (3, 5),
        "5x3": (5, 3),
        "5x5": (5, 5),
        "7x7": (7, 7),
    }

    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry(app_config.operations_window_resolution)

        self.tab_bg = tab
        self.vision_result = computer_vision.Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.size = (300, 300)
        self.tk_img_background = None
        self.cv_img_result = self.tab_bg.vision.cvImage

        self.operation_name = tk.StringVar()
        self.kernel_size = tk.StringVar()
        self.border_type = tk.StringVar()

        self.border_type.set(list(computer_vision.borderType.keys())[0])

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
        self.outer_pan = tk.PanedWindow(self.panels, handlesize=10, showhandle=True, handlepad=12, sashwidth=3)
        self.outer_pan.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_panned_window = tk.PanedWindow(self.outer_pan, handlesize=10, showhandle=True, handlepad=12,
                                                 sashwidth=3,
                                                 orient=tk.VERTICAL)
        self.left_panned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.outer_pan.add(self.left_panned_window, minsize=100)

        # todo switch self.panels to self.kernel_panel
        lf_top = tk.LabelFrame(master=self.panels, text='Image')
        lf_top.pack()
        self.left_panned_window.add(lf_top, minsize=100)

        self.panel_back = tk.Label(master=lf_top)
        self.panel_back.pack()

        self.options_panned_frame = tk.LabelFrame(master=self.panels, text='Filter')
        self.options_panned_frame.pack()
        self.left_panned_window.add(self.options_panned_frame, minsize=100)

        self.lf_result = tk.LabelFrame(master=self.panels, text='Result')
        self.lf_result.pack()
        self.outer_pan.add(self.lf_result, minsize=100)

        self.result_tabs = ttk.Notebook(self.lf_result)
        self.result_tabs.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.img_frame = tk.Frame(self.result_tabs)
        self.img_frame.pack(fill=tk.BOTH, expand=1)
        self.result_tabs.add(self.img_frame, text="Resulat Image")
        self.hist_frame = tk.Frame(self.result_tabs)
        self.hist_frame.pack(fill=tk.BOTH, expand=1)
        self.result_tabs.add(self.hist_frame, text="Hiastogram")

        self.image_canvas = ImageFrame(self.img_frame)
        self.histogram = Histogram(self.hist_frame)

        self.widget_buttons()

        self.refresh_panel_img()

    def widget_buttons(self):
        def confirm():
            name = tk.StringVar()
            name.set("*" + self.tab_bg.name.get())
            tab_frame = self.tab_bg.main_window.new_tab(name.get())
            tab_pic = TabPicture(tab_frame, self.tab_bg.main_window, name)
            self.operation_command(True)
            tab_pic.vision = copy.copy(self.vision_result)
            tab_pic.refresh()
            self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
            self.vision_result.cvImage_tmp.image = copy.copy(self.tab_bg.vision.cvImage.image)

        def undo():
            self.tab_bg.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab_bg.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def preview():
            self.operation_command()
            # self.vision_result.preview()

        def _exit():
            self.tab_bg.vision.cvImage_tmp.image = None
            self.window.destroy()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)
        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)
        b_refresh = ttk.Button(self.buttons, text="Reload Original Image", command=self.refresh_panel_img)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)
        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)
        b_preview = ttk.Button(self.buttons, text="Preview", command=preview)
        b_preview.pack(side=tk.LEFT, padx=2, after=b_confirm)
        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panel_img(self):
        self.tk_img_background = computer_vision.Vision.resize_tk_image(self.tab_bg.vision.cvImage.image, self.size)
        self.panel_back.configure(image=self.tk_img_background)
        self.panel_back.image = self.tk_img_background
        self.cv_img_result = self.tab_bg.vision.cvImage
        self.draw_result()

    def draw_result(self):
        """

        :return:
        """
        self.image_canvas(self.cv_img_result)
        self.histogram(image=self.cv_img_result.image)


    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        pass
