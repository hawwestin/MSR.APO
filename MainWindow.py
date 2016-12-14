# coding=utf-8
from tkinter import *
from tkinter import filedialog
import ComputerVision
from PIL import Image
import matplotlib.pyplot as plt


""" # Old version of Shit

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "right"})

"""

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    panelA = None
    panelB = None
    image = None

    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        #init a CV instance
        self.image = ComputerVision.Vision()
        # Panel is a box to display an image
        self.panelA = None
        # Panel to preview changed image
        self.panelB = None
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("APO")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

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
        #operation.add_cascade(label="Stegangorafia")
        #operation.add_cascade(label="Kompresja")
        #operation.add_cascade(label="Opis kszztałtu")
        menu.add_cascade(label="Operation", menu=operation)

        self.master.config(menu=menu)

    def client_exit(self):
        exit()


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
        if self.panelA is None or self.panelB is None:
            # the first panel will store our original image
            self.panelA = Label(image=self.image.tkImage)
            self.panelA.image = self.image.tkImage
            self.panelA.pack(side="left", padx=10, pady=10)

            # while the second panel will store the edge map
            # panelB = Label(image=edged)
            # panelB.image = edged
            # panelB.pack(side="right", padx=10, pady=10)

        # otherwise, update the image panels
        else:
            # update the pannels
            self.panelA.configure(image=self.image.tkImage)
            # panelB.configure(image=edged)
            self.panelA.image = self.image.tkImage
            # panelB.image = edged


    def select_image(self):
        # open a file chooser dialog and allow the user to select an input
        # image
        path = filedialog.askopenfilename()

        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk and init CV
            # nowy obiekt ? okno ? jak wiele okien ?
            self.image.open_img(path)
