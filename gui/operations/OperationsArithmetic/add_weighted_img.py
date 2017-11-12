import tkinter as tk

from gui.operations.OperationsArithmetic.add_template import AddTemplate
from gui.tabpicture import TabPicture


class AddWeighted(AddTemplate):
    def __init__(self, tab: TabPicture):
        self.weight_img_1 = tk.DoubleVar()
        self.weight_img_1.set(0.5)
        self.weight_img_2 = tk.DoubleVar()
        self.weight_img_2.set(0.5)

        super().__init__("Dodawanie obrazów", tab)

    def control_plugin(self):
        label_1 = tk.Label(self.plugins, text="Waga tła")
        label_1.pack(side=tk.LEFT)

        entry_1 = tk.Entry(self.plugins, textvariable=self.weight_img_1)
        entry_1.pack(side=tk.LEFT)

        label_2 = tk.Label(self.plugins, text="Waga drugiego")
        label_2.pack(side=tk.LEFT)

        entry_2 = tk.Entry(self.plugins, textvariable=self.weight_img_2)
        entry_2.pack(side=tk.LEFT)

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.ar_add(self.tab_fg.vision.cvImage.image, place,
                                  weight=(self.weight_img_1.get(), self.weight_img_2.get()), preview=preview)
