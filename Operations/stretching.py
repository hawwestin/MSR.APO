import tkinter

from Operations.operation_template import OperationTemplate
from tabpicture import TabPicture


class OperationStretching(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Rozciąganie", tab)

    def control_plugin(self):
        def stretch():
            self.tab.vision.image_stretching(int(p1.get()), int(p2.get()))
            self.refresh()

        p1 = tkinter.IntVar()
        p2 = tkinter.IntVar()

        p1_e = tkinter.Entry(self.plugins, textvariable=p1)
        p1_e.pack()
        p2_e = tkinter.Entry(self.plugins, textvariable=p2)
        p2_e.pack()

        button = tkinter.Button(self.plugins, text="stretch", command=stretch)
        button.pack()
