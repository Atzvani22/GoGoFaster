import imaplib
import email
from bs4 import BeautifulSoup


m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login("j.consultora.a@gmail.com","Consulta2.ja")
m.select("INBOX")
#función que reciba los datos de arriba
#meter todo a una función
#en return devolver el text
#el correo es el que cambia 
#return devuelve lo (fdatos)que esta en print

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
        soup = BeautifulSoup(text,"lxml")
           
        print (soup.prettify())
        
        context = soup.find_all('b')
        print(len(context)) #esto es lo que devuelve
        print(context[0].get_text().encode('utf-8'))
        print(context[1].get_text())
        print(context[2].get_text())
        #mandar los datos en html para que tenga las ñ y acentos
        #que se verifique o modifique y de ahi se guarda a la base de datos

m.close()
m.logout()