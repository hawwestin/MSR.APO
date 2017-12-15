import copy
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

        self.kernel_options = tk.Frame(self.lf_bottom)
        self.kernel_grid = tk.Frame(self.lf_bottom)
        self.table = EntryTable(self.kernel_grid, Morphology.Kernel_Size.get(self.kernel_size.get()))

        self.kernel_panel()
        self.border_type.trace('w', lambda *args: self.operation_command())

        self.window.mainloop()

    def kernel_panel(self):
        om_kernel = tk.OptionMenu(self.kernel_options, self.kernel_size,
                                  *Morphology.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.draw_kernel_grid())

        om_operation_name = tk.OptionMenu(self.kernel_options, self.operation_name,
                                          *sorted(self.operations.keys()))
        self.operation_name.trace("w", lambda *args: self.operation_command())

        om_border = tk.OptionMenu(self.kernel_options, self.border_type,
                                  *computer_vision.borderType.keys())

        b_preview = tk.Button(self.lf_bottom, text="Preview", command=self.operation_command)

        om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_operation_name.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_border.pack(side=tk.LEFT, padx=2, anchor='nw')
        b_preview.pack(side=tk.BOTTOM, padx=2, anchor='s')

        self.kernel_options.pack(side=tk.TOP)
        self.kernel_grid.pack(side=tk.TOP, anchor='center', expand=True, fill=tk.BOTH)

        self.draw_kernel_grid()

    def draw_kernel_grid(self, values=None):
        self.table.size = Morphology.Kernel_Size.get(self.kernel_size.get())
        self.table.draw(values)
        self.operation_command()

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        operation = self.operations[self.operation_name.get()]

        operation(kernel=self.table.get_values(),
                  border_type=self.border_type.get())
        self.img_result = self.vision_result.cvImage_tmp.image
        self.draw_result()
        if persist:
            self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
