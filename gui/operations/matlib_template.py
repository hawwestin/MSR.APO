import copy
import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.pyplot import Figure

from app_config import resolution
from gui.operations import computer_vision
from gui.tabpicture import TabPicture, TabColorPicture, TabGreyPicture
from img_utils.scrolled_frame import ScrolledCanvas


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
        self.window.geometry(resolution)

        self.tab_bg = tab
        self.vision_result = computer_vision.Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.size = (300, 300)
        self.tk_img_background = None
        self.img_result = self.tab_bg.vision.cvImage.image

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

        self.lf_bottom = tk.LabelFrame(master=self.panels, text='Filter')
        self.lf_bottom.pack()
        self.left_panned_window.add(self.lf_bottom, minsize=100)

        self.lf_result = tk.LabelFrame(master=self.panels, text='Result')
        self.lf_result.pack()
        self.outer_pan.add(self.lf_result, minsize=100)

        self.fig = Figure(tight_layout=True)
        self.fig_subplot = self.fig.add_subplot(111)

        self.ml_canvas = FigureCanvasTkAgg(self.fig, self.lf_result)
        self.ml_canvas.show()
        self.ml_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='nw')
        self.toolbar = NavigationToolbar2TkAgg(self.ml_canvas, self.lf_result)
        self.toolbar.update()

        self.widget_buttons()

        self.refresh_panel_img()
        self.draw_result()

    def widget_buttons(self):
        def confirm():
            name = tk.StringVar()
            name.set("*" + self.tab_bg.name.get())
            tab_frame = self.tab_bg.main_window.new_tab(name.get())
            if self.tab_bg.vision.color is True:
                tab_pic = TabColorPicture(tab_frame, self.tab_bg.main_window, name)
            else:
                tab_pic = TabGreyPicture(tab_frame, self.tab_bg.main_window, name)

            self.operation_command(True)
            tab_pic.vision = self.vision_result
            tab_pic.refresh()
            self.vision_result = computer_vision.Vision()
            self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)

        def undo():
            self.tab_bg.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab_bg.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def preview():
            self.operation_command()

        def _exit():
            self.tab_bg.vision.cvImage_tmp.image = None
            self.window.destroy()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)
        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)
        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panel_img)
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

    def draw_result(self):
        """

        :return:
        """
        # FIXME With no clearing subplot ram is rising in usages!!!
        # self.fig_subplot.clear()
        self.fig_subplot.imshow(self.img_result,
                                cmap='gray',
                                interpolation='none',
                                vmin=0,
                                vmax=255,
                                aspect='equal')
        self.toolbar.draw()

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        pass
