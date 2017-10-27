import tkinter as tk

from menu_command import MenuCmd


class MainMenu(tk.Frame):
    def __init__(self, parent_frame, main_window):
        """

        :param parent_frame: Frame
        :param main_window: Tk
        """
        tk.Frame.__init__(self, parent_frame)
        self.tkController = main_window
        self.menu = tk.Menu(self.tkController)
        self.tkController.config(menu=self.menu)

        self._menucmd = self.tkController.command
        self.menu_bar()

    @property
    def menu_cmd(self) -> MenuCmd:
        return self._menucmd

    def menu_bar(self):
        file_open = tk.Menu(self.menu, tearoff=0)
        file_open.add_command(label="Open in Color", command=self.menu_cmd.open_color_image)
        file_open.add_command(label="Open in Grey Scale", command=self.menu_cmd.open_grey_image)

        file = tk.Menu(self.menu, tearoff=0)
        file.add_command(label="New", command=self.menu_cmd.new_img)
        file.add_cascade(label="Open", menu=file_open)
        file.add_command(label="Reload", command=self.menu_cmd.load_image)
        file.add_command(label="Save", command=self.menu_cmd.save)
        file.add_command(label="Save as", command=self.menu_cmd.save_as)
        file.add_separator()  # Tabs Options
        file.add_command(label="Close Current Tab", command=self.tkController.close_Current_tab)
        file.add_separator()
        file.add_command(label="Exit", command=self.menu_cmd.client_exit)

        edit = tk.Menu(self.menu, tearoff=0)
        edit.add_command(label="Undo", command=self.menu_cmd.undo_image)
        edit.add_command(label="Redo", command=self.menu_cmd.redo_image)
        edit.add_separator()
        edit.add_command(label="Duplicate", command=self.menu_cmd.duplicate)
        edit.add_command(label="Color picker", command=self._menucmd.picker)

        # view = tk.Menu(self.menu, tearoff=0)
        # view.add_command(label="Full screen")
        # view.add_command(label="tab num", command=self._menucmd.imgList)
        # self.menu.add_cascade(label="View", menu=view)

        histogram = tk.Menu(self.menu, tearoff=0)
        histogram.add_command(label="Wewnatrz histogram", command=self._menucmd.inHist)
        histogram.add_command(label="Popup hist", command=self._menucmd.outHist)
        histogram.add_command(label="Hist Equalization", command=self._menucmd.hist_Equ)

        points = tk.Menu(self.menu, tearoff=0)
        points.add_command(label="Negacja", command=self._menucmd.negation)
        points.add_command(label="Binaryzacja", command=self._menucmd.light_threshold)
        points.add_command(label="Progowanie z zachowaniem poziomów szarości",
                           command=self._menucmd.progowanie_z_zachowaniem)
        points.add_command(label="Redukcja poziomów szarości", command=self._menucmd.redukcja_p_s)
        points.add_command(label="Rozciąganie", command=self._menucmd.stretching)
        points.add_command(label="Progowanie adaptacyjne", command=self._menucmd.adaptive_light_threshold)
        points.add_command(label="Uniwersalna operacja jednopunktowa", command=self._menucmd.uop)

        arithmetic = tk.Menu(self.menu, tearoff=0)
        arithmetic.add_command(label="Dodawanie", command=self._menucmd.add_img)
        # arithmetic.add_command(label="Image Blending", command=self._menucmd.not_implemented)
        # arithmetic.add_command(label="Bitwise", command=self._menucmd.not_implemented)

        operation = tk.Menu(self.menu, tearoff=0)
        operation.add_cascade(label="Histogram", menu=histogram)
        operation.add_cascade(label="Punktowe", menu=points)
        operation.add_cascade(label="Arithmetic Operations", menu=arithmetic)
        # operation.add_command(label="Sąsiedztwa")
        # operation.add_command(label="Korekcja")
        # operation.add_cascade(label="Segmentacja")
        # operation.add_cascade(label="Stegangorafia")
        # operation.add_cascade(label="Kompresja")
        # operation.add_cascade(label="Opis kszztałtu")

        help = tk.Menu(self.menu, tearoff=0)
        help.add_command(label="Info", command=self._menucmd.info)
        help.add_command(label="debug", command=self.tkController.tab_index)

        self.menu.add_cascade(label="File", menu=file)
        self.menu.add_cascade(label="Edit", menu=edit)
        self.menu.add_cascade(label="Operation", menu=operation)
        self.menu.add_cascade(label="Help", menu=help)

        self.tkController.config(menu=self.menu)
