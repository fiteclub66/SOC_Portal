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

def addEditCategory(cN, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    catSkills = []
    csSet = cS.split(',')
    for item in csSet:
        if (item!=""):
            id, name = item.split('/')
            catSkills.append((id,name))
     
    oldName = ""

    #GETS OLD NAME FOR CATEGORY
    cur.execute("SELECT category FROM CategoryRelations WHERE catSkillID ='"+catSkills[1][0]+"'")
    for item in cur:
        oldName = item[0]
        
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM CategoryRelations WHERE category = '"+oldName+"'")
    
    for item in catSkills:
        if item != "":
            insertCat = ("INSERT INTO CategoryRelations "
                       "(catSkillID, category, skillset) "
                       "VALUES (%s, %s, %s)")
        
            catData = (item[0], cN, item[1])
            cur.execute(insertCat,catData)
    cur.execute("SET foreign_key_checks = 1")
        
    db.commit()
    cur.close()  
    db.close()
    return ("DONE")  

def catCount():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    num = 0;
    cur.execute("SELECT COUNT(DISTINCT category) FROM CategoryRelations;")
    for item in cur:
        num = (item[0])
    num+=1
    return (num)

def saveNewCategory(cN, cS):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    catSkills = []
    csSet = cS.split(',')
    for item in csSet:
        if (item!=""):
            id, name = item.split('/')
            catSkills.append((id,name))
    
    for item in catSkills:
        if item != "":
            insertCat = ("INSERT INTO CategoryRelations "
                       "(catSkillID, category, skillset) "
                       "VALUES (%s, %s, %s)")
        
            catData = (item[0], cN, item[1])
            cur.execute(insertCat,catData)
            
    
        
    db.commit()
    cur.close()  
    db.close()
    
def deleteCategory(cN):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM CategoryRelations WHERE category = '"+cN+"'")
    cur.execute("SET foreign_key_checks = 1")
        
    db.commit()
    cur.close()  
    db.close()
    
