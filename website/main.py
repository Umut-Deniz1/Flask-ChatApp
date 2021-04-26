from flask import *
import pyrebase
import os
from firebase_admin import db
import json
from client.client import Client
import threading
import time


# your app config
config = {
    "apiKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "authDomain": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "databaseURL": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "projectId": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "storageBucket": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "messagingSenderId": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()

client = None
messages = []
userList = []
NICK = ""


app = Flask(__name__)

def disconnect():
    global client
    if client != None:
        client.disconnect()

@app.route("/forgotpassword" , methods=['GET', 'POST'])
def forgot():
    if (request.method == 'POST'):
        email = request.form['Email']
        auth.send_password_reset_email(email)
        return render_template('index.html')
    return render_template("forgotpassword.html")


@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['signUpEmail']
        password = request.form['signUpPassword']
        username = request.form['signUpUsername']
        
        global client
        global NICK
        users = db.child("users").get()
        if users.val() != "none":
            for user in users.each():
                userList.append(user.val())

            unseccessful = "Username has already taken"
            forgot_message = "E-mail has already taken"

            for user in userList:
                newUser = user.get("username")
                newUserMail = user.get("email")
                
                if newUserMail == email:
                    return render_template("signup.html", forgot_message = forgot_message)
                if newUser == username:
                    return render_template("signup.html", unmessage = unseccessful)

            NICK = username
            client = Client(NICK) 
            print(NICK)    
        db.child("users").push({
            "email": email,
            "username": username
        })  
        try:
            auth.create_user_with_email_and_password(email, password)
        except:
            unseccessful = "Make sure you enter it completely"
            if username == "" or email == "" or password == "":
                return render_template("signup.html", unmessage = unseccessful)

        return render_template("chat.html")
    return render_template("signup.html")


@app.route("/" , methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        email = request.form['signInEmail']
        password = request.form['signInPassword']

        global client 
        global NICK

        users = db.child("users").get()
        if users.val() != "none":
            for user in users.each():
                userList.append(user.val())
                
            for user in userList:
                newUser = user.get("username")
                newUserMail = user.get("email")

                
                if newUserMail == email:
                    NICK = newUser
            client = Client(NICK)
            print(NICK)

        try:
            auth.sign_in_with_email_and_password(email, password)
            # user_id = auth.get_account_info(user['idToken'])
            # session['usr'] = user_id
            # print(session['usr'])  
            return render_template("chat.html")
        except:
            unseccessful = "please check your e-mail or password"
            return render_template("index.html", unmessage = unseccessful)

    return render_template("index.html")

@app.route("/run", methods=['GET'])
def run(url=None):
    global client
    msg = request.args.get("val")
    if client != None:
        client.write(msg)
    print(msg)         
    return "none"



def update_messages():
    global messages
    run = True
    while run:
        time.sleep(0.1)
        if not client: 
            continue
        new_messages = client.get_messages()
        messages.extend(new_messages)

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})



if __name__ == "__main__": 
    threading.Thread(target=update_messages).start()
    app.run()