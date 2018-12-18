from sys import exit
from time import time
 
KeyLength = 10
SubKeyLength = 8
DataLength = 8
FLength = 4
 
initialPermutationTable = (2, 6, 3, 1, 4, 8, 5, 7)
finalPermutationTable = (4, 1, 3, 5, 7, 2, 8, 6)
 
P10table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8table = (6, 3, 7, 4, 8, 5, 10, 9)
 
EPtable = (4, 1, 2, 3, 2, 3, 4, 1)
S0table = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
S1table = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
P4table = (2, 4, 3, 1)
 
def perm(inputByte, permTable):
    outputByte = 0
    for index, elem in enumerate(permTable):
        if index >= elem:
            outputByte |= (inputByte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            outputByte |= (inputByte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return outputByte
 
def initialPermutation(inputByte):
    return perm(inputByte, initialPermutationTable)
 
def finalPermutation(inputByte):
    return perm(inputByte, finalPermutationTable)
 
def swapNibbles(inputByte):
    return (inputByte << 4 | inputByte >> 4) & 0xff
 
def keyGen(key):
    def leftShift(keyBitList):
        shiftedKey = [0] * KeyLength
        shiftedKey[0:9] = keyBitList[1:10]
        shiftedKey[4] = keyBitList[0]
        shiftedKey[9] = keyBitList[5]
        return shiftedKey
 
    keyList = [(key & 1 << i) >> i for i in reversed(range(KeyLength))]
    permKeyList = [0] * KeyLength
    for index, elem in enumerate(P10table):
        permKeyList[index] = keyList[elem - 1]
    shiftedOnceKey = leftShift(permKeyList)
    shiftedTwiceKey = leftShift(leftShift(shiftedOnceKey))
    subKey1 = subKey2 = 0
    for index, elem in enumerate(P8table):
        subKey1 += (128 >> index) * shiftedOnceKey[elem - 1]
        subKey2 += (128 >> index) * shiftedTwiceKey[elem - 1]
    return (subKey1, subKey2)
 
def fk(subKey, inputData):
    def F(sKey, rightNibble):
        #permutation and exor
        data = sKey ^ perm(swapNibbles(rightNibble), EPtable)
        #row,column for sbox
        index1 = ((data & 0x80) >> 4) | ((data & 0x40) >> 5) | \
                 ((data & 0x20) >> 5) | ((data & 0x10) >> 2)
        index2 = ((data & 0x08) >> 0) | ((data & 0x04) >> 1) | \
                 ((data & 0x02) >> 1) | ((data & 0x01) << 2)
        sboxOutputs = swapNibbles((S0table[index1] << 2) | S1table[index2])
        return perm(sboxOutputs, P4table)
 
    leftNibble, rightNibble = inputData & 0xf0, inputData & 0x0f
    return (leftNibble ^ F(subKey, rightNibble)) | rightNibble
 
def applyProcedure(key, plaintext, a):
    generatedKey = keyGen(key)

    data = initialPermutation(plaintext)
    data = fk(generatedKey[a%2], data)
    data = swapNibbles(data)

    data = fk(generatedKey[(a+1)%2], data)

    return finalPermutation(data)

def encrypt(key, plaintext):
    return applyProcedure(key, plaintext, 0)

def decrypt(key, plaintext):
    return applyProcedure(key, plaintext, 1)

if __name__ == '__main__':
    plaintext = 0b10101010
    key = 0b1110001110
    print("plaintext:"+str(bin(plaintext)))
    encrypted = encrypt(key, plaintext)
    print("encrypted:"+str(bin(encrypted)))
    decrypted = decrypt(key, encrypted)
    print("decrypted:"+str(bin(decrypted)))
    try:
        assert plaintext == decrypted
        print("Success")
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", str(bin(decrypted)), "Expected: ", str(bin(plaintext)))
