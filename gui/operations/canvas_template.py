import copy
import tkinter as tk
from tkinter import ttk

from app_config import resolution
from gui.operations.computer_vision import Vision
from gui.tabpicture import TabPicture, TabColorPicture, TabGreyPicture
from img_utils.scrolled_canvas import ScrolledCanvas


class CanvasTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry(resolution)

        self.tab_bg = tab
        self.tab_fg = None
        self.vision_result = Vision()
        self.vision_result.cvImage.image = copy.copy(self.tab_bg.vision.cvImage.image)
        self.size = (300, 300)
        self.tk_img_background = None
        self.tk_img_foreground = None
        self.img_result = self.tab_bg.vision.cvImage.tk_image
        self.img_fg = None

        self.foreground_name = tk.StringVar()
        self.foreground_name.set(self.tab_bg.name.get())

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
        self.outer_pan = tk.PanedWindow(self.panels, handlesize=10, showhandle=True, handlepad=12, sashwidth=3)
        self.outer_pan.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_pan = tk.PanedWindow(self.outer_pan, handlesize=10, showhandle=True, handlepad=12, sashwidth=3,
                                       orient=tk.VERTICAL)
        self.left_pan.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.outer_pan.add(self.left_pan, minsize=100)

        lf_back = tk.LabelFrame(master=self.panels, text='Background')
        lf_back.pack()
        self.left_pan.add(lf_back, minsize=100)
        self.panel_back = tk.Label(master=lf_back)
        self.panel_back.pack()

        lf_front = tk.LabelFrame(master=self.panels, text='Foreground')
        lf_front.pack()
        self.left_pan.add(lf_front, minsize=100)
        self.panel_front = tk.Label(master=lf_front)
        self.panel_front.pack()

        # todo with transparent
        lf_result = tk.LabelFrame(master=self.panels, text='Result')
        lf_result.pack()
        self.can = ScrolledCanvas(lf_result)
        self.can.create_image(0, 0, image=self.img_result, tags="img_bg", anchor='nw')
        self.can.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='nw')
        self.outer_pan.add(lf_result, minsize=100)

        self.can.configure(scrollregion=(0, 0, self.img_result.width(), self.img_result.height()))

        self.widget_buttons()

        self.control_plugin()
        self.refresh_panel_img()

        self.window.mainloop()

    def _drag_img(self, event):
        self.can.coords('img_f', event.x, event.y)

    def blend(self):
        self.img_fg = self.tab_fg.vision.cvImage.tk_image
        if len(self.can.find_above('img_bg')) > 0:
            self.can.delete('img_f')
        self.can.create_image(0, 0, image=self.img_fg, tags="img_f", anchor='nw')
        self.can.tag_bind("img_f", "<B1-Motion>", self._drag_img, add=True)
        y = self.img_fg.height() if self.img_fg.height() > self.img_result.height() else self.img_result.height()
        x = self.img_fg.width() if self.img_fg.width() > self.img_result.width() else self.img_result.width()
        self.can.configure(scrollregion=(0, 0, x, y))
        self.can.update_idletasks()

    def widget_buttons(self):
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

        def undo():
            self.tab_bg.vision.cvImage.undo(self.status_message)
            self.refresh_panel_img()

        def redo():
            self.tab_bg.vision.cvImage.redo(self.status_message)
            self.refresh_panel_img()

        def preview():
            self.operation_command(True)

        def _exit():
            self.tab_bg.vision.cvImage_tmp.image = None
            self.window.destroy()

        def choose_foreground():
            chose = TabPicture.search(self.foreground_name.get())
            if len(chose) > 0:
                self.tab_fg = chose[0]
                self.blend()
                self.refresh_panel_img()
            else:
                self.status_message.set("Error reading and img")

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panel_img)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        om_choose = tk.OptionMenu(self.buttons, self.foreground_name,
                                  *[tab.name.get() for tab in TabPicture.gallery.values()])
        om_choose.pack(side=tk.LEFT, padx=2, after=b_refresh)
        self.foreground_name.trace("w", lambda *args: choose_foreground())

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=om_choose)
        b_preview = ttk.Button(self.buttons, text="Preview", command=preview)
        b_preview.pack(side=tk.LEFT, padx=2, after=b_confirm)

        b_exit = ttk.Button(self.buttons, text="Exit", command=_exit)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panel_img(self):
        self.tk_img_background = Vision.resize_tk_image(self.tab_bg.vision.cvImage.image, self.size)
        self.panel_back.configure(image=self.tk_img_background)
        self.panel_back.image = self.tk_img_background
        if self.tab_fg is not None:
            self.tk_img_foreground = Vision.resize_tk_image(self.tab_fg.vision.cvImage.image, self.size)
            self.panel_front.configure(image=self.tk_img_foreground)
            self.panel_front.image = self.tk_img_foreground

        self.can.update_idletasks()
        # self.img_result = ImageTk.PhotoImage(Image.fromarray(self.tab.vision.cvImage.image))
        # self.panel_result.configure(image=self.img_result)
        # self.panel_result.image = self.img_result

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass

    def operation_command(self, preview):
        """
        Mock method to be filled by concrete operation.
        :param preview:
        :return:
        """
        pass
