import tkinter as tk
from tkinter import ttk

from PIL import ImageTk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from computer_vision import Vision
from utils import resolution
from tabpicture import TabPicture


class OperationTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry(resolution)

        self.tab = tab
        # todo resized Frame ????
        self.size = (500, 500)
        self.img_background = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)
        # todo dialog box or sth to choose other tab or img from hdd.
        self.img_foreground = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)
        # todo brand new Vision
        self.img_result = Vision.resize_tk_image(self.tab.vision.cvImage.image, self.size)

        self.body = tk.Frame(master=self.window)

        self.body.pack(fill=tk.BOTH, expand=True)

        self.buttons = tk.Frame(master=self.body)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        self.plugins = tk.Frame(master=self.body)
        self.plugins.pack(after=self.buttons, side=tk.TOP, fill=tk.X)

        self.panels = tk.Frame(master=self.body)
        self.panels.pack(after=self.plugins, side=tk.TOP, fill=tk.BOTH, expand=True)

        self.status_message = tk.StringVar()
        self.status_message.set('*')
        self.status_bar = tk.Label(self.body, textvariable=self.status_message, bd=1, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        ###############
        # Panels
        ###############
        self.pan = tk.PanedWindow(self.panels, handlesize=10, showhandle=True, handlepad=12, sashwidth=3)
        self.pan.pack(side=tk.TOP, fill=tk.BOTH)

        lf_back = tk.LabelFrame(master=self.panels, text='Background')
        lf_back.pack()
        self.can = tk.Canvas(master=lf_back)
        # img = ImageTk.PhotoImage(Image.fromarray(self.tab.vision.cvImage.image))
        self.can.create_image(1, 1, image=self.img_background, tags="img_background")
        # can.create_image(10, 10, image=self.img_background, tags="img_background")
        # self.can.create_line(10, 10, 200, 50, fill='red', width=3)
        self.can.pack(side=tk.TOP)
        self.pan.add(lf_back, minsize=80)
        # self.panel_back = tk.Label(master=lf_back, image=self.img_background)
        # self.panel_back.pack()

        lf_front = tk.LabelFrame(master=self.panels, text='Foreground')
        lf_front.pack()
        self.pan.add(lf_front, minsize=80)
        self.panel_front = tk.Label(master=lf_front)
        self.panel_front.pack()

        lf_result = tk.LabelFrame(master=self.panels, text='Result')
        lf_result.pack()
        self.pan.add(lf_result, minsize=80)
        self.panel_result = tk.Label(master=lf_result)
        self.panel_result.pack()

        self.widget_buttons()

        self.control_plugin()
        self.refresh_panel_img()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def confirm():
            # todo persist brand new vision in new tab . save path ?
            self.tab.persist_tmp()
            self.refresh_panel_img()

        def _exit():
            self.tab.vision.cvImage_tmp.image = None
            self.window.destroy()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panel_img)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)

        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panel_img(self):
        # todo Drop Resize. !
        # self.img_background = ImageTk.PhotoImage(Image.fromarray(self.tab.vision.cvImage.image))
        # self.panel_back.configure(image=self.img_background)
        # self.panel_back.image = self.img_background
        # if self.tab.vision.cvImage_tmp.image is not None:
        self.img_foreground = ImageTk.PhotoImage(Image.fromarray(self.tab.vision.cvImage.image))
        self.panel_front.configure(image=self.img_foreground)
        self.panel_front.image = self.img_foreground

        self.img_result = ImageTk.PhotoImage(Image.fromarray(self.tab.vision.cvImage.image))
        self.panel_result.configure(image=self.img_result)
        self.panel_result.image = self.img_result

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass
