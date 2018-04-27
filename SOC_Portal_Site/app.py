from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, TextAreaField, IntegerField, DateTimeField, FloatField, HiddenField, BooleanField, validators, PasswordField
from wtforms.validators import InputRequired
from taskQueueFill import populateAnalystTable
from fillAdminTable import populateAdminTable, populatePastTasks
from writeCompletedTask import handleCompTask, handleExpiredTask
from fillAddNewTask import populateDropdowns
from TaskHandling import taskIntake
from writeNewClient import addClient, addEditClient, deleteClient
from writeNewUser import addUser, addEditUser, deleteUser
from writeEditTask import handleEditTask, deleteTask
from fillAddNewClient import populateCatSkills
from fillViewClients import fillClients
from fillViewUser import fillUsers
from fillEditClient import editCatSkills
from fillEditUser import editUserCatSkills
from fillEditTask import editTaskInfo
from Categories import populateCategories, addEditCategory, catCount, saveNewCategory, deleteCategory
from NewCategory import insertCategoryData
from Skillsets import populateAllSkillsets, populateCategorySkillset
from NewSkillset import insertSkillsetData
from fillLoginData import userList, idPosition
from fillOverview import getMetrics
from fillPackages import populateClientPackages, getPackages, getEditPackage
from datetime import datetime
from crontab import CronTab

app=Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

#my_cron = CronTab(user=True)
#---------------------------------
# UPDATES DATABASE DAILY AT 00:00
#---------------------------------
#job1 = my_cron.new(command='/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/zachauzenne/Desktop/DESKTOP/SOC_Portal_Site/updateDB.py')
#job1.minute.on(0)
#job1.hour.on(0)
#---------------------------------

#---------------------------------
# UPDATES DATABASE TO REMOVE EXPIRED TASKS
#---------------------------------
#job2 = my_cron.new(command='/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/zachauzenne/Desktop/DESKTOP/SOC_Portal_Site/taskExpiration.py')
#job2.minute.every(15)
#---------------------------------

#---------------------------------
# UPDATES DATABASE TO ADJUST USER METRICS
#---------------------------------
#job3 = my_cron.new(command='/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/zachauzenne/Desktop/DESKTOP/SOC_Portal_Site/updateMetrics.py')
#job3.minute.every(14)
#---------------------------------

#my_cron.write()
#my_cron.remove_all()   

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
session = { 'logged_in': False, 'userID': '', 'position': ''  }

#INDEX PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
    session['userID'] = ''
    session['position'] = ''
    session['logged_in'] = False
    form = LoginForm(request.form)
    data = userList()
    users = data[0]
    pw = data[1]
    loginAttempt = 0
    print(loginAttempt)
    if request.method == "POST":
        loginAttempt+=1
        for m in users:
            if form.username.data == m:
                for n in pw:
                    if form.password.data == n:
                        data1 =idPosition(m)
                        uID = data1[0]
                        position = data1[1]
                        session['userID'] = uID
                        session['position'] = position
                        session['logged_in'] = True
                        if position == "Analyst":
                            return redirect(url_for("taskQueue"))
                        elif position == "Manager":
                            return redirect(url_for("mTaskQueue"))
                        elif position == "Admin":
                            return redirect(url_for("adminTaskList"))
        return render_template('index.html', form=form, lga = loginAttempt)
    return render_template('index.html', form=form, lga = loginAttempt)

@app.route('/logout')
def logout():
    session.pop('userID', None)
    session.pop('position', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/badLogin', methods=['GET', 'POST'])
def badLogin():
    if request.method == 'POST':
        return redirect(url_for('/logout'))
    return render_template('badLogin.html')

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
    startDate = StringField("Due Date")
    endDate = StringField("endDate")
    freqType = StringField("Frequency Type")
    frequency = IntegerField("Frequency")
    totalTime = StringField("Total Time")
    status = StringField("Status")
    SLA = StringField("SLA")
    specialNotes = TextAreaField("Special Notes")
    reason = TextAreaField("Reasoning")
    formKey = StringField("Form Key")

#TASK QUEUE - ANALYST VIEW    
@app.route('/taskQueue', methods=['GET', 'POST'])
def taskQueue():
    if (session['position'] == "Analyst") and (session['logged_in'] == True):
        taskList = populateAnalystTable(session['userID'])
        form = taskForm(request.form)
        if request.method == "POST":
            if(form.formKey.data == "complete"):
                print (handleCompTask(session['userID'], form.taskID.data, form.clientName.data, taskList[0][5], taskList[0][6], taskList[0][7], taskList[0][8], taskList[0][9], taskList[0][10], form.totalTime.data, form.status.data, form.SLA.data, form.specialNotes.data, taskList[0][15], taskList[0][16], form.reason.data))
                taskList = populateAnalystTable(session['userID'])
                return redirect(url_for('taskQueue'))
            elif(form.formKey.data == "expired"):
                handleExpiredTask(session['userID'], form.taskID.data, form.clientName.data, taskList[0][5], taskList[0][6], taskList[0][7], taskList[0][8], taskList[0][9], taskList[0][10], form.totalTime.data, form.status.data, form.SLA.data, form.specialNotes.data, taskList[0][15], taskList[0][16], form.reason.data)
                taskList = populateAnalystTable(session['userID'])
                return redirect(url_for('taskQueue'))
        return render_template('taskQueue.html', tasks = taskList, form=form, session=session)
    return redirect(url_for('badLogin'))

#MANAGER TASK QUEUE
@app.route('/mTaskQueue', methods=['GET','POST'])
def mTaskQueue():
    if (session['position'] == "Manager") and (session['logged_in'] == True):
        mtaskList = populateAnalystTable(session['userID'])
        form = taskForm(request.form)
        if request.method == "POST":
            if (form.formKey.data == "complete"):
                print (handleCompTask(session['userID'], form.taskID.data, form.clientName.data, mtaskList[0][5], mtaskList[0][6], mtaskList[0][7], mtaskList[0][8], mtaskList[0][9], mtaskList[0][10], form.totalTime.data, form.status.data, mtaskList[0][13], form.specialNotes.data, mtaskList[0][15], mtaskList[0][16], form.reason.data))
                mtaskList = populateAnalystTable(session['userID'])
                return redirect(url_for('mTaskQueue'))
            elif (form.formKey.data == "edit"):
                return redirect(url_for('editTask', id=form.taskID.data))
        return render_template('mTaskQueue.html', tasks = mtaskList, form=form)
    return redirect(url_for('badLogin'))

#ADMIN TASK LIST - Upcoming
@app.route('/adminTaskList', methods=['GET', 'POST'])
def adminTaskList():
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        aTaskList = populateAdminTable()
        form = taskForm(request.form)
        if request.method == "POST":
            if (form.formKey.data == "edit"):
                return redirect(url_for('editTask', id=form.taskID.data))
        return render_template('adminTaskList.html', tasks = aTaskList, form=form)
    return redirect(url_for('badLogin'))

#ADMIN TASK LIST _ Past Tasks
@app.route('/pastTasks', methods=['GET', 'POST'])
def pastTasks():
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        pTaskList = populatePastTasks()
        form = taskForm(request.form)
        if request.method == "POST":
            pTaskList = populatePastTasks()
            return redirect(url_for('pastTasks'))
        return render_template('pastTasks.html', tasks = pTaskList, form=form)
    return redirect(url_for('badLogin'))

################################
###      USER OVERVIEW       ###
################################


#ANALYST OVERVIEW PAGE
@app.route('/overview', methods=['GET','POST'])
def overview():
    if (session['position'] == "Analyst") and (session['logged_in'] == True):
        m = getMetrics(session['userID'])
        return render_template('analystOverview.html', metrics=m)
    elif (session['position'] == "Manager") and (session['logged_in'] == True):
        m = getMetrics(session['userID'])
        return render_template('managerOverview.html', metrics=m)
    elif (session['position'] == "Admin") and (session['logged_in'] == True):
        m = getMetrics(session['userID'])
        return render_template('adminOverview.html', metrics=m)
    return redirect(url_for('badLogin'))
#MANAGER OVERVIEW PAGE
#@app.route('/mOverview', methods=['GET','POST'])
#def mOverview():
#    return render_template('managerOverview.html')

#ADMIN OVERVIEW PAGE
#@app.route('/adminOverview', methods=['GET','POST'])
#def aOverview():
#    return render_template('adminOverview.html')

################################
###      NEW TASK PAGE       ###
################################

#ADD NEW TASK PAGE - CREATING SINGULAR AND RECURRING TASKS
@app.route('/addNewTask', methods=['GET', 'POST'])
def addNewTask():
    if ((session['position'] != "Analyst") and session['logged_in'] == True):
        data = populateDropdowns()
        clientList = data[0]
        clientCatSkills = data[1]
        form = taskForm(request.form)
        if request.method == "POST":
            if(form.formKey.data == "add"):
                y,m,d,h = form.startDate.data.split(",")
                y2,m2,d2,h2 = form.endDate.data.split(",")
                taskIntake(form.clientName.data, form.taskName.data, form.category.data, datetime(int(y),int(m),int(d),int(h)), datetime(int(y2),int(m2),int(d2),int(h2)), form.freqType.data, form.frequency.data)
                if (session['position'] == "Manager"):
                    return redirect(url_for('mTaskQueue'))
                elif (session['position'] == "Admin"):
                    return redirect(url_for('adminTaskList'))
            elif(form.formKey.data == "back"):
                if (session['position'] == "Manager"):
                    return redirect(url_for('mTaskQueue'))
                elif (session['position'] == "Admin"):
                    return redirect(url_for('adminTaskList'))
        return render_template('addNewTask.html', form = form, clients = clientList, catSkills = clientCatSkills)
    return redirect(url_for('badLogin'))

#EDIT TASK PAGE - EDIT EXISTING TASKS
@app.route('/editTask/<id>', methods=['GET', 'POST'])
def editTask(id):
    if ((session['position'] != "Analyst") and session['logged_in'] == True):
        data = editTaskInfo(id)
        taskInfo = data[0]
        d2 = populateDropdowns()
        clientInfo = d2[0]
        catSkills = d2[1]
        form = taskForm(request.form)
        if request.method == "POST":
            if(form.formKey.data == "edit"):
                print(handleEditTask(id, form.clientName.data, form.taskName.data, form.category.data, datetime(form.startDate.data), datetime(form.endDate.data), form.freqType.data, form.frequency.data))
                if (session['position'] == "Manager"):
                    return redirect(url_for('mTaskQueue'))
                elif (session['position'] == "Admin"):
                    return redirect(url_for('adminTaskList'))
            elif(form.formKey.data == "delete"):
                print(deleteTask(id, form.clientName.data, form.taskName.data, form.category.data, datetime(form.startDate.data), datetime(form.endDate.data), form.freqType.data, form.frequency.data))
                if (session['position'] == "Manager"):
                    return redirect(url_for('mTaskQueue'))
                elif (session['position'] == "Admin"):
                    return redirect(url_for('adminTaskList'))
            elif(form.formKey.data == "back"):
                #CHECK FOR POSITION TO DETERMINE PAGE
                if (session['position'] == "Manager"):
                    return redirect(url_for('mTaskQueue'))
                elif (session['position'] == "Admin"):
                    return redirect(url_for('adminTaskList'))
        return render_template('editTask.html', form = form, tasks = taskInfo, catSkills = catSkills, clients = clientInfo)
    return redirect(url_for('badLogin'))

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
    if ((session['position'] != "Analyst") and session['logged_in'] == True):
        cS = populateCatSkills()
        form = clientForm(request.form)
        if request.method == "POST":
            if(form.formKey.data == "add"):
                addClient(form.clientName.data, form.clientEmail.data, form.clientPhone.data, form.catSkills.data)
                return redirect(url_for('viewClients'))
            elif(form.formKey.data == "back"):
                #CHECK FOR POSITION TO DETERMINE PAGE
                return redirect(url_for('viewClients'))
        return render_template('addNewClient.html', form=form, catSkills = cS)
    return redirect(url_for('badLogin'))

#EDIT CLIENT PAGE - EDIT EXISTING CLIENTS
@app.route('/editClient/<id>', methods=['GET','POST'])
def editClient(id):
    if ((session['position'] != "Analyst") and session['logged_in'] == True):
        data = editCatSkills(id)
        cS = data[0]
        curCS = data[1]
        cInfo = data[2]
        form = clientForm(request.form)
        if (request.method == "POST"):
            if(form.formKey.data == "edit"):
                addEditClient(form.clientID.data, form.clientName.data, form.clientEmail.data, form.clientPhone.data, form.catSkills.data)
                #CHECK FOR POSITION TO DETERMINE PAGE
                return redirect(url_for('viewClients'))
            elif(form.formKey.data == "back"):
                #CHECK FOR POSITION TO DETERMINE PAGE
                return redirect(url_for('viewClients'))
        return render_template('editClient.html', form=form, clientInfo=cInfo, catSkills = cS, clientCatSkills = curCS)
    return redirect(url_for('badLogin'))

#VIEW CLIENTS PAGE - VIEW ALL AVAILABLE CLIENTS
@app.route('/viewClients', methods=['GET', 'POST'])
def viewClients():
    if ((session['position'] != "Analyst") and session['logged_in'] == True):
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
        return render_template('viewClients.html', form=form, clientInfo=cInfo, catSkills=cCS, session=session)
    return redirect(url_for('badLogin'))

#VIEW CLIENTS PAGE - VIEW ALL AVAILABLE CLIENTS
#@app.route('/mViewClients', methods=['GET', 'POST'])
#def mViewClients():
#    form = clientForm(request.form)
#    data = fillClients()
#    cInfo = data[0]
#    cCS = data[1]
#    if (request.method == "POST"):
#        if (form.formKey.data == "edit"):
#            return redirect(url_for('editClient', id=form.clientID.data ))
#        elif(form.formKey.data == "delete"):
#            deleteClient(form.clientID.data)
#            return redirect(url_for('mViewClients'))
#    return render_template('mViewClients.html', form=form, clientInfo=cInfo, catSkills=cCS)

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
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        data = editUserCatSkills(id)
        cS = data[0]
        curCS = data[1]
        uInfo = data[2]
        form = userForm(request.form)
        if (request.method == "POST"):
            if(form.formKey.data == "edit"):
                addEditUser(id, form.userName.data, form.password.data, form.firstName.data, form.lastName.data, form.email.data, form.phoneNumber.data, form.position.data, form.catSkills.data)
                return redirect(url_for('viewUser'))
            elif(form.formKey.data == "back"):
                return redirect(url_for('viewUser'))
        return render_template('editUser.html', form=form, userInfo=uInfo, catSkills = cS, userCatSkills = curCS)
    return redirect(url_for('badLogin'))
    
#ADD NEW USER PAGE - CREATE NEW USER AND ADD THEM TO DB
@app.route('/addNewUser', methods=['GET','POST'])
def addNewuser():
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        form = userForm(request.form)
        uCS = populateCatSkills()
        if request.method == "POST":
            if(form.formKey.data == "add"):
                addUser(form.userName.data, form.password.data, form.firstName.data, form.lastName.data, form.email.data, form.phoneNumber.data, form.position.data, form.catSkills.data)
                return redirect(url_for('viewUser'))
            elif(form.formKey.data == "back"):
                return redirect(url_for('viewUser'))
        return render_template('addNewUser.html', form=form, catSkills = uCS)
    return redirect(url_for('badLogin'))

#VIEW USER PAGE - SEE ALL AVAILABLE USERS
@app.route('/viewUsers', methods=['GET', 'POST'])
def viewUser():
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        form = userForm(request.form)
        data = fillUsers()
        uInfo = data[0]
        uCS = data[1]
        print (uInfo)
        print (uCS)
        if (request.method == "POST"):
            if (form.formKey.data == "edit"):
                return redirect(url_for('editUser', id=form.userID.data ))
            elif (form.formKey.data == "delete"):
                deleteUser(form.userID.data)
                return redirect(url_for('viewUser'))
        return render_template('viewUsers.html', form=form, userInfo=uInfo, catSkills=uCS)
    return redirect(url_for('badLogin'))

#VIEW USER PAGE - SEE ALL AVAILABLE USERS
@app.route('/mViewUsers', methods=['GET', 'POST'])
def mViewUser():
    if (session['position'] == "Manager") and (session['logged_in'] == True):
        form = userForm(request.form)
        data = fillUsers()
        uInfo = data[0]
        uCS = data[1]
    #    if (request.method == "POST"):
    #        if (form.formKey.data == "edit"):
    #            return redirect(url_for('editUser', id=form.userID.data ))
    #        elif (form.formKey.data == "delete"):
    #            deleteUser(form.userID.data)
    #            return redirect(url_for('viewUser'))
        return render_template('mViewUsers.html', form=form, userInfo=uInfo, catSkills=uCS)
    return redirect(url_for('badLogin'))

################################
###  CATEGORY/SKILLSET PAGES ###
################################

class categoryForm(Form):
    catSkills = StringField("CatSkills")
    categoryName = StringField("Category", [validators.length(min=1)])
    formKey = StringField("FormKey")
    
class skillsetForm(Form):
    catSkillID = HiddenField("catSkillID")
    categoryName = BooleanField("Skillsets")
    skillsetName = StringField("Skillset", [validators.length(min=1)])

#VIEW CATEGORIES - SEE ALL AVAILABLE CATEGORIES AND ACCOMPANYING SKILLSETS
@app.route('/viewCategories', methods=['GET', 'POST'])
def viewCategories():
    if (session['position'] == "Admin") and (session['logged_in'] == True):
        eNote = 0
        if(request.args.get('edN') != None):
            eNote = request.args.get('edN')
        print (eNote)
        categories = populateCategories()
        form = categoryForm(request.form)
        if request.method == "POST":
            if(form.formKey.data == "edit"):
                catName = form.categoryName.data
                return redirect(url_for('editCategory', cN = catName))
            elif(form.formKey.data == "delete"):
                deleteCategory(form.categoryName.data)
                return redirect(url_for('viewCategories'))
        return render_template('viewCategories.html', categories=categories, form=form, eNote=eNote)
    return redirect(url_for('badLogin'))

@app.route('/editCategory', methods=['GET', 'POST'])
def editCategory():
    editNote = 0
    cName = request.args.get('cN')
    currentSkillset = populateCategorySkillset(cName)
    allSkillsets = populateAllSkillsets()
    form = categoryForm(request.form)
    if(request.method == "POST"):
       if(form.formKey.data == "edit"):
           print (addEditCategory(form.categoryName.data, form.catSkills.data))
           editNote = 1
           return redirect(url_for('viewCategories', edN = editNote))
       elif(form.formKey.data == "back"):
           return redirect(url_for('viewCategories', edN = editNote))
    return render_template('editCategories.html', curSki=currentSkillset, allSki=allSkillsets, form=form)

@app.route('/newCategory', methods=['GET', 'POST'])
def newCategory():
    editNote = 0
    allSkillsets = populateAllSkillsets()
    count = catCount()
    form = categoryForm(request.form)
    if(request.method == "POST"):
        if(form.formKey.data == "save"):
            editNote = 1
            saveNewCategory(form.categoryName.data, form.catSkills.data)
            return redirect(url_for('viewCategories', edN = editNote))
        elif(form.formKey.data == "back"):
            return redirect(url_for('viewCategories', edN = editNote))
    return render_template('newCategory.html', allSki=allSkillsets, form=form, cCount = count)

class packagesForm(Form):
    packageName = StringField("Package Name")
    packageID = IntegerField("Package ID")
    packageContents = StringField("Package Contents")
    formKey = StringField("Form Key")

@app.route('/viewPackages', methods=['GET','POST'])
def viewPackages():
    pkgs = getPackages()
    form = packagesForm(request.form)
    if(request.method == 'POST'):
        if(form.formKey.data=='add'):
            return redirect(url_for('addNewPackage'))
        elif(form.formKey.data=='edit'):
            return redirect(url_for('editPackages', pID=form.packageID.data))
        elif(form.formKey.data=='delete'):
            return redirect(url_for('viewPackages'))
    return render_template('viewPackages.html', form=form, packages=pkgs)

@app.route('/editPackages', methods=['GET', 'POST'])
def editPackages():
    pkgID = request.args.get('pID')
    data = getEditPackage(pkgID)
    pkgs = data[0]
    cats = data[1]
    form = packagesForm(request.form) 
    if(request.method == 'POST'):
        print(form.formKey.data)
        if(form.formKey.data=='add'):
            return redirect(url_for('viewPackages'))
        elif(form.formKey.data=='back'):
            return redirect(url_for('viewPackages'))
    return render_template('editPackage.html', form=form, packages = pkgs, categories=cats)

#STARTS AND RUNS SITE
if __name__ == '__main__':
    app.run(debug = True)