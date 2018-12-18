from myModule import encrypt
import requests
import getpass

username = input("Username: ")
try:
    password = getpass.getpass()

except Exception as error:
    print('Error',error)
    exit()
enc_password = encrypt(password)
data={'username': username, 'password': enc_password}
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post('http://localhost:5000/login', data=data, headers=headers)
print(r.text)
