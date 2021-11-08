import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from Compression.Compress_gzip import Compress_using_gzip
from Compression.Compress_bzip2 import Compress_using_bzip2
from Compression.Compress_LZMA import Compress_using_LZMA
from Compression.Compress_custom import Compress_using_custom
from Encryption.AES_Encrypt import AESEncrypt

def Open_file():
    filepath = askopenfilename(initialdir="/", title="Open a file", filetypes=[("All files","*.*")])
    file_path["text"] = filepath
    if not filepath:
        file_path["text"] = ""
        return

def Open_folder():
    folderpath = askdirectory()
    file_path["text"] = folderpath
    if not folderpath:
        file_path["text"] = ""
        return

def Compression_toggle():
    if(Compression_value.get()==0):
        for child in Compression_frame.winfo_children():
            child.configure(state="disabled")
    else:
        for child in Compression_frame.winfo_children():
            child.configure(state="normal")
        Compression_algo.configure(state="readonly")
        File_name_toggle()

def File_name_toggle():
    if(File_name_check.get()==0):
        Custom_filename.configure(state="disabled")
        Output_filename = ""
    else:
        Custom_filename.configure(state="normal")
        Output_filename = Custom_filename.get()

def Encryption_toggle():
    if(Encryption_value.get()==0):
        for child in Encryption_frame.winfo_children():
            child.configure(state="disabled")
    else:
        for child in Encryption_frame.winfo_children():
            child.configure(state="normal")
        Encryption_algo.configure(state="readonly")
        Encry_File_name_toggle()

def Encry_File_name_toggle():
    if(Encry_File_name_check.get()==0):
        Encry_Custom_filename.configure(state="disabled")
        Encry_Output_filename = ""
    else:
        Encry_Custom_filename.configure(state="normal")
        Encry_Output_filename = Custom_filename.get()

def Final_submit():
    print("Submitted")
    print(Compression_value.get())
    o = ""
    if(Compression_value.get()==1):
        if(Compression_algo.get()=="LZMA"):
            print("Called")
            o = Compress_using_LZMA(file_path["text"], Comp_algo_scale.get(), Custom_filename.get())
            print("Returned")
        elif(Compression_algo.get()=="gzip"):
            print("Called")
            o = Compress_using_gzip(file_path["text"], Comp_algo_scale.get(), Custom_filename.get())
            print("Returned")
        elif(Compression_algo.get()=="bzip2"):
            print("Called")
            o = Compress_using_bzip2(file_path["text"], Comp_algo_scale.get(), Custom_filename.get())
            print("Returned")
        elif(Compression_algo.get()=="Custom"):
            print("Called")
            if(".txt" in file_path["text"]):
                o = Compress_using_custom(file_path["text"], Custom_filename.get())
            else:
                print("Custom mode only supports text file")
                o = ""
            print("Returned")
        if(Encryption_value.get()==1 and o!=""):
            AESEncrypt(o, Encry_Custom_filename.get(), 1)
    elif(Encryption_value.get()==1):
        AESEncrypt(file_path["text"], Encry_Custom_filename.get(), 0)
    file_path["text"]=""

window = tk.Tk()
window.title("Compact-Safe")
window.resizable(False, False)

frame_top = tk.Frame(master=window, relief=tk.GROOVE, bd=2)
frame_left = tk.Frame(master=window, relief=tk.GROOVE, bd=1)
frame_right = tk.Frame(master=window, relief=tk.GROOVE, bd=1)
frame_bottom = tk.Frame(master=window, relief=tk.GROOVE, bd=1)
frame_credit = tk.Frame(master=window, relief=tk.GROOVE, bd=2)

### Top Frame
file_label = tk.Label(master=frame_top, text="File")
file_path = tk.Label(master=frame_top, text="", width="84")
open_file = tk.Button(master=frame_top, text="Open File", command=Open_file)
#open_folder = tk.Button(master=frame_top, text="Open Folder", command=Open_folder)

file_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
file_path.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
open_file.grid(row=0, column=2, sticky="e", padx=10, pady=10)
#open_folder.grid(row=0, column=3, sticky="e", padx=10, pady=10)

### Left Frame
Compression_value = tk.IntVar()
Compression_enable = tk.Checkbutton(master=frame_left, text="Compress", variable=Compression_value, onvalue=1, offvalue=0, command=Compression_toggle)
Compression_frame = tk.Frame(master=frame_left, relief=tk.FLAT)

Compression_enable.grid(row=0, column=0, padx=10, pady=10)
Compression_frame.grid(row=1, column=0, padx=10, pady=10)

### Compression Frame
Comp_algo_value = tk.StringVar()
Comp_algo_scale = tk.DoubleVar()
Compression_label = tk.Label(master=Compression_frame, text="Compression Method :")
Compression_algo = ttk.Combobox(master=Compression_frame, textvariable=Comp_algo_value, state="readonly")
Compression_algo["values"] = ("LZMA", "gzip", "bzip2", "Custom")
Compression_algo.current(0)
Compression_scale = tk.Scale(master=Compression_frame, variable=Comp_algo_scale, from_=1, to=9, orient=tk.HORIZONTAL, length=250)
Compression_scale.set(6)
File_name_check = tk.IntVar()
Compression_filename = tk.Checkbutton(master=Compression_frame, text="Custom File name", variable=File_name_check, onvalue=1, offvalue=0, command=File_name_toggle)
Custom_filename = tk.Entry(master=Compression_frame, width=30)
Output_filename = ""

Compression_label.grid(row=0, columnspan=2, padx=10, pady=10)
Compression_algo.grid(row=1, columnspan=2, padx=10, pady=10)
Compression_scale.grid(row=2, columnspan=2, padx=10, pady=10)
Compression_filename.grid(row=3, column=0, padx=10, pady=10)
Custom_filename.grid(row=3, column=1, padx=10, pady=10)

for child in Compression_frame.winfo_children():
    child.configure(state="disabled")

### Right Frame
Encryption_value = tk.IntVar()
Encryption_enable = tk.Checkbutton(master=frame_right, text="Encrypt", variable=Encryption_value, onvalue=1, offvalue=0, command=Encryption_toggle)
Encryption_frame = tk.Frame(master=frame_right, relief=tk.FLAT)

Encryption_enable.grid(row=0, column=0, padx=10, pady=10)
Encryption_frame.grid(row=1, column=0, padx=10, pady=10)

### Compression Frame
Encry_algo_value = tk.StringVar()
Encryption_label = tk.Label(master=Encryption_frame, text="Encryption Method :")
Encryption_algo = ttk.Combobox(master=Encryption_frame, textvariable=Encry_algo_value, state="readonly")
Encryption_algo["values"] = ("AES-128")
Encryption_algo.current(0)
Encry_File_name_check = tk.IntVar()
Encryption_filename = tk.Checkbutton(master=Encryption_frame, text="Custom File name", variable=Encry_File_name_check, onvalue=1, offvalue=0, command=Encry_File_name_toggle)
Encry_Custom_filename = tk.Entry(master=Encryption_frame, width=30)
Encry_Output_filename = ""

Encryption_label.grid(row=0, columnspan=2, padx=10, pady=10)
Encryption_algo.grid(row=1, columnspan=2, padx=10, pady=10)
Encryption_filename.grid(row=3, column=0, padx=10, pady=10)
Encry_Custom_filename.grid(row=3, column=1, padx=10, pady=10)

for child in Encryption_frame.winfo_children():
    child.configure(state="disabled")

### Bottom Frame
Submit_btn = tk.Button(master=frame_bottom, text="Submit", height=2, width=7, command=Final_submit)

Submit_btn.pack()

### Credit Frame
credit_title = tk.Label(master=frame_credit, text="Prepared by : ")
credit_name = tk.Label(master=frame_credit, text="\tJilsa Chandarana")
credit_id = tk.Label(master=frame_credit, text="\t18DCS010")

credit_title.grid(row=0, column=0, sticky="w")
credit_name.grid(row=1, column=0, sticky="w")
credit_id.grid(row=2, column=0, sticky="w")

frame_top.grid(row=0, columnspan=3, sticky="n")
frame_left.grid(rowspan=2, column=0, sticky="w")
frame_right.grid(row=1, column=1, columnspan=2, sticky="e")
frame_bottom.grid(row=2, column=1, sticky="e")
frame_credit.grid(row=2, column=2, sticky="e")

window.mainloop()