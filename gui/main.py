from gui.main_window import MainWindow
from app_config import resolution

# creation of an instance
app = MainWindow()

app.geometry(resolution)
# mainloop
app.mainloop()
