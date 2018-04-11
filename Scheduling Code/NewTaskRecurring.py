'''
Created on Mar 14, 2018

@author: zachauzenne
'''
import datetime
from datetime import timedelta

taskList = []
class Task(object):
    def __init__(self, taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, startTime, stopTime, totalTime, status, SLA, specialNotes, counter, subTask):
        self.taskID = taskID
        self.clientName = clientName
        self.taskName = taskName
        self.catSkillID = catSkillID
        self.startDate = startDate
        self.endDate = endDate
        self.freqType = freqType
        self.frequency = frequency
        self.startTime = startTime
        self.stopTime = stopTime
        self.totalTime = totalTime
        self.status = status
        self.SLA = SLA
        self.specialNotes = specialNotes
        self.counter = counter
        self.subTask = subTask
        
        
    def display(self):
        t = self.taskID, self.clientName, self.taskName, self.catSkillID, str(self.startDate), str(self.endDate), self.freqType, self.frequency, self.startTime, self.stopTime, self.totalTime, self.status, self.SLA, self.specialNotes, self.counter, self.subTask
        return t
    
    def setCount(self):
        dateDiff = self.endDate - self.startDate
        if(self.freqType=="Singular"):
            self.counter=0
        elif(self.freqType=="Minutely"):
            temp = int(dateDiff.total_seconds())/60
            self.counter = temp/self.frequency
        elif(self.freqType=="Hourly"):
            if(dateDiff >= timedelta(hours=24)):
                temp = dateDiff.days
                temp*=24
                self.counter = temp/self.frequency
            else:
                temp = int(dateDiff.total_seconds())/3600
                self.counter = temp/self.frequency
        elif(self.freqType=="Daily"):
            temp = self.frequency
            self.counter = dateDiff.days
        elif(self.freqType=="Weekly"):
            temp = self.frequency*7
            temp2 = dateDiff.days/temp
            if temp2<1:
                self.counter = 0
            else:
                self.counter = temp2
        elif(self.freqType=="Monthly"):
            temp = self.frequency*30
            temp2 = dateDiff.days/temp
            if temp2<1:
                self.counter=0
            else:
                self.counter=temp2

#text_file = open("Output.txt", "w")
def adjustCount(t):
    present = datetime.datetime.today()
    margin = (datetime.datetime(present.year, present.month, present.day) + datetime.timedelta(days = 29))
    adjDateDiff = margin - t.startDate
    if(t.freqType=="Singular"):
        c = 0
    elif(t.freqType=="Minutely"):
        temp = int(adjDateDiff.total_seconds())/60
        c = temp/t.frequency
    elif(t.freqType=="Hourly"):
        if(adjDateDiff >= timedelta(hours=24)):
            temp = adjDateDiff.days
            temp*=24
            c = temp/t.frequency
        else:
            temp = int(adjDateDiff.total_seconds())/3600
            c = temp/t.frequency
    elif(t.freqType=="Daily"):
        temp = t.frequency
        c = adjDateDiff.days
    elif(t.freqType=="Weekly"):
        temp = t.frequency*7
        temp2 = adjDateDiff.days/temp
        if temp2<1:
            c = 0
        else:
            c = temp2
    elif(t.freqType=="Monthly"):
        temp = t.frequency*30
        temp2 = adjDateDiff.days/temp
        if temp2<1:
            c=0
        else:
            c=temp2
    return c
    
def populateRecurring(rT):
    rT.setCount()
    sT = 1;
    if (rT.freqType=='Singular'):
        tStr = rT.display()
        #taskList.append(rT)
        #print ((str(tStr))+"\n")
    else:
        choices = {'Daily': datetime.timedelta(days=1), 
                   'Hourly': datetime.timedelta(hours=1),
                   'Minutely': datetime.timedelta(minutes=rT.frequency),
                   'Weekly': datetime.timedelta(weeks=1)}
        result = choices.get(rT.freqType, 'default')
        if(rT.endDate <= (datetime.datetime.today() + datetime.timedelta(days = 28))):
            tOStr = rT.display()
            #taskList.append(rT)
            #print((str(tOStr))+"\n")
            if (rT.freqType!='Monthly'):
                nextDueDate = (rT.startDate + result)
            while (rT.counter > 0):
                taskNew = Task(rT.taskID, rT.clientName, rT.taskName, rT.catSkillID, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.startTime, rT.stopTime, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask)
                taskNew.startDate = nextDueDate
                if (rT.freqType=='Monthly'):
                    nextDueDate.month += 1
                else:
                    nextDueDate += result
                rT.counter -= 1
                taskNew.counter = rT.counter
                taskNew.subTask = sT
                sT+=1
                tNStr = taskNew.display()
                taskList.append(taskNew)
                #print((str(tNStr))+"\n")
        else:
            tOStr = rT.display()
            #taskList.append(rT)
            #print((str(tOStr))+"\n")
            if (rT.freqType!='Monthly'):
                nextDueDate = (rT.startDate + result)
            tempcounter = adjustCount(rT)
            while (tempcounter > 0):
                taskNew = Task(rT.taskID, rT.clientName, rT.taskName, rT.catSkillID, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.startTime, rT.stopTime, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask)
                taskNew.startDate = nextDueDate
                if (rT.freqType=='Monthly'):
                    nextDueDate.month += 1
                else:
                    nextDueDate += result
                tempcounter -= 1
                rT.counter -= 1
                taskNew.counter = rT.counter
                taskNew.subTask = sT
                sT+=1
                tNStr = taskNew.display()
                taskList.append(taskNew)
                #print((str(tNStr))+"\n")
                
def main(tID, cN, tN, csID, sD, eD, fT, f, staT, stoT, totT, stat, SLA, spN, c, sT):
    rootTask = Task(tID, cN, tN, csID, sD, eD, fT, f, staT, stoT, totT, stat, SLA, spN, c, sT)
    populateRecurring(rootTask)
    return taskList
 
#infile = open("Input.txt", "r") 
#for line in infile: 
#    p1,p2 = line.split("&")
#    tID,cName,name,csID,sD,eD,fT = p1.split("/")
#    f,startT,stopT,tT,stat,SLA,spN,c,subT = p2.split("/")
#    yy1,mm1,dd1,hh1 = sD.split(",")
#    yy2,mm2,dd2,hh2 = eD.split(",")
#    task1 = Task(int(tID), cName, name, int(csID), datetime.datetime(int(yy1),int(mm1),int(dd1),int(hh1)), datetime.datetime(int(yy2),int(mm2),int(dd2),int(hh2)),fT,int(f), int(startT),int(stopT),int(tT),stat,SLA,spN,int(c),int(subT))
#    populateRecurring(task1)  

#infile.close()     
#text_file.close()
