from Lib import bz2

def Decompress_using_bzip2(filepath, level, output_filename=""):
    with bz2.open(filepath, "rb") as file:
        data = file.read()
        output = bz2.decompress(data)

    if (output_filename==""):
        temp_name = filepath.split(".")
        temp_name = temp_name[0] + str("_decompressed")
    else:
        temp_name = filepath.split("/")
        temp_name[-1] = output_filename
        temp_name = "/".join(temp_name)
        print(temp_name)
    with open(temp_name, "wb") as f:
        f.write(output)
    print("Compression Ratio : ",len(output)/len(data))