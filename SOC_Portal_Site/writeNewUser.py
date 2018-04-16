'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
from flask import Flask, render_template

def addUser(u, pW, fN, lN, e, pN, p):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    insertUser = ("INSERT INTO Users "
                   "(username, password, firstName, lastName, email, phoneNumber, position) "
                   "VALUES (%s, %s, %s, %s ,%s, %s, %s)")
    
    userData = (u, pW, fN, lN, e, pN, p)
    
    cur.execute(insertUser,userData)
    db.commit()
    cur.close()  
    db.close()