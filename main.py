from main_window import MainWindow
from utils import resolution

# creation of an instance
app = MainWindow()

app.geometry(resolution)
# mainloop
app.mainloop()
