'''
Created on Apr 17, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def editCatSkills(cID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    catSkills = []
    clientCatSkills = []
    clientInfo = []
    q1 = ("SELECT * FROM ClientInformation WHERE clientID = "+str(cID)+"")
    cur.execute(q1)
    for item in cur:
        clientInfo = item
    
    query = ("SELECT j1.clientID, j1.clientName, j1.catSkillID, j2.category, j2.skillset FROM ((SELECT t1.clientID, clientName, catSkillID FROM ((SELECT * FROM ClientInformation WHERE clientID = "+str(cID)+") t1 INNER JOIN (SELECT * FROM ClientSkillsets) t2 ON t1.clientID = t2.clientID)) j1 INNER JOIN (SELECT * FROM CategoryRelations) j2 ON j1.catSkillID = j2.catSkillID) ORDER BY j1.catSkillID ASC")
    cur.execute(query)
    for item in cur:
        clientCatSkills.append(item)
    
    q2 = ("SELECT * FROM CategoryRelations")
    cur.execute(q2)
    for item in cur:
        catSkills.append(item)
    
    
    cur.close()
    db.close()
    return (catSkills, clientCatSkills, clientInfo)
