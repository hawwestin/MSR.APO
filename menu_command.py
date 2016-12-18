from tkinter import *
from tkinter import filedialog
import MainGui
import os

class menucmd(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.statusmsg= None
        # self.image = None
        # Panel is a box to display an image
        self.panelA = None # todo przenieść do MainWindow

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
        if MainGui.panelA is None:
            MainGui.panelA = Label(image=MainGui.image.tkImage)
            # self.panelA.image = self.image.tkImage
            MainGui.panelA.pack(side="left", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            MainGui.panelA.configure(image=MainGui.image.tkImage)
            # self.panelA.image = self.image.tkImage

    def select_image(self):
        # open a file chooser dialog and allow the user to select an input
        # image
        # todo potrzeba blokowac i sprawdzac czy wybrany plik jest obrazkiem o dozwolonym typie
        path = filedialog.askopenfilename()
        # self.statusbar()
        MainGui.statusmsg.configure(text=os.path.splitext(path)[0])

        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk and init CV
            # nowy obiekt ? okno ? jak wiele okien ?
            MainGui.image.open_img(path)
            self.show_img()

    def not_implemented(self):
        print("not implemented")
