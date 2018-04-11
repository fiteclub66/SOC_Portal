'''
Created on Apr 9, 2018

@author: zachauzenne
'''
import mysql.connector
from NewTaskRecurring import Task
import datetime
from datetime import timedelta

taskList = []
def nextDayTasks(rT):
    rT.setCount()
    rT.counter -= 1
    sT = rT.subTask+1
    today = datetime.datetime.today()
    current = datetime.datetime(today.year, today.month, today.day, rT.startDate.hour)
    targetDate = (current + timedelta(days=29))
    nextDueDate = (targetDate)
    dateDiff = nextDueDate - rT.startDate
    #print dateDiff
    if (dateDiff.days % 7) == 0:
        tempCount = 1
    else:
        tempCount = 0
    while (tempCount > 0):
        taskNew = Task(rT.taskID, rT.clientName, rT.taskName, rT.catSkillID, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.startTime, rT.stopTime, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask)
        taskNew.startDate = nextDueDate
        nextDueDate += timedelta(days=rT.frequency)
        tempCount -= 1
        rT.counter -= 1
        taskNew.subTask = sT
        sT+=1
        taskNew.count = rT.counter
        taskList.append(taskNew)

def main(tID, cN, tN, csID, sD, eD, fT, f, staT, stoT, totT, stat, SLA, spN, c, sT):
    rootTask = Task(tID, cN, tN, csID, sD, eD, fT, f, staT, stoT, totT, stat, SLA, spN, c, sT)
    nextDayTasks(rootTask)
    return taskList

db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')


cur = db.cursor(buffered=True)

query = ("SELECT * FROM (SELECT DISTINCT taskName, min(counter) as mincounter FROM UpcomingTasks WHERE freqType = ('Weekly') GROUP BY taskName) AS x INNER JOIN UpcomingTasks as f on f.taskName = x.taskName and f.counter = x.mincounter")
cur.execute(query)

for (item) in cur:
    tList = main(item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16], item[17])
    for item in tList:
        query = ("INSERT INTO UpcomingTasks (taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) VALUES (1, BMT, Task1, 1001, (2018,04,03,1), (2018,08,21,1), Daily, 1, 0, 0, 0, pending, SLA, This is a task, 0, 0)")
        insertTask = ("INSERT INTO UpcomingTasks "
                      "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        taskData = (item.clientName, item.taskName, item.catSkillID, item.startDate, item.endDate, item.freqType, item.frequency, item.startTime, item.stopTime, item.totalTime, item.status, item.SLA, item.specialNotes, item.counter, item.subTask)

        cur.execute(insertTask,taskData)
db.commit()          
cur.close()  
db.close()
