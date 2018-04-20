'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
from flask import Flask, render_template

def addUser(u, pW, fN, lN, e, pN, p, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    catSkills = cS.split(',')
    uID = 0
    
    insertUser = ("INSERT INTO Users "
                   "(username, password, firstName, lastName, email, phoneNumber, position) "
                   "VALUES (%s, %s, %s, %s ,%s, %s, %s)")
    
    userData = (u, pW, fN, lN, e, pN, p)
    cur.execute(insertUser,userData)
    
    q1 = ("SELECT userID FROM Users WHERE password = '"+pW+"'")
    cur.execute(q1)
    
    for userID in cur:
        uID = userID[0]
    
    for item in catSkills:
        if item != "":

            insertCat = ("INSERT INTO SkillsetRelations "
                       "(userID, catSkillID) "
                       "VALUES (%s, %s)")
        
            catData = (uID, item)
            cur.execute(insertCat,catData)
    
    db.commit()
    cur.close()  
    db.close()
    
def addEditUser(uID, u, pW, fN, lN, e, pN, p, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    catSkills = cS.split(',')
    usID = uID
    
    #SETS FOREIGN KEY CHECK TO ) AND UPDATE USER INFO TABLE
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("UPDATE Users SET username = '"+u+"', password = '"+pW+"', firstName = '"+fN+"', lastName = '"+lN+"', email = '"+e+"', phoneNumber = '"+pN+"', position = '"+p+"' WHERE userID = "+usID+"")
    cur.execute("SET foreign_key_checks = 1")
    
    #DELETE ALL SKILLSETS AND START FROM SCRATCH
    q2 = ("DELETE FROM SkillsetRelations WHERE userID = "+usID+"")
    cur.execute(q2)
    
    #UPDATE USER SKILLSET RELATIONS WITH NEW SET OF SKILLSETS
    for item in catSkills:
        if item != "":
            insertCat = ("INSERT INTO SkillsetRelations "
                       "(userID, catSkillID) "
                       "VALUES (%s, %s)")
        
            catData = (usID, item)
            cur.execute(insertCat,catData)
    
    db.commit()
    cur.close()  
    db.close()

def deleteUser(uID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM Users WHERE userID = "+str(uID)+"")
    cur.execute("SET foreign_key_checks = 1")
    
    db.commit()
    cur.close()  
    db.close() 
