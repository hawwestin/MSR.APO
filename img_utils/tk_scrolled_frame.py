import tkinter as tk
from tkinter import ttk


# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame


class ScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """

    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set,
                           xscrollcommand=hscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas, name="interior")
        interior_id = canvas.create_window(0, 0,
                                           window=interior,
                                           anchor='nw')

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
            # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
            if interior.winfo_reqheight() != canvas.winfo_height():
            # update the canvas's width to fit the inner frame
                canvas.config(height=interior.winfo_reqheight())

        interior.bind('<Configure>', _configure_interior)

        # def _configure_canvas(event):
        #     if interior.winfo_reqwidth() != canvas.winfo_width():
        #         # update the inner frame's width to fill the canvas
        #         canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        #     if interior.winfo_reqheight() != canvas.winfo_height():
        #         canvas.itemconfigure(interior_id, height=canvas.winfo_height())
        #
        # canvas.bind('<Configure>', _configure_canvas)

        # bind mouse wheel.


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        def __init__(self, *args, **kwargs):
            root = tk.Tk.__init__(self, *args, **kwargs)

            self.frame = ScrolledFrame(root)
            self.frame.pack(expand=True,fill=tk.BOTH)
            buttons = []
            for i in range(10):
                buttons.append(tk.Button(self.frame.interior, text="Button  " + str(i)))
                buttons[-1].pack()

            self.label = tk.Label(text="Shrink the window to activate the scrollbar.")
            self.label.pack()


    app = SampleApp()
    app.mainloop()
