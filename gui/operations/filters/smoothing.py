import copy
import logging
import tkinter as tk

from gui.operations import computer_vision
from gui.operations.matlib_template import MatLibTemplate


class Smoothing(MatLibTemplate):
    def __init__(self, tab):
        super(Smoothing, self).__init__("Smootihng", tab)

        self.operation_name.set("Median")
        self.kernel_size.set(list(MatLibTemplate.Kernel_Size.keys())[0])

        self.control()

        self.window.mainloop()

    def control(self):
        l_kernel = tk.Label(self.options_panned_frame, text="Kernel size")
        l_border = tk.Label(self.options_panned_frame, text="Border type")
        om_kernel = tk.OptionMenu(self.options_panned_frame, self.kernel_size,
                                  *MatLibTemplate.Kernel_Size.keys())
        self.kernel_size.trace("w", lambda *args: self.operation_command())

        om_border = tk.OptionMenu(self.options_panned_frame, self.border_type,
                                  *computer_vision.borderType.keys())
        self.border_type.trace("w", lambda *args: self.operation_command())

        l_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_kernel.pack(side=tk.LEFT, padx=2, anchor='nw')
        l_border.pack(side=tk.LEFT, padx=2, anchor='nw')
        om_border.pack(side=tk.LEFT, padx=2, anchor='nw')

    def operation_command(self, persist=False):
        """
        Mock method to be filled by concrete operation.
        :param persist:
        :return:
        """
        try:
            self.vision_result.blur(MatLibTemplate.Kernel_Size.get(self.kernel_size.get()),
                                    border_type=self.border_type.get())
            self.img_result = self.vision_result.cvImage_tmp.image
            self.draw_result()
            if persist:
                self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")
