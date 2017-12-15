"""
http://cx-freeze.readthedocs.io/en/latest/index.html

Command to run:
python setup.py bdist_msi
"""
import cx_Freeze
import sys
import cv2
import tkinter
import numpy
import matplotlib
import PIL
import app_config
import sample_img

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("gui\main.py", base=base, shortcutName="APO_{}".format(app_config.__VERSION__))]

cx_Freeze.setup(
    name="APO",
    options={"build_exe": {"packages": ["tkinter", "matplotlib", "numpy", "cv2"]}},
    # , "include_files":["clienticon.ico"]}},
    version=app_config.__VERSION__,
    description="APO RobaszewLab17_18",
    executables=executables
)
