import cx_Freeze
import sys
import cv2
import tkinter
import numpy
import matplotlib
import PIL

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name="APO",
    options={"build_exe": {"packages": ["tkinter", "matplotlib", "numpy", "cv2"]}},
    # , "include_files":["clienticon.ico"]}},
    version="0.01",
    description="RobaszewLab17_18)",
    executables=executables
)
