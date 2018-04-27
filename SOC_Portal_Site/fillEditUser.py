'''
Created on Apr 19, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def editUserCatSkills(uID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    catSkills = []
    userCatSkills = []
    userInfo = []
    q1 = ("SELECT * FROM Users WHERE userID = "+str(uID)+"")
    cur.execute(q1)
    for item in cur:
        userInfo = item
    
    query = ("SELECT j1.userID, j1.userName, j1.catSkillID, j2.category, j2.skillset FROM ((SELECT t1.userID, userName, catSkillID FROM ((SELECT * FROM Users WHERE userID = "+str(uID)+") t1 INNER JOIN (SELECT * FROM SkillsetRelations) t2 ON t1.userID = t2.userID)) j1 INNER JOIN (SELECT * FROM CategoryRelations) j2 ON j1.catSkillID = j2.catSkillID) ORDER BY j1.catSkillID ASC")
    cur.execute(query)
    for item in cur:
        userCatSkills.append(item)
    
    q2 = ("SELECT * FROM CategoryRelations")
    cur.execute(q2)
    for item in cur:
        catSkills.append(item)
    
    
    cur.close()
    db.close()
    return (catSkills, userCatSkills, userInfo)
