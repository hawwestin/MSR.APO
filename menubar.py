from tkinter import *
from menu_command import *
from ComputerVision import *

class mainmenu(Frame):
    def __init__(self, parentFrame, tkController):
        """

        :param parentFrame: Frame
        :param tkController: Tk
        """
        Frame.__init__(self, parentFrame)
        self.tkController = tkController
        # Menu controller
        self.menu = Menu(self.tkController)
        # todo rename image
        # self.image = Vision(controller, self)

        self._menucmd = MenuCmd(self, self.tkController)
        self.menu_bar()


    def menu_bar(self):
        # creating a menu instance
        # menu = Menu(self.master)
        self.tkController.config(menu=self.menu)

        # create the file object
        file = Menu(self.menu, tearoff=0)

        file.add_command(label="New")
        # todo przerobic na otwarcie kolorowego obrazka i szarego
        file.add_command(label="Open", command=self._menucmd.load_image)
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_separator()
        # Tabs Options
        file.add_command(label="Close Current Tab", command=self.tkController.close_Current_tab)
        file.add_separator()
        file.add_command(label="Exit", command=self._menucmd.client_exit)
        self.menu.add_cascade(label="File", menu=file)

        edit = Menu(self.menu, tearoff=0)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        edit.add_separator()
        edit.add_command(label="Duplicate")
        # added "file" to our menu
        self.menu.add_cascade(label="Edit", menu=edit)

        view = Menu(self.menu, tearoff=0)
        view.add_command(label="Full screen")
        view.add_command(label="List of tab", command=self._menucmd.imgList)
        self.menu.add_cascade(label="View", menu=view)

        histogram = Menu(self.menu, tearoff=0)
        histogram.add_command(label="Wewnatrz histogram", command=self._menucmd.inHist)
        histogram.add_command(label="Popup hist", command=self._menucmd.outHist)
        operation = Menu(self.menu, tearoff=0)
        operation.add_cascade(label="Histogram", menu=histogram)
        operation.add_command(label="Punktowe")
        operation.add_command(label="Sąsiedztwa")
        operation.add_command(label="Korekcja")
        operation.add_cascade(label="Segmentacja")
        # operation.add_cascade(label="Stegangorafia")
        # operation.add_cascade(label="Kompresja")
        # operation.add_cascade(label="Opis kszztałtu")
        self.menu.add_cascade(label="Operation", menu=operation)

        help = Menu(self.menu, tearoff=0)
        help.add_command(label="Info", command=self._menucmd.info)
        self.menu.add_cascade(label="Help", menu=help)

        self.tkController.config(menu=self.menu)


    # def statusbar(self):
    #     MainGui.statusmsg = Label(self.tkController, text=MainGui.statusmsg, bd=1, relief=SUNKEN, anchor=W)
    #     MainGui.statusmsg.pack(side=BOTTOM, fill=X)
