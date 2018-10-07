from mongoengine import *
from incontrol.models import *
from incontrol.app_environment import *
import datetime
connect('in_control')

def populate_database():
	u1 = User(name="Liu Zheng")
	u1.save()

	idea1 = Idea(title='The first idea gave birth to this InControl program', users=[u1, ])
	idea1.content = """
	The development will have 3 stages. First, we build up the database and write
	some tool functions and scripts for command-line usage.
	Second, we think about writing an API server for this. Third, we wrap up
	everything into mobile apps and webpages.
	"""
	idea1.status = 'W'
	idea1.save()

	r1 = Reminder(title="things to do in this weekend", users=[u1, ])
	r1.content="""
	1. Learn beautiful soup and write a crawler and the `parse_logs` function.
	2. Finish watching the NLP Lecture 2.
	3. Read the spec.
	"""
	r1.deadline = datetime.datetime.strptime('2018-09-23T20:00:00', "%Y-%m-%dT%H:%M:%S")
	r1.save()

	p1 = Project(users=[u1, ])
	p1.title = "InControl task management system"
	p1.content = """
	Write a program managing tasks in a logical way.
	This project has 3 stages:
	1. Build up the data model and develop some tool functions and command-line scripts.
	2. After some usage and polishment, start to build an API.
	3. Consider wrapping it up to a webpage or a mobile app.
	"""
	p1.save()


	
# Project.list_properties()



# populate_database()

u1 = User.objects.first()
app = AppEnvironment(u1)
print(app.current_user)
projects = app.query_tasks(Project)
print("projects:", projects)
current_task = projects[0]
print("current_task:", current_task)

# # # test sprawn_subtask function
# # -------------------------------
# p11 = current_task.sprawn_subtask(Idea)
# p11.title = 'Implement the `parse_logs` and `parse_content` functions'
# p11.content = "Thinks about whether to put these functions and decide whether to use JSON or XML."
# p11.save()


# # # test create_log function, and began to use the functions to create something great
# # -------------------------------------------------------------------------------------
# log1 = current_task.create_log(u1)
# log1.title = "Created 'create_log` function, among others."
# log1.content = "N.A."
# log1.save()


# p12 = current_task.sprawn_subtask(Project)
# p12.title = "Build a mapping between list items and numbers"
# p12.content = """
# For command-line usage, since each query returns a list of
# objects, we should automatically build a mapping between numbers
# and objects.

# Add "Choose task", "switch user", "choose log", etc will help users
# to choose things to work on and switch between one and another.

# This should be added into `AppEnvironment` class. The class should not
# only take 'current_user', but 'current_task', 'current_log', etc.
# 'list_*' methods should show all * objects with an index in front of each
# object, and one can use `switch_*` method to choose the corresponding object. 
# """
# p12.deadline = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
# p12.save()

# p13 = current_task.sprawn_subtask(Project)
# p13.title = "Add 'switch_to_parent_task' method"
# p13.deadline = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
# p13.save()

# # # create sub-tasks and logs using the AppEnvironment object
# # ------------------------------------------------------------

# u1 = User.objects.first()
# app = AppEnvironment(u1, "/Users/zheng/.incontrol")
# projects = app.list_main_tasks(Project)
# print(projects)

# app.switch_task(projects[0])
# print(app.current_task.title)
# tasks = app.list_subtasks(Project)
# print(tasks)
# app.switch_task(tasks[1])
# print(app.current_task.title)
# app.switch_to_parent_task()
# print(app.current_task.title)
# 后面就开发显示层，把get到的信息格式化显示。

# # add log
# log_list = app.list_logs()
# print(log_list)
# log1 = app.create_log()
# log1.title = "method added"
# log1.content = "`switch_to_parent_task` added. Now task switching functionality is almost done."
# log1.save()

# log_list = app.list_logs()
# print(log_list)

# app.current_task.update_status('DONE')
# print(app.current_task.status)
# app.switch_to_parent_task()
# subtask = app.create_subtask(task_cls=Idea, switch_to_it=True, users=None)
# print(app.current_task.title)
# print(app.previous_task.title)
