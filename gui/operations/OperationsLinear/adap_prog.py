import tkinter as tk

import cv2
from cv2 import *

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class OperationAdaptiveThreshold(OperationTemplate):
    adaptiveMethodOptions = {'Gaussion': cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             'Mean': cv2.ADAPTIVE_THRESH_MEAN_C}
    thresholdTypeOptions = {'Binary': cv2.THRESH_BINARY,
                            'Binary inv': cv2.THRESH_BINARY_INV}

    def __init__(self, tab: TabPicture):
        self.amo_v = tk.StringVar()
        self.tto_v = tk.StringVar()
        self.block = tk.IntVar()
        self.constant = tk.IntVar()
        super().__init__("Progowanie Adaptacyjne", tab)

    def control_plugin(self):
        # todo validate whole input not last digit.
        def check_entry(why, what):
            if int(why) >= 0:
                # todo value in 3<x<11
                if int(what) % 2 == 1:
                    return True
                else:
                    return False
            else:
                return True

        self.amo_v.set(sorted(OperationAdaptiveThreshold.adaptiveMethodOptions.keys())[0])
        self.tto_v.set(sorted(OperationAdaptiveThreshold.thresholdTypeOptions.keys())[0])
        self.block.set(7)
        self.constant.set(3)

        amo_l = tk.Label(self.plugins, text="Metoda progowania")
        amo_l.pack(side=tk.LEFT, padx=2)

        amo = tk.OptionMenu(self.plugins, self.amo_v, *OperationAdaptiveThreshold.adaptiveMethodOptions.keys())
        amo.pack(side=tk.LEFT, padx=2)

        tto_l = tk.Label(self.plugins, text="Typ progowania")
        tto_l.pack(side=tk.LEFT, padx=2)

        tto = tk.OptionMenu(self.plugins, self.tto_v, *OperationAdaptiveThreshold.thresholdTypeOptions.keys())
        tto.pack(side=tk.LEFT, padx=2)

        label_1 = tk.Label(self.plugins, text="Rozmiar bloku \nliczba nieparzysta, >1")
        label_1.pack(side=tk.LEFT, padx=2)

        entry_1 = tk.Entry(self.plugins, textvariable=self.block, width=10)
        vcmd = entry_1.register(check_entry)
        entry_1.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))
        entry_1.pack(side=tk.LEFT, padx=2)

        label_1 = tk.Label(self.plugins, text="Stała do dodania")
        label_1.pack(side=tk.LEFT, padx=2)

        entry_1 = tk.Entry(self.plugins, textvariable=self.constant, width=10)
        entry_1.pack(side=tk.LEFT, padx=2)

        self.amo_v.trace("w", lambda *args: self.operation_command())
        self.tto_v.trace("w", lambda *args: self.operation_command())
        self.tto_v.set(sorted(OperationAdaptiveThreshold.thresholdTypeOptions.keys())[0])

    def operation_command(self, persist=False):
        if self.block.get() > 1:
            self.tab.vision.adaptive_prog(OperationAdaptiveThreshold.adaptiveMethodOptions[self.amo_v.get()],
                                          OperationAdaptiveThreshold.thresholdTypeOptions[self.tto_v.get()],
                                          blockSize=self.block.get(),
                                          C=self.constant.get())
            self.refresh()
            self.status_message.set("*")
            if persist:
                self.tab.persist_tmp()
                self.refresh()
        else:
            self.status_message.set("Rozmiar bloku musi być liczbą nieparzysta i większą od 1")
