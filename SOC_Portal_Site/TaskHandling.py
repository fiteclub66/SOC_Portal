'''
Created on Apr 15, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
import NewTaskRecurring
from NewTaskRecurring import Task

def taskIntake(cN, tN, csID, sD, eD, fT, f):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    #WHERE INITIAL TASK VALUES WILL BE SET
    iTask = Task(0, cN, tN, csID, sD, eD, fT, f, "0", "NEW", "", "", 0, 0);

    #INSERT THE FIRST TASK
    insertTask = ("INSERT INTO UpcomingTasks "
                   "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    taskData = (iTask.clientName, iTask.taskName, iTask.catSkillID, iTask.startDate, iTask.endDate, iTask.freqType, iTask.frequency, iTask.totalTime, iTask.status, iTask.SLA, iTask.specialNotes, iTask.counter, iTask.subTask)
    
    cur.execute(insertTask,taskData)
    db.commit()
    
    #SELECT AND UPDATE NEW TASKS 29 DAYS OUT
    q2 = ("SELECT * FROM UpcomingTasks WHERE taskName = '"+iTask.taskName+"'")
    cur.execute(q2)
    
    for (taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask) in cur:
        tList = NewTaskRecurring.main(taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask)
        for item in tList:
            if(item.freqType != "Monthly"):
                insertTask = ("INSERT INTO UpcomingTasks "
                              "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
                taskData = (item.clientName, item.taskName, item.catSkillID, item.startDate, item.endDate, item.freqType, item.frequency, item.totalTime, item.status, item.SLA, item.specialNotes, item.counter, item.subTask)
        
                cur.execute(insertTask,taskData)
            else:
                print ("Monthly")
    db.commit()          
    cur.close()  
    db.close()

