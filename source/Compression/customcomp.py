def Custom_Compression(filepath, output_file=""):
    with open(filepath, "r") as file:
        print("Reading File...")
        data = file.read()
        print("Uncompressed file received")
        print("Starting Compression")
        vocab = {}
        temp_str = ""
        comp_temp_str = ""
        compressed_str = ""
        index = 0
        for i in range(len(data)):
            if data[i] in ["[", "]"]:
                if(temp_str in vocab):
                    if((len(str(vocab[temp_str])))<4):
                        compressed_str += temp_str
                    else:
                        compressed_str += "[" + str(vocab[temp_str]) + "]"
                else:
                    tmp = ""
                    for j in range(len(temp_str)):
                        tmp += temp_str[j]
                        if(tmp in vocab):
                            comp_temp_str = vocab[tmp]
                        else:
                            if((len(tmp[:-1]))<4):
                                compressed_str += tmp
                            else:
                                compressed_str += "[" + str(comp_temp_str) + "]" + str(tmp[-1])
                            vocab[str(tmp)] = index
                            index+=1
                temp_str = ""
                comp_temp_str = ""
                compressed_str += "[[" if (data[i]=="[") else "]]"
                continue
            temp_str += data[i]
            if(temp_str in vocab):
                comp_temp_str = vocab[temp_str]
            else:
                if((len(temp_str[:-1])<4)):
                    compressed_str += str(temp_str)
                else:
                    compressed_str += "[" + str(comp_temp_str) + "]" + str(temp_str[-1])
                vocab[str(temp_str)] = index
                index+=1
                temp_str = ""
                comp_temp_str = ""
        compressed_str += "[" + str(comp_temp_str) + "]"
        print("Compression done")
    compressed_str = compressed_str.replace("[]","")

    with open(filepath+"_vocab","w") as f:
        for i, value in vocab.items():
            f.write(str(i) + " " + str(value) + "\n")
    print("Creating compressed file")

    if(output_file==""):
        temp_name = filepath.split(".")
        temp_name = temp_name[0] + str("_compressed")
        output_file = temp_name
    else:
        temp_name = filepath.split("/")
        temp_name[-1] = output_file
        temp_name = "/".join(temp_name)
    with open(output_file, "w") as file:
        file.write(compressed_str)

    print("File creation successful")

    print("Length of original : ",len(data))
    print("Length of Compressed : ",len(compressed_str))
    print("Compression Ratio : ",(len(data)/len(compressed_str)))
    return output_file
