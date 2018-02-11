import logging
import tkinter as tk

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class OperationLightLeveling(OperationTemplate):
    def __init__(self, tab: TabPicture):
        self.scale_value = tk.StringVar()
        super().__init__("Redukcja poziomow szarosci", tab)

    def control_plugin(self):
        slider = tk.Frame(self.plugins)
        slider.pack()

        sl = tk.Scale(slider,
                      orient=tk.HORIZONTAL,
                      from_=1,
                      to=255,
                      length=500,
                      variable=self.scale_value)
        self.scale_value.trace("w", lambda *args: self.operation_command())
        sl.pack(expand=1, anchor='nw')
        sl.set(127)

    def operation_command(self, persist=False):
        try:
            self.tab.vision.rps(int(self.scale_value.get()))
            self.refresh()
            self.status_message.set("*")
            if persist:
                self.tab.persist_tmp()
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")


