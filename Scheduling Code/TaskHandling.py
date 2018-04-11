'''
Created on Mar 29, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
import NewTaskRecurring
from NewTaskRecurring import Task

db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')


cur = db.cursor(buffered=True)
#WHERE INITIAL TASK VALUES WILL BE SET

#INSERT THE FIRST TASK
query = ("INSERT INTO UpcomingTasks (taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) VALUES (1, BMT, Task1, 1001, (2018,04,03,1), (2018,08,21,1), Daily, 1, 0, 0, 0, pending, SLA, This is a task, 0, 0)")

insertTask = ("INSERT INTO UpcomingTasks "
               "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

taskData = ("Liberty Behavioral","Task3",1004,datetime.datetime(2018,4,8,1),datetime.datetime(2018,6,03,1),"Daily", 1, 0, 0, 0, "pending", "SLA", "DESCRIPTION!", 0, 0)

cur.execute(insertTask,taskData)
db.commit()

#SELECT AND UPDATE NEW TASKS 29 DAYS OUT
q2 = ("SELECT * FROM UpcomingTasks WHERE taskName = 'Task3'")
cur.execute(q2)

for (taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) in cur:
    tList = NewTaskRecurring.main(taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask)
    for item in tList:
        if(item.freqType != "Monthly"):
            query = ("INSERT INTO UpcomingTasks (taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) VALUES (1, BMT, Task1, 1001, (2018,04,03,1), (2018,08,21,1), Daily, 1, 0, 0, 0, pending, SLA, This is a task, 0, 0)")
            insertTask = ("INSERT INTO UpcomingTasks "
                          "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
            taskData = (item.clientName, item.taskName, item.catSkillID, item.startDate, item.endDate, item.freqType, item.frequency, item.startTime, item.stopTime, item.totalTime, item.status, item.SLA, item.specialNotes, item.counter, item.subTask)
    
            cur.execute(insertTask,taskData)
        else:
            print "Monthly"
db.commit()          
cur.close()  
db.close()