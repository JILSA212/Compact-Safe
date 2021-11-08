from Lib import lzma

def Decompress_using_LZMA(filepath, level, output_filename=""):
    with lzma.open(filepath, "rb") as file:
        data = file.read()
        output = lzma.decompress(data)

    if(output_filename==""):
        temp_name = filepath.split(".")
        temp_name = temp_name[0] + str("_decompressed")
        with open(temp_name, "wb") as f:
            f.write(output)
    else:
        temp_name = filepath.split("/")
        temp_name[-1] = output_filename
        temp_name = "/".join(temp_name)
        print(temp_name)
        with open(temp_name, "wb") as f:
            f.write(output)

    print("Compression Ratio : ",len(output)/len(data))