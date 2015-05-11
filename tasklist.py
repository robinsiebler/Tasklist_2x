# ------------------------------------------
# Name:     tasklist
# Purpose:  Class for the creation/management of tasks
#
# Author:   Robin Siebler
# Created:  7/14/13
# ------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/14/13'

import arrow


class Task:
	last_id = 0

	def __init__(self, task, priority, due_date, tags, note):

		"""Initialize a Task object.

		:param task: a string containing the task
		:param priority: the priority of the task (low, medium, high)
		:param tags: any desired tags for the task
		"""

		self.task = task
		self.priority = priority
		self.tags = tags
		self.note = note
		self.completed = False
		self.creation_date = arrow.now().format('MM/DD/YYYY h:mm:ss A ZZ')
		if due_date:
			self.due_date = due_date[0]
			self.due_date_format = due_date[1]
		else:
			self.due_date = None
		Task.last_id += 1
		self.id = Task.last_id
		print 'Created task ' + str(self.id)

	def match(self, search_string):
		"""Return a list of tasks where search_string is found in either the task or tags.

		:return: a list of matches
		"""
		result2 = result3 = False

		result1 = search_string in self.task.lower()

		if self.note:
			result2 = search_string in self.note.lower()
		if self.tags:
			result3 = search_string in self.tags.lower()

		return result1 or result2 or result3


class TaskList:
	def __init__(self):

		self.tasks = []

	def add_task(self, task, priority='', due_date=None, tags=None, note=None):
		"""Add a new task to the task list.

		:param task:        a string containing the task
		:param priority:    the priority of the task (low, medium, high)
		:param tags:        any desired tags for the task
		:param note:        a lengthier description of the task
		"""

		self.tasks.append(Task(task, priority, due_date, tags, note))

	def delete_task(self, task_id):
		"""Delete the given task.

		:param task_id: id of the task to delete
		"""

		task = self.find_task(task_id)
		if task:
			self.tasks.remove(task)

	def search(self, search_string):
		"""Return all task that match the given search string

		:param search_string: search string
		:return: task list
		"""

		return [task for task in self.tasks if task.match(search_string)]

	def find_task(self, task_id):
		"""Find a task by task.id

		:param task_id: The task.id for the task to find.
		:return: a task object if found, otherwise None
		"""
		for task in self.tasks:
			if str(task.id) == str(task_id):
				return task
		return None

	def renumber_tasks(self):
		"""Renumber all of the tasks. Useful when a task is deleted."""

		if len(self.tasks) > 0:
			global last_id
			last_id = 1

			for task in self.tasks:
				task.id = last_id
				last_id += 1


if __name__ == '__main__':
	pass  # put call to unit tests here?