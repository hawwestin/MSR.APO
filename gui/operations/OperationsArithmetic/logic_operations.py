import tkinter as tk

from gui.operations.canvas_template import CanvasTemplate
from gui.tabpicture import TabPicture


class LogicOperations(CanvasTemplate):
    def __init__(self, tab: TabPicture):
        self.OPERATIONS = {}
        self.operation_name = tk.StringVar()

        super(LogicOperations, self).__init__("Operacje Logiczne", tab)

    def control_plugin(self):
        self.OPERATIONS = {'Or': self.vision_result.logic_or,
                           'And': self.vision_result.logic_and,
                           'Xor': self.vision_result.logic_xor}
        self.operation_name.set(list(self.OPERATIONS.keys())[0])

        description = tk.Label(self.plugins, text='Dostępne operacje')
        description.pack(side=tk.LEFT, anchor='nw')
        om_operation = tk.OptionMenu(self.plugins, self.operation_name,
                                     *self.OPERATIONS.keys())
        om_operation.pack(side=tk.LEFT, anchor='nw')

    def operation_command(self, preview):
        place = self.can.coords('img_f')

        self.OPERATIONS.get(self.operation_name.get())(self.tab_bg.vision.cvImage.image,
                                                       self.tab_fg.vision.cvImage.image,
                                                       place)
        if preview:
            self.vision_result.preview()
