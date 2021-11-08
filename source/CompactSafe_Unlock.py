import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from Compression.Decompress_gzip import Decompress_using_gzip
from Compression.Decompress_bzip2 import Decompress_using_bzip2
from Compression.Decompress_LZMA import Decompress_using_LZMA
from Compression.Decompress_custom import Decompress_using_custom
from Encryption.AES_Decrypt import AESDecrypt

def Open_file():
    filepath = askopenfilename(initialdir="/", title="Open a file", filetypes=[("All files","*.*")])
    file_path["text"] = filepath
    if not filepath:
        file_path["text"] = ""
        return

def Open_key():
    keyfile = askopenfilename(initialdir="/", title="Open a file", filetypes=[("All files","*.*")])
    key_path["text"] = keyfile
    if not keyfile:
        file_path["text"] = ""
        return

def Open_folder():
    folderpath = askdirectory()
    file_path["text"] = folderpath
    if not folderpath:
        file_path["text"] = ""
        return

def Decompression_toggle():
    if(Decompression_value.get()==0):
        for child in Decompression_frame.winfo_children():
            child.configure(state="disabled")
    else:
        for child in Decompression_frame.winfo_children():
            child.configure(state="normal")
        Decompression_algo.configure(state="readonly")
        File_name_toggle()

def File_name_toggle():
    if(File_name_check.get()==0):
        Custom_filename.configure(state="disabled")
        Output_filename = ""
    else:
        Custom_filename.configure(state="normal")
        Output_filename = Custom_filename.get()

def Decryption_toggle():
    if(Decryption_value.get()==0):
        for child in Decryption_frame.winfo_children():
            child.configure(state="disabled")
    else:
        for child in Decryption_frame.winfo_children():
            child.configure(state="normal")
        Decryption_algo.configure(state="readonly")
        Decry_File_name_toggle()

def Decry_File_name_toggle():
    if(Decry_File_name_check.get()==0):
        Decry_Custom_filename.configure(state="disabled")
        Decry_Output_filename = ""
    else:
        Decry_Custom_filename.configure(state="normal")
        Decry_Output_filename = Custom_filename.get()

def Final_submit():
    print("Submitted")
    print(Decompression_value.get())
    if(Decompression_value.get()==1):
        k = Custom_filename.get()
        if(Decryption_value.get()==1):
            o = AESDecrypt(file_path["text"], key_path["text"])
            k = Decry_Custom_filename.get()
        else:
            o = file_path["text"]
        if(Decompression_algo.get()=="LZMA"):
            print("Called")
            Decompress_using_LZMA(o, Decomp_algo_scale.get(), k)
            print("Returned")
        elif(Decompression_algo.get()=="gzip"):
            print("Called")
            Decompress_using_gzip(o, Decomp_algo_scale.get(), k)
            print("Returned")
        elif(Decompression_algo.get()=="bzip2"):
            print("Called")
            Decompress_using_bzip2(o, Decomp_algo_scale.get(), k)
            print("Returned")
        elif(Decompression_algo.get()=="Custom"):
            print("Called")
            Decompress_using_custom(o, Custom_filename.get())
            print("Returned")
    elif(Decryption_value.get()==1):
        AESDecrypt(file_path["text"], key_path["text"], k)
    file_path["text"]=""
    key_path["text"]=""
window = tk.Tk()
window.title("Compact-Safe-Unlock")
window.resizable(False, False)

frame_top = tk.Frame(master=window, relief=tk.GROOVE, bd=2)
frame_top2 = tk.Frame(master=window, relief=tk.GROOVE, bd=2)
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

### Top Frame 2
key_label = tk.Label(master=frame_top2, text="Key File")
key_path = tk.Label(master=frame_top2, text="", width="82")
key_file = tk.Button(master=frame_top2, text="Open File", command=Open_key)
#open_folder = tk.Button(master=frame_top, text="Open Folder", command=Open_folder)

key_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
key_path.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
key_file.grid(row=0, column=2, sticky="e", padx=10, pady=10)
#open_folder.grid(row=0, column=3, sticky="e", padx=10, pady=10)

### Left Frame
Decompression_value = tk.IntVar()
Decompression_enable = tk.Checkbutton(master=frame_left, text="Decompress", variable=Decompression_value, onvalue=1, offvalue=0, command=Decompression_toggle)
Decompression_frame = tk.Frame(master=frame_left, relief=tk.FLAT)

Decompression_enable.grid(row=0, column=0, padx=10, pady=10)
Decompression_frame.grid(row=1, column=0, padx=10, pady=10)

### Decompression Frame
Decomp_algo_value = tk.StringVar()
Decomp_algo_scale = tk.DoubleVar()
Decompression_label = tk.Label(master=Decompression_frame, text="Decompression Method :")
Decompression_algo = ttk.Combobox(master=Decompression_frame, textvariable=Decomp_algo_value, state="readonly")
Decompression_algo["values"] = ("LZMA", "gzip", "bzip2", "Custom")
Decompression_algo.current(0)
File_name_check = tk.IntVar()
Decompression_filename = tk.Checkbutton(master=Decompression_frame, text="Custom File name", variable=File_name_check, onvalue=1, offvalue=0, command=File_name_toggle)
Custom_filename = tk.Entry(master=Decompression_frame, width=30)
Output_filename = ""

Decompression_label.grid(row=0, columnspan=2, padx=10, pady=10)
Decompression_algo.grid(row=1, columnspan=2, padx=10, pady=10)
Decompression_filename.grid(row=3, column=0, padx=10, pady=10)
Custom_filename.grid(row=3, column=1, padx=10, pady=10)

for child in Decompression_frame.winfo_children():
    child.configure(state="disabled")

### Right Frame
Decryption_value = tk.IntVar()
Decryption_enable = tk.Checkbutton(master=frame_right, text="Decrypt", variable=Decryption_value, onvalue=1, offvalue=0, command=Decryption_toggle)
Decryption_frame = tk.Frame(master=frame_right, relief=tk.FLAT)

Decryption_enable.grid(row=0, column=0, padx=10, pady=10)
Decryption_frame.grid(row=1, column=0, padx=10, pady=10)

### Decompression Frame
Decry_algo_value = tk.StringVar()
Decryption_label = tk.Label(master=Decryption_frame, text="Decryption Method :")
Decryption_algo = ttk.Combobox(master=Decryption_frame, textvariable=Decry_algo_value, state="readonly")
Decryption_algo["values"] = ("AES-128")
Decryption_algo.current(0)
Decry_File_name_check = tk.IntVar()
Decryption_filename = tk.Checkbutton(master=Decryption_frame, text="Custom File name", variable=Decry_File_name_check, onvalue=1, offvalue=0, command=Decry_File_name_toggle)
Decry_Custom_filename = tk.Entry(master=Decryption_frame, width=30)
Decry_Output_filename = ""

Decryption_label.grid(row=0, columnspan=2, padx=10, pady=10)
Decryption_algo.grid(row=1, columnspan=2, padx=10, pady=10)
Decryption_filename.grid(row=3, column=0, padx=10, pady=10)
Decry_Custom_filename.grid(row=3, column=1, padx=10, pady=10)

for child in Decryption_frame.winfo_children():
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
frame_top2.grid(row=1, columnspan=3, sticky="n")
frame_left.grid(rowspan=2, column=0, sticky="w")
frame_right.grid(row=2, column=1, columnspan=2, sticky="e")
frame_bottom.grid(row=3, column=1, sticky="e")
frame_credit.grid(row=3, column=2, sticky="e")

window.mainloop()