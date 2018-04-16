'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
from flask import Flask, render_template

def addClient(cN, e, pN):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    insertClient = ("INSERT INTO ClientInformation "
                   "(clientName, email, phoneNumber) "
                   "VALUES (%s, %s, %s)")
    
    clientData = (cN, e, pN)
    
    cur.execute(insertClient,clientData)
    db.commit()
    cur.close()  
    db.close()