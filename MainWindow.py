# coding=utf-8
from tkinter import *
from tkinter import filedialog
#my py
from ComputerVision import *
from imgtree import *
from menubar import *
import os
import MainGui
from PIL import Image
import matplotlib.pyplot as plt


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    # panelA = None
    # panelB = None
    # image = None
    # statusmsg = None

    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # self.statusmsg = None

        # init a CV instance
        MainGui.image = Vision()
        self.imgtree = img_tree(master)

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("APO")

        # Panel is a box to display an image
        # MainGui.panelA = None
        # Panel to preview changed image
        # MainGui.panelB = None

        # allowing the widget to take the full space of the root window
        # self.pack(fill=BOTH, expand=1)
        # self.menubar()

        mainmenu(self.master)

        # self.statusbar()

    # def statusbar(self):
    #     self.statusmsg = Label(self.master, text=self.statusmsg, bd=1, relief=SUNKEN, anchor=W)
    #     self.statusmsg.pack(side=BOTTOM, fill=X)

    def menubar(self):
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        file.add_command(label="New")
        file.add_command(label="Open", command=self.select_image)
        file.add_command(label="Show", command=self.show_img)
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_separator()
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        edit.add_separator()
        edit.add_command(label="Duplicate")
        # added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        view = Menu(menu)
        view.add_command(label="Full screen")
        view.add_command(label="picture", command=self.show_img)
        menu.add_cascade(label="View", menu=view)

        operation = Menu(menu)
        operation.add_command(label="Histogram", command=self.image.show_hist)
        operation.add_command(label="Punktowe")
        operation.add_command(label="Sąsiedztwa")
        operation.add_command(label="Korekcja")
        operation.add_cascade(label="Segmentacja")
        # operation.add_cascade(label="Stegangorafia")
        # operation.add_cascade(label="Kompresja")
        # operation.add_cascade(label="Opis kszztałtu")
        menu.add_cascade(label="Operation", menu=operation)

        self.master.config(menu=menu)

    def client_exit(self):
        exit()

    def treelist(self):
        """
        Lista obrazkowu przechowywana w tree liscie plikow po lewej stronie ekranu
        z mozliwoscia rozszerzenia .
        :return:
        """
        # todo https://docs.python.org/3.5/library/tkinter.ttk.html?highlight=ttk#treeview
        self.not_implemented()

    def show_img(self):
        """
        Logic : odpalenie okna z obrazkiem ktore  ma wlasne Menu do operacji.
        Kazde okienko to nowy obiekt.
        Undowanie na tablicach ? może pod spodem baze danych machnac

        :return:
        """
        # plt.imshow(self.image, cmap='Greys', interpolation='bicubic')
        # plt.show()
        # if the panels are None, initialize them
        if self.panelA is None:
            self.panelA = Label(image=self.image.tkImage)
            # self.panelA.image = self.image.tkImage
            self.panelA.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panelA.configure(image=self.image.tkImage)
            # self.panelA.image = self.image.tkImage

    def select_image(self):
        # open a file chooser dialog and allow the user to select an input
        # image
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
        path = filedialog.askopenfilename()
        # self.statusbar()
        self.statusmsg.configure(text=os.path.splitext(path)[0])

        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk and init CV
            # nowy obiekt ? okno ? jak wiele okien ?
            self.image.open_img(path)
            self.show_img()

    def not_implemented(self):
        print("not implemented")


