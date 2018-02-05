"""
http://cx-freeze.readthedocs.io/en/latest/index.html

Command to run:
python setup.py bdist_msi
"""
from cx_Freeze import setup, Executable
import sys
import app_config
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

build_exe_options = {
    "packages": ["tkinter", "matplotlib", "numpy", "cv2"],
    "include_files": [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
    ]
    # , "include_files":["clienticon.ico"]
}

shortcutName = "APO_{}".format(app_config.__VERSION__)
executables = [Executable("gui\main.py", base=base, shortcutName=shortcutName), ]

setup(
    name="APO",
    options=dict(build_exe=build_exe_options),
    version=app_config.__VERSION__,
    description="APO RobaszewLab17_18",
    executables=executables
)
