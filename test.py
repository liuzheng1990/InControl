from mongoengine import *
from incontrol.models import *
from incontrol.app_environment import *
import datetime
connect('in_control')

# Project.list_properties()
u1 = User.objects(name="Liu Zheng").first()
# print(u1 is None)

app = AppEnvironment(u1, "/Users/zheng/.incontrol")
# projects = app.list_main_tasks(Project)
# print(projects)
# app.switch_task(projects[0])
# subtasks = app.list_subtasks()
# print("TODO today:", app.list_today_tasks())
# print("subtasks:", subtasks)
# app.do_it_today(subtasks[0])
# print("Task added to today!")
# print("TODO today:", app.list_today_tasks())
# tasks_today = app.list_today_tasks()
# print(tasks_today)
# # app.switch_task(tasks_today[0])
# # app.current_task.update_status('W')
# # app.push_to_tmr()
# print(app.list_today_tasks())
# print(app.list_tmr_tasks())
# print()
# print(app.tmr_task.generate_diary_str())

main_tasks = app.list_main_tasks(TimelineTask)
app.switch_task(main_tasks[0])
p_imp = app.list_subtasks(status="P")[0]
print(p_imp.content)




# app.switch_task(projects[0])
# print(app.current_task.title)
# print("Sub tasks:")
# tasks = app.list_subtasks(Project)
# print(tasks)

# app.switch_task(tasks[1])
# print(app.list_logs())
# tasks = app.list_subtasks(Task)
# print(tasks)
# app.switch_task(tasks[1])
# app.current_task.update_status("DONE")
# print(app.current_task.status)

# subtask = app.create_subtask(Project, switch_to_it=True, users=None)
# subtask.title = "add working directory"
# subtask.content = """The app object should take a member called `default_working_directory`,
# indicating where the attached files should be stored. A file link will look like
# <file path='photos/1.jpg'>group photo</file>.
# """
# subtask.save()
# app.current_task.update_status("F")
# print(app.current_task)