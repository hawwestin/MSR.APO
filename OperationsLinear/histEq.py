import tkinter as tk
from tkinter import ttk

from OperationsLinear.operation_template import OperationTemplate
from tabpicture import TabPicture


class OperationHistEQ(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("APO Histogram Equalization", tab)

    def control_plugin(self):
        def heq():
            self.tab.vision.hist_eq()
            self.refresh()

        def hnum():
            self.tab.vision.hist_num()
            self.refresh()

        def hcl3():
            self.tab.vision.hist_CLAHE(3, 3)
            self.refresh()

        def hcl8():
            self.tab.vision.hist_CLAHE(8, 8)
            self.refresh()

        def hrand():
            self.tab.vision.hist_rand()
            self.refresh()

        B4 = ttk.Button(self.plugins, text="Hist EQ", command=heq)
        B4.pack(side=tk.LEFT, padx=2)
        # B4.grid(row=0, column=0, sticky='nsew')
        B5 = ttk.Button(self.plugins, text="Hist num", command=hnum)
        B5.pack(side=tk.LEFT, padx=2)
        # B5.grid(row=0, column=1, sticky='nsew')
        B6 = ttk.Button(self.plugins, text="Sąsiedztwa 3x3", command=hcl3)
        B6.pack(side=tk.LEFT, padx=2)
        # B6.grid(row=0, column=2, sticky='nsew')
        B8 = ttk.Button(self.plugins, text="Sąsiedztwa 8x8", command=hcl8)
        B8.pack(side=tk.LEFT, padx=2)
        # B8.grid(row=0, column=3, sticky='nsew')
        b_rand = ttk.Button(self.plugins, text="Metoda losowa", command=hrand)
        b_rand.pack(side=tk.LEFT, padx=2)
