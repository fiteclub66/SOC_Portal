'''
Created on Apr 24, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')

cur = db.cursor(buffered=True)
cur2 = db.cursor(buffered=True)

cur.execute("SELECT userID FROM Metrics")
userList = []
for item in cur:
    userList.append(item[0])
    
for user in userList:
    metrics = []
    metrics.append(user)
    
    #Tasks Completed
    cCount = 0
    cur2.execute("SELECT COUNT(*) FROM (SELECT * FROM PastTasks WHERE userID = '"+str(user)+"')t1 WHERE t1.status='Complete'")
    for item in cur2:
        cCount=item[0]
    metrics.append(cCount)
    
    #SLA Ratio
    mCount = 0
    bCount = 1
    cur2.execute("SELECT COUNT(*) FROM (SELECT * FROM PastTasks WHERE userID = '"+str(user)+"')t1 WHERE t1.SLA='Met'")
    for item in cur2:
        mCount = item[0]
    cur2.execute("SELECT COUNT(*) FROM (SELECT * FROM PastTasks WHERE userID = '"+str(user)+"')t1 WHERE t1.SLA='Broken'")
    for item in cur2:
        if(item[0]!=0):
            bCount = item[0] 
    ratio = (mCount/bCount)
    ratio = round(ratio,2)
    metrics.append(ratio)  
    
    #Tasks Escalated
    cur2.execute("SELECT COUNT(*) FROM (SELECT * FROM PastTasks WHERE userID = '"+str(user)+"')t1 WHERE t1.status='Escalated'")
    for item in cur2:
        metrics.append(item[0])
    
    #Completion Ratio
    eCount = 1
    cur2.execute("SELECT COUNT(*) FROM (SELECT * FROM PastTasks WHERE userID = '"+str(user)+"')t1")
    for item in cur2:
        if(item[0]!=0):
            eCount = item[0] 
    ratio = (cCount/eCount)
    ratio = round(ratio,2)
    metrics.append(ratio)
    
    cur2.execute("UPDATE Metrics SET tasksCompleted = '"+str(metrics[1])+"', SLAratio = '"+str(metrics[2])+"', tasksEscalated = '"+str(metrics[3])+"', completionRatio = '"+str(metrics[4])+"' WHERE userID='"+str(metrics[0])+"'")
    
db.commit() 
cur2.close()         
cur.close()  
db.close()