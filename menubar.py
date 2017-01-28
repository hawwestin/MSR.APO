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

        open = Menu(self.menu, tearoff=0)
        open.add_command(label="Open in Color", command=self._menucmd.open_color_image)
        open.add_command(label="Open in Grey Scale", command=self._menucmd.open_grey_image)

        file = Menu(self.menu, tearoff=0)

        file.add_command(label="New")
        # todo przerobic na otwarcie kolorowego obrazka i szarego
        file.add_cascade(label="Open", menu=open)
        file.add_command(label="Reload", command=self._menucmd.load_image)
        file.add_command(label="Save", command=self._menucmd.save)
        file.add_command(label="Save as", command=self._menucmd.save_as)
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
        edit.add_command(label="Color picker", command=self._menucmd.picker)
        # added "file" to our menu
        self.menu.add_cascade(label="Edit", menu=edit)

        view = Menu(self.menu, tearoff=0)
        view.add_command(label="Full screen")
        view.add_command(label="tab num", command=self._menucmd.imgList)
        self.menu.add_cascade(label="View", menu=view)

        arithmetic = Menu(self.menu, tearoff=0)
        arithmetic.add_command(label="Image Addition", command=self._menucmd.not_implemented)
        arithmetic.add_command(label="Image Blending", command=self._menucmd.not_implemented)
        arithmetic.add_command(label="Bitwise", command=self._menucmd.not_implemented)

        histogram = Menu(self.menu, tearoff=0)
        histogram.add_command(label="Wewnatrz histogram", command=self._menucmd.inHist)
        histogram.add_command(label="Popup hist", command=self._menucmd.outHist)
        histogram.add_command(label="Hist Equalization", command=self._menucmd.hist_Equ)
        histogram.add_command(label="Clear hist", command=self._menucmd.clear_hist)

        punktowe = Menu(self.menu, tearoff=0)
        punktowe.add_command(label="Negacja", command=self._menucmd.negacja)
        punktowe.add_command(label="Progowanie", command=self._menucmd.progowanie)
        punktowe.add_command(label="Progowanie adaptacyjne", command=self._menucmd.adap_progowanie)
        punktowe.add_command(label="Redukcja poziomów szarości", command=self._menucmd.redukcja_p_s)

        operation = Menu(self.menu, tearoff=0)
        operation.add_cascade(label="Histogram", menu=histogram)
        # operation.add_cascade(label="Arithmetic Operations", menu=arithmetic)
        operation.add_cascade(label="Punktowe", menu=punktowe)

        # operation.add_command(label="Sąsiedztwa")
        # operation.add_command(label="Korekcja")
        # operation.add_cascade(label="Segmentacja")
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
