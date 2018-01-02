import logging

from gui.operations.canvas_template import CanvasTemplate
from gui.tabpicture import TabPicture
import tkinter as tk

from img_utils.rect_tracker import RectTracker


class ArithmeticOperations(CanvasTemplate):
    def __init__(self, tab: TabPicture):
        self.operations = {}
        self.operation_name = tk.StringVar()
        self.rect = None
        self.weight_img_1 = tk.DoubleVar()
        self.weight_img_1.set(0.5)
        self.weight_img_2 = tk.DoubleVar()
        self.weight_img_2.set(0.5)

        super().__init__("Operacje arytmetyczne", tab)

    def control_plugin(self):
        self.rect = RectTracker(self.can)
        self.operations = {"Odejmowanie obrazka": self.vision_result.ar_diff,
                           "Wycinanie zaznaczenia": self.vision_result.image_cut,
                           "Wklejanie obrazka": self.vision_result.img_paste,
                           "Wstawianie z wagami": self.vision_result.ar_add
                           }
        self.operation_name.set(sorted(self.operations.keys())[0])
        label_1 = tk.Label(self.plugins, text="Waga tła")
        label_1.pack(side=tk.LEFT)

        entry_1 = tk.Entry(self.plugins, textvariable=self.weight_img_1)
        entry_1.pack(side=tk.LEFT)

        label_2 = tk.Label(self.plugins, text="Waga drugiego")
        label_2.pack(side=tk.LEFT)

        entry_2 = tk.Entry(self.plugins, textvariable=self.weight_img_2)
        entry_2.pack(side=tk.LEFT)

        om_choose = tk.OptionMenu(self.plugins, self.operation_name,
                                  *sorted(self.operations.keys()))
        om_choose.pack(side=tk.LEFT, padx=20, after=entry_2)

    def operation_command(self):
        try:
            img_place = self.can.coords('img_f')
            rect_place = self.can.coords('rect')
            operation = self.operations[self.operation_name.get()]

            if self.tab_fg is not None:
                operation(source=self.tab_fg.vision.cvImage.image,
                          img_place=img_place,
                          rect_place=rect_place,
                          weight=(self.weight_img_1.get(), self.weight_img_2.get()))
            else:
                operation(img_place=img_place,
                          rect_place=rect_place,
                          weight=(self.weight_img_1.get(), self.weight_img_2.get()))
        except Exception as ex:
            logging.exception(ex)
            self.status_message.set("Operation have Failed check given options!")
