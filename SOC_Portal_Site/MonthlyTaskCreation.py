'''
Created on Apr 9, 2018

@author: zachauzenne
'''
import mysql.connector
from NewTaskRecurring import Task
import datetime
from dateutil.relativedelta import *

taskList = []
def nextDayTasks(rT):
    rT.setCount()
    rT.counter -= 1
    sT = rT.subTask+1
    today = datetime.datetime.today()
    current = datetime.datetime(today.year, today.month, today.day, rT.startDate.hour)
    targetDate = current+relativedelta(months=+1)
    nextDueDate = (targetDate)
    if ((rT.startDate+relativedelta(months=+1)) == targetDate):
        tempCount = 1
    else:
        tempCount = 0
    while (tempCount > 0):
        taskNew = Task(rT.taskID, rT.clientName, rT.taskName, rT.catSkillID, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask)
        taskNew.startDate = nextDueDate
        nextDueDate += relativedelta(months=+1)
        tempCount -= 1
        rT.counter -= 1
        taskNew.subTask = sT
        sT+=1
        taskNew.count = rT.counter
        taskList.append(taskNew)

def main(tID, cN, tN, csID, sD, eD, fT, f, spN, c, sT):
    rootTask = Task(tID, cN, tN, csID, sD, eD, fT, f, "0", "NEW", "PENDING", spN, c, sT)
    nextDayTasks(rootTask)
    return taskList

def monthlyUpdate():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    query = ("SELECT * FROM (SELECT DISTINCT taskName, min(counter) as mincounter FROM UpcomingTasks WHERE freqType = ('Monthly') GROUP BY taskName) AS x INNER JOIN UpcomingTasks as f on f.taskName = x.taskName and f.counter = x.mincounter")
    cur.execute(query)
    
    if(cur.rowcount != 0):
        for (item) in cur:
            tList = main(item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[13], item[14], item[15])
            for item in tList:
                insertTask = ("INSERT INTO UpcomingTasks "
                              "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
                taskData = (item.clientName, item.taskName, item.catSkillID, item.startDate, item.endDate, item.freqType, item.frequency, item.totalTime, item.status, item.SLA, item.specialNotes, item.counter, item.subTask)
        
                cur.execute(insertTask,taskData)
            
    db.commit()          
    cur.close()  
    db.close()
    return (("Monthly done at "+str(datetime.datetime.now())))
