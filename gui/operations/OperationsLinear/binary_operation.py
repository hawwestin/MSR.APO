"""
Binaryzacja
"""
import logging
import tkinter as tk

import cv2
from cv2 import *

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class OperationLightThreshold(OperationTemplate):
    thresholdTypeOptions = {'Binary': cv2.THRESH_BINARY,
                            'Binary inv': cv2.THRESH_BINARY_INV,
                            'Trunc': cv2.THRESH_TRUNC,
                            'Tozero': cv2.THRESH_TOZERO,
                            'Tozero inv': cv2.THRESH_TOZERO_INV}

    def __init__(self, tab: TabPicture):
        self.operations = {}
        self.operation_name = tk.StringVar()
        super().__init__("Binaryzacja", tab)

    def control_plugin(self):
        def threshold(x):
            try:
                self.tab.vision.global_prog(float(x),
                                            OperationLightThreshold.thresholdTypeOptions[
                                                tto_v.get()])
                self.refresh()
            except Exception as ex:
                logging.exception(ex)
                self.status_message.set("Operation have Failed check given options!")

        def threshold_bind():
            try:
                self.tab.vision.global_prog(float(scale.get()), OperationLightThreshold.thresholdTypeOptions[tto_v.get()])
                self.refresh()
            except Exception as ex:
                logging.exception(ex)
                self.status_message.set("Operation have Failed check given options!")

        self.operations = {"threshold": lambda x: threshold(x),
                           "threshold_bind": threshold_bind}

        tto_v = tk.StringVar()
        tto_v.set('Binary')

        type_label = tk.Label(self.plugins, text="Typ progowania")
        type_label.grid(column=0, row=0)

        thresh_options = tk.OptionMenu(self.plugins, tto_v, *OperationLightThreshold.thresholdTypeOptions.keys())
        thresh_options.grid(column=1, row=0)

        slider = tk.Frame(self.plugins)
        slider.grid(column=2, row=0)
        scale = tk.Scale(slider, orient=tk.HORIZONTAL, to=255, length=500)
        scale.configure(command=lambda x: threshold(x))
        scale.pack(expand=1)
        scale.set(127)
        tto_v.trace("w", lambda *args: threshold_bind())
        tto_v.set('Binary')

    def operation_command(self, persist=False):
        try:
            if persist:
                self.tab.persist_tmp()
            self.status_message.set("*")
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")
