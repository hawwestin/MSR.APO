import tkinter as tk
import app_config


LARGE_FONT = app_config.LARGE_FONT
NORM_FONT = app_config.NORM_FONT
SMALL_FONT = app_config.SMALL_FONT


def popup_message_box(msg):
    popup = tk.Toplevel()
    popup.wm_title("Info")
    # popup.geometry("240x180")
    label = tk.Label(popup, text=msg, font=NORM_FONT, justify=tk.CENTER)
    label.pack(pady=20, padx=20)
    b1 = tk.Button(popup, text="ok", command=popup.destroy)
    b1.pack(side=tk.BOTTOM, pady=20)
    popup.mainloop()
