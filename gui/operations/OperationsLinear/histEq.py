import tkinter as tk

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class OperationHistEQ(OperationTemplate):
    def __init__(self, tab: TabPicture):
        self.operation_name = tk.StringVar()
        self.operations = None

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

        self.operations = {"Hist EQ": heq,
                           "Hist num": hnum,
                           "Sąsiedztwa 3x3": hcl3,
                           "Sąsiedztwa 8x8": hcl8,
                           "Metoda losowa": hrand}

        operation_label = tk.Label(self.plugins, text="nazwa operacji")
        om_choose = tk.OptionMenu(self.plugins, self.operation_name,
                                  *sorted(self.operations.keys()))

        operation_label.pack(side=tk.LEFT, padx=2)
        om_choose.pack(side=tk.LEFT, padx=2)

        self.operation_name.trace("w", lambda *args: self.operation_command())
        self.operation_name.set(sorted(self.operations.keys())[0])

    def operation_command(self, persist=False):
        try:
            operation = self.operations[self.operation_name.get()]
            operation()
            if persist:
                self.tab.persist_tmp()
                self.refresh()
        except:
            self.status_message.set("Operation have Failed check given options!")
