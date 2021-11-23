import random
import binascii
from . import Sbox

def KeyGenerate():
    key = random.getrandbits(128)
    key = str(hex(key)).replace("0x","")
    #print(key)
    with open("whatever.key","wb") as f:
        f.write(binascii.unhexlify(key))
    return key

def MakeList(key):
    temp_list = []
    for i in range(0, len(key), 2):
        x = str(key[i] + key[i+1])
        temp_list.append(x)
    #print(temp_list)

    temp_list2 = []
    for i in range(0, len(temp_list), 4):
        x = [temp_list[i], temp_list[i+1], temp_list[i+2], temp_list[i+3]]
        temp_list2.append(x)
    return temp_list2


def RowShift(key):
    key[0], key[1], key[2], key[3] = key[1], key[2], key[3], key[0]

def SubByte(onebyte):
    #print(onebyte)
    #print(int(onebyte[0], 16),"\t",int(onebyte[1], 16))
    return Sbox.S_box[int(onebyte[0], 16)][int(onebyte[1], 16)]

def SubBytes(key):
    return [SubByte(key[i]) for i in range(4)]

def Rcon(key, round):
    variable = ""
    if(round==1):
        variable = "01"
    elif(round==2):
        variable = "02"
    elif(round==3):
        variable = "04"
    elif(round==4):
        variable = "08"
    elif(round==5):
        variable = "10"
    elif(round==6):
        variable = "20"
    elif(round==7):
        variable = "40"
    elif(round==8):
        variable = "80"
    elif(round==9):
        variable = "1B"
    elif(round==10):
        variable = "36"

    #print("Variable : ",variable)
    key[0] = str(hex(int(key[0], 16) ^ int(variable, 16))).replace("0x","")
    key[1] = str(hex(int(key[1], 16) ^ int("00", 16))).replace("0x","")
    key[2] = str(hex(int(key[2], 16) ^ int("00", 16))).replace("0x","")
    key[3] = str(hex(int(key[3], 16) ^ int("00", 16))).replace("0x","")

    for i in range(4):
        key[i] = "0" + key[i] if len(key[i])==1 else key[i]
        
def Expand(key, order):
    new_key = []
    current_state = key[3].copy()
    RowShift(current_state)
    #print("Rowshift : ",current_state)
    current_state = SubBytes(current_state)
    #print("Sub : ",current_state)
    Rcon(current_state, order)
    #print("New round generated : ",current_state)
    #print("XOR with key : ",key[0])
    for j in range(4):
        current_state[j] = int(current_state[j], 16) ^ int(key[0][j], 16)
        current_state[j] = str(hex(current_state[j])).replace("0x","")
        current_state[j] = "0" + current_state[j] if(len(current_state[j])==1) else current_state[j]
    #print("Final result : ",current_state)
    new_key.append(current_state)
    #print("New key right now : ",new_key)
    current_state = new_key[0].copy()
    for i in range(1,4):
        #print("I : ",i,"\tKey : ",key[i])
        for j in range(4):
            current_state[j] = int(current_state[j], 16) ^ int(key[i][j], 16)
            current_state[j] = str(hex(current_state[j])).replace("0x","")
            current_state[j] = "0" + current_state[j] if(len(current_state[j])==1) else current_state[j]
        new_key.append(current_state)
        try:
            current_state = new_key[i].copy()
        except:
            print("",end="")
    return new_key

def callme(given_key=""):
    key = KeyGenerate() if(given_key=="") else given_key
    #key = "1A91F7205E456706A25B66DE5F145988"
    #key = "e15a33efbf1f54e91d44323742506bbf"
    #key = "b0253bc30f3a6f2a127e5d1d502e36a2"
    #key = "1A5EA25F91455B14F76766592006DE88"
    #key = "E1BF1D425A1F44503354326BEFE937BF"
    #key = "744366e8e5062dfc12614ba53267952d"
    key_list = []
    #print(key)
    key = MakeList(key)
    key_list.append(key)
    for i in range(1, 11):
        #print(key)
        key = Expand(key, i)
        key_list.append(key)
        #print(key)
    #for x in key_list:
        #print(x)
    return key_list