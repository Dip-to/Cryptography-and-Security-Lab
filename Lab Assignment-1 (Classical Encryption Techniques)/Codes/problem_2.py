import re
import csv
import math
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



def getFreq(text):
    text_len = len(text)
    frequency = []
    for i in range(26):
        frequency.append(round(100*text.count(chr(i+ord("a")))/text_len,10))
    for i in range(26):
        frequency.append(round(100*text.count(chr(i+ord("A")))/text_len,10))
    return frequency



def getAlphabetFrequency():
    with open('alphabetFrequency.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    
    alphabetFreq = []
    for i in range(26):
        alphabetFreq.append(float(mydict.get(chr(i+ord("a")))))
    for i in range(26):
        alphabetFreq.append(float(mydict.get(chr(i+ord("A")))))

    return alphabetFreq


def findpredictedKey(keyLength,text):
    freq = getAlphabetFrequency()
    text_len = len(text)
    nthCharArr = []
    finalPredictedKey = ""
    for i in range(keyLength):
        tempCharArr = ""
        for j in range(i,text_len,keyLength):
            tempCharArr+=text[j]
        # print(tempCharArr)
        nthCharArr.append(tempCharArr)

    for i in range(keyLength):
        cipherTextFreq = getFreq(nthCharArr[i])
        isCipherCharachterFound = False
        for j in range(52):
            for k in range(25):
                if freq[k] > cipherTextFreq[(k+j)%52]+5 or freq[k] < cipherTextFreq[(k+j)%52]-5:
                    break
                elif k == 24:
                    isCipherCharachterFound = True
            if isCipherCharachterFound == True:
                if j<26:
                    finalPredictedKey+=chr(ord('a')+j)
                else:
                    finalPredictedKey+=chr(ord('A')+j-26)
                break
        if isCipherCharachterFound == False:
            finalPredictedKey+="X"
    return finalPredictedKey

def kasiskiKeyLength(cipherText):
    #find most occurring 3-letter pattern
    patterns = {}
    for i in range(len(cipherText) - 3):
        pattern = cipherText[i:i+3]
        if pattern not in patterns.keys():
            patterns[pattern] = 0
        patterns[pattern] += 1
    sortedPatterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
    
    #find probable key length
    occurrences = []
    pattern = sortedPatterns[0][0]
    for i in range(len(cipherText) - 3):
        if cipherText[i:i+3] == pattern:
            occurrences.append(i)
    probableLengths = []
    for i in range(1, len(occurrences)):
        probableLengths.append(occurrences[i] - occurrences[i-1])
    probableLength = probableLengths[0]
    for i in range(1, len(probableLengths)):
        probableLength = math.gcd(probableLength, probableLengths[i])
    return probableLength
 

cipherText=read_from_file('output.txt')
cipherText=cipherText.replace(" ", "")
predictedKeyLength=kasiskiKeyLength(cipherText)
print("kasiski predicted key length: " + str(predictedKeyLength))
predictedKey=findpredictedKey(predictedKeyLength,cipherText)
print("Predicted Key: " + predictedKey)

predicted_message=Decryption(cipherText,predictedKey)
write_to_file('predicted_out[ut.txt',str('Predicted Message:\n\n')+predicted_message)


