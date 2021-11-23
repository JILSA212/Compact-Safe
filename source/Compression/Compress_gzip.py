from Lib import gzip

def Compress_using_gzip(filepath, level, output_filename=""):
    with open(filepath, "rb") as file:
        data = file.read()
        output = gzip.compress(data, int(abs(level)))

    if (output_filename==""):
        temp_name = filepath.split(".")
        temp_name = temp_name[0] + str("_compressed")
    else:
        temp_name = filepath.split("/")
        temp_name[-1] = output_filename
        temp_name = "/".join(temp_name)
        print(temp_name)
    with gzip.open(temp_name, "wb") as f:
        f.write(output)
    print("Compression Ratio : ",len(data)/len(output))
    return temp_name