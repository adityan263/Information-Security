def encrypt(key, plain_text):
    cipher_text = ""
    k_len = len(key)
    p_len = len(plain_text)
    for i in range(p_len):
        cipher_text += chr(97 + (ord(key[i%k_len]) +
            ord(plain_text[i]) - 97*2)%26) 
    return cipher_text

def decrypt(key, cipher_text):
    plain_text = ""
    k_len = len(key)
    c_len = len(cipher_text)
    for i in range(c_len):
        plain_text += chr(97 + (ord(cipher_text[i]) -
            ord(key[i%k_len]))%26)
    return plain_text


if __name__ == "__main__":
    plain_text = input("Enter plain text: ").lower()
    key = input("Enter key: ").lower()
    encrypted_text = encrypt(key, plain_text)
    print("Encrypted text: " + encrypted_text)
    decrypted_text = decrypt(key, encrypted_text)
    try:
        assert decrypted_text == plain_text
        print("Decryption Successful")
    except AssertionError:
        print("Output: expected=" + plain_text + " decryption=" + decrypted_text)
