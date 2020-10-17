from flask import Flask, render_template, request, json, url_for, session, redirect
from flaskext.mysql import MySQL
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import os
import Modelo as Modelo
import imaplib
import email
from bs4 import BeautifulSoup
from plyer import notification
#import Email as Em

app = Flask(__name__)
app.secret_key = 'matangalachanga'



@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == "POST":
        _n = request.form['Name']
        _l = request.form['Lastname']
        _e = request.form['Email']
        _p = request.form['Password']
        #.encode('utf-8')
        #hash_p = bcrypt.hashpw(_p, bcrypt.gensalt())
        notification.notify(
                title="ÉXITO",
                message="Te registraste con éxito",
                timeout=10
            )

        if _n and _l and _e and _p:
            Modelo.insertarUsuario(_n, _l, _e, _p)
            return redirect(url_for("login"))
            
            
        else:
            return "Error correo y contra"
            
    else:
        return render_template("Register.html")
        notification.notify(
                title="ERROR",
                message="No te pudiste registrar",
                timeout=10
            )


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _e = request.form['Email']
        _p = request.form['Password']
        #.encode('utf-8')
        
        if _e and _p:
            return Modelo.login(_e, _p)
            #_a = m.login(_e,_p)

    else:
        return render_template("Login.html")



m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login("j.consultora.a@gmail.com","Consulta2.ja")
m.select("INBOX")

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


result, data = m.uid('search', None, "ALL") # search all email and return uids
if result == 'OK':
    for num in data[0].split():
        result, data = m.uid('fetch', num, '(RFC822)')
        text = str(data[0][1])
        soup = BeautifulSoup(text,"html.parser")
        #print (soup.prettify())       
        context = soup.find_all('b')
        count =(len(context))
        a = (context[0].get_text())
        b = (context[1].get_text())
        c = (context[2].get_text())

m.close()
m.logout()











    


if __name__ == "__main__":
    app.run(debug=True)

