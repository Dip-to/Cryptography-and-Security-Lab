import sys
from BitVector import BitVector
import re

if len(sys.argv) != 3:
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

ciphertext_file = sys.argv[1]
output_file = sys.argv[2]
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
def decrypt_for_fun(ciphertext, key_bv, bv_iv):
    BLOCKSIZE = 16
    msg_decrypted_bv = BitVector(size=0)

    previous_decrypted_block = bv_iv
    for i in range(0, len(ciphertext) // BLOCKSIZE):
        bv = ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        temp = bv.deep_copy()
        bv ^= previous_decrypted_block
        previous_decrypted_block = temp
        bv ^= key_bv
        msg_decrypted_bv += bv

    return msg_decrypted_bv.get_text_from_bitvector()


#i= 29556
def brute_force_attack(ciphertext, bv_iv):
    for i in range(29500,2**16):
        # print(i)
        key_bv = BitVector(intVal=i, size=16)
        predicted_text = decrypt_for_fun(ciphertext, key_bv, bv_iv)
        if "Douglas Adams" in predicted_text:
            key_string = key_bv.get_bitvector_in_ascii()
            write_to_file(output_file, predicted_text)
            print(f"Key: {key_string}\n\nDecrypted text: {predicted_text}")
            break

# Initialize passphrase and IV
PassPhrase = "Hopes and dreams of a million years"
bv_iv = BitVector(bitlist=[0]*16)
for i in range(0, len(PassPhrase) // 2):
    textstr = PassPhrase[i*2:(i+1)*2]
    bv_iv ^= BitVector(textstring=textstr) #1101


ciphertext_encrpyted = read_from_file(ciphertext_file)
ciphertext_BV = BitVector(hexstring=ciphertext_encrpyted)

brute_force_attack(ciphertext_BV, bv_iv)
