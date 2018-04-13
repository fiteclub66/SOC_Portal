from flask import Flask, render_template, request, flash, session, redirect, url_for
from wtforms import Form, StringField, TextAreaField, IntegerField, DateTimeField, FloatField
from taskQueueFill import populateTable
from writeCompletedTask import handleCompTask


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

if __name__ == '__main__':
    app.run(debug=True)