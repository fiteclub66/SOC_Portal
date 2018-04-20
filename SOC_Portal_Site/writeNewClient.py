'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
from flask import Flask, render_template

def addClient(cN, e, pN, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    catSkills = cS.split(',')
    cID = 0
    insertClient = ("INSERT INTO ClientInformation "
                   "(clientName, email, phoneNumber) "
                   "VALUES (%s, %s, %s)")
    
    clientData = (cN, e, pN)
    
    cur.execute(insertClient,clientData)
    
    q1 = ("SELECT clientID FROM ClientInformation WHERE clientName = '"+cN+"'")
    cur.execute(q1)
    
    for clientID in cur:
        cID = clientID[0]
    
    for item in catSkills:
        if item != "":
            insertCat = ("INSERT INTO ClientSkillsets "
                       "(clientID, catSkillID) "
                       "VALUES (%s, %s)")
        
            catData = (cID, item)
            cur.execute(insertCat,catData)
    
    db.commit()
    cur.close()  
    db.close()
    
def addEditClient(cID, cN, e, pN, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    catSkills = cS.split(',')
    cliID = str(cID)
    oldName = ""
    
    #GETS OLD NAME FOR CLIENT
    cur.execute("SELECT clientName FROM ClientInformation WHERE clientID ="+cliID+"")
    for item in cur:
        oldName = item[0]
        
    #SETS FOREIGN KEY CHECK TO ) AND UPDATE CLIENT INFO TABLE
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("UPDATE ClientInformation SET clientName = '"+cN+"', email = '"+e+"', phoneNumber = '"+pN+"' WHERE clientID = "+cliID+"")
    
    #CHECKS TO SEE IF THERE ARE ANY WITH THE CLIENT NAME IN UPCOMING TASKS
    empty = True; 
    cur.execute("SELECT clientName FROM UpcomingTasks HAVING clientName = '"+oldName+"'")
    for item in cur:
        empty = False;
        
    #IF YES, UPDATE ALL THOSE TASKS
    if empty == False:
        cur.execute("UPDATE UpcomingTasks SET clientName = '"+cN+"' WHERE clientName = '"+oldName+"'")
        
    #CHECKS TO SEE IF THERE ARE ANY WITH CLIENT NAME IN PAST TASKS   
    empty = True; 
    cur.execute("SELECT clientName FROM PastTasks HAVING clientName = '"+oldName+"'")
    for item in cur:
        empty = False;
        
    #IF YES, UPDATE ALL THOSE TASKS
    if empty == False:    
        cur.execute("UPDATE PastTasks SET clientName = '"+cN+"' WHERE clientName = '"+oldName+"'")
    cur.execute("SET foreign_key_checks = 1")
    
    #DELETE ALL SKILLSETS AND START FROM SCRATCH
    q2 = ("DELETE FROM ClientSkillsets WHERE clientID = "+str(cliID)+"")
    cur.execute(q2)
    
    #UPDATE CLIENT SKILLSET RELATIONS WITH NEW SET OF SKILLSETS
    for item in catSkills:
        if item != "":
            insertCat = ("INSERT INTO ClientSkillsets "
                       "(clientID, catSkillID) "
                       "VALUES (%s, %s)")
        
            catData = (cID, item)
            cur.execute(insertCat,catData)
    
    db.commit()
    cur.close()  
    db.close()

def deleteClient(cID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM ClientInformation WHERE clientID = "+str(cID)+"")
    cur.execute("SET foreign_key_checks = 1")
    
    db.commit()
    cur.close()  
    db.close()
