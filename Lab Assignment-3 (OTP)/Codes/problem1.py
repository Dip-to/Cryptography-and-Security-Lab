from BitVector import *
def getAllPossibleWords(length):

    wordList = []

    with open("words.txt") as file:
        for line in file:
            if len(line) == length+1:
                line = line[:-1]
                wordList.append(line.capitalize())
   
    return wordList


def getBitvectorOfEncryptedText():
    encryptWords = []
    BitVectors = []

    with open ("input1.txt", "r") as myfile:
        encryptWords = myfile.read().splitlines()

    firstEncryptWord = encryptWords[0].strip().replace(" ", "")
    secondEncryptWord = encryptWords[1].strip().replace(" ", "")

    BitVectors.append(BitVector(hexstring  =firstEncryptWord))
    BitVectors.append(BitVector(hexstring  =secondEncryptWord))

    return BitVectors

def betterApproach(allWords):
    finalans = []

    encryptedTextBitVectors = getBitvectorOfEncryptedText()
    xorEncrypt = encryptedTextBitVectors[0]^encryptedTextBitVectors[1]

    for x in allWords:
      
        secondWordBV = xorEncrypt^BitVector(textstring  = x)
        secondWord =  secondWordBV.get_text_from_bitvector() 
        if secondWord in allWords:
            finalans.append(x)
            finalans.append(secondWord)
            return finalans


allWords = getAllPossibleWords(8)
# decryptFunction
ans = betterApproach(allWords)
if ans != None:
    print(ans)
    # save the answer
    with open("output1.txt", "w") as a_file:
        a_file.write(str(ans))
else:
    print("no answer found")
           
        