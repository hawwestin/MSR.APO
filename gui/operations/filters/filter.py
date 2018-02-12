import copy
import tkinter as tk
import numpy as np
import logging

from gui.operations import computer_vision
from gui.operations.matlib_template import MatLibTemplate
from gui.tabpicture import TabPicture
from img_utils.EntryTable import EntryTable


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
                                                                  [-1, 4, -1],
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
               "HP2": ("3x3", np.array([[1, -2, 1],
                                        [-2, 5, -2],
                                        [1, -2, 1]])),
               "Prewitta NW": ("3x3", np.array([[1, 1, 1],
                                                [1, -2, -1],
                                                [1, -1, -1]]))
               }

    def __init__(self, tab: TabPicture):
        super(Filter, self).__init__("Filter", tab)

        self.raw_kernel = None
        self.np_kernel = None
        self.operation_name_2 = tk.StringVar()
        self.kernel_size_2 = tk.StringVar()
        self.border_type_2 = tk.StringVar()

        self.bundle_1 = (self.kernel_size, self.operation_name, self.border_type)
        self.bundle_2 = (self.kernel_size_2, self.operation_name_2, self.border_type_2)

        self.operation_name.set(list(Filter.KERNELS.keys())[0])
        self.kernel_size.set(list(Filter.Kernel_Size.keys())[0])
        self.operation_name_2.set(list(Filter.KERNELS.keys())[0])
        self.kernel_size_2.set(list(Filter.Kernel_Size.keys())[0])
        self.border_type_2.set(list(computer_vision.borderType.keys())[0])

        self.np_kernel = Filter.KERNELS.get(self.operation_name.get())

        self.kernel_options_1 = tk.Frame(self.options_panned_frame)
        self.kernel_options_2 = tk.Frame(self.options_panned_frame)
        self.kernel_grid = tk.Frame(self.options_panned_frame)
        self.kernel_grid_2 = tk.Frame(self.options_panned_frame)

        self.table = EntryTable(self.kernel_grid, Filter.Kernel_Size.get(self.kernel_size.get()))
        self.table_2 = EntryTable(self.kernel_grid_2, Filter.Kernel_Size.get(self.kernel_size_2.get()))

        self.phase_var = tk.StringVar()
        self.phase_var.set(0)
        self.phase = tk.Checkbutton(self.options_panned_frame, variable=self.phase_var, text="Druga Faza")

        self.kernel_panel(self.kernel_options_1, self.bundle_1)
        self.kernel_panel(self.kernel_options_2, self.bundle_2)

        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid(self.table, self.bundle_1))
        self.operation_name.trace("w", lambda *args: self.kernel_from_list(self.table, self.bundle_1))
        self.border_type.trace('w', lambda *args: self.operation_command())

        self.kernel_size_2.trace("w", lambda *args: self.draw_kernel_grid(self.table_2, self.bundle_2))
        self.operation_name_2.trace("w", lambda *args: self.kernel_from_list(self.table_2, self.bundle_2))
        self.border_type_2.trace('w', lambda *args: self.operation_command())

        self.kernel_options_1.pack(side=tk.TOP, anchor='nw')
        self.kernel_grid.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.phase.pack(side=tk.TOP, anchor='n')
        self.kernel_options_2.pack(side=tk.TOP, anchor='nw')
        self.kernel_grid_2.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.draw_kernel_grid(self.table, self.bundle_1)
        self.draw_kernel_grid(self.table_2, self.bundle_2)

        b_preview = tk.Button(self.options_panned_frame, text="Preview", command=self.operation_command)
        b_preview.pack(side=tk.BOTTOM, padx=2, anchor='s')

        self.window.mainloop()

    def kernel_panel(self, master, vars: tuple):
        l_kernel = tk.Label(master, text="Wielkość rdzenia")
        om_kernel = tk.OptionMenu(master, vars[0],
                                  *Filter.Kernel_Size.keys())

        l_operation_name = tk.Label(master, text="Typ Operacji")
        om_operation_name = tk.OptionMenu(master, vars[1],
                                          *sorted(Filter.KERNELS.keys()))

        l_border_type = tk.Label(master, text="Pixele brzegowe")
        om_border = tk.OptionMenu(master, vars[2],
                                  *computer_vision.borderType.keys())

        l_operation_name.grid(row=0, column=0, sticky='nw')
        l_border_type.grid(row=1, column=0, sticky='nw')
        l_kernel.grid(row=2, column=0, sticky='nw')

        om_operation_name.grid(row=0, column=1, sticky='nw')
        om_border.grid(row=1, column=1, sticky='nw')
        om_kernel.grid(row=2, column=1, sticky='nw')

        # om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        # om_operation_name.pack(side=tk.LEFT, padx=2, anchor='nw')
        # om_border.pack(side=tk.LEFT, padx=2, anchor='nw')

    def draw_kernel_grid(self, table: EntryTable, vars: tuple, values=None):
        table.size = Filter.Kernel_Size.get(vars[0].get())
        table.draw(values)

    def kernel_from_list(self, table, vars):
        kernel = Filter.KERNELS.get(vars[1].get(), None)
        if kernel is not None:
            vars[0].set(kernel[0])
            self.draw_kernel_grid(table, vars, kernel[1])
            self.operation_command()
        else:
            self.status_message.set('Kernel not found!')

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        try:
            self.vision_result.filter(kernel=self.table.get_values(),
                                      border_type=self.border_type.get(),
                                      image=self.vision_result.cvImage.image)
            if int(self.phase_var.get()) == 1:
                self.vision_result.filter(kernel=self.table_2.get_values(),
                                          border_type=self.border_type_2.get(),
                                          image=self.vision_result.cvImage_tmp.image)
            self.cv_img_result = self.vision_result.cvImage_tmp
            self.draw_result()
            if persist:
                self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")
        else:
            logging.info("Filter operation Succeed")
