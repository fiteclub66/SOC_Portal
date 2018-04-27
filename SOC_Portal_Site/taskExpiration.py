'''
Created on Apr 24, 2018

@author: zachauzenne
'''
import mysql.connector
from datetime import timedelta, datetime
from flask import Flask, render_template

db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
cur = db.cursor(buffered=True)

t = datetime.now()
currentTime = t

query = ("SELECT taskID, startDate FROM UpcomingTasks WHERE startDate<'"+str(currentTime)+"'")
cur.execute(query)

if (cur.rowcount != 0):
    cur2 = db.cursor(buffered=True)
    for item in cur:
        q2 = ("DELETE FROM UpcomingTasks WHERE taskID = "+str(item[0])+"")
        cur2.execute(q2)
        
        
db.commit()          
cur.close()
cur2.close()  
db.close()