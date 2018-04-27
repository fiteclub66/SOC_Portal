import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def idPosition(user):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                 host='10.0.51.21',
                                 database='SOC_Portal')
    cur = db.cursor(buffered=True)

    getInfo = ("SELECT userID, position FROM Users WHERE userName ='"+user+"';")

    cur.execute(getInfo)

    for item in cur:


        uID = item[0]
        position = item[1]

    db.commit()
    cur.close()
    db.close()
    return uID, position

def userList():
    ulist=[]
    pwlist=[]
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                 host='10.0.51.21',
                                 database='SOC_Portal')
    cur=db.cursor(buffered=True)

    getList = ("SELECT userName, password FROM Users;")

    cur.execute(getList)

    for item in cur:

        temp = item[0]
        ulist.append(temp)
        temp2 = item[1]
        pwlist.append(temp2)

    db.commit()
    cur.close()
    db.close()
    return ulist, pwlist