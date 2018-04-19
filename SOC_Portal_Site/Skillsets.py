import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')
    
def populateSkillsets():
    db = getDB()
    
    cur = db.cursor(buffered=True)
    skillsetList = []
    skillQuery = ("Select * from CategoryRelations")
    cur.execute(skillQuery)
    for item in cur:
        skillsetList.append(item)
        
    cur.close()
    db.close()
    return skillsetList
