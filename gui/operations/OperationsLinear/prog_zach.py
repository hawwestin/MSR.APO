import tkinter

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class OperationLightThresholdKeepingValue(OperationTemplate):
    def __init__(self, tab: TabPicture):
        self.p1 = tkinter.StringVar()
        self.p2 = tkinter.StringVar()
        super().__init__("Progowanie z zachowaniem poziomów szarości", tab)

    def control_plugin(self):
        def check_entry(why, what):
            if int(why) >= 0:
                if what in "0123456789":
                    return True
                else:
                    return False
            else:
                return True

        self.p1.set(50)
        self.p2.set(150)

        p1_l = tkinter.Label(self.plugins, text="p1")
        p1_l.pack(side=tkinter.LEFT, padx=2)
        p1_e = tkinter.Entry(self.plugins, textvariable=self.p1)
        p1_e.pack(side=tkinter.LEFT, padx=2)
        p2_l = tkinter.Label(self.plugins, text="p2")
        p2_l.pack(side=tkinter.LEFT, padx=2)
        p2_e = tkinter.Entry(self.plugins, textvariable=self.p2)
        p2_e.pack(side=tkinter.LEFT, padx=2)

        vcmd1 = p1_e.register(check_entry)
        vcmd2 = p2_e.register(check_entry)
        p1_e.configure(validate='key', validatecommand=(vcmd1, '%d', '%S'))
        p2_e.configure(validate='key', validatecommand=(vcmd2, '%d', '%S'))

        self.p1.trace("w", lambda *args: self.operation_command())
        self.p2.trace("w", lambda *args: self.operation_command())

    def operation_command(self, persist=False):
        if self.p1.get() != "" and self.p2.get() != "":
            if int(self.p1.get()) == int(self.p2.get()):
                self.status_message.set("p1 and p2 can't by equal")
            else:
                self.tab.vision.progowanie_z_zachowaniem_poziomow(int(self.p1.get()), int(self.p2.get()))
                self.refresh()
                self.status_message.set("*")
