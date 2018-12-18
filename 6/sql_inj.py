from flask import Flask, render_template, request, flash
app = Flask(__name__)

import mysql.connector
#enter user, database and password before running
try:
    conn = mysql.connector.connect(database="", user="",host="127.0.0.1",password="")
except:
    print("Edit code and enter database username and password")
    exit(0)
cursor = conn.cursor(buffered=True)


@app.route('/')
@app.route('/home.html')
def show_content(name=None):
    return render_template('home.html', name=name)

@app.route('/', methods=['POST','GET'])
@app.route('/home.html', methods=['POST', 'GET'])
def perform_attack(name=None):
    query = request.form['query']
    #change query accoding to your database
    query = "select * from player where name = '"+query+"';"
    #flask doesn't allow multiple queries 
    queries = query.split(";")
    output = []
    for i in queries:
        if i.count("drop") or i.count("remove") or i.count("delete"):
            #just to avoid deleting useful database while experimenting
            break
        if i:
            try:
                cursor.execute((i+";"))
                output += [j for j in cursor]
            except:
                pass
    return render_template('home.html', name=name, content = output)
