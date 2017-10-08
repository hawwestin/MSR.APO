import tkinter as tk
from tkinter import ttk

from tabpicture import TabPicture


class OperationTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry("1024x720")

        self.tab = tab

        self.body = tk.Frame(master=self.window)

        self.body.pack(fill=tk.BOTH, expand=True)

        self.buttons = tk.Frame(master=self.body)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        self.controls = tk.Frame(master=self.body)
        self.controls.pack(after=self.buttons, side=tk.TOP, fill=tk.X)

        self.panels = tk.Frame(master=self.body)
        self.panels.pack(after=self.controls, side=tk.TOP, fill=tk.BOTH, expand=True)

        ###############
        # Panels
        ###############
        lf_original = tk.LabelFrame(master=self.panels, text='Original')
        lf_original.pack(side=tk.LEFT)
        self.panel = tk.Label(master=lf_original, image=self.tab.vision.tkImage)
        lf_equalised = tk.LabelFrame(master=self.panels, text='Equalised')
        lf_equalised.pack(side=tk.LEFT, after=lf_original)
        self.panel_tmp = tk.Label(master=lf_equalised)

        self.frame_for_Canvas = tk.Frame(master=self.panels)

        self.panel.pack()
        self.panel_tmp.pack()
        self.frame_for_Canvas.pack(side=tk.RIGHT)

        self.widget_buttons()

        self.control_plugin()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab.vision.cvImage.undo()
            self.tab.vision.tkImage = self.tab.vision.cvImage.tk_image
            self.refresh_panels()

        def redo():
            self.tab.vision.cvImage.redo()
            self.tab.vision.tkImage = self.tab.vision.cvImage.tk_image
            self.refresh_panels()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panels)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        b_exit = ttk.Button(self.buttons, text="Exit", command=self.window.destroy)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panels(self):
        self.panel_tmp.configure(image=self.tab.vision.tkImage_tmp)
        self.panel.configure(image=self.tab.vision.tkImage)
        self.panel_tmp.image = self.tab.vision.tkImage_tmp
        self.panel.image = self.tab.vision.tkImage
        # todo Refresh Histogram

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass
