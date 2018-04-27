'''
Created on Apr 17, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta
from flask import Flask, render_template

def populateCatSkills():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                              host='10.0.51.21',
                             database='SOC_Portal')


    cur = db.cursor(buffered=True)
    catSkills = []
    query = ("SELECT * FROM CategoryRelations")
    cur.execute(query)
    for item in cur:
        catSkills.append(item)
    
    cur.close()
    db.close()
    return (catSkills)