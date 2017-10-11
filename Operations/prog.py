import utils
import tkinter as tk
from cv2 import *
import cv2
from tkinter import ttk

from Operations.operation_template import OperationTemplate
from computer_vision import Vision
from tabpicture import TabPicture


class OperationLightThreshold(OperationTemplate):
    thresholdTypeOptions = {'Binary': cv2.THRESH_BINARY,
                            'Binary inv': cv2.THRESH_BINARY_INV,
                            'Trunc': cv2.THRESH_TRUNC,
                            'Tozero': cv2.THRESH_TOZERO,
                            'Tozero inv': cv2.THRESH_TOZERO_INV}

    def __init__(self, tab: TabPicture):
        super().__init__("Progowanie", tab)

    def control_plugin(self):
        def threshold(x):
            self.tab.vision.global_prog(float(x),
                                        OperationLightThreshold.thresholdTypeOptions[
                                            tto_v.get()])
            self.refresh_panels()

        def threshold_bind():
            self.tab.vision.global_prog(float(scale.get()), OperationLightThreshold.thresholdTypeOptions[tto_v.get()])
            self.refresh_panels()

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
        tto_v.trace("w", lambda *args: threshold_bind())

        tto_v.set('Binary')
