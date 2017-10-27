import tkinter

from OperationsLinear.operation_template import OperationTemplate
from tabpicture import TabPicture


class OperationLightThresholdKeepingValue(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Progowanie z zachowaniem poziomów szarości", tab)

    def control_plugin(self):
        def stretch():
            if int(p1.get()) == int(p2.get()):
                self.status_message.set("p1 and p2 can't by equal")
                return
            self.tab.vision.progowanie_z_zachowaniem_poziomow(int(p1.get()), int(p2.get()))
            self.refresh()

        p1 = tkinter.IntVar()
        p2 = tkinter.IntVar()

        p1_l = tkinter.Label(self.plugins, text="p1")
        p1_l.pack(side=tkinter.LEFT, padx=2)
        p1_e = tkinter.Entry(self.plugins, textvariable=p1)
        p1_e.pack(side=tkinter.LEFT, padx=2)
        p2_l = tkinter.Label(self.plugins, text="p2")
        p2_l.pack(side=tkinter.LEFT, padx=2)
        p2_e = tkinter.Entry(self.plugins, textvariable=p2)
        p2_e.pack(side=tkinter.LEFT, padx=2)

        button = tkinter.Button(self.plugins, text="stretch", command=stretch)
        button.pack(side=tkinter.LEFT, padx=2)
