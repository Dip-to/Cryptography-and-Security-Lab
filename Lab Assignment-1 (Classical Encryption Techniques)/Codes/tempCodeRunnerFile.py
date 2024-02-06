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
