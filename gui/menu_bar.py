import tkinter as tk

from gui.menu_command import MenuCmd


class MainMenu(tk.Frame):
    def __init__(self, parent_frame, main_window):
        """

        :param parent_frame: Frame
        :param main_window: Tk
        """
        tk.Frame.__init__(self, parent_frame)
        self.tkController = main_window
        self.menu = tk.Menu(self.tkController)
        self.points = tk.Menu(self.menu, tearoff=0)
        self.tkController.config(menu=self.menu)

        self._menucmd = self.tkController.command
        self.menu_bar()

        self.bind_all('<<NotebookTabChanged>>', func=self.color_mode)

    def color_mode(self, x=None):
        if not self.menu_cmd.color_mode():
            self.points.entryconfig("Progowanie adaptacyjne", state="normal")
        else:
            self.points.entryconfig("Progowanie adaptacyjne", state="disabled")

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
        file.add_command(label="Reload", command=self.menu_cmd.reload_image)
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
        edit.add_command(label="Convert to RGB", command=self.menu_cmd.gray_2_rgb)
        edit.add_command(label="Convert to Gray", command=self.menu_cmd.rgb_2_gray)
        edit.add_command(label="Refresh Image", command=self.menu_cmd.reload_image)

        # view = tk.Menu(self.menu, tearoff=0)
        # view.add_command(label="Full screen")
        # view.add_command(label="tab num", command=self._menucmd.img_list)
        # self.menu.add_cascade(label="View", menu=view)

        self.points.add_command(label="Negacja", command=self.menu_cmd.negation)
        self.points.add_command(label="Binaryzacja", command=self.menu_cmd.light_threshold)
        self.points.add_command(label="Dwu argumentowe metody",
                           command=self.menu_cmd.progowanie_z_zachowaniem)
        self.points.add_command(label="Redukcja poziomów szarości", command=self.menu_cmd.redukcja_p_s)
        self.points.add_command(label="Progowanie adaptacyjne", command=self.menu_cmd.adaptive_light_threshold)
        self.points.add_command(label="Uniwersalna operacja jednopunktowa", command=self.menu_cmd.uop)

        kernels = tk.Menu(self.menu, tearoff=0)
        kernels.add_command(label="Uniwersalne filtry", command=self.menu_cmd.filter)
        kernels.add_command(label="Blurowanie", command=self.menu_cmd.smooth)

        operation = tk.Menu(self.menu, tearoff=0)
        operation.add_command(label="Equalizacja Histogram", command=self.menu_cmd.hist_equ)
        operation.add_cascade(label="Jednopunktowe", menu=self.points)
        operation.add_command(label="Arytmetyczne", command=self.menu_cmd.arithmetics)
        operation.add_command(label="Logiczne", command=self.menu_cmd.logic_all)
        operation.add_cascade(label="Sąsiedztwa", menu=kernels)
        operation.add_command(label="Morfologiczne", command=self.menu_cmd.morphologic)
        operation.add_command(label="Hough", command=self.menu_cmd.hough)
        # operation.add_command(label="Korekcja")
        # operation.add_cascade(label="Segmentacja")
        # operation.add_cascade(label="Stegangorafia")
        # operation.add_cascade(label="Kompresja")
        # operation.add_cascade(label="Opis kszztałtu")

        help = tk.Menu(self.menu, tearoff=0)
        help.add_command(label="Info", command=self.menu_cmd.info)

        self.menu.add_cascade(label="File", menu=file)
        self.menu.add_cascade(label="Edit", menu=edit)
        self.menu.add_cascade(label="Operation", menu=operation)
        self.menu.add_cascade(label="Help", menu=help)

        self.tkController.config(menu=self.menu)
