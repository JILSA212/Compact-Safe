import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
#import CompactSafe

file_name = "Hello"

def Open_file():
    filepath = askopenfilename(initialdir="/", title="Open a file", filetypes=[("All files","*.*")])
    file_name = filepath
    if not file_name:
        file_name = ""
        return

def Open_folder():
    folderpath = askdirectory()
    file_name = folderpath
    if not file_name:
        file_name = ""
        return