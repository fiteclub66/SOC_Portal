import mysql.connector
import csv
import datetime

connection = mysql.connector.connect(host = '10.0.51.21', user = 'root', password = 'MyR00t1423!', database ='SOC_Portal')
cur = connection.cursor()
cur.execute("USE SOC_Portal")

    
## query
query = ("SELECT * FROM PastTasks ")
cur.execute(query)

### write to csv file
csv_writer = csv.writer(open("PastTasks.csv", "w", encoding='utf-8-sig')) # create csv
csv_writer.writerow([i[0] for i in cur.description]) # write headers
csv_writer.writerows(cur) # write records
del csv_writer # close csv file

cur.close()
connection.close()
print ("Query executed.")