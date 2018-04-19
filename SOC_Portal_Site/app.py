from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, TextAreaField, IntegerField, DateTimeField, FloatField
from taskQueueFill import populateTable
from writeCompletedTask import handleCompTask
from fillAddNewTask import populateDropdowns
from TaskHandling import taskIntake
from writeNewClient import addClient
from writeNewUser import addUser
from datetime import datetime
from NewCategory import insertCategoryData
from NewSkillset import insertSkillsetData
from Skillsets import populateSkillsets
from Categories import populateCategories
from wtforms.validators import length

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
class categoryForm(Form):
    catSkillID = HiddenField("catSkillID")
    skillset = BooleanField("Skillsets")
    categoryName = StringField("Category", [validators.length(min=1)])
    
class skillsetForm(Form):
    catSkillID = HiddenField("catSkillID")
    categoryName = BooleanField("Skillsets")
    skillsetName = StringField("Skillset", [validators.length(min=1)])
    
@app.route('/NewSkillset', methods=['GET','POST'])
def addNewSkillset():
    form = skillsetForm(request.form)
    if request.method == "POST":
        
        insertSkillsetData("""will come from category that is checkboxed""", """whatever category is checkboxed""", form.skillsetName.data)
    return render_template('NewSkillset.html', form=form)

@app.route('/NewCategory', methods=['GET','POST'])
def addNewCategory():
    form = categoryForm(request.form)
    if request.method == "POST":
        """if multiple skillsets checkboxed, will have to increment catskillID per skillset"""
        insertCategoryData("""however i include the category id""", form.categoryName.data, """whatever skillset is checkboxed, or null if no skillsets are checkboxed""")
    return render_template('NewCategory.html', form=form)

@app.route('/Skillsets', methods=['GET', 'POST'])
def skillsetList():
    skillsets = populateSkillsets()
    form = skillsetForm(request.form)
    if request.method == "POST":
        """will need more here"""
        skillsets = populateSkillets()
        return redirect(url_for('Skillsets'))
    return render_template('Skillsets.html', skillsets=skillsets, form=form)

@app.route('/Categories', methods=['GET', 'POST'])
def categoryList():
    categories = populateCategories()
    form = categoryForm(request.form)
    if request.method == "POST":
        """will need more here"""
        categories = populateCategories()
        return redirect(url_for('Categories'))
    return render_template('Categories.html', categories=categories, form=form)

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
