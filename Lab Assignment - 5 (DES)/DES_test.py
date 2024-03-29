import sys
from BitVector import *
import DES

def getTextFromFile(fileName,isEncrypt):           
    f = open(fileName, 'r')
    t = f.read()
    f.close()
    ans = ""
    if isEncrypt:
        ans = t
    else:
        ans = BitVector(hexstring = t).get_text_from_bitvector()

    return ans
def read_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content 
    except Exception as e:
        print(f"Error reading from file: {e}")
        return None
def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file: {e}")
def getKey():
    return read_from_file(sys.argv[2])

    
if len(sys.argv) != 4: 
    sys.exit("Needs three command-line arguments, one for  the encrypted file and the other for the  decrypted file and another for key ")

keyStr = getKey()
path='./Part1_file/'
if sys.argv[1] == "message.txt":
    # get plain text
    text = getTextFromFile(path+sys.argv[1],True)
    # get BV of cipher text
    encryptedBV = DES.DES_function(text,keyStr,True)
    
    print("The encrypted Text is: ")
    print(encryptedBV.get_hex_string_from_bitvector())
    
    # save cipher Text
    with open(path+sys.argv[3], "w") as file:
        file.write(encryptedBV.get_hex_string_from_bitvector())

else:
    # get cipherText text
    text = getTextFromFile(path+sys.argv[1],False)
    # get BV of plain text
    decryptededBV = DES.DES_function(text,keyStr,False)
    
    print("The decrypted Text is: ")
    print(decryptededBV.get_text_from_bitvector())
    
    # save cipher Text
    with open(path+sys.argv[3], "w") as file:
        file.write(decryptededBV.get_text_from_bitvector().replace("\x00", ""))
    