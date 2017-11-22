import copy
import tkinter as tk

from gui.operations import computer_vision
from gui.operations.filters.filters_template import FiltersTemplate


class Smoothing(FiltersTemplate):
    def __init__(self, tab):
        super(Smoothing, self).__init__("Smootihng", tab)

        self.operation_name.set("Median")
        self.kernel_size.set(list(FiltersTemplate.Kernel_Size.keys())[0])

        self.control()

        self.window.mainloop()

    def control(self):
        om_kernel = tk.OptionMenu(self.lf_bottom, self.kernel_size,
                                  *FiltersTemplate.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.operation_command())

        om_border = tk.OptionMenu(self.lf_bottom, self.border_type,
                                  *computer_vision.borderType.keys())
        self.border_type.trace("w", lambda *args: self.operation_command())

        om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_border.pack(side=tk.LEFT, padx=2, anchor='nw')

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        self.vision_result.blur(FiltersTemplate.Kernel_Size.get(self.kernel_size.get()),
                                border_type=self.border_type.get())
        self.img_result = self.vision_result.cvImage_tmp.image
        self.draw_result()
        if persist:
            self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
