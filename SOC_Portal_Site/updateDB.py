from MinutelyTaskCreation import minutelyUpdate
from HourlyTaskCreation import hourlyUpdate
from DailyTaskCreation import dailyUpdate
from WeeklyTaskCreation import weeklyUpdate
from MonthlyTaskCreation import monthlyUpdate
from datetime import datetime

file = open("/Users/zachauzenne/Desktop/DESKTOP/SOC_Portal_Site/updateLog.txt", "a")
file.write(("---------------------------------------------------------------"+"\n"))
file.write(("Task Updates for "+str(datetime.now())+"\n"))

#MINUTELY TASK UPDATES
#minutelyTime = minutelyUpdate()
#file.write(minutelyTime+"\n")

#HOURLY TASK UPDATES
#hourlyTime = hourlyUpdate()
#file.write(hourlyTime+"\n")

#DAILY TASK UPDATES
#dailyTime = dailyUpdate()
#file.write(dailyTime+"\n")

#WEEKLY TASK UPDATE
#weeklyTime = weeklyUpdate()
#file.write(weeklyTime+"\n")

#MONTHLY TASK UPDATES
#monthlyTime = monthlyUpdate()
#file.write(monthlyTime+"\n")

file.write(("Finished at "+str(datetime.now())+"\n"))
file.write(("---------------------------------------------------------------"+"\n"+"\n"))
file.close()
