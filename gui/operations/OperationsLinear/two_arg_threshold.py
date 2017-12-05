import tkinter as tk

from gui.operations.operation_template import OperationTemplate
from gui.tabpicture import TabPicture


class TwoArgLightThreshold(OperationTemplate):
    def __init__(self, tab: TabPicture):
        self.p1 = tk.StringVar()
        self.p2 = tk.StringVar()
        self.operations = {}
        self.operation_name = tk.StringVar()
        super().__init__("Dwu argumentowe metody", tab)

    def control_plugin(self):
        def check_entry(why, what):
            if int(why) >= 0:
                if what in "0123456789":
                    return True
                else:
                    return False
            else:
                return True

        self.operations = {
            "Progowanie z zachowaniem poziomów szarości": self.tab.vision.progowanie_z_zachowaniem_poziomow,
            "Rozciąganie": self.tab.vision.image_stretching}
        self.operation_name.set(sorted(self.operations.keys())[0])
        self.p1.set(50)
        self.p2.set(150)

        om_choose = tk.OptionMenu(self.plugins, self.operation_name,
                                  *sorted(self.operations.keys()))
        om_choose.pack(side=tk.LEFT, padx=2)

        p1_l = tk.Label(self.plugins, text="p1")
        p1_l.pack(side=tk.LEFT, padx=2)
        p1_e = tk.Entry(self.plugins, textvariable=self.p1)
        p1_e.pack(side=tk.LEFT, padx=2)
        p2_l = tk.Label(self.plugins, text="p2")
        p2_l.pack(side=tk.LEFT, padx=2)
        p2_e = tk.Entry(self.plugins, textvariable=self.p2)
        p2_e.pack(side=tk.LEFT, padx=2)

        vcmd1 = p1_e.register(check_entry)
        vcmd2 = p2_e.register(check_entry)
        p1_e.configure(validate='key', validatecommand=(vcmd1, '%d', '%S'))
        p2_e.configure(validate='key', validatecommand=(vcmd2, '%d', '%S'))

        self.p1.trace("w", lambda *args: self.operation_command())
        self.p2.trace("w", lambda *args: self.operation_command())

        self.operation_command()

    def operation_command(self, persist=False):
        if self.p1.get() != "" and self.p2.get() != "":
            if int(self.p1.get()) == int(self.p2.get()):
                self.status_message.set("p1 and p2 can't by equal")
            else:
                operation = self.operations[self.operation_name.get()]
                operation(int(self.p1.get()), int(self.p2.get()))
                self.refresh()
                self.status_message.set("*")
                if persist:
                    self.tab.persist_tmp()
