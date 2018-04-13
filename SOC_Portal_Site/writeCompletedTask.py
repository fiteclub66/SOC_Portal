import mysql.connector
from NewTaskRecurring import Task



def handleCompTask(tID, cN, tN, csID, sD, eD, fT, f, totT, stat, SLA, spN, c, sT, r):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                              database='SOC_Portal')

    cur = db.cursor(buffered=True)
    rea = r
    print totT
    rT = Task(tID, cN, tN, csID, sD, eD, fT, f, totT, stat, SLA, spN, c, sT)
    
    #PUSH COMPLETED TASK TO PAST TASKS DB
    insertTask = ("INSERT INTO PastTasks "
                  "(taskID, clientName, taskName, catSkillID, userID, startDate, endDate, freqType, frequency, totalTime, status, SLA, specialNotes, counter, subTask, reason) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    taskData = (rT.taskID, rT.clientName, rT.taskName, rT.catSkillID, 1, rT.startDate, rT.endDate, rT.freqType, rT.frequency, rT.totalTime, rT.status, rT.SLA, rT.specialNotes, rT.counter, rT.subTask, rea)
    #print (insertTask.format(taskData))
    cur.execute(insertTask,taskData)
    #REMOVE COMPLETED TASK FROM UPCOMING TASK DB
    deleteTask = ("DELETE FROM UpcomingTasks WHERE taskID = "+str(rT.taskID)+"")
    #print deleteTask
    cur.execute(deleteTask)
    db.commit()          
    cur.close()  
    db.close()
    return "DONE"
    

   
