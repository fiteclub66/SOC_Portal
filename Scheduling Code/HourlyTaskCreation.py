'''
Created on Mar 21, 2018

@author: zachauzenne
'''
from NewTaskRecurring import Task
import datetime
from datetime import timedelta

def adjCount(t):
    margin = timedelta(days=1)
    temp = int(margin.total_seconds())/24
    c = temp/t.freq
    return c

def nextDayTasks(rT):
    rT.setCount()
    today = datetime.datetime.today()
    current = datetime.datetime(today.year, today.month, today.day)
    targetDate = (current + timedelta(days=29))
    nextDueDate = (targetDate +  timedelta(hours=rT.freq))
    tempCount = adjCount(rT)
    while (tempCount > 0):
        taskNew = Task(rT.taskName, rT.startDate, rT.endDate, rT.freqType, rT.freq, rT.count)
        if ((nextDueDate > (targetDate + timedelta(days=1))) or (nextDueDate > rT.endDate)):
            tempCount = 0
        else:
            taskNew.startDate = nextDueDate
            nextDueDate += timedelta(hours=rT.freq)
            tempCount -= 1
            rT.count -= 1
            taskNew.count = rT.count
            tNStr = taskNew.display()
            outfile.write((str(tNStr))+"\n")

infile = open("ExistingTasks.txt", "r") 
outfile = open("NextDay.txt", "w")
for line in infile:
    name,dt1,dt2,ft,f,c = line.split("/")
    yy1,mm1,dd1,hh1 = dt1.split(",")
    yy2,mm2,dd2,hh2 = dt2.split(",")
    task1 = Task(name, datetime.datetime(int(yy1),int(mm1),int(dd1),int(hh1)), datetime.datetime(int(yy2),int(mm2),int(dd2),int(hh2)),ft,int(f),int(c))
    nextDayTasks(task1)
    
    
    #populateRecurring(task1) 