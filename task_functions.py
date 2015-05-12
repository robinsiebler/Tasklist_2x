# ------------------------------------------
# Name:     task_functions
# Purpose:  Functions creating/managing tasks/displaying.
#
# Author:   Robin Siebler
# Created:  5/6/15
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '5/6/15'

import arrow
import platform
import util

from tasklist import Task, TaskList
from collections import OrderedDict

from colorama import init, Fore, Back, Style

if platform.system() == 'Windows':
	init()


class Functions:
	def __init__(self):
		"""Initialize the task list."""

		self.tasklist = TaskList()
		self.legend = '\nLegend: Not Due  ' + Fore.CYAN + Style.BRIGHT + 'Upcoming  ' + Fore.BLUE + \
		              Style.BRIGHT + 'Due  ' + Fore.RED + Style.BRIGHT + 'Overdue  ' + Fore.WHITE + Style.DIM + \
		              'Completed' + Fore.RESET + Style.NORMAL

	def show_tasks(self, tasks=None, date_format=None):
		"""Display the tasks (in ID order)

		:param tasks: tasks object
		"""

		if not tasks:
			tasks = self.tasklist.tasks

		if len(tasks) > 0:

			template = '{0:^3} {1:^3} {2:20} {3:20} {4:20} {5:20}'
			print template.format('\nID', ' Pri', 'Due', 'Created', 'Description', 'Tags')
			print template.format('---', '---', '--------------------', '--------------------', '--------------------',
			                      '--------------------')
			for task in tasks:
				if task.priority == 'L':
					priority = Fore.YELLOW + Style.BRIGHT + task.priority.center(3) + Fore.RESET + Style.NORMAL
				elif task.priority == 'M':
					priority = Fore.BLUE + Style.BRIGHT + task.priority.center(3) + Fore.RESET + Style.NORMAL
				elif task.priority == 'H':
					priority = Fore.RED + Style.BRIGHT + task.priority.center(3) + Fore.RESET + Style.NORMAL
				else:
					priority = ''

				if task.due_date is None:
					due_date = ''
				else:
					if date_format:
						due_date = task.due_date.rsplit(' ', 1)[0].ljust(20)
					else:
						due_date = (arrow.get(task.due_date, task.due_date_format).humanize()).ljust(20)

					if not task.completed:
						today = arrow.now()
						diff = arrow.get(task.due_date, task.due_date_format) - today
						if diff.days >= 1 and diff.seconds > 0:
							due_date = Fore.CYAN + Style.BRIGHT + due_date + Fore.RESET + Style.NORMAL
						elif diff.days >= 0:
							due_date = Fore.BLUE + Style.BRIGHT + due_date + Fore.RESET + Style.NORMAL
						elif diff.days <= 0:
							due_date = Fore.RED + Style.BRIGHT +  due_date + Fore.RESET + Style.NORMAL

				if date_format:
					age = (str(task.creation_date).split()[0]).ljust(20)  # drop the time zone
				else:
					age = (arrow.get(task.creation_date, 'MM/DD/YYYY h:mm:ss A ZZ').humanize()).ljust(20)

				if task.note:
					desc = task.task + ' *'
				else:
					desc = task.task

				if task.completed:
					if task.priority:
						priority = task.priority
					else:
						priority = ''
					task_id = Fore.WHITE + Style.DIM + str(task.id).center(3)
					tags = str(task.tags) + Fore.RESET + Style.NORMAL
					print template.format(task_id, priority, due_date, age, desc, tags)
				else:
					print template.format(task.id, priority, due_date, age, desc, task.tags)

			print self.legend
		else:
			print('\nThere are no tasks to display!\n')

	def show_tasks_by_priority(self, tasks=None, date_format=None):
		"""Display the tasks (in Priority order)

		:param tasks: tasks object
		"""

		low_dict = OrderedDict()
		med_dict = OrderedDict()
		high_dict = OrderedDict()
		no_dict = OrderedDict()
		completed_dict = OrderedDict()

		if not tasks:
			tasks = self.tasklist.tasks

		if len(tasks) > 0:
			for task in tasks:

				if task.due_date is None:
					due_date = ''
				else:
					if date_format:
						due_date = task.due_date.rsplit(' ', 1)[0].ljust(20)
					else:
						due_date = (arrow.get(task.due_date, task.due_date_format).humanize()).ljust(20)

					if not task.completed:
						today = arrow.now()
						diff = arrow.get(task.due_date, task.due_date_format) - today
						if diff.days >= 1 and diff.seconds > 0:
							due_date = Fore.CYAN + Style.BRIGHT + due_date + Fore.RESET + Style.NORMAL
						elif diff.days >= 0:
							due_date = Fore.BLUE + Style.BRIGHT + due_date + Fore.RESET + Style.NORMAL
						elif diff.days <= 0:
							due_date = Fore.RED + Style.BRIGHT +  due_date + Fore.RESET + Style.NORMAL

				if date_format:
					age = (str(task.creation_date).split()[0]).ljust(20)
				else:
					age = (arrow.get(task.creation_date, 'MM/DD/YYYY h:mm:ss A ZZ').humanize()).ljust(20)

				if task.note:
					desc = task.task + ' *'
				else:
					desc = task.task

				if task.completed:
					completed_dict[task.id] = task.priority, due_date, age, desc, task.tags
				elif task.priority == 'L':
					priority = Fore.YELLOW + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
					low_dict[task.id] = [priority, due_date, age, desc, task.tags]
				elif task.priority == 'M':
					priority = Fore.BLUE + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
					med_dict[task.id] = [priority, due_date, age, desc, task.tags]
				elif task.priority == 'H':
					priority = Fore.RED + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
					high_dict[task.id] = [priority, due_date, age, desc, task.tags]
				else:
					priority = ''
					no_dict[task.id] = [priority, due_date, age, desc, task.tags]
		else:
			print('\nThere are no tasks to display!\n')
			return

		template = '{0:^3} {1:^3} {2:20} {3:20} {4:20} {5:20}'
		print template.format('\nPri', 'ID', 'Due', 'Created', 'Description', 'Tags')
		print template.format('---', '---', '--------------------', '--------------------', '--------------------',
		                      '--------------------')

		if len(high_dict) > 0:
			for key in high_dict:
				print template.format(high_dict[key][0], key, high_dict[key][1], high_dict[key][2], 
				                      high_dict[key][3], high_dict[key][4])
		if len(med_dict) > 0:
			for key in med_dict:
				print template.format(med_dict[key][0], key, med_dict[key][1], med_dict[key][2], 
				                      med_dict[key][3], med_dict[key][4])
		if len(low_dict) > 0:
			for key in low_dict:
				print template.format(low_dict[key][0], key, low_dict[key][1], low_dict[key][2], 
				                      low_dict[key][3], low_dict[key][4])
		if len(no_dict) > 0:
			for key in no_dict:
				print template.format(no_dict[key][0], key, no_dict[key][1], no_dict[key][2], 
				                      no_dict[key][3], no_dict[key][4])
		
		completed_template = Fore.WHITE + Style.DIM + '{0:^3} {1:^3} {2:20} {3:20} {4:20} {5:20}' + Fore.RESET + Style.NORMAL
		if len(completed_dict) > 0:
			for key in completed_dict:
				if completed_dict[key][0]:
					priority = completed_dict[key][0]
				else:
					priority = ''
				print completed_template.format(priority, key, completed_dict[key][1],
				                                completed_dict[key][2], completed_dict[key][3], completed_dict[key][4])
		print self.legend

	def show_task(self, task_id):
		"""Display the specified task, including its notes, if any.

		:param str task_id: the task_id of the task.
		"""

		task_id = self._validate_task_id(task_id)
		if task_id:
			task = self.tasklist.find_task(task_id)
			if task:
				if task.priority == 'L':
					priority = Fore.YELLOW + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				elif task.priority == 'M':
					priority = Fore.BLUE + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				elif task.priority == 'H':
					priority = Fore.RED + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				else:
					priority = ''
				template = '{0:^3} {1:^3} {2:20} {3:40}'
				print template.format('\nID', ' Pri', 'Description', 'Note')
				print template.format('---', '---', '--------------------',
				                      '----------------------------------------')
				print template.format(task.id, priority, task.task, task.note)

	def search_tasks(self, search_string):
		"""Search the task list for a task whose contents contains the user provided search string.

		:param str search_string    the string to search for.
		"""

		tasks = self.tasklist.search(search_string.lower())
		if tasks:
			self.show_tasks(tasks)
		else:
			print('\nThere were no tasks containing "{}".\n'.format(search_string))

	def add_task(self, task, priority=None, due_date=None, tags=None, note=None):
		"""Add a new task."""

		self.tasklist.add_task(task, priority, due_date, tags, note)

	def delete_task(self, task_id):
		"""Delete a task."""

		task_id = self._validate_task_id(task_id)
		if task_id:
			self.tasklist.delete_task(task_id)
			self.tasklist.renumber_tasks()
			print('Task ' + task_id + ' was deleted.')

	def modify_task(self, task_id, task_=None, completed = False, priority=None, due_date=None, note=None, tags=None):
		"""Modify a task."""

		task_id = self._validate_task_id(task_id)
		if task_id:
			task = self.tasklist.find_task(task_id)
			if task:
				print 'Modifying task ' + str(task_id) + ': ' + task.task
				if task_:
					task.task = task_
				elif priority:
					task.priority = priority
				elif due_date:
					task.due_date = due_date
				elif note:
					task.note = note
				elif tags:
					task.tags = tags
				elif completed:
					task.completed = True
				print 'Modified task ' + str(task_id)

	def load_tasks(self, task_file):
		"""Load the task file and retrieve the tasks."""

		self.tasklist.tasks = util.load(task_file)
		Task.last_id = len(self.tasklist.tasks)

	def save_tasks(self, task_file):
		"""Save the task file."""

		util.save(self.tasklist.tasks, task_file)

	def _validate_task_id(self, task_id):
		"""Validate a task id.

		:return: None if an invalid ID was provided, otherwise a string containing the valid task id.
		"""

		if task_id.isdigit() and int(task_id) <= len(self.tasklist.tasks):
			return task_id
		else:
			print('{} is not an existing task!'.format(task_id))
			return None