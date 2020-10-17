from flask import Flask, render_template, request, json, session, render_template
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import imaplib
import email
from bs4 import BeautifulSoup



app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)




def insertarUsuario(_name, _lastname, _email, _password):
    if _name and _lastname and _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO USERS (name, last_name, email, password) VALUES (%s, %s, %s, %s)", (_name, _lastname, _email, _password))
        conn.commit()
        data = cursor.fetchall()
        return data
        
    cursor.close()
    conn.close()      

def login( _email, _password):
    if _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            sqld="DROP PROCEDURE IF EXISTS login;"
            cursor.execute(sqld)
            sql="CREATE PROCEDURE login(IN p_email VARCHAR(60), IN p_password VARCHAR(60)) SELECT * FROM  USERS WHERE email = p_email AND password = p_password"
            cursor.execute(sql)
            cursor.callproc('login', (_email, _password))
            #cursor.execute("SELECT * FROM USERS WHERE email = %s AND password = %s", (_email, _password))
            data = cursor.fetchall()

            if len(data) > 0:
                if check_password_hash(str(data[0][4]),_password.encode('utf-8')):
                    session['name'] = data[0][1]
                return render_template("jennito.html")   
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
                ##convertirlo en notificación
                
    conn.close() 
    cursor.close() 

def SelectAll():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "ASPIRANTE"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

