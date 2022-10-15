from email import message
import os
from datetime import datetime

def errorRegister(error):
    path = "error.log"
    now = datetime.now()
    date = now.strftime("%H:%M:%S %B %d, %Y")
    message = f"""-{date}____{error}"""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write("don't worry be happy :) \n"+message)
    else:
        with open("sample.txt", "a") as f:
            f.write("\n"+message)

def queryRegister(query):
    path = "query.log"
    now = datetime.now()
    date = now.strftime("%H:%M:%S %B %d, %Y")
    message = f"""-{date}____{query}"""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write("se cayo el servicio puede que el culpable este aqui, \n si no esta es culpa de felipe \n"+message)
    else:
        with open("sample.txt", "a") as f:
            f.write("\n"+message)