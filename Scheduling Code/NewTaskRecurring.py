'''
Created on Mar 14, 2018

@author: zachauzenne
'''
import datetime
from datetime import timedelta

class Task(object):
    def __init__(self, taskName, startDate, endDate, freqType, freq, count):
        self.taskName = taskName
        self.startDate = startDate
        self.endDate = endDate
        self.freqType = freqType
        self.freq = freq
        self.count = count
        
    def display(self):
        t = self.taskName, str(self.startDate), str(self.endDate), self.freqType, self.freq, self.count
        return t
    
    def setCount(self):
        dateDiff = self.endDate - self.startDate
        if(self.freqType=="Singular"):
            self.count=0
        elif(self.freqType=="Minutely"):
            temp = int(dateDiff.total_seconds())/60
            self.count = temp/self.freq
        elif(self.freqType=="Hourly"):
            if(dateDiff >= timedelta(hours=24)):
                temp = dateDiff.days
                temp*=24
                self.count = temp/self.freq
            else:
                temp = int(dateDiff.total_seconds())/3600
                self.count = temp/self.freq
        elif(self.freqType=="Daily"):
            temp = self.freq
            self.count = dateDiff.days
        elif(self.freqType=="Weekly"):
            temp = self.freq*7
            temp2 = dateDiff.days/temp
            if temp2<1:
                self.count = 0
            else:
                self.count = temp2
        elif(self.freqType=="Monthly"):
            temp = self.freq*30
            temp2 = dateDiff.days/temp
            if temp2<1:
                self.count=0
            else:
                self.count=temp2

text_file = open("Output.txt", "w")
def adjustCount(t):
    present = datetime.datetime.today()
    margin = (datetime.datetime(present.year, present.month, present.day) + datetime.timedelta(days = 29))
    adjDateDiff = margin - t.startDate
    if(t.freqType=="Singular"):
        c = 0
    elif(t.freqType=="Minutely"):
        temp = int(adjDateDiff.total_seconds())/60
        c = temp/t.freq
    elif(t.freqType=="Hourly"):
        if(adjDateDiff >= timedelta(hours=24)):
            temp = adjDateDiff.days
            temp*=24
            c = temp/t.freq
        else:
            temp = int(adjDateDiff.total_seconds())/3600
            c = temp/t.freq
    elif(t.freqType=="Daily"):
        temp = t.freq
        c = adjDateDiff.days
    elif(t.freqType=="Weekly"):
        temp = t.freq*7
        temp2 = adjDateDiff.days/temp
        if temp2<1:
            c = 0
        else:
            c = temp2
    return c
  
def populateRecurring(rT):
    rT.setCount()
    if (rT.freqType=='Singular'):
        tStr = rT.display()
        text_file.write((str(tStr))+"\n")
    else:
        choices = {'Daily': datedelta.DAY, 
                   'Hourly': datetime.timedelta(hours=1),
                   'Minutely': datetime.timedelta(minutes=rT.freq),
                   'Weekly': datetime.timedelta(weeks=1)}
        result = choices.get(rT.freqType, 'default')
        if(rT.endDate <= (datetime.datetime.today() + datetime.timedelta(days = 28))):
            tOStr = rT.display()
            text_file.write((str(tOStr))+"\n")
            if (rT.freqType=='Monthly'):
                nextDueDate = (rT.startDate)
                nextDueDate.month = (rT.startDate.month+1)
            else:
                nextDueDate = (rT.startDate + result)
            while (rT.count > 0):
                taskNew = Task(rT.taskName, rT.startDate, rT.endDate, rT.freqType, rT.freq, rT.count)
                taskNew.startDate = nextDueDate
                if (rT.freqType=='Monthly'):
                    nextDueDate.month += 1
                else:
                    nextDueDate += result
                rT.count -= 1
                taskNew.count = rT.count
                tNStr = taskNew.display()
                #print tNStr
                text_file.write((str(tNStr))+"\n")
        else:
            tOStr = rT.display()
            text_file.write((str(tOStr))+"\n")
            if (rT.freqType=='Monthly'):
                nextDueDate = (rT.startDate)
                nextDueDate.month = (rT.startDate.month+1)
            else:
                nextDueDate = (rT.startDate + result)
            tempCount = adjustCount(rT)
            while (tempCount > 0):
                taskNew = Task(rT.taskName, rT.startDate, rT.endDate, rT.freqType, rT.freq, rT.count)
                taskNew.startDate = nextDueDate
                if (rT.freqType=='Monthly'):
                    nextDueDate.month += 1
                else:
                    nextDueDate += result
                tempCount -= 1
                rT.count -= 1
                taskNew.count = rT.count
                tNStr = taskNew.display()
                #print tNStr
                text_file.write((str(tNStr))+"\n")
   
infile = open("Input.txt", "r") 
for line in infile: 
    name,dt1,dt2,ft,f,c = line.split("/")
    yy1,mm1,dd1,hh1 = dt1.split(",")
    yy2,mm2,dd2,hh2 = dt2.split(",")
    task1 = Task(name, datetime.datetime(int(yy1),int(mm1),int(dd1),int(hh1)), datetime.datetime(int(yy2),int(mm2),int(dd2),int(hh2)),ft,int(f),c)
    populateRecurring(task1)  

infile.close()     
text_file.close()
