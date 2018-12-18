from flask import Flask, render_template, request,flash
app = Flask(__name__)

from myModule import decrypt

passwords = {
        "user": "password",
        "admin": "admin",
        "aditya": "neralkar",
        "abcd":"abcd"
        }

@app.route('/')
@app.route('/login', methods=['POST','GET'])
def login_page(name=None):
    data=str(request.data)[2:-1]
    print(data)
    a = data.split("&")
    if a[0][0] == 'u':
        username = a[0].split("=")[1]
        password = a[1].split("=")[1]
    else:
        username = a[1].split("=")[1]
        password = a[0].split("=")[1]
    try:
        if(passwords[username] == decrypt(password)):
            return('Login successful for '+username)
        return("incorrect password")
    except:
        return("incorrect username: "+username)
