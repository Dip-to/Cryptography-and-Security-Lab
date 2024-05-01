import DES
from BitVector import *
import sys

def getKey():
    f = open(sys.argv[2] ,'r')
    tempString = f.read()
    f.close()
    return tempString

def getTextFromPPMFile(fileName):
    imgData = ""
    headers = []
    with open(fileName, "rb") as file:
        for x in range(0,3):
            headers.append(file.readline())
        imgData = file.read()
     
    return headers,imgData



    


if len(sys.argv) != 4: 
    sys.exit("Needs three command-line arguments, one for  the encrypted file and the other for the  decrypted file and another for key ")
path='./Part2_file/'
# get key from file
key = getKey()
# get header files and image data from ppm
headerfile,imageData = getTextFromPPMFile(path+sys.argv[1])

# save the image data in a temp file
with open(path+"tempImageData.txt", "wb") as file:
    file.write(imageData)

# save the header file in the output file
with open(path+sys.argv[3], "wb") as file:
        for x in headerfile:
            file.write(x)

# get bitvector from temp file
bv  =  BitVector(filename = path+'tempImageData.txt')

   
# open output file
FILEOUT = open(path+sys.argv[3], 'ab')

# encrypt or decrypt loop
while (bv.more_to_read): #(U)

    # read 64 bits from the file
    bv_read = bv.read_bits_from_file(64)
    
    # if encrypting then Des function is called with True. else False
    if sys.argv[1] == "image.ppm":
        tempBv = DES.DES_function(bv_read.get_text_from_bitvector(), key, True)
    else:
        tempBv = DES.DES_function(bv_read.get_text_from_bitvector(), key, False)
    
    # write to output file
    tempBv.write_to_file(FILEOUT)
# close output file
FILEOUT.close()
