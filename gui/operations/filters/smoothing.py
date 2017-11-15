import copy
import tkinter as tk
from tkinter import ttk
import numpy as np

from app_config import resolution
from gui.operations.computer_vision import Vision
from gui.tabpicture import TabPicture, TabColorPicture, TabGreyPicture
from img_utils.scrolled_frame import ScrolledCanvas


class Smoothing:
    """
    Dictionary to hold all valid filter operations with kernel
    """
    KERNELS = {"Wygładzanie": np.array([[-1, -1, -1],
                                        [-1, 9, -1],
                                        [-1, -1, -1]]),
               "Wyostrzanie": np.array([[1, 1, 1],
                                        [1, -8, 1],
                                        [1, 1, 1]])}

    Kernel_Size = {"3x3": (3, 3),
                   "3x5": (3, 5),
                   "5x3": (5, 3),
                   "5x5": (5, 5),
                   "7x7": (7, 7),
                   }

    def __init__(self, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title("Smoothing")
        self.window.geometry(resolution)

        self.kernel = None
        self.tab_bg = tab
        self.vision_result = Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.size = (300, 300)
        self.tk_img_background = None
        self.img_result = self.tab_bg.vision.cvImage.tk_image
        self.img_fg = None

        self.operation_name = tk.StringVar()
        self.operation_name.set(list(Smoothing.KERNELS.keys())[0])
        self.kernel = Smoothing.KERNELS.get(self.operation_name.get())
        self.kernel_size = tk.StringVar()
        self.kernel_size.set(list(Smoothing.Kernel_Size.keys())[0])

        self.refresh_krenel()

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
        self.kernel_panel = tk.PanedWindow(self.outer_pan, handlesize=10, showhandle=True, handlepad=12, sashwidth=3,
                                           orient=tk.VERTICAL)
        self.kernel_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.outer_pan.add(self.kernel_panel, minsize=100)

        # todo switch self.panels to self.kernel_panel
        lf_back = tk.LabelFrame(master=self.panels, text='Image')
        lf_back.pack()
        self.kernel_panel.add(lf_back, minsize=100)
        self.panel_back = tk.Label(master=lf_back)
        self.panel_back.pack()

        self.lf_kernel = tk.LabelFrame(master=self.panels, text='Kernel')
        self.lf_kernel.pack()
        self.kernel_panel.add(self.lf_kernel, minsize=100)
        om_choose = tk.OptionMenu(self.lf_kernel, self.kernel_size,
                                  *Smoothing.Kernel_Size.keys())
        om_choose.pack(side=tk.TOP, padx=2, anchor='nw')
        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid())
        self.kernel_grid = tk.Frame(self.lf_kernel)
        self.kernel_grid.pack(side=tk.TOP)

        # todo implement displaying current Kernel

        lf_result = tk.LabelFrame(master=self.panels, text='Result')
        lf_result.pack()
        self.can = ScrolledCanvas(lf_result)
        self.can.create_image(0, 0, image=self.img_result, tags="img_bg", anchor='nw')
        self.can.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='nw')
        self.outer_pan.add(lf_result, minsize=100)

        self.draw_kernel_grid()
        self.widget_buttons()

        self.control_plugin()
        self.refresh_panel_img()

        self.window.mainloop()

    def draw_kernel_grid(self):
        self.kernel_grid.destroy()
        self.kernel_grid = tk.Frame(self.lf_kernel)
        self.kernel_grid.pack(side=tk.TOP)
        _x, _y = Smoothing.Kernel_Size.get(self.kernel_size.get())
        for x in range(_x):
            for y in range(_y):
                Bucket(self.kernel_grid, x, y)

    def operation(self):
        kernel = Smoothing.KERNELS.get(self.operation_name.get(), None)
        if kernel is not None:
            self.kernel = kernel
            self.refresh_krenel()
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

            self.vision_result.filter(kernel=self.kernel,
                                      preview=False)
            tab_pic.vision = self.vision_result
            tab_pic.refresh()
            self.vision_result = Vision()
            self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)

        def undo():
            self.tab_bg.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab_bg.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def preview():
            self.vision_result.filter(kernel=self.kernel,
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

        om_choose = tk.OptionMenu(self.buttons, self.operation_name,
                                  *Smoothing.KERNELS.keys())
        om_choose.pack(side=tk.LEFT, padx=2, after=b_refresh)
        self.operation_name.trace("w", lambda *args: self.operation())

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=om_choose)
        b_preview = ttk.Button(self.buttons, text="Preview", command=preview)
        b_preview.pack(side=tk.LEFT, padx=2, after=b_confirm)

        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panel_img(self):
        self.tk_img_background = Vision.resize_tk_image(self.tab_bg.vision.cvImage.image, self.size)
        self.panel_back.configure(image=self.tk_img_background)
        self.panel_back.image = self.tk_img_background

        self.can.update_idletasks()

    def refresh_krenel(self):
        """
        Refresh kernel grid values.
        :return:
        """
        pass

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass


class Bucket:
    GALLERY = {}

    def __init__(self, master: tk.Frame, x, y, value=0):
        self.master = master
        self.x = x
        self.y = y
        self.value = tk.StringVar()
        self.value.set(value)
        self.bucket = tk.Entry(master, textvariable=self.value, width=5)
        vcmd = self.bucket.register(self.check_entry)
        self.bucket.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))
        self.bucket.grid(column=x, row=y, padx=2, pady=2)

    @staticmethod
    def check_entry(why, what):
        if int(why) >= 0:
            if what in '0123456789-.':
                return True
            else:
                return False
        else:
            return True
