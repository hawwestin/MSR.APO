import tkinter as tk

from OperationsLinear.operation_template import OperationTemplate
from tabpicture import TabPicture


class OperationLightLeveling(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Redukcja poziomow szarosci", tab)

    def control_plugin(self):
        def rps(x):
            self.tab.vision.rps(x)
            self.refresh()

        slider = tk.Frame(self.plugins)
        slider.pack()

        sl = tk.Scale(slider, orient=tk.HORIZONTAL, from_=1, to=255, length=500)
        sl.configure(command=lambda x: rps(int(x)))
        sl.pack(expand=1, anchor='nw')
