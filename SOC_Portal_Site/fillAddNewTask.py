'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def populateDropdowns():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    clients = []
    clientCat = []
    query = ("SELECT * FROM ClientInformation")
    cur.execute(query)
    for item in cur:
        clients.append(item)
    
    for item in clients:
        q2 = ("SELECT j1.clientID, j1.clientName, j1.catSkillID, j2.category, j2.skillset FROM ((SELECT t1.clientID, clientName, catSkillID FROM ((SELECT * FROM ClientInformation WHERE clientID = "+str(item[0])+") t1 INNER JOIN (SELECT * FROM ClientSkillsets) t2 ON t1.clientID = t2.clientID)) j1 INNER JOIN (SELECT * FROM CategoryRelations) j2 ON j1.catSkillID = j2.catSkillID) ORDER BY j1.catSkillID ASC")
        cur.execute(q2)
        clist = []
        for item in cur:
            clist.append(item)
        clientCat.append(clist)     
    
    cur.close()
    db.close()
    return (clients,clientCat)