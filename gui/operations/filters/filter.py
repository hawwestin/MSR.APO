import copy
import tkinter as tk
import numpy as np

from gui.operations import computer_vision
from gui.operations.matlib_template import MatLibTemplate
from gui.tabpicture import TabPicture


class Filter(MatLibTemplate):
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
                                                      [1, -2, 1]])),
               "Roberts Gx": ("2x2", np.array([[1, 0],
                                               [0, -1]])),
               "Roberts Gy": ("2x2", np.array([[0, -1],
                                               [1, 0]])),
               "Sobel Gx": ("3x3", np.array([[-1, 0, 1],
                                             [-2, 0, 2],
                                             [-1, 0, 1]])),
               "Soble Gy": ("3x3", np.array([[-1, -2, -1],
                                             [0, 0, 0],
                                             [1, 2, 1]])),
               "Prewitta N": ("3x3", np.array([[1, 1, 1],
                                               [1, -2, 1],
                                               [-1, -1, -1]])),
               "Prewitta NE": ("3x3", np.array([[1, 1, 1],
                                                [-1, -2, 1],
                                                [-1, -1, 1]])),
               "Prewitta E": ("3x3", np.array([[-1, 1, 1],
                                               [-1, -2, 1],
                                               [-1, 1, 1]])),
               "Prewitta SE": ("3x3", np.array([[-1, -1, 1],
                                                [-1, -2, 1],
                                                [1, 1, 1]])),
               "Prewitta S": ("3x3", np.array([[-1, -1, -1],
                                               [1, -2, 1],
                                               [1, 1, 1]])),
               "Prewitta SW": ("3x3", np.array([[1, -1, -1],
                                                [1, -2, -1],
                                                [1, 1, 1]])),
               "Prewitta W": ("3x3", np.array([[1, 1, -1],
                                               [1, -2, -1],
                                               [1, 1, -1]])),
               "Prewitta NW": ("3x3", np.array([[1, 1, 1],
                                                [1, -2, -1],
                                                [1, -1, -1]]))
               }

    def __init__(self, tab: TabPicture):
        super(Filter, self).__init__("Filter", tab)

        self.raw_kernel = None
        self.np_kernel = None

        self.operation_name.set(list(Filter.KERNELS.keys())[0])
        self.kernel_size.set(list(Filter.Kernel_Size.keys())[0])

        self.np_kernel = Filter.KERNELS.get(self.operation_name.get())

        self.kernel_options = tk.Frame(self.lf_bottom)
        self.kernel_grid = tk.Frame(self.lf_bottom)

        self.kernel_panel()
        self.border_type.trace('w', lambda *args: self.operation_command())

        self.window.mainloop()

    def kernel(self):
        _x, _y = Filter.Kernel_Size.get(self.kernel_size.get())
        self.np_kernel = np.zeros((_x, _y))
        for x in range(_x):
            for y in range(_y):
                self.np_kernel[x][y] = self.raw_kernel[x][y].get()
        return self.np_kernel

    def kernel_panel(self):
        om_kernel = tk.OptionMenu(self.kernel_options, self.kernel_size,
                                  *Filter.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid())

        om_operation_name = tk.OptionMenu(self.kernel_options, self.operation_name,
                                          *sorted(Filter.KERNELS.keys()))
        self.operation_name.trace("w", lambda *args: self.kernel_from_list())

        om_border = tk.OptionMenu(self.kernel_options, self.border_type,
                                  *computer_vision.borderType.keys())

        b_preview = tk.Button(self.lf_bottom, text="Preview", command=self.operation_command)

        om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_operation_name.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_border.pack(side=tk.LEFT, padx=2, anchor='nw')
        b_preview.pack(side=tk.BOTTOM, padx=2, anchor='s')
        self.kernel_options.pack(side=tk.TOP)
        self.kernel_grid.pack(side=tk.TOP, anchor='center')

        self.draw_kernel_grid()

    def draw_kernel_grid(self, values=None):
        self.kernel_grid.destroy()
        self.raw_kernel = []

        self.kernel_grid = tk.Frame(self.lf_bottom)
        self.kernel_grid.pack(side=tk.TOP)
        _x, _y = Filter.Kernel_Size.get(self.kernel_size.get())
        for x in range(_x):
            for y in range(_y):
                value = values[x][y] if values is not None else 0
                Bucket(raw=self.raw_kernel, master=self.kernel_grid, x=x, y=y, value=value)

        self.raw_kernel.append(copy.copy(Bucket.ROW))
        Bucket.ROW = []

    def kernel_from_list(self):
        kernel = Filter.KERNELS.get(self.operation_name.get(), None)
        if kernel is not None:
            self.kernel_size.set(kernel[0])
            self.draw_kernel_grid(kernel[1])
            self.operation_command()
        else:
            self.status_message.set('Kernel not found!')

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        self.vision_result.filter(kernel=self.kernel(),
                                  border_type=self.border_type.get())
        self.img_result = self.vision_result.cvImage_tmp.image
        self.draw_result()
        if persist:
            self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)


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
