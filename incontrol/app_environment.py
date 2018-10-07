from .models import *
import datetime
from .utils import create_group
from .config import *

class AppEnvironment:
	current_user = None
	current_task = None
	previous_task = None
	current_log = None
	previous_log = None
	default_working_directory = None
	groups = None
	daily_task = None
	tmr_task = None

	def __init__(self, user, working_directory=""):
		self.current_user = user
		self.default_working_directory = working_directory
		grps = WorkGroup.objects(members=self.current_user)
		self.groups = [grp.name for grp in grps]
		today = datetime.date.today().isoformat()
		daily_task = DailyTask.objects(date=today, user=user).first()
		if daily_task is None:
			daily_task = DailyTask(date=today, user=user)
			daily_task.save()
		self.daily_task = daily_task
		tmr = (datetime.date.today() + datetime.timedelta(1)).isoformat()
		tmr_task = DailyTask.objects(date=tmr, user=user).first()
		if tmr_task is None:
			tmr_task = DailyTask(date=tmr, user=user)
			tmr_task.save()
		self.tmr_task = tmr_task

	
	def create_group(self, group_name, other_users):
		user_list = [self.current_user, ] + other_users
		return create_group(user_list, user_name)


	def query_tasks(self, task_cls=Task, **kwargs):
		"""
		Generic task query function. No restriction to main task or so.
		"""
		kwargs['users'] = self.current_user
		return task_cls.objects(**kwargs)

	def list_main_tasks(self, task_cls=Task, **kwargs):
		kwargs = {'parent_task__exists': False}
		return self.query_tasks(task_cls, **kwargs)

	def switch_task(self, task):
		self.previous_task = self.current_task
		self.current_task = task
		return self.current_task

	def rewind_task(self):
		"For now, we can only rewind one step."
		if self.previous_task is not None:
			self.current_task = self.previous_task
			self.previous_task = None

	def list_subtasks(self, task_cls=None, **kwargs):
		if not isinstance(self.current_task, Project):
			raise ValueError('The current task is not a project!')
		if task_cls is None:
			return Task.objects.filter(parent_task=self.current_task, **kwargs)
		return task_cls.objects.filter(parent_task=self.current_task, **kwargs)

	def switch_to_parent_task(self):
		current_task = self.current_task
		if current_task.parent_task is None:
			raise ValueError('The current task has no parent!')
		self.previous_task = self.current_task
		self.current_task = self.current_task.parent_task
		return self.current_task

	def create_log(self):
		current_task = self.current_task
		if not isinstance(current_task, TimelineTask):
			raise ValueError("The current task does not accomodate progress logs!")
		log1 = current_task.create_log(self.current_user)
		return log1

	def list_logs(self):
		if not isinstance(self.current_task, TimelineTask):
			raise ValueError("The current task does not accomodate progress logs!")
		return self.current_task.progress_logs

	def create_main_task(self, task_cls=Project, switch_to_it=True, users=None, **kwargs):
		if users is None:
			users = [self.current_user]
		new_task = task_cls(users=users, **kwargs)
		

	def create_subtask(self, task_cls=Project, switch_to_it=True, users=None):
		if not isinstance(self.current_task, Project):
			raise ValueError("Only Project instances can have subtasks!")
		subtask = self.current_task.sprawn_subtask(task_cls, users)
		if switch_to_it:
			self.switch_task(subtask)
		return subtask

	def list_today_tasks(self, include_finished=False):
		if include_finished:
			return self.daily_task.tasks
		else:
			return [task for task in self.daily_task.tasks if task.status not in ['A', 'B', 'F']]

	def list_tmr_tasks(self):
		return self.tmr_task.tasks

	def do_it_today(self, task=None):
		if task is None:
			task = self.current_task

		self.daily_task.add_task(task)

	def new_task_today(self, task_cls=Project, switch_to_it=True, users=None):
		if users is None:
			users = [self.current_user, ]
		new_task = task_cls(users=users, title='daily task: %s' % self.daily_task.date)
		self.do_it_today(new_task)

		if switch_to_it:
			self.switch_task(new_task)
		return new_task

	def push_to_tmr(self, task=None):
		if task is None:
			task = self.current_task
		r = self.daily_task.remove_task(task)
		if r == 0:
			raise ValueError("task not in today's task list!")
		self.tmr_task.add_task(task)

