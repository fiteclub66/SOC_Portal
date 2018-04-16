from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, TextAreaField, IntegerField, DateTimeField, FloatField
from taskQueueFill import populateTable
from writeCompletedTask import handleCompTask
from fillAddNewTask import populateDropdowns
from TaskHandling import taskIntake
from writeNewClient import addClient
from writeNewUser import addUser
from datetime import datetime

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

class taskForm(Form):
    taskID = IntegerField("Task ID")
    clientName = StringField("Client Name")
    taskName = StringField("Task Name")
    category = StringField("Category")
    skillset = StringField("Skillset")
    startDate = DateTimeField("Due Date")
    endDate = DateTimeField("endDate")
    freqType = StringField("Frequency Type")
    frequency = IntegerField("Frequency")
    totalTime = StringField("Total Time")
    status = StringField("Status")
    specialNotes = TextAreaField("Special Notes")
    reason = TextAreaField("Reasoning")
    
@app.route('/taskQueue', methods=['GET', 'POST'])
def taskQueue():
    taskList = populateTable()
    form = taskForm(request.form)
    if request.method == "POST":
        print form.reason.data
        print handleCompTask(form.taskID.data, form.clientName.data, taskList[0][5], taskList[0][6], taskList[0][7], taskList[0][8], taskList[0][9], taskList[0][10], form.totalTime.data, form.status.data, taskList[0][13], form.specialNotes.data, taskList[0][15], taskList[0][16], form.reason.data)
        taskList = populateTable()
        return redirect(url_for('taskQueue'))
    return render_template('TaskQueue.html', tasks = taskList, form=form)

@app.route('/addNewTask', methods=['GET', 'POST'])
def addNewTask():
    data = populateDropdowns()
    clientList = data[0]
    cC = data[1]
    #cS = data[2]
    form = taskForm(request.form)
    if request.method == "POST":
        taskIntake(form.clientName.data, form.taskName.data, form.category.data, datetime(2018,04,15, 2), datetime(2018,04,30, 2), form.freqType.data, form.frequency.data)
        return redirect(url_for('index'))
    return render_template('addNewTask.html', form=form, clients = clientList, catSkills = cC)

class clientForm(Form):
    clientName = StringField("Client Name")
    clientEmail = StringField("Email")
    clientPhone = StringField("Phone Number")

@app.route('/addNewClient', methods=['GET','POST'])
def addNewClient():
    form = clientForm(request.form)
    if request.method == "POST":
        addClient(form.clientName.data, form.clientEmail.data, form.clientPhone.data)
        return redirect(url_for('index'))
    return render_template('addNewClient.html', form=form)

class userForm(Form):
    userName = StringField("UserName")
    password = StringField("Password")
    firstName = StringField("First Name")
    lastName = StringField("Last Name")
    email = StringField("Email")
    phoneNumber = StringField("Phone Number")
    position = StringField("Position")
    
@app.route('/addNewUser', methods=['GET','POST'])
def addNewuser():
    form = userForm(request.form)
    if request.method == "POST":
        addUser(form.userName.data, form.password.data, form.firstName.data, form.lastName.data, form.email.data, form.phoneNumber.data, form.position.data)
        return redirect(url_for('index'))
    return render_template('addNewUser.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)