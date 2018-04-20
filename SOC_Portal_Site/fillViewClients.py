'''
Created on Apr 17, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def fillClients():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    cur2 = db.cursor(buffered=True)
    
    cInfo = []
    catSkills = []
    
    query = ("SELECT * FROM ClientInformation")
    cur.execute(query)
    
    for (clientID, clientName, email, phoneNumber) in cur:
        cInfo.append((clientID, clientName, email, phoneNumber))
    
        q2 = ("SELECT j1.clientID, j1.clientName, j1.catSkillID, j2.category, j2.skillset FROM ((SELECT t1.clientID, clientName, catSkillID FROM ((SELECT * FROM ClientInformation WHERE clientID = "+str(clientID)+") t1 INNER JOIN (SELECT * FROM ClientSkillsets) t2 ON t1.clientID = t2.clientID)) j1 INNER JOIN (SELECT * FROM CategoryRelations) j2 ON j1.catSkillID = j2.catSkillID) ORDER BY j1.catSkillID ASC")
        cur2.execute(q2)
        clist = []
        for thing in cur2:
            clist.append(thing)
        catSkills.append(clist) 
        
    cur.close()
    cur2.close()
    db.close()
    return (cInfo,catSkills)