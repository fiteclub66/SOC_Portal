import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                            host='10.0.51.21',
                            database='SOC_Portal')
    
def populateCategories():
    
    db = getDb()
    
    cur = db.cursor(buffered=True)
    categoryList = []
    catQuery = ("Select * from CategoryRelations")
    cur.execute(catQuery)
    for item in cur:
        categoryList.append(item)
        
    cur.close()
    db.close()
    return categoryList

def retrieveSkillsets():
    
    db = getDB()
    
    cur=db.cursor(buffered=True)
    
    skillsetList = []
    catQuery = ("Select skillset from CategoryRelations WHERE catSkillID=")
    cur.execute(catQuery)
    for item in cur:
        skillsetList.append(item)
        
    cur.close()
    db.close()
    return skillsetList
