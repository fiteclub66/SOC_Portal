'''
Created on Apr 20, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template


class Task(object):
    def __init__(self, taskID, clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask):
        self.taskID = taskID
        self.clientName = clientName
        self.taskName = taskName
        self.catSkillID = catSkillID
        self.startDate = startDate
        self.endDate = endDate
        self.freqType = freqType
        self.frequency = frequency
        self.totalTime = totalTime
        self.status = status
        self.SLA = SLA
        self.specialNotes = specialNotes
        self.counter = counter
        self.subTask = subTask
        
        
    def display(self):
        t = self.taskID, self.clientName, self.taskName, self.catSkillID, str(self.startDate), str(self.endDate), self.freqType, self.frequency, self.totalTime, self.status, self.SLA, self.specialNotes, self.counter, self.subTask
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


def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')

def populateAdminTable():
    db = getDB()
    
    cur = db.cursor(buffered=True)
    q1 = ("SELECT t2.taskID, t2.clientName, t2.taskName, t1.category, t1.skillset, t2.startDate, t2.endDate, t2.freqType, t2.frequency, t2.totalTime, t2.status, t2.SLA, t2.specialNotes, t2.counter, t2.subTask FROM ((SELECT * FROM CategoryRelations) t1 INNER JOIN (SELECT * FROM UpcomingTasks ORDER BY startDate) t2 ON (t1.catSkillID = t2.catSkillID)) ORDER BY taskID ASC")
    cur.execute(q1)
    tList = []
    for item in cur:
        tList.append(item)
            
    cur.close()
    db.close()
    return tList

def populatePastTasks():
    db = getDB()
    
    cur = db.cursor(buffered=True)
    q1 = ("SELECT k2.taskID, k2.clientName, k2.taskName, k2.category, k2.skillset, k1.userID, k1.username, k2.startDate, k2.endDate, k2.freqType, k2.frequency, k2.totalTime, k2.status, k2.SLA, k2.specialNotes, k2.counter, k2.subTask, k2.reason FROM ((SELECT userID, username FROM Users) k1 INNER JOIN (SELECT t2.taskID, t2.clientName, t2.taskName, t1.category, t1.skillset, t2.startDate, t2.endDate, t2.freqType, t2.frequency, t2.totalTime, t2.status, t2.SLA, t2.userID, t2.specialNotes, t2.counter, t2.subTask, t2.reason FROM ((SELECT * FROM CategoryRelations) t1 INNER JOIN (SELECT * FROM PastTasks ORDER BY startDate DESC ) t2 ON (t1.catSkillID = t2.catSkillID))) k2 ON k1.userID = k2.userID) ORDER BY taskID ASC")
    cur.execute(q1)
    tList = []
    for item in cur:
        tList.append(item)
            
    cur.close()
    db.close()
    return tList