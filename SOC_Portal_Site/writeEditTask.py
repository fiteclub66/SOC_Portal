import mysql.connector
import NewTaskRecurring
from NewTaskRecurring import Task

def handleEditTask(tID, cN, tN, csID, sD, eD, fT, f):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')

    cur = db.cursor(buffered=True)
    
    oldName = ""
    spN = ""
    
    q1 = ("SELECT taskName, specialNotes FROM UpcomingTasks WHERE taskID = "+str(tID)+"")
    cur.execute(q1)
    for item in cur:
        oldName = item[0]
        spN = item[1]
    
    rT = Task(tID, cN, tN, csID, sD, eD, fT, f, "0", "NEW", "", spN, 0, 0)
        
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM UpcomingTasks WHERE taskName = '"+oldName+"'")
    db.commit()
      
     #INSERT THE FIRST TASK
    insertTask = ("INSERT INTO UpcomingTasks "
                   "(clientName, taskName, catSkillID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    taskData = (rT.clientName, rT.taskName, rT.catSkillID, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask)
    
    cur.execute(insertTask,taskData)
    
    
    #SELECT AND UPDATE NEW TASKS 29 DAYS OUT
    q2 = ("SELECT * FROM UpcomingTasks WHERE taskName = '"+rT.taskName+"'")
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
    cur.execute("SET foreign_key_checks = 1")
    db.commit()          
    cur.close()  
    db.close()
    return "DONE"


def deleteTask(tID, cN, tN, csID, sD, eD, fT, f):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')

    cur = db.cursor(buffered=True)
    
    oldName = ""
    
    q1 = ("SELECT taskName FROM UpcomingTasks WHERE taskID = "+str(tID)+"")
    cur.execute(q1)
    for item in cur:
        oldName = item[0]
    

    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM UpcomingTasks WHERE taskName = '"+oldName+"'")
    cur.execute("SET foreign_key_checks = 1")
    db.commit()          
    cur.close()  
    db.close()
    return "DONE"
    

   

    

   
