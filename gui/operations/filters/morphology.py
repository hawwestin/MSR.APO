import copy
import logging
import tkinter as tk
import numpy as np

from gui.operations import computer_vision
from gui.operations.matlib_template import MatLibTemplate
from gui.tabpicture import TabPicture
from img_utils.EntryTable import EntryTable


class Morphology(MatLibTemplate):
    """
    Dictionary to hold all valid filter operations with kernel
    """

    def __init__(self, tab: TabPicture):
        super(Morphology, self).__init__("Morphological Operations", tab)

        self.raw_kernel = None
        self.np_kernel = None

        self.iterations = tk.StringVar()
        self.iterations.set("1.0")

        self.operations = {"Erozja": self.vision_result.erode,
                           "Otwarcie": self.vision_result.opening,
                           "Zamykanie": self.vision_result.closing,
                           "Dylatacja": self.vision_result.dilate,
                           "GRADIENT": self.vision_result.GRADIENT,
                           "TOPHAT": self.vision_result.TOPHAT,
                           "BLACKHAT": self.vision_result.BLACKHAT,
                           "Szkeiletyzacja": self.vision_result.skeleton
                           }

        self.operation_name.set(sorted(self.operations.keys())[0])
        self.kernel_size.set(list(Morphology.Kernel_Size.keys())[0])

        self.np_kernel = self.operations.get(self.operation_name.get())

        self.kernel_options = tk.Frame(self.options_panned_frame)
        self.kernel_grid = tk.Frame(self.options_panned_frame)
        self.table = EntryTable(self.kernel_grid, Morphology.Kernel_Size.get(self.kernel_size.get()))

        self.kernel_panel()
        self.border_type.trace('w', lambda *args: self.operation_command())
        self.iterations.trace('w', lambda *args: self.operation_command())

        self.window.mainloop()

    def kernel_panel(self):
        def check_entry(why, what):
            if int(why) >= 0:
                if what in '0123456789':
                    return True
                else:
                    return False
            else:
                return True

        l_kernel = tk.Label(self.kernel_options, text="Wielkość rdzenia")
        om_kernel = tk.OptionMenu(self.kernel_options, self.kernel_size,
                                  *Morphology.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid())

        l_operation_name = tk.Label(self.kernel_options, text="Typ Operacji")
        om_operation_name = tk.OptionMenu(self.kernel_options, self.operation_name,
                                          *sorted(self.operations.keys()))
        self.operation_name.trace("w", lambda *args: self.operation_command())

        l_border_type = tk.Label(self.kernel_options, text="Pixele brzegowe")
        om_border = tk.OptionMenu(self.kernel_options, self.border_type,
                                  *computer_vision.borderType.keys())

        l_iterator = tk.Label(self.kernel_options, text="Liczba iteracji")
        s_iteration = tk.Spinbox(self.kernel_options, from_=1.0, to=100.0, increment=1.0, textvariable=self.iterations)
        vcmd = s_iteration.register(check_entry)
        s_iteration.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))

        l_operation_name.grid(row=0, column=0, sticky='nw')
        l_border_type.grid(row=1, column=0, sticky='nw')
        l_iterator.grid(row=2, column=0, sticky='nw')
        l_kernel.grid(row=3, column=0, sticky='nw')

        om_operation_name.grid(row=0, column=1, sticky='nw')
        om_border.grid(row=1, column=1, sticky='nw')
        s_iteration.grid(row=2, column=1, sticky='nw')
        om_kernel.grid(row=3, column=1, sticky='nw')

        self.kernel_options.pack(side=tk.TOP, anchor='nw', fill=tk.X)
        self.kernel_grid.pack(side=tk.TOP, anchor='center', expand=True, fill=tk.BOTH)

        self.draw_kernel_grid()

    def draw_kernel_grid(self, values=None):
        self.table.size = Morphology.Kernel_Size.get(self.kernel_size.get())
        self.table.draw(values)
        self.operation_command()

    def operation_validate(self) -> bool:
        if self.iterations.get() is '':
            self.status_message.set("Unsuported iteration value")
            return False
        if self.operation_name.get() == "Szkeiletyzacja" and Morphology.Kernel_Size.get(self.kernel_size.get()) < (
                3, 3):
            self.status_message.set("Skeletonization possible with kernel at least 3X3")
            return False
        if self.operation_name.get() == "Szkeiletyzacja" and self.vision_result.cvImage.color:
            self.status_message.set("Skeletonization possible ONLY with gray scale image")
            return False

        return True

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        try:
            if not self.operation_validate():
                return
            self.status_message.set("*")
            operation = self.operations[self.operation_name.get()]

            operation(kernel=self.table.get_values(),
                      border_type=self.border_type.get(),
                      iterations=int(self.iterations.get()))
            self.cv_img_result = self.vision_result.cvImage_tmp
            self.draw_result()
            if persist:
                self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")
