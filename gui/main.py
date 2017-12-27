import json
import os
from gui.main_window import MainWindow
import app_config

app = MainWindow()
if os.path.isfile('config.cfg'):
    with open('config.cfg', 'r+') as f:
        # config = f.read()
        config = json.load(f)
        if len(config) > 0:
            config = json.loads(config)
            app_config.main_window_resolution = config["resolution"]
            app_config.image_path = config["path"]

app.geometry(app_config.main_window_resolution)

app.mainloop()

with open('config.cfg', 'w') as f:
    config = {"resolution": app_config.main_window_resolution,
              "path": app_config.image_path}
    json.dump(config, f)
