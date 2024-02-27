def ListToWord(array):
  res =''.join(map(chr, array))
  return str(res)

def decryption(cipher, key):
  m = []
  c0 = 0

  for i in range(len(cipher)):
    n = (key[i] + c0) % 256
    m.append(cipher[i]^n)
    c0 = cipher[i]

  tmp =''.join(map(chr, m))
  print(tmp)
  return str(tmp)


def isValidCharacter(c):
    if c in keyletters:
        return True
    elif ord('a') <= ord(c) <= ord('z'):
        return True
    elif ord('A') <= ord(c) <= ord('Z'):
        return True
    return False

def isValidString(s):
    for i in s:
        if not isValidCharacter(i):
            return False
    return True


ciphertext = []
f = open('input2.txt')
for line in f:
    ciphertext.append(eval(line))

keyletters = ' ,.?!-()'
cipher_line = len(ciphertext)
length = len(ciphertext[0])


prefixDictionary = {}
prefixDictionary[''] = 1

with open('words.txt') as f:
  words = f.read().split()

for word in words:
    temp = word.lower()
    for i in range(len(temp)):
        prefixDictionary[temp[0:i+1].lower()] = 1

all_keys = [[]]

for i in range(0, length):
    tmp_key = []
    for k in all_keys:
        for l in range(256):
            flag = True
            for j in range(cipher_line): 
                partMessage = decryption(ciphertext[j][0:i+1], k + [l])
                if not isValidCharacter(partMessage[-1]):
                    flag = False
                    break
                word = []
                for h in range(i, -1, -1):
                    if not partMessage[h].isalpha():
                        break
                    word.append(partMessage[h])
                word.reverse()
                word = ''.join(word).lower()
                if word not in prefixDictionary:
                    flag = False
                    break
            if flag:
                tmp_key.append(k+[l])    
    all_keys = tmp_key

key=all_keys[1]
print(f"key= {key}")
for i in range(cipher_line):
    print(decryption(ciphertext[i], key))