import copy
import tkinter as tk
from pprint import pprint
from tkinter import ttk
import numpy as np

from app_config import resolution
from gui.operations import computer_vision
from gui.tabpicture import TabPicture, TabColorPicture, TabGreyPicture
from img_utils.scrolled_frame import ScrolledCanvas


class Smoothing:
    """
    Dictionary to hold all valid filter operations with kernel
    """
    KERNELS = {"Laplasjan Detekcja krawędzi B": ("3x3", np.array([[-1, -1, -1],
                                                                  [-1, 9, -1],
                                                                  [-1, -1, -1]])),
               "Laplasjan a": ("3x3", np.array([[0, -1, 0],
                                                [-1, 4, -1],
                                                [0, -1, 0]])),
               "Laplasjan b": ("3x3", np.array([[-1, -1, -1],
                                                [-1, 8, -1],
                                                [-1, -1, -1]])),
               "Laplasjan c": ("3x3", np.array([[1, -2, 1],
                                                [-2, 4, -2],
                                                [1, -2, 1]])),
               "Laplasjan Detekcja Krawędzi C": ("3x3", np.array([[0, -1, 0],
                                                                  [-1, 5, -1],
                                                                  [0, -1, 0]])),
               "Wygładzanie a": ("3x3", np.array([[1, 1, 1],
                                                  [1, 2, 1],
                                                  [1, 2, 1]])),
               "Wygładzanie b": ("3x3", np.array([[1, 2, 1],
                                                  [2, 4, 2],
                                                  [1, 2, 1]])),
               "Detekcja Krawędzi": ("3x3", np.array([[1, -2, 1],
                                                      [-2, 5, -2],
                                                      [1, -2, 1]]))
               }

    Kernel_Size = {
        "3x3": (3, 3),
        "3x5": (3, 5),
        "5x3": (5, 3),
        "5x5": (5, 5),
        "7x7": (7, 7),
    }

    def __init__(self, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title("Smoothing")
        self.window.geometry(resolution)

        self.raw_kernel = None
        self.np_kernel = None
        self.tab_bg = tab
        self.vision_result = computer_vision.Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.size = (300, 300)
        self.tk_img_background = None
        self.img_result = self.tab_bg.vision.cvImage.tk_image
        self.img_fg = None

        self.operation_name = tk.StringVar()
        self.operation_name.set(list(Smoothing.KERNELS.keys())[0])
        self.np_kernel = Smoothing.KERNELS.get(self.operation_name.get())
        self.kernel_size = tk.StringVar()
        self.kernel_size.set(list(Smoothing.Kernel_Size.keys())[0])
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
        lf_back = tk.LabelFrame(master=self.panels, text='Image')
        lf_back.pack()
        self.left_panned_window.add(lf_back, minsize=100)

        self.panel_back = tk.Label(master=lf_back)
        self.panel_back.pack()

        self.lf_kernel = tk.LabelFrame(master=self.panels, text='Kernel')
        self.lf_kernel.pack()
        self.left_panned_window.add(self.lf_kernel, minsize=100)

        self.kernel_options = tk.Frame(self.lf_kernel)
        self.kernel_grid = tk.Frame(self.lf_kernel)

        lf_result = tk.LabelFrame(master=self.panels, text='Result')
        lf_result.pack()
        self.can = ScrolledCanvas(lf_result)
        self.can.create_image(0, 0, image=self.img_result, tags="img_bg", anchor='nw')
        self.can.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='nw')
        self.outer_pan.add(lf_result, minsize=100)

        self.widget_buttons()
        self.kernel_panel()

        self.control_plugin()
        self.refresh_panel_img()

        self.window.mainloop()

    def kernel(self):
        _x, _y = Smoothing.Kernel_Size.get(self.kernel_size.get())
        self.np_kernel = np.zeros((_x, _y))
        for x in range(_x):
            for y in range(_y):
                self.np_kernel[x][y] = self.raw_kernel[x][y].get()
        return self.np_kernel

    def kernel_panel(self):
        om_kernel = tk.OptionMenu(self.kernel_options, self.kernel_size,
                                  *Smoothing.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid())

        om_operation_name = tk.OptionMenu(self.kernel_options, self.operation_name,
                                          *Smoothing.KERNELS.keys())
        self.operation_name.trace("w", lambda *args: self.kernel_from_list())

        om_border = tk.OptionMenu(self.kernel_options, self.border_type,
                                  *computer_vision.borderType.keys())

        om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_operation_name.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_border.pack(side=tk.LEFT, padx=2, anchor='nw')
        self.kernel_options.pack(side=tk.TOP)
        self.kernel_grid.pack(side=tk.TOP, anchor='center')

        self.draw_kernel_grid()

    def draw_kernel_grid(self, values=None):
        self.kernel_grid.destroy()
        self.raw_kernel = []

        self.kernel_grid = tk.Frame(self.lf_kernel)
        self.kernel_grid.pack(side=tk.TOP)
        _x, _y = Smoothing.Kernel_Size.get(self.kernel_size.get())
        for x in range(_x):
            for y in range(_y):
                value = values[x][y] if values is not None else 0
                Bucket(raw=self.raw_kernel, master=self.kernel_grid, x=x, y=y, value=value)

        self.raw_kernel.append(copy.copy(Bucket.ROW))
        Bucket.ROW = []
        # pprint(self.raw_kernel)

    def kernel_from_list(self):
        kernel = Smoothing.KERNELS.get(self.operation_name.get(), None)
        if kernel is not None:
            self.kernel_size.set(kernel[0])
            self.draw_kernel_grid(kernel[1])
        else:
            self.status_message.set('Kernel not found!')

    def widget_buttons(self):
        def confirm():
            name = tk.StringVar()
            name.set("*" + self.tab_bg.name.get())
            tab_frame = self.tab_bg.main_window.new_tab(name.get())
            if self.tab_bg.vision.color is True:
                tab_pic = TabColorPicture(tab_frame, self.tab_bg.main_window, name)
            else:
                tab_pic = TabGreyPicture(tab_frame, self.tab_bg.main_window, name)

            self.vision_result.filter(kernel=self.kernel(),
                                      border_type=self.border_type.get(),
                                      preview=False)
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
            self.vision_result.filter(kernel=self.kernel(),
                                      border_type=self.border_type.get(),
                                      preview=True)

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

        self.can.update_idletasks()

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass


class Bucket:
    ROW = []

    def __init__(self, raw, master: tk.Frame, x, y, value=0):
        self.master = master
        self.x = x
        self.y = y
        self.value = tk.StringVar()
        self.value.set(value)
        self.bucket = tk.Entry(master, textvariable=self.value, width=3)
        vcmd = self.bucket.register(self.check_entry)
        self.bucket.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))
        self.bucket.grid(column=x, row=y, padx=2, pady=2)

        """
        Append to GRID
        """
        if y >= len(Bucket.ROW):
            Bucket.ROW.append(self.value)
        else:
            raw.append(copy.copy(Bucket.ROW))
            Bucket.ROW = [self.value]

    @staticmethod
    def check_entry(why, what):
        if int(why) >= 0:
            if what in '0123456789-.':
                return True
            else:
                return False
        else:
            return True
