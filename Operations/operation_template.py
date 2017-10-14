import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from tabpicture import TabPicture


class OperationTemplate:
    def __init__(self, name, tab: TabPicture):
        self.window = tk.Toplevel()
        self.window.title(name)
        self.window.geometry("1024x720")

        self.tab = tab
        self.tab.vision.size = (300, 600)
        self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.current())

        self.body = tk.Frame(master=self.window)

        self.body.pack(fill=tk.BOTH, expand=True)

        self.buttons = tk.Frame(master=self.body)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        self.plugins = tk.Frame(master=self.body)
        self.plugins.pack(after=self.buttons, side=tk.TOP, fill=tk.X)

        self.panels = tk.Frame(master=self.body)
        self.panels.pack(after=self.plugins, side=tk.TOP, fill=tk.BOTH, expand=True)

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
        self.hist_pos_label = tk.Label(master=self.frame_for_Canvas)

        self.panel.pack()
        self.panel_tmp.pack()
        self.frame_for_Canvas.pack(side=tk.RIGHT)
        self.hist_pos_label.pack(side=tk.TOP)

        self.toolbar = None
        self.histCanvas = None
        self.fig = Figure()
        self.fig_subplot = self.fig.add_subplot(111)

        self.widget_buttons()

        self.control_plugin()
        self.refresh_panels()

        self.window.mainloop()

    def widget_buttons(self):
        def undo():
            self.tab.vision.cvImage.undo()
            self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.current())
            self.refresh_panels()

        def redo():
            self.tab.vision.cvImage.redo()
            self.tab.vision.tkImage = self.tab.vision.prepare_tk_image(self.tab.vision.cvImage.current())
            self.refresh_panels()

        def confirm():
            self.tab.persist_tmp()
            self.refresh_panels()

        b_undo = ttk.Button(self.buttons, text="Undo", command=undo)
        b_undo.pack(side=tk.LEFT, padx=2)

        b_redo = ttk.Button(self.buttons, text="Redo", command=redo)
        b_redo.pack(side=tk.LEFT, padx=2, after=b_undo)

        b_refresh = ttk.Button(self.buttons, text="Refresh images", command=self.refresh_panels)
        b_refresh.pack(side=tk.LEFT, padx=2, after=b_redo)

        b_confirm = ttk.Button(self.buttons, text="Confirm", command=confirm)
        b_confirm.pack(side=tk.LEFT, padx=2, after=b_refresh)

        b_exit = ttk.Button(self.buttons, text="Exit", command=self.window.destroy)
        b_exit.pack(side=tk.RIGHT, padx=2)

    def refresh_panels(self):
        self.panel_tmp.configure(image=self.tab.vision.tkImage_tmp)
        self.panel.configure(image=self.tab.vision.tkImage)
        self.panel_tmp.image = self.tab.vision.tkImage_tmp
        self.panel.image = self.tab.vision.tkImage
        self.histogram()
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)
        # todo Refresh Histogram

    def on_plot_hover(self, event):
        if event.xdata is not None:
            if event.xdata <=256:
                x = int(event.xdata)
                y = int(self.tab.vision.calculate_hist()[int(event.xdata)])
                self.hist_pos_label.config(text="{}:{}".format(x, y))

    def histogram(self):
        self.fig_subplot.clear()
        self.fig_subplot.bar(range(0, 256), self.tab.vision.calculate_hist(), width=1)
        # self.fig_subplot.hist(self.tab.vision.cvImage_tmp.ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
        # self.fig_subplot.hist(self.tab.vision.cvImage.current().ravel(), bins=256, range=[0.0, 256.0], alpha=0.5)
        self.fig_subplot.set_xlim([-1, 256])

        if self.histCanvas is None:
            self.histCanvas = FigureCanvasTkAgg(self.fig, self.frame_for_Canvas)
        self.histCanvas.show()

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2TkAgg(self.histCanvas,
                                                   self.frame_for_Canvas)
        self.toolbar.update()

        self.histCanvas.get_tk_widget().pack(side=tk.TOP,
                                             fill=tk.BOTH,
                                             expand=True)

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        pass
