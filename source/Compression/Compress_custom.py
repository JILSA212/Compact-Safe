from . import customcomp

def Compress_using_custom(filepath, output_filename=""):
    o = customcomp.Custom_Compression(filepath, output_filename)
    return o