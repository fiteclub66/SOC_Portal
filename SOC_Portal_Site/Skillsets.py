import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')
    
def populateAllSkillsets():
    db = getDB()
    
    cur = db.cursor(buffered=True)
    skillsetList = []
    skillQuery = ("SELECT * FROM CategoryRelations")
    cur.execute(skillQuery)
    for item in cur:
        skillsetList.append(item)
        
    cur.close()
    db.close()
    return skillsetList

def populateCategorySkillset(catName):
    db = getDB()
    
    cur = db.cursor(buffered=True)
    catSkills = []
    query = ("SELECT * FROM CategoryRelations WHERE category = '"+catName+"'")
    cur.execute(query)
    for item in cur:
        catSkills.append(item)
        
    cur.close()
    db.close()
    return catSkills