from tkinter import *
from menu_command import *
from ComputerVision import *

class mainmenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        # Menu controller
        self.menu = Menu(self.controller)
        # todo rename image
        self.image = Vision(controller, self)
        self._menucmd = MenuCmd(self.controller)
        # zbudowanie paneli menu
        self.menu_bar()
        self.statusbar()

    def menu_bar(self):
        # creating a menu instance
        # menu = Menu(self.master)
        self.controller.config(menu=self.menu)

        # create the file object)
        file = Menu(self.menu, tearoff=0)

        file.add_command(label="New")
        # todo przerobic na otwarcie kolorowego obrazka i szarego
        file.add_command(label="Open", command=self._menucmd.load_image)
        # todo do wywalenia
        file.add_command(label="Show", command=self._menucmd.show_img)
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_separator()
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self._menucmd.client_exit)
        # added "file" to our menu
        self.menu.add_cascade(label="File", menu=file)

        edit = Menu(self.menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        edit.add_separator()
        edit.add_command(label="Duplicate")
        # added "file" to our menu
        self.menu.add_cascade(label="Edit", menu=edit)

        view = Menu(self.menu)
        view.add_command(label="Full screen")
        view.add_command(label="picture", command=self._menucmd.show_img)
        self.menu.add_cascade(label="View", menu=view)

        operation = Menu(self.menu)
        # todo rozbicie na 2 akcje , in popupwindow i w aplikacji
        histogram = Menu(self.menu)
        histogram.add_command(label="Wewnatrz histogram", command=MainGui.image.load_hist)
        histogram.add_command(label="Popup hist", command=MainGui.image.show_hist)
        operation.add_cascade(label="Histogram", menu=histogram)
        operation.add_command(label="Punktowe")
        operation.add_command(label="Sąsiedztwa")
        operation.add_command(label="Korekcja")
        operation.add_cascade(label="Segmentacja")
        # operation.add_cascade(label="Stegangorafia")
        # operation.add_cascade(label="Kompresja")
        # operation.add_cascade(label="Opis kszztałtu")
        self.menu.add_cascade(label="Operation", menu=operation)

        help = Menu(self.menu)
        help.add_command(label="Info", command=lambda: self._menucmd.popupmsg("APO Made by Michal R"))
        self.menu.add_cascade(label="Help", menu=help)

        self.controller.config(menu=self.menu)


    def statusbar(self):
        MainGui.statusmsg = Label(self.controller, text=MainGui.statusmsg, bd=1, relief=SUNKEN, anchor=W)
        MainGui.statusmsg.pack(side=BOTTOM, fill=X)
