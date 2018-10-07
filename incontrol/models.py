from mongoengine import Document, EmbeddedDocument, StringField, ListField, ReferenceField, IntField, EmbeddedDocumentField, DateTimeField
from mongoengine import CASCADE, NULLIFY, PULL
import datetime
from .config import *
from .utils import today_isoformat
import re
import io

READ = 1
WRITE = 2
READ_WRITE = 3
regex_date = re.compile(r"\d\d\d\d[/-]\d\d[/-]\d\d")

class WorkGroup( Document ):
	name = StringField(max_length=255, required=True, unique=True)
	created_at = DateTimeField(default=datetime.datetime.now)
	members = ListField(ReferenceField("User", delete_rule=PULL))
	# may add other fields
	def __str__(self):
		return self.name

	@classmethod
	def list_properties(cls):
		print("WorkGroup variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("name", "True", "None"))
		print(PRINT_STRING.format("created_at", "True", "now()"))
		print(PRINT_STRING.format("members", "False", "[]"))
		print('\n')


class User( Document ):
	name = StringField(max_length=255, required=True)
	# groups = ListField(ReferenceField(WorkGroup, delete_rule=PULL))
	created_at = DateTimeField(default=datetime.datetime.now)
	# may add other user info fields

	def __str__(self):
		return self.name

	@classmethod
	def list_properties(cls):
		print("User variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("name", "True", "None"))
		print(PRINT_STRING.format("created_at", "False", "now()"))
		print('\n')


class ProgressLog( Document ):
	title = StringField(max_length=255, default='untitled log')
	author = ReferenceField(User, required=True, delete_rule=NULLIFY)
	# task = ReferenceField('Task', delete_rule=NULLIFY)
	content = StringField()
	created_at = DateTimeField(default=datetime.datetime.now)

	def __str__(self):
		return "{} (by {})".format(self.title, self.author)

	@classmethod
	def list_properties(cls):
		print("ProgressLog variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("title", "False", "untitled log"))
		print(PRINT_STRING.format("author", "True", "None"))
		print(PRINT_STRING.format("content", "False", "None"))
		print(PRINT_STRING.format("created_at", "False", "now()"))
		print('\n')

class Permission( EmbeddedDocument ):
	users = IntField(default=READ_WRITE)
	# groups = IntField(default=READ)
	others = IntField(default=0)

	def __str__(self):
		d = {1: 'View', 2: 'Modify', 3: 'View and Modify'}
		return "Users: {}, Others: {}".format(d[self.users], d[self.others])

class Task( Document ):
	"""
	This is the base class of all task classes,
	including 'idea' class and timeline' class (which
	itself is the base class of 'reminder' and 'project').
	"""
	users = ListField(ReferenceField(User, delete_rule=PULL))
	title = StringField(max_length=255, default='untitled task')
	content = StringField()
	parent_task = ReferenceField("Project", delete_rule=NULLIFY)

	# permission = EmbeddedDocumentField(Permission, default=Permission())

	created_at = DateTimeField(required=True, default=datetime.datetime.now)

	meta = {'allow_inheritance': True}

	def __str__(self):
		return self.title

	@classmethod
	def list_properties(cls):
		print("Task variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("users", "False", "[]"))
		print(PRINT_STRING.format("title", "False", "untitled task"))
		print(PRINT_STRING.format("content", "False", "None"))
		print(PRINT_STRING.format("created_at", "True", "now()"))
		print("\n")
		# print("\tproperty\trequired\tdefault")
		# print("\tusers\tfalse\t[]")
		# print("\ttitle\tfalse\tuntitled task")
		# print("\tcontent\tfalse\tnull")
		# print("\tcreated_at\ttrue\tnow()")



class Idea( Task ):
	"""
	The Idea class models a pre-mature task which is not yet fully
	planed and scheduled (as the name suggests, it's just an idea).
	"""
	status = StringField(choices=(('I', 'Just an Idea'),
								  ('W', 'Working'),
								  ('A', 'Abandoned')), default='I')
	def __str__(self):
		return "{} ({})".format(self.title, self.status)

	def update_status(self, status):
		status_string = status.lower()
		if status in ['I', 'W', 'A']:
			self.status = status
		else:
			raise ValueError("status should be in ['I', 'W', 'A']!")
		self.save()

	# def implement_idea(self, task_cls=Project, **kwargs):
	# 	pass
		# kwargs['users'] = kwargs.get('users', self.users)
		# kwargs['title'] = kwargs.get('title', self.title)
		# kwargs['content'] = kwargs.get('content', self.content)
		# kwargs['parent_task'] = kwargs.get('parent_task', self.parent_task)


	@classmethod
	def list_properties(cls):
		super().list_properties()
		print("Idea variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("status", "False", "'I'"))
		print("\n")


class TimelineTask( Task ):
	"""
	This is the base class of all tasks having a schedule.
	"""
	status = StringField(choices=(('P', 'In Progress'),
								  ('F', 'Finished'),
								  ('B', 'Blocked'),
								  ('A', 'Aborted')), default='P')
	deadline = DateTimeField()
	progress_logs = ListField(ReferenceField(ProgressLog, delete_rule=PULL))

	meta = {'allow_inheritance': True}

	def __str__(self):
		return "{} ({})".format(self.title, self.status)

	def update_status(self, status):
		status_string = status.lower()
		if status == 'P' or 'progress' in status_string:
			self.status = 'P'
		elif status == 'F' or 'finish' in status_string or 'done' in status_string:
			self.status = 'F'
		elif status == 'B' or 'block' in status_string or 'pause' in status_string:
			self.status = 'B'
		elif status == 'A' or 'abort' in status_string or 'cancel' in status_string or 'stop' in status_string:
			self.status = 'A'
		else:
			raise ValueError("status should be in ['P', 'F', 'B', 'A']!")
		self.save()

	def create_log(self, user):
		log1 = ProgressLog(author=user)
		log1.save()
		self.progress_logs.append(log1)
		self.save()
		return log1

	@classmethod
	def list_properties(cls):
		super().list_properties()
		print("TimelineTask variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("deadline", "False", "None"))
		print(PRINT_STRING.format("progress_logs", "False", "[]"))
		print("\n")



class Reminder( TimelineTask ):
	"""
	lightweight timeline task.
	"""
	def __str__(self):
		return "{} before {} ({})".format(self.title, self.deadline.isoformat(), self.status)

	@classmethod
	def list_properties(cls):
		super().list_properties()
		print("Reminder variables:")
		print("-"*60)

class Project( TimelineTask ):
	"""
	the most sophisticated task
	"""
	# sub_tasks = ListField(ReferenceField(Task, delete_rule=CASCADE))

	def __str__(self):
		if self.deadline is not None:
			return "{} before {} ({})".format(self.title, self.deadline.isoformat(), self.status)
		else:
			return "{} ({})".format(self.title, self.status)

	def sprawn_subtask(self, task_cls, users=None):
		if users is None:
			users = self.users
		stask = task_cls(users=users)
		stask.parent_task = self
		stask.save()
		# self.save()
		return stask




	def parse_content(self):
		pass

	def parse_logs(self):
		pass
		# filter out specific logs? or write another `parse_log` function to `ProgressLog` class?

	@classmethod
	def list_properties(cls):
		super().list_properties()
		print("Project variables:")
		print("-"*60)
		print(PRINT_STRING.format("property:", "required:", "default:"))
		print(PRINT_STRING.format("sub_tasks", "False", "[]"))


class DailyTask( Document ):
	user = ReferenceField(User, delete_rule=NULLIFY, required=True)
	date = StringField(primary_key=True, default=today_isoformat)
	diary = StringField()
	tasks = ListField(ReferenceField(Task, delete_rule=PULL))

	def clean(self):
		self.date = self.date.replace('/', '-')

	def add_task(self, task):
		self.tasks.append(task)
		self.save()

	def remove_task(self, task):
		if task in self.tasks:
			self.tasks.remove(task)
			self.save()
			return 1
		return 0

	def generate_diary_str(self, verbose=False):
		s = io.StringIO()
		print("Date: %s" % self.date, file=s)
		print("Author: %s" % self.user.name, file=s)
		print("-"*20, file=s)
		print("Tasks:", file=s)
		for task in self.tasks:
			print("\t{}({})\n".format(task.title, task.status), file=s)
			if verbose:
				print("\tcontent:\n{}\n".format(task.content), file=s)
				# if isinstance(task, TimelineTask):
				# 	for log in task.progress_logs:
				# 		print("\t\tprogress log: {}\n".format(log.title) f)

		return s.getvalue()
	# add generate_diary function

