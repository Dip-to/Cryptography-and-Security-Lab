from BitVector import *
from sys import exit

def encryptFuntion(text,key,length):

    plainBV = BitVector(textstring = text)
    keyBV = BitVector(textstring = key)
    ans = BitVector(size = 0)
    previousCipherBV = BitVector(intVal = 0,size = 8)
    
    for x in range(0,length):  

        temp = int(previousCipherBV)+int(keyBV[x*8:(x+1)*8])
        temp = temp%256
        previousCipherBV = BitVector(intVal = temp,size = 8)^plainBV[x*8:(x+1)*8]
        ans+=previousCipherBV

    return ans

def decryptFunction(cipherText,key,length):

    cipherBv  = BitVector(textstring = cipherText)
    keyBV = BitVector( textstring= key)
    previousCipherBV = BitVector(intVal = 0,size = 8)
    ans = BitVector(size = 0)

    for x in range(0,length):  

        temp = int(previousCipherBV)+int(keyBV[x*8:(x+1)*8])
        temp = temp%256
        ans+=BitVector(intVal = temp,size = 8)^cipherBv[x*8:(x+1)*8]
        previousCipherBV = cipherBv[x*8:(x+1)*8]
        
    return ans


inputString = input("Write a 10 letter word: ")
inputKey = input("Write a 10 letter key: ")

if len(inputKey) != len(inputString):
    print("The length of message and key must be equal")
    sys.exit()
length = len(inputString)

encryptedTextBV = encryptFuntion(inputString,inputKey,length)

temp = encryptedTextBV.get_hex_string_from_bitvector()
encryptHexCode = ' '.join(temp[i:i+2] for i in range(0,len(temp),2))
print(encryptHexCode)

inputKey = input("Write a 10 letter key: ")

if len(inputKey) != length:
    print("invalid length of key")
    sys.exit()

plainTextBv = decryptFunction(encryptedTextBV.get_text_from_bitvector(),inputKey,length)
print(plainTextBv.get_text_from_bitvector())


           
        