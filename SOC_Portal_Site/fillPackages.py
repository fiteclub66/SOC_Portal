import mysql.connector
from flask import Flask, render_template
from Categories import populateCategories

def getDB():
    return mysql.connector.connect(user='root', password='MyR00t1423!',
                            host='10.0.51.21',
                            database='SOC_Portal')
    
def getPackages():
    db = getDB()
    
    cur = db.cursor(buffered=True)
    cur2 = db.cursor(buffered=True)
    
    q1 = ("SELECT DISTINCT packageID, packageName FROM Packages")
    cur.execute(q1)
    
    pkgInfo = []
    
    for item in cur:
        q2 = ("SELECT t1.packageID, t1.packageName, t1.category, t2.catSkillID, t2.skillset FROM (SELECT packageID, packageName, category FROM Packages WHERE packageID = '"+str(item[0])+"') t1 INNER JOIN (SELECT catSkillID, category, skillset FROM CategoryRelations) t2 ON t1.category=t2.category")
        cur2.execute(q2)
        temp = []
        
        for obj in cur2:
            temp.append(obj)
        
        pkgInfo.append((item[1], temp)) 
    
    cur.close()
    cur2.close()
    db.close()
    return(pkgInfo)


def getEditPackage(pID):
    db = getDB()
    
    cur = db.cursor(buffered=True)
    pkgContents = []
    cur.execute("SELECT t1.packageID, t1.packageName, t1.category, t2.catSkillID, t2.skillset FROM (SELECT packageID, packageName, category FROM Packages WHERE packageID = '"+str(pID)+"') t1 INNER JOIN (SELECT catSkillID, category, skillset FROM CategoryRelations) t2 ON t1.category=t2.category")
    for item in cur:
        pkgContents.append(item)
        
    categories = populateCategories()
    cur.close()
    db.close()
    return((pkgContents, categories))

def populateClientPackages():
    
    db = getDB()
    
    cur = db.cursor(buffered=True)
    cur2 = db.cursor(buffered=True)
    cur3 = db.cursor(buffered=True)
    
    q1=("SELECT clientID FROM ClientInformation")
    cur.execute(q1)
    
    clientPackages = []
    
    for client in cur:
        q2 = ("SELECT * FROM ClientPackageRelation WHERE clientID = '"+str(client[0])+"'")
        cur2.execute(q2)
        pkgContents = []
        
        for pkg in cur2:
            q3 = ("SELECT t1.packageID, t1.packageName, t1.category, t2.catSkillID, t2.skillset FROM (SELECT packageID, packageName, category FROM Packages WHERE packageID = '"+str(pkg[2])+"') t1 INNER JOIN (SELECT catSkillID, category, skillset FROM CategoryRelations) t2 ON t1.category=t2.category")
            cur3.execute(q3)
            pInfo = []
            
            for item in cur3:
                pInfo.append(item)
            
            pkgContents.append((pkg[2],pInfo))    
        
        clientPackages.append((client[0],pkgContents))
    
   
        
    cur.close()
    cur2.close()
    cur3.close()
    db.close()
    return(clientPackages)
  