import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                            host='10.0.51.21',
                            database='SOC_Portal')
    
def populateCategories():
    
    db = getDB()
    
    cur = db.cursor(buffered=True)
    cur2 = db.cursor(buffered=True)
    categoryList = []
    
    catQuery = ("Select catSkillID, category from CategoryRelations GROUP BY category;")
    cur.execute(catQuery)
    for item in cur:
        skillsetList = []
        skiQuery = ("SELECT * FROM CategoryRelations WHERE category = '"+item[1]+"'")
        cur2.execute(skiQuery)
        for thing in cur2:
            skillsetList.append(thing)
        categoryList.append((item, skillsetList))
        
    cur.close()
    db.close()
    return categoryList

def retrieveSkillsets():
    
    db = getDB()
    
    cur=db.cursor(buffered=True)
    
    skillsetList = []
    catQuery = ("SELECT * FROM CategoryRelations WHERE category = '"+item[1]+"'")
    cur.execute(catQuery)
    for item in cur:
        skillsetList.append(item)
        
    cur.close()
    db.close()
    return skillsetList
