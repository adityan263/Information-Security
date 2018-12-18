import math 
import numpy as np

def encrypt(key, matrix_size, plain_text):
    pad_size = len(plain_text)%matrix_size
    if pad_size:
        plain_text += (matrix_size - pad_size)*"x"

    key_matrix = list(map(lambda k: ord(k) - 97, key))
    
    k = 0
    while matrix_size*matrix_size - len(key)-k:
        key_matrix += [k]
        k+=1
    key_matrix = np.asarray(key_matrix)
    key_matrix = key_matrix.reshape((matrix_size, matrix_size))

    plain_text_matrix = list(map(lambda k: ord(k) - 97, plain_text))
    plain_text_matrix = np.asarray(plain_text_matrix)
    plain_text_matrix = plain_text_matrix.reshape((matrix_size, len(plain_text)//matrix_size))

    cipher_text = np.dot(key_matrix, plain_text_matrix)
    cipher_text = cipher_text.flatten()

    func = lambda k: chr(k%26 + 97)
    a = np.vectorize(func)
    cipher_text = a(cipher_text)

    return cipher_text

def modInverse(det):
    # extended euclidean algorithm
    a1,a2,a3 = 1,0,26
    b1,b2,b3 = 0,1,det%26
    while b3 != 1 and b3 != 0:
        k = a3//b3
        t1 = a1-b1*k
        t2 = a2-b2*k
        t3 = a3-b3*k
        a1,a2,a3 = b1,b2,b3
        b1,b2,b3 = t1,t2,t3
    if b3 == 1:
        return b2%26
    else:
        return 0


def getCofactor(matrix, p, q, n) :
    temp = [[i for i in range(n-1)] for j in range(n-1)]
    i = 0
    j = 0
    for row in range(n):
        for col in range(n):
            if (row != p and col != q) :
                temp[i][j] = matrix[row][col]
                j += 1
                if (j == n - 1) :
                    j = 0
                    i += 1
    return temp


def key_inverse(matrix, det_inverse) :
    N = len(matrix[0])
    if (N == 1) :
        return matrix
    sign = 1
    inv_matrix = [[i for i in range(N)] for j in range(N)]

    for i in range(N):
        for j in range(N):
            temp = getCofactor(matrix, i, j, N); 
            if (i+j)%2 :
                sign = -1
            else :
                sign = 1
            det = int(round(np.linalg.det(temp)))
            inv_matrix[j][i] = (((sign)*det)%26*det_inverse)%26
    return inv_matrix

def decrypt(key, matrix_size, cipher_text):

    key_matrix = list(map(lambda k: ord(k) - 97, key))
    
    k = 0
    while matrix_size*matrix_size - len(key)-k:
        key_matrix += [k]
        k+=1
    key_matrix = np.asarray(key_matrix)
    key_matrix = key_matrix.reshape((matrix_size, matrix_size))

    cipher_text_len = len(cipher_text)
    cipher_text_matrix = list(map(lambda k: ord(k) - 97, cipher_text))
    cipher_text_matrix = np.asarray(cipher_text_matrix)
    cipher_text_matrix = cipher_text_matrix.reshape((matrix_size,cipher_text_len//matrix_size))

    if cipher_text_len % matrix_size != 0:
        print("INPUT ERROR : CIPHER_TEXT INVALID")
        exit(0)

    det = int(round(np.linalg.det(key_matrix)))
    det_inverse = modInverse(det)
    if det_inverse == 0:
        print("Determinant="+str(det))
        print("KEY ERROR : NOT_INVERSIBLE_MOD 26")
        exit()

    inverse = np.asarray(key_inverse(key_matrix, det_inverse))

    # inaccurate results while rounding values of inverse_matrix calculated using numpy
    
    #inverse = np.linalg.inv(key_matrix)*det
    #func = lambda k: (int(round(k))*det_inverse)%26
    #apply_func = np.vectorize(func)
    #inverse = apply_func(inverse)

    plain_text_matrix = np.dot(inverse, cipher_text_matrix)
    plain_text = plain_text_matrix.flatten()

    func = lambda k: chr(int(k)%26 + 97)
    apply_func = np.vectorize(func)
    plain_text = apply_func(plain_text)

    return plain_text


if __name__ == "__main__":
    key = input("Enter Key: ")
    matrix_size = int(math.ceil(math.sqrt(len(key))))
    plain_text = input("Enter plain text: ").lower()
    cipher_text = "".join(encrypt(key, matrix_size, plain_text))
    print("encrypted: " + cipher_text)
    plain_text = "".join(decrypt(key, matrix_size, cipher_text))
    print("decrypted: " +plain_text)
