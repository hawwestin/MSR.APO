import copy
import tkinter as tk
from tkinter import ttk

from app_config import resolution
from gui.operations.computer_vision import Vision
from gui.tabpicture import TabPicture, TabColorPicture, TabGreyPicture
from img_utils.rect_tracker import RectTracker
from img_utils.scrolled_frame import ScrolledCanvas


class Substraction:
    def __init__(self, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title("Wycinanie fragmentów")
        self.window.geometry(resolution)

        self.tab_bg = tab
        self.vision_result = Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.tk_img_background = None
        self.img_result = self.tab_bg.vision.cvImage.tk_image

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
        lf_result = tk.LabelFrame(master=self.panels, text='Result')
        lf_result.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.can = ScrolledCanvas(lf_result)
        self.can.create_image(0, 0, image=self.img_result, tags="img_bg", anchor='nw')
        self.can.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='nw')
        y = self.img_result.height()
        x = self.img_result.width()
        self.can.configure(scrollregion=(0, 0, x, y))

        self.rect = RectTracker(self.can)

        self.widget_buttons()

        self.control_plugin()
        self.refresh_panel_img()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab_bg.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab_bg.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def preview():
            self.operation_command(True)

        def confirm():
            name = tk.StringVar()
            name.set("*" + self.tab_bg.name.get())
            tab_frame = self.tab_bg.main_window.new_tab(name.get())
            if self.tab_bg.vision.color is True:
                tab_pic = TabColorPicture(tab_frame, self.tab_bg.main_window, name)
            else:
                tab_pic = TabGreyPicture(tab_frame, self.tab_bg.main_window, name)
            self.operation_command(False)
            self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)
            tab_pic.vision = self.vision_result
            tab_pic.refresh()
            self.vision_result = Vision()
            self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)

        def _exit():
            self.tab_bg.vision.cvImage_tmp.image = None
            self.window.destroy()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panel_img)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)
        b_preview = ttk.Button(self.buttons, text="Preview", command=preview)
        b_preview.pack(side=tk.LEFT, padx=2, after=b_confirm)

        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panel_img(self):
        self.can.update_idletasks()

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.image_cut(place)
        if preview:
            self.vision_result.preview()
