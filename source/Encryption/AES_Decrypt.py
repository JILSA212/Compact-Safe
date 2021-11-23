from . import InvSbox
from . import Ltable
from . import Etable
from . import InvColumnMix as ICM
from . import aes_key
import binascii
import math

def SubByte(onebyte):
    return InvSbox.InvS_box[int(onebyte[0], 16)][int(onebyte[1], 16)]

def InvSubBytes(block):
    new_list = []
    for i in range(4):
        temp_list = [SubByte(block[i][j]) for j in range(4)]
        new_list.append(temp_list)
    return new_list

def InvShiftRows(block):
    block[0][0], block[0][1], block[0][2], block[0][3] = block[0][0], block[0][1], block[0][2], block[0][3]
    block[1][0], block[1][1], block[1][2], block[1][3] = block[1][3], block[1][0], block[1][1], block[1][2]
    block[2][0], block[2][1], block[2][2], block[2][3] = block[2][2], block[2][3], block[2][0], block[2][1]
    block[3][0], block[3][1], block[3][2], block[3][3] = block[3][1], block[3][2], block[3][3], block[3][0]

def Mul(a, b):
    if a == "00" or b == "00":
        #print("Returning 0 : 00")
        return "00"
    if b == "01":
        #print("Returning A : ",a)
        return a
    #print("A[0] : ",a[0],"\tA[1] : ",a[1],"\tB[0] : ",b[0],"\tB[1] : ",b[1])
    #print(int(a[0],16),"\t",int(a[1],16),"\t",int(b[0],16),"\t",int(b[1],16))
    x = int(a[0], 16)
    y = int(a[1], 16)
    z = int(b[0], 16)
    w = int(b[1], 16)
    #print(Ltable.L_table[x][y])
    #print(Ltable.L_table[z][w])
    temp = (int(Ltable.L_table[x][y], 16) + int(Ltable.L_table[z][w],16)) % 255
    #print("Temp : ",temp)
    temp = str(hex(temp)).replace("0x","")
    temp = "0" + temp if len(temp)==1 else temp
    #print("Returning : ",Etable.E_table[int(temp[0],16)][int(temp[1],16)])
    return Etable.E_table[int(temp[0],16)][int(temp[1],16)]

def InvColumnMix(block):
    temp_list = []
    for i in range(4):
        temp_list2 = []
        for j in range(4):
            #print("I : ",i,"\tJ : ",j)
            #print(block[0][j])
            #print(block[1][j])
            #print(block[2][j])
            #print(block[3][j])
            temp = int(Mul(block[0][j], ICM.Inv_mix[i][0]), 16) ^ int(Mul(block[1][j], ICM.Inv_mix[i][1]), 16) ^ int(Mul(block[2][j], ICM.Inv_mix[i][2]), 16) ^ int(Mul(block[3][j], ICM.Inv_mix[i][3]), 16)
            temp = str(hex(temp)).replace("0x","")
            temp = "0" + temp if len(temp)==1 else temp
            temp_list2.append(str(temp))
            #print("After XOR : ",temp)
        temp_list.append(temp_list2)
    return temp_list

def OP_XOR(a, b):
    temp_list = []
    for i in range(4):
        temp_list2 = []
        for j in range(4):
            temp = int(a[i][j], 16) ^ int(b[i][j], 16)
            temp = str(hex(temp)).replace("0x","")
            temp = "0" + temp if(len(temp)==1) else temp
            temp_list2.append(temp)
        temp_list.append(temp_list2)
    return temp_list

def AESDecrypt(filename, keyname, destination=""):
    with open(filename, "rb") as f:
        data = f.read()
        #print(data)
        data = binascii.hexlify(data).decode()
        #print(data)
        data = str(data)

        temp_list = []
        temp_list2 = []
        for i in range(0, len(data), 2):
            x = str(data[i] + data[i+1])
            temp_list.append(x)
        #print(temp_list)

        #for i in range((math.ceil(len(temp_list)/16) - math.floor(len(temp_list)/16)) * 16):
        #    temp_list.append("00")

        try:
            for i in range(0, len(temp_list), 4):
                x = [temp_list[i], temp_list[i+1], temp_list[i+2], temp_list[i+3]]
                temp_list2.append(x)
        except:
            print("", end="")
        #print(temp_list2)

        temp_list = []
        try:
            for i in range(0, len(temp_list2), 4):
                x = [temp_list2[i], temp_list2[i+1], temp_list2[i+2], temp_list2[i+3]]
                temp_list.append(x)
        except:
            print("", end="")
        #print("Temp_list : ",temp_list)

        #print("Length : ",len(temp_list))

        with open(keyname, "rb") as key_file:
            key = key_file.read()
            key = binascii.hexlify(key).decode()

        key_list = aes_key.callme(key)
        file = open("decrypt.txt", "w")
        file.close()

        for subs in temp_list:
            #print("Final FOR with subs : ",subs)
            subs = OP_XOR(subs, key_list[10])

            for x in range(10):
                InvShiftRows(subs)
                #print("Shiftrows : ",subs)
                subs = InvSubBytes(subs)
                #print("Subbytes : ",subs)
                subs = OP_XOR(subs, key_list[9-x])
                #print("Key XOR : ",subs)
                subs = InvColumnMix(subs) if(x!=9) else subs
                #print("Column Mix : ",subs)
                
                #x = bytearray()
                #for i in range(0, len(data), 2):
                #    x += binascii.unhexlify(Sbox.S_box[int(data[i], 16)][int(data[i+1], 16)])
                #print(x)

            #for i in range(len(subs)):
            #    if(subs[len(subs)-1-i]=="00"):
            #        subs.remove(subs[len(subs)-1-i])
            #    else:
            #        break

            x = bytearray()
            for i in subs:
                for j in i:
                    #print(j)
                    x += binascii.unhexlify(j)
            #print(x)

            if(destination==""):
                try:
                    temp = filename.split(".")
                    destination = temp[0] + "_decrypt." + temp[1]
                except:
                    destination = temp[0] + "_decrypt"
            with open(destination, "ab") as file:
                file.write(x)

    return destination

#AESDecrypt()