'''
Created on Mar 21, 2018

@author: zachauzenne
'''
from NewTaskRecurring import Task
import datetime
from dateutil.relativedelta import *

def nextDayTasks(rT):
    rT.setCount()
    today = datetime.datetime.today()
    current = datetime.datetime(today.year, today.month, today.day, rT.startDate.hour)
    targetDate =current+relativedelta(months=+1)
    nextDueDate = (targetDate)
    if ((rT.startDate+relativedelta(months=+1)) == targetDate):
        tempCount = 1
    else:
        tempCount = 0
    while (tempCount > 0):
        taskNew = Task(rT.taskName, rT.startDate, rT.endDate, rT.freqType, rT.freq, rT.count)
        taskNew.startDate = nextDueDate
        nextDueDate += relativedelta(months=+1)
        tempCount -= 1
        rT.count -= 1
        taskNew.count = rT.count
        tNStr = taskNew.display()
        #print tNStr
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