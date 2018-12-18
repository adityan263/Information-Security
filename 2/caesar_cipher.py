def encrypt(key, plain_text):
    cipher_text = ""
    for l in plain_text:
        if (ord(l) >= 97):
            cipher_text += chr(97 + (ord(l)-97 + key)%26)
        else:
            cipher_text += chr(65 + (ord(l)-65 + key)%26)
    return cipher_text

def decrypt(key, cipher_text):
    plain_text = ""
    for l in cipher_text:
        if (ord(l) >= 97):
            plain_text += chr(97 + (ord(l)-97 - key)%26)
        else:
            plain_text += chr(65 + (ord(l)-65 - key)%26)
    return plain_text


if __name__ == "__main__":
    plain_text = input("Enter plain text: ") 
    key = int(input("Enter integer key: "))
    encrypted_text = encrypt(key, plain_text)
    print("Encrypted text: " + encrypted_text)
    decrypted_text = decrypt(key, encrypted_text)
    try:
        assert decrypted_text == plain_text
        print("Decryption Successful")
    except AssertionError:
        print("Output: expected=" + plain_text + " decryption=" + decrypted_text)
