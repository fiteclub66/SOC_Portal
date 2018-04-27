import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')
    
def insertSkillsetData(cSID, cat, sS):
    db = getDB()
    
    cur = db.cursor(buffered=true)
    insertSkillset = ("INSERT INTO CategoryRelations(catSkillID, category, skillset) Values(%s, %s, %s)")
    
    skillsetData = (cSID, cat, sS)
    
    cur.execute(insertSkillset, skillsetData)
    
    db.commit()
    cur.close()
    db.close()
