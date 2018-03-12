import pymysql

connection = pymysql.connect(host = 'localhost', user = 'root', password = 'root')
cur = connection.cursor()
cur.execute ("CREATE DATABASE PastTasks")
cur.execute("USE PastTasks")

cur.execute("""CREATE TABLE Users
(
userID int NOT NULL AUTO_INCREMENT,
firstName varchar(30),
lastName varchar(40),
email varchar(50),
phoneNumber varchar(20),
position varchar(30),
PRIMARY KEY (userID))""")

cur.execute("""CREATE TABLE CategoryRelations
(
catSkillID int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (catSkillID),
category varchar(200),
skillset varchar(200))""")


cur.execute("""CREATE TABLE SkillsetRelations 
(
userID int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (userID),
catSkillID int,
FOREIGN KEY (catSkillID) REFERENCES CategoryRelations(catSkillID))""" )



cur.execute("""CREATE TABLE pastTasks
(
taskID int NOT NULL AUTO_INCREMENT,
clientName varchar(200),
taskName varchar(200),
catSkillID int,
userID int NOT NULL AUTO_INCREMENT,
dueDate datetime,
frequency datetime,
startTime float,
stopTime float,
totalTime float,
status varchar(255),
SLA varchar(255),
specialNotes varchar(255),
PRIMARY KEY (taskID),
KEY(ID),
FOREIGN KEY (catSkillID) REFERENCES CategoryRelations(catSkillID),
FOREIGN KEY (userID) REFERENCES Users(userID)) """)

#Fetch all the rows

rows = cur.fetchall()
for row in rows:
    print(row)
    

connection.close()

#writing past 30 days data to CSV file
def execute(c, command):
    c.execute(command)
    return c.fetchall()

db = pymysql.connect(host = "localhost", user = "root", password = "root",
                              db = "PastTasks")#, charset='utf8')

c = db.cursor()

for table in execute(c, "show tables;"):
    table = table[0]
    cols = []
    for item in execute(c, "show columns from " + table + ";"):
        cols.append(item[0])
    data = execute(c, "select * from " + table + ";")
    with open(table + ".csv", "w", encoding="utf-8") as out:
        out.write("\t".join(cols) + "\n")
        for row in data:
            out.write("\t".join(str(el) for el in row) + "\n")
    print(table + ".csv written")
    
connection.close()

