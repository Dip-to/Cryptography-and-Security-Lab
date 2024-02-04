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
def charToInt(c):
    if c <= 'Z':
        return ord(c)-ord('A')+26    
    else:
        return ord(c)-ord('a')
def intToChar(x):
    x = x%52
    if x < 26:   
        return chr(x+ord('a'))
    else:
       return chr(x+ord('A')-26)
def formatText(text):
    finalText = ""
    for i,c in enumerate(text):    
        if i%5 == 0 and i != 0:
            finalText+=" "
        finalText+=c
    return finalText

def Encryption(text,key):
    keyLength = len(key)
    encryptedText = ""
    for i, c in enumerate(text):
        encryptedInt = charToInt(c) + charToInt(key[i%keyLength])
        encryptedCharachter = intToChar(encryptedInt)
        encryptedText+=encryptedCharachter
    return encryptedText

def Decryption(text,key):
    plainText = text.replace(" ", "")
    keyLength = len(key)
    decryptedText = ""
    for i, c in enumerate(plainText):
        decryptedInt = charToInt(c) - charToInt(key[i%keyLength])
        decryptedCharachter = intToChar(decryptedInt)
        decryptedText+=decryptedCharachter
    return decryptedText




plainText=read_from_file('input.txt')
#remove unecessary char
plainText = re.sub('[^A-Za-z]+', '',  plainText) 
key=read_from_file('key.txt')
cipherText = Encryption(plainText,key)
formattedText=formatText(cipherText)
write_to_file('output.txt',formattedText)
decrypted_plainText = Decryption(cipherText,key)
write_to_file('decrypted_output.txt',decrypted_plainText)

