import mysql.connector
from flask import Flask, render_template

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')
    
def insertCategoryData(cSID, ca, sS):
    db = getDB()
    
    cur = db.cursor(buffered=True)
    insertCategory = ("INSERT INTO CategoryRelations(catSkillID, category, skillset) Values(%s, %s, %s)")
    
    categoryData = (cSID, cat, sS)
    
    cur.execute(insertCategory, categoryData)
    
    db.commit()
    cur.close()
    db.close()
