'''
Created on Apr 19, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def fillUsers():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    cur2 = db.cursor(buffered=True)
    
    uInfo = []
    catSkills = []
    
    query = ("SELECT * FROM Users")
    cur.execute(query)
    
    for item in cur:
        uInfo.append(item)
        q2 = ("SELECT j1.userID, j1.userName, j1.catSkillID, j2.category, j2.skillset FROM ((SELECT t1.userID, userName, catSkillID FROM ((SELECT * FROM Users WHERE userID = "+str(item[0])+") t1 INNER JOIN (SELECT * FROM SkillsetRelations) t2 ON t1.userID = t2.userID)) j1 INNER JOIN (SELECT * FROM CategoryRelations) j2 ON j1.catSkillID = j2.catSkillID) ORDER BY j1.catSkillID ASC")
        cur2.execute(q2)
        ulist = []
        for thing in cur2:
            ulist.append(thing)
        catSkills.append(ulist) 
        
    cur.close()
    cur2.close()
    db.close()
    return (uInfo,catSkills)