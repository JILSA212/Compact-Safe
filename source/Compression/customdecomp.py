def Custom_Decompression(filename, output_file=""):
    with open(filename, "r") as file:
        data = file.read()

        vocab = {}
        vocab_str = ""
        temp_str = ""
        current_str = "temp_str"
        uncompressed_str = ""
        index = 0


        split_data = data.split("[")
        flag=1
        for i in split_data:
            #print("Vocab : ",vocab)
            #print("I : ",i)
            if (i=="" and flag==0):
                #print("Second i space")
                flag=1
            elif(i=="" and flag==1):
                #print("First i space, [ added")
                uncompressed_str += "["
                flag=0
            else:
                flag=1
                temp_array = i.split("]")
                #print("Temp array : ",temp_array)
                if (len(temp_array)==1):
                    temp_str = temp_array[0]
                    uncompressed_str += temp_array[0]
                    tmp = ""
                    for j in range(len(temp_str)):
                        tmp += temp_str[j]
                        if(tmp not in vocab.values()):
                            vocab[str(index)] = tmp
                            index+=1
                            tmp = ""
                elif(len(temp_array)==2):
                    if("" in temp_array):
                        uncompressed_str += str(vocab[temp_array[0]])
                    else:
                        temp_str = temp_array[1]
                        uncompressed_str += str(vocab[temp_array[0]]) + str(temp_str)
                        vocab[str(index)] = str(vocab[temp_array[0]]) + str(temp_str[0])
                        index+=1
                        tmp = ""
                        for j in range(1,len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""
                elif len(temp_array)==3:
                    temp_str = temp_array[0]
                    tmp = ""
                    for j in range(len(temp_str)):
                        tmp += temp_str[j]
                        if(tmp not in vocab.values()):
                            vocab[str(index)] = tmp
                            index+=1
                            tmp = ""
                    if (temp_array[2]==""):
                        uncompressed_str += str(temp_array[0]) + "]"
                    else:
                        uncompressed_str += str(temp_array[0]) + "]" + str(temp_array[2])
                        temp_str = temp_array[2]
                        tmp = ""
                        for j in range(len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""
                elif len(temp_array)==4:
                    if (temp_array[3]=="" and temp_array[1]==""):
                        uncompressed_str += vocab[str(temp_array[0])] + "]"
                    elif(temp_array[3]!="" and temp_array[1]==""):
                        uncompressed_str += vocab[str(temp_array[0])] + "]" + str(temp_array[3])
                        temp_str = temp_array[3]
                        tmp = ""
                        for j in range(len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""
                    elif temp_array[3] == "":
                        uncompressed_str += vocab[str(temp_array[0])] + str(temp_array[1]) + "]"
                        temp_str = temp_array[1]
                        tmp = ""
                        vocab[str(index)] = vocab[str(temp_array[0])] + str(temp_str[0])
                        index+=1
                        for j in range(1,len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""
                    else:
                        uncompressed_str += vocab[str(temp_array[0])] + str(temp_array[1]) + "]" + str(temp_array[3])
                        temp_str = temp_array[1]
                        tmp = ""
                        vocab[str(index)] = vocab[str(temp_array[0])] + str(temp_str[0])
                        index+=1
                        for j in range(1,len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""
                        temp_str = temp_array[3]
                        tmp = ""
                        for j in range(len(temp_str)):
                            tmp += temp_str[j]
                            if(tmp not in vocab.values()):
                                vocab[str(index)] = tmp
                                index+=1
                                tmp = ""

                else:
                    continue
                            #print("Vocab : ",vocab)
                            #print(uncompressed_str)

    with open(filename+"_devocab", "w") as f:
        for i in vocab:
            f.write(i + " " + vocab[i] + "\n")

    if(output_file==""):
        temp_name = filename.split(".")
        temp_name = temp_name[0] + str("_decompressed")
        output_file = temp_name
    else:
        temp_name = filename.split("/")
        temp_name[-1] = output_file
        temp_name = "/".join(temp_name)
    with open(output_file, "w") as f:
        f.write(uncompressed_str)

    print("Length of data : ",len(data))
    print("Length of Uncompressed data : ",len(uncompressed_str))
