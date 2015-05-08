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
import util
from tasklist import Task, TaskList
from collections import OrderedDict

from colorama import init, Fore, Style  # , Back
init()


class Functions:
	def __init__(self):
		"""Initialize the task list."""

		self.tasklist = TaskList()

	def show_tasks(self, tasks=None, date_format=None):
		"""Display the tasks (in ID order)

		:param tasks: tasks object
		"""

		if not tasks:
			tasks = self.tasklist.tasks

		if len(tasks) > 0:

			template = '{0:^3} {1:^3} {2:15} {3:15} {4:20}'
			print template.format('\nID', ' Pri', 'Due', 'Created', 'Description')
			print template.format('---', '---', '---------------', '---------------', '--------------------')
			for task in tasks:
				if task.priority == 'L':
					priority = Fore.YELLOW + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				elif task.priority == 'M':
					priority = Fore.BLUE + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				elif task.priority == 'H':
					priority = Fore.RED + Style.BRIGHT + ' ' + task.priority + ' ' + Fore.RESET + Style.NORMAL
				else:
					priority = ''

				if task.due_date is None:
					due_date = ''
				else:
					if date_format:
						due_date = arrow.get(task.due_date, task.due_date_format).humanize()
					else:
						due_date = task.due_date

				if date_format:
					age = arrow.get(task.creation_date, 'MM/DD/YYYY hh:mm:ss A ZZ').humanize()
				else:
					age = str(task.creation_date).split()[0]

				# TODO: add tags

				if task.note:
					desc = task.task + ' *'
				else:
					desc = task.task
				print template.format(task.id, priority, due_date, age, desc)

		else:
			print('\nThere are no tasks to display!\n')

	def show_tasks_by_priority(self, tasks=None):
		"""Display the tasks (in Priority order)

		:param tasks: tasks object
		"""

		low_dict = OrderedDict()
		med_dict = OrderedDict()
		high_dict = OrderedDict()

		if not tasks:
			tasks = self.tasklist.tasks

		if len(tasks) > 0:
			print('\nTasks:\n')
			for task in tasks:
				if task.priority == 'Low':
					low_dict[task.id] = [task.note, task.priority, task.tags]
				if task.priority == 'Medium':
					med_dict[task.id] = [task.note, task.priority, task.tags]
				if task.priority == 'High':
					high_dict[task.id] = [task.note, task.priority, task.tags]
		else:
			print('\nThere are no tasks to display!\n')
			return

		print('High\n' + '-' * 20)
		if len(high_dict) > 0:
			for key in high_dict:
				print('{}: {}\n\tTags: {}\n'.format(key, high_dict[key][0], high_dict[key][2]))
		else:
			print('There are no high priority tasks\n')

		print('Medium\n' + '-' * 20)
		if len(med_dict) > 0:
			for key in med_dict:
				print('{}: {}\n\tTags: {}\n'.format(key, med_dict[key][0], med_dict[key][2]))
		else:
			print('There are no medium priority tasks\n')

		print('Low\n' + '-' * 20)
		if len(low_dict) > 0:
			for key in low_dict:
				print('{}: {}\n\tTags: {}\n'.format(key, low_dict[key][0], low_dict[key][2]))
		else:
			print('There are no low priority tasks!\n')

	def search_tasks(self):
		"""Search the task list for a task whose note or tag contains the user provided search string."""

		search_string = raw_input('Enter the text you wish to search for: ').lower()
		tasks = self.tasklist.search(search_string)
		if tasks:
			self.show_tasks(tasks)
		else:
			print('\nThere were no tasks containing "{}".\n'.format(search_string))

	def add_task(self, task, priority=None, due_date=None, tags=None, note=None):
		"""Add a new task."""

		self.tasklist.add_task(task, priority, due_date, tags, note)

	def delete_task(self):
		"""Delete a task."""

		task_id = self._validate_task_id('delete: ')
		if task_id:
			self.tasklist.delete_task(task_id)
			self.tasklist.renumber_tasks()
			print('The task was deleted.')

	def load_tasks(self, task_file):
		"""Load the task file and retrieve the tasks."""

		self.tasklist.tasks = util.load(task_file)
		Task.last_id = len(self.tasklist.tasks)

	def save_tasks(self, task_file):
		"""Save the task file."""

		util.save(self.tasklist.tasks, task_file)

	def _validate_task_id(self, prompt):
		"""Prompt the user for a task ID and validate it.

		:param prompt: string appended to user prompt indicating the action to be taken after validation.
		:return: False if an invalid ID was provided, otherwise a string containing the valid task id.
		"""

		task_id = raw_input('Enter the Number of the Task you wish to ' + prompt)
		if task_id.isdecimal() and int(task_id) <= len(self.tasklist.tasks):
			return task_id
		else:
			print('{} is not an existing task!'.format(task_id))
			return None