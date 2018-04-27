'''
Created on Apr 22, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def editTaskInfo(tID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    taskInfo = []
    catSkills = []
    clients = []
    q1 = ("SELECT t2.taskID, t2.clientName, t2.taskName, t2.catSkillID, t1.category, t1.skillset, t2.startDate, t2.endDate, t2.freqType, t2.frequency, t2.totalTime, t2.status, t2.SLA, t2.specialNotes, t2.counter, t2.subTask FROM ((SELECT * FROM CategoryRelations) t1 INNER JOIN (SELECT * FROM UpcomingTasks WHERE taskID = "+str(tID)+") t2 ON (t1.catSkillID = t2.catSkillID))")
    cur.execute(q1)
    for item in cur:
        taskInfo = item
    
    q2 = ("SELECT * FROM CategoryRelations")
    cur.execute(q2)
    for item in cur:
        catSkills.append(item)
        
    q3 = ("SELECT * FROM ClientInformation")
    cur.execute(q3)
    for item in cur:
        clients.append(item)
    
    
    cur.close()
    db.close()
    return (taskInfo, catSkills, clients)
