import utils
import tkinter as tk
from cv2 import *
import cv2
from tkinter import ttk

from Operations.operation_template import OperationTemplate
from computer_vision import Vision
from tabpicture import TabPicture


class OperationAdaptiveThreshold(OperationTemplate):
    adaptiveMethodOptions = {'Gaussion': cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             'Mean': cv2.ADAPTIVE_THRESH_MEAN_C}
    thresholdTypeOptions = {'Binary': cv2.THRESH_BINARY,
                            'Binary inv': cv2.THRESH_BINARY_INV}

    def __init__(self, tab: TabPicture):
        super().__init__("Progowanie Adaptacyjne", tab)

    # TODO jezeli wybrana opcje z kolorowego obrazka powinna byc informacja ze nastapi konwersja na szary .
    def control_plugin(self):
        def threshold():
            self.tab.vision.adaptive_prog(OperationAdaptiveThreshold.adaptiveMethodOptions[amo_v.get()],
                                          OperationAdaptiveThreshold.thresholdTypeOptions[tto_v.get()])
            self.refresh_panels()

        amo_v = tk.StringVar()
        amo_v.set('Mean')

        tto_v = tk.StringVar()
        tto_v.set('Binary')

        amo_l = tk.Label(self.plugins, text="Metoda progowania")
        amo_l.grid(row=0, column=0, sticky='nsew')

        amo = tk.OptionMenu(self.plugins, amo_v, *OperationAdaptiveThreshold.adaptiveMethodOptions.keys())
        amo.grid(row=0, column=1, sticky='nsew')

        tto_l = tk.Label(self.plugins, text="Typ progowania")
        tto_l.grid(row=0, column=2, sticky='nsew')

        tto = tk.OptionMenu(self.plugins, tto_v, *OperationAdaptiveThreshold.thresholdTypeOptions.keys())
        tto.grid(row=0, column=3, sticky='nsew')

        amo_v.trace("w", lambda *args: threshold())
        tto_v.trace("w", lambda *args: threshold())
        tto_v.set('Binary')
