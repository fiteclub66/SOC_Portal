from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, TextAreaField, IntegerField, DateTimeField, FloatField, HiddenField, BooleanField, validators
from taskQueueFill import populateAnalystTable
from fillAdminTable import populateAdminTable, populatePastTasks
from writeCompletedTask import handleCompTask
from fillAddNewTask import populateDropdowns
from TaskHandling import taskIntake
from writeNewClient import addClient, addEditClient, deleteClient
from writeNewUser import addUser, addEditUser, deleteUser
from fillAddNewClient import populateCatSkills
from fillViewClients import fillClients
from fillViewUser import fillUsers
from fillEditClient import editCatSkills
from fillEditUser import editUserCatSkills
from Categories import populateCategories
from NewCategory import insertCategoryData
from Skillsets import populateSkillsets
from NewSkillset import insertSkillsetData
from datetime import datetime

app=Flask(__name__)

#INDEX PAGE
@app.route('/')
def index():
    return render_template('index.html')

################################
###   TASK QUEUES / LISTS    ###
################################

#TASK FORM
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
    SLA = StringField("SLA")
    specialNotes = TextAreaField("Special Notes")
    reason = TextAreaField("Reasoning")

#TASK QUEUE - ANALYST VIEW    
@app.route('/taskQueue', methods=['GET', 'POST'])
def taskQueue():
    taskList = populateAnalystTable()
    form = taskForm(request.form)
    if request.method == "POST":
        #print form.reason.data
        print (handleCompTask(form.taskID.data, form.clientName.data, taskList[0][5], taskList[0][6], taskList[0][7], taskList[0][8], taskList[0][9], taskList[0][10], form.totalTime.data, form.status.data, taskList[0][13], form.specialNotes.data, taskList[0][15], taskList[0][16], form.reason.data))
        taskList = populateAnalystTable()
        return redirect(url_for('taskQueue'))
    return render_template('taskQueue.html', tasks = taskList, form=form)

#MANAGER TASK QUEUE
@app.route('/mTaskQueue', methods=['GET','POST'])
def mTaskQueue():
    mtaskList = populateAnalystTable()
    form = taskForm(request.form)
    if request.method == "POST":
        #print form.reason.data
        #print handleCompTask(form.taskID.data, form.clientName.data, taskList[0][5], taskList[0][6], taskList[0][7], taskList[0][8], taskList[0][9], taskList[0][10], form.totalTime.data, form.status.data, taskList[0][13], form.specialNotes.data, taskList[0][15], taskList[0][16], form.reason.data)
        mtaskList = populateAnalystTable()
        return redirect(url_for('mTaskQueue'))
    return render_template('mTaskQueue.html', tasks = mtaskList, form=form)

#ADMIN TASK LIST - Upcoming
@app.route('/adminTaskList', methods=['GET', 'POST'])
def adminTaskList():
    aTaskList = populateAdminTable()
    form = taskForm(request.form)
    if request.method == "POST":
        aTaskList = populateAdminTable()
        return redirect(url_for('adminTaskList'))
    return render_template('adminTaskList.html', tasks = aTaskList, form=form)

#ADMIN TASK LIST _ Past Tasks
@app.route('/pastTasks', methods=['GET', 'POST'])
def pastTasks():
    pTaskList = populatePastTasks()
    form = taskForm(request.form)
    if request.method == "POST":
        pTaskList = populatePastTasks()
        return redirect(url_for('pastTasks'))
    return render_template('pastTasks.html', tasks = pTaskList, form=form)

################################
###      USER OVERVIEW       ###
################################

#ANALYST OVERVIEW PAGE
@app.route('/overview', methods=['GET','POST'])
def overview():
    return render_template('analystOverview.html')

#MANAGER OVERVIEW PAGE
@app.route('/mOverview', methods=['GET','POST'])
def mOverview():
    return render_template('managerOverview.html')

#ADMIN OVERVIEW PAGE
@app.route('/adminOverview', methods=['GET','POST'])
def aOverview():
    return render_template('adminOverview.html')

################################
###      NEW TASK PAGE       ###
################################

#ADD NEW TASK PAGE - CREATING SINGULAR AND RECURRING TASKS
@app.route('/addNewTask', methods=['GET', 'POST'])
def addNewTask():
    data = populateDropdowns()
    clientList = data[0]
    clientCatSkills = data[1]
    form = taskForm(request.form)
    if request.method == "POST":
        taskIntake(form.clientName.data, form.taskName.data, form.category.data, datetime(2018,4,20, 2), datetime(2018,5,31, 2), form.freqType.data, form.frequency.data)
        return redirect(url_for('mTaskQueue'))
    return render_template('addNewTask.html', form = form, clients = clientList, catSkills = clientCatSkills)

#CLIENT FORM
class clientForm(Form):
    clientID = IntegerField("Client ID")
    clientName = StringField("Client Name")
    clientEmail = StringField("Email")
    clientPhone = StringField("Phone Number")
    catSkills = StringField("Category/Skillsets")
    formKey = StringField("Form Key")
    
################################
###      CLIENT PAGES        ###
################################

#ADD NEW CLIENT PAGE - CREATE NEW CLIENTS AND ADD TO DB
@app.route('/addNewClient', methods=['GET','POST'])
def addNewClient():
    cS = populateCatSkills()
    form = clientForm(request.form)
    if request.method == "POST":
        addClient(form.clientName.data, form.clientEmail.data, form.clientPhone.data, form.catSkills.data)
        return redirect(url_for('viewClients'))
    return render_template('addNewClient.html', form=form, catSkills = cS)

#EDIT CLIENT PAGE - EDIT EXISTING CLIENTS
@app.route('/editClient/<id>', methods=['GET','POST'])
def editClient(id):
    data = editCatSkills(id)
    cS = data[0]
    curCS = data[1]
    cInfo = data[2]
    form = clientForm(request.form)
    if (request.method == "POST"):
        addEditClient(form.clientID.data, form.clientName.data, form.clientEmail.data, form.clientPhone.data, form.catSkills.data)
        return redirect(url_for('viewClients'))
    return render_template('editClient.html', form=form, clientInfo=cInfo, catSkills = cS, clientCatSkills = curCS)

#VIEW CLIENTS PAGE - VIEW ALL AVAILABLE CLIENTS
@app.route('/viewClients', methods=['GET', 'POST'])
def viewClients():
    form = clientForm(request.form)
    data = fillClients()
    cInfo = data[0]
    cCS = data[1]
    if (request.method == "POST"):
        if (form.formKey.data == "edit"):
            return redirect(url_for('editClient', id=form.clientID.data ))
        elif(form.formKey.data == "delete"):
            deleteClient(form.clientID.data)
            return redirect(url_for('viewClients'))
    return render_template('viewClients.html', form=form, clientInfo=cInfo, catSkills=cCS)

#VIEW CLIENTS PAGE - VIEW ALL AVAILABLE CLIENTS
@app.route('/mViewClients', methods=['GET', 'POST'])
def mViewClients():
    form = clientForm(request.form)
    data = fillClients()
    cInfo = data[0]
    cCS = data[1]
    if (request.method == "POST"):
        if (form.formKey.data == "edit"):
            return redirect(url_for('editClient', id=form.clientID.data ))
        elif(form.formKey.data == "delete"):
            deleteClient(form.clientID.data)
            return redirect(url_for('mViewClients'))
    return render_template('mViewClients.html', form=form, clientInfo=cInfo, catSkills=cCS)

################################
###         USE PAGES        ###
################################

#USER FORM
class userForm(Form):
    userName = StringField("UserName")
    password = StringField("Password")
    firstName = StringField("First Name")
    lastName = StringField("Last Name")
    email = StringField("Email")
    phoneNumber = StringField("Phone Number")
    position = StringField("Position")
    catSkills = StringField("Category/Skillsets")
    userID = IntegerField("UserID")
    formKey = StringField("Form Key")
    
#EDIT USER PAGE - EDIT EXISTING USER INFORMATION   
@app.route('/editUser/<id>', methods=['GET','POST'])
def editUser(id):
    data = editUserCatSkills(id)
    cS = data[0]
    curCS = data[1]
    uInfo = data[2]
    form = userForm(request.form)
    if (request.method == "POST"):
        addEditUser(id, form.userName.data, form.password.data, form.firstName.data, form.lastName.data, form.email.data, form.phoneNumber.data, form.position.data, form.catSkills.data)
        return redirect(url_for('viewUser'))
    return render_template('editUser.html', form=form, userInfo=uInfo, catSkills = cS, userCatSkills = curCS)    
    
#ADD NEW USER PAGE - CREATE NEW USER AND ADD THEM TO DB
@app.route('/addNewUser', methods=['GET','POST'])
def addNewuser():
    form = userForm(request.form)
    uCS = populateCatSkills()
    if request.method == "POST":
        addUser(form.userName.data, form.password.data, form.firstName.data, form.lastName.data, form.email.data, form.phoneNumber.data, form.position.data, form.catSkills.data)
        return redirect(url_for('index'))
    return render_template('addNewUser.html', form=form, catSkills = uCS)

#VIEW USER PAGE - SEE ALL AVAILABLE USERS
@app.route('/viewUsers', methods=['GET', 'POST'])
def viewUser():
    form = userForm(request.form)
    data = fillUsers()
    uInfo = data[0]
    uCS = data[1]
    if (request.method == "POST"):
        if (form.formKey.data == "edit"):
            return redirect(url_for('editUser', id=form.userID.data ))
        elif (form.formKey.data == "delete"):
            deleteUser(form.userID.data)
            return redirect(url_for('viewUser'))
    return render_template('viewUsers.html', form=form, userInfo=uInfo, catSkills=uCS)

#VIEW USER PAGE - SEE ALL AVAILABLE USERS
@app.route('/mViewUsers', methods=['GET', 'POST'])
def mViewUser():
    form = userForm(request.form)
    data = fillUsers()
    uInfo = data[0]
    uCS = data[1]
    if (request.method == "POST"):
        if (form.formKey.data == "edit"):
            return redirect(url_for('editUser', id=form.userID.data ))
        elif (form.formKey.data == "delete"):
            deleteUser(form.userID.data)
            return redirect(url_for('viewUser'))
    return render_template('mViewUsers.html', form=form, userInfo=uInfo, catSkills=uCS)

################################
###  CATEGORY/SKILLSET PAGES ###
################################

class categoryForm(Form):
    catSkillID = HiddenField("catSkillID")
    skillset = BooleanField("Skillsets")
    categoryName = StringField("Category", [validators.length(min=1)])
    
class skillsetForm(Form):
    catSkillID = HiddenField("catSkillID")
    categoryName = BooleanField("Skillsets")
    skillsetName = StringField("Skillset", [validators.length(min=1)])

#NEW SKILLSET - CREATE NEW SKILLSETS    
@app.route('/newSkillset', methods=['GET','POST'])
def addNewSkillset():
    form = skillsetForm(request.form)
    if request.method == "POST":
        
        insertSkillsetData("""will come from category that is checkboxed""", """whatever category is checkboxed""", form.skillsetName.data)
    return render_template('NewSkillset.html', form=form)

#NEW CATEGORY - CREATE NEW CATEGORIES
@app.route('/newCategory', methods=['GET','POST'])
def addNewCategory():
    form = categoryForm(request.form)
    if request.method == "POST":
        """if multiple skillsets checkboxed, will have to increment catskillID per skillset"""
        insertCategoryData("""however i include the category id""", form.categoryName.data, """whatever skillset is checkboxed, or null if no skillsets are checkboxed""")
    return render_template('NewCategory.html', form=form)

#VIEW SKILLSETS - SEE ALL AVALIABLE SKILLSETS
@app.route('/viewSkillsets', methods=['GET', 'POST'])
def skillsetList():
    skillsets = populateSkillsets()
    form = skillsetForm(request.form)
    if request.method == "POST":
        """will need more here"""
        skillsets = populateSkillets()
        return redirect(url_for('Skillsets'))
    return render_template('Skillsets.html', skillsets=skillsets, form=form)

#VIEW CATEGORIES - SEE ALL AVAILABLE CATEGORIES AND ACCOMPANYING SKILLSETS
@app.route('/viewCategories', methods=['GET', 'POST'])
def categoryList():
    categories = populateCategories()
    form = categoryForm(request.form)
    if request.method == "POST":
        """will need more here"""
        categories = populateCategories()
        return redirect(url_for('Categories'))
    return render_template('viewCategories.html', categories=categories, form=form)

#STARTS AND RUNS SITE
if __name__ == '__main__':
    app.run(debug=True)