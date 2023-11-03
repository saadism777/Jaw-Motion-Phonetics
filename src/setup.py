import sys
import os
from cx_Freeze import setup, Executable

files= ['']

target =  Executable(
    script = "main.py",
    base = "Win32GUI"
    icon =  ""
)