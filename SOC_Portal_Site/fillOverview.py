'''
Created on Apr 24, 2018

@author: zachauzenne
'''
import mysql.connector
import datetime
from datetime import timedelta, time
from flask import Flask, render_template
import pandas as pd
from pandas import Series,DataFrame
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.models import  DatetimeAxis, Plot
from bokeh.models import PrintfTickFormatter
from bokeh.embed import autoload_static
from bokeh.resources import CDN
import math

def getMetrics(uID):
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    query = ("SELECT * FROM Metrics WHERE userID ='"+str(uID)+"'")
    cur.execute(query)

    metrics=[]

    for item in cur:
       metrics.append(item)
     
    return(metrics)  

def graph():
    db = mysql.connector.connect(user='root', password='MyR00t1423!',
                                  host='10.0.51.21',
                                  database='SOC_Portal')
    
    
    cur = db.cursor(buffered=True)
    
    cur.execute('SELECT startDate, totalTime FROM PastTasks WHERE status="Complete" ORDER BY startDate ASC')
    dates = []
    times = []
    for item in cur:
       d = item[0]
       h,m,s = item[1].split(":")
       t = datetime.time(0,int(h),int(m))
       dates.append(d)
       times.append(t)

    rows = cur.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.rename(columns={0: 'endDate', 1: 'totalTime'}, inplace = True);
    
    # prepare some data
    x = dates#df['endDate']
    y = times#df['totalTime']
    
    # create a new plot with a title and axis labels
    p = figure(title="User Completion Time", x_axis_type='datetime', x_axis_label = 'Date(M/D)', y_axis_type='datetime', y_axis_label='Average Completion Time' )
    
    
    
    # add a line renderer with legend and line thickness
    p.line(x, y, color ='#FDC14A', line_width=3)
    
    # must be applied to the 1st element, not the axis itself 
    #p.yaxis.formatter = DatetimeTickFormatter(
     #                                          hourmin = ['%H:%M'],
      #                                         hours = ['%H:%M'])
    
    # show the results
    output_file("Users.html")
    #show(p)
    js, tag = autoload_static(p, CDN, "/Users/zachauzenne/Desktop/DESKTOP/SOC_Portal_Site/templates/analystOverview.html")
graph()