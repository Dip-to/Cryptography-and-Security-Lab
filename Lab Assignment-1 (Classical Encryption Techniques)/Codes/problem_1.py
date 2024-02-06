import re
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
def charToInt(chr):
    if chr <= 'Z':
        return (ord(chr)-ord('A'))+26    
    else:
        return (ord(chr)-ord('a'))
def intToChar(char_num):
    char_num = char_num%52
    if char_num < 26:   
        return chr(char_num+ord('a'))
    else:
       return chr(char_num+ord('A')-26)


def Encryption(text,key):
    E_text = ""
    k_length = len(key)

    for i, c in enumerate(text):
        tmp = charToInt(c) + charToInt(key[i%k_length])
        #print(tmp)
        E_int=tmp
        encryptedCharachter = intToChar(E_int)
        #print(encryptedCharachter)
        E_text+=encryptedCharachter
    return E_text

def formatText(text):
    tex = ""
    for i,c in enumerate(text):    
        if i%5 == 0 and i != 0:
            tex+=" "
        tex+=c
    return tex
def Decryption(text,key):
    k_length = len(key)
    D_text = ""
    plainText = text.replace(" ", "")
    for i, c in enumerate(plainText):
        tmp = charToInt(c) - charToInt(key[i%k_length])
        #print(tmp)
        D_int=tmp
        decryptedCharachter = intToChar(D_int)
        #print(decryptedCharachter)
        D_text+=decryptedCharachter
    return D_text




plainText=read_from_file('input.txt')
#remove unecessary char
plainText = re.sub('[^A-Za-z]+', '',  plainText) 
key=read_from_file('key.txt')
cipherText = Encryption(plainText,key)
formattedText=formatText(cipherText)
write_to_file('output.txt',formattedText)
decrypted_plainText = Decryption(cipherText,key)
write_to_file('decrypted_output.txt',decrypted_plainText)

