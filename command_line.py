#!/usr/bin/python
# ------------------------------------------
# Name:     command_line
# Purpose:  Handle command-line options.
#
# Author:   Robin Siebler
# Created:  5/6/15
# ------------------------------------------

"""
Usage: tasks.py priority [-a]
	   tasks.py display <Task_ID>
	   tasks.py search <Search_String>
	   tasks.py modify <Task_ID> ([<Task>] | [-p <Priority>] | [-d <Due_Date>] | [-n <Note>] | [-t <Tags>])
	   tasks.py [<Task>] [-a] ([-p <Priority>] [-d <Due_Date>] [-n <Note>] [-t <Tags>]) | [-r <Task_ID>]


	Commands:
		display <Task_ID>       Display the note for a Task. This allows you to add more info to a task
		modify <Task_ID>        The Task to modify followed by the updated information
		priority                Display the Tasks in priority order
		search <Search-string>  Search all the tasks for a given work or phrase. If the phrase contains
								spaces, it must be enclosed in double quotes.

    Arguments:
        Task                    The task to add (Only 20 chars will be displayed)

    Options:
        -h --help               Show this screen.
        -a                      Display absolute dates
        -d <Due_Date>           Date the task is due (Ex: M/D/YY, MM-DD-YYYY, MM.DD.YY)
        -n <Note>               A lengthier description of the task
        -p <Priority>           Priority - L, M, H (Low, Medium or High)
        -r <Task_ID>            Remove a task
        -t <Tags>               Words you want to associate with this task

    Note: The Task, the Note and any Tags need to be in double quotes if they contain spaces.
"""

# TODO: Add coloring to task if it is: a) due in a week or less or b) due today.


__author__ = 'Robin Siebler'
__date__ = '5/6/15'

import arrow
import os
import platform
import sys

from docopt import docopt
from pyparsing import Regex, ParseException
from task_functions import Functions


def validate_args(docopt_args):
	"""Validate the user provided information."""

	# validate priority
	if docopt_args['-p']:
		docopt_args['-p'] = docopt_args['-p'].upper()
		if docopt_args['-p'] not in ['L', 'M', 'H']:
			print '\nThe priority given is not valid.\n'
			sys.exit(-4)

	# validate date
	if docopt_args['-d']:
		pattern = Regex('^(1[0-2]|0?[1-9])(/|-|.)(3[01]|[12][0-9]|0?[1-9])(/|-|.)(?:[0-9]{2})?[0-9]{2}$')
		try:
			pattern.parseString(docopt_args['-d'])
		except ParseException:
			print '\n' + docopt_args['-d'] + ' is not a valid date\n'
			sys.exit(-3)
		else:
			# figure out what format the user provided...
			if '/' in docopt_args['-d']:
				date_sep = '/'
			elif '-' in docopt_args['-d']:
				date_sep = '-'
			elif '.' in docopt_args['-d']:
				date_sep = '.'
			else:
				print '\nAn invalid date format was provided.\n'
				sys.exit(-3)
			date = docopt_args['-d'].split(date_sep)

			if len(date[0]) == 1:
				month_format = 'M'
			else:
				month_format = 'MM'

			if len(date[1]) == 1:
				day_format = 'D'
			else:
				day_format = 'DD'

			if len(date[2]) == 2:
				year_format = 'YY'
			else:
				year_format = 'YYYY'

			date_format = date_sep.join([month_format, day_format, year_format])
			date = arrow.get(docopt_args['-d'], date_format)
			print type(date)


			# validate due date occurs in the future
			if 'ago' in date.humanize():
				print '\nThe due date provided occurs in the past. Removing it.\n'
				docopt_args['-d'] = None
			else:
				docopt_args['-d'] = [date.format(date_format), date_format]

	return docopt_args


def main(docopt_args):
	docopt_args = validate_args(docopt_args)

	tasks = Functions()

	if platform.system() == 'Windows':
		home_path = os.path.join(os.path.expandvars('%HOMEDRIVE%'), os.path.expandvars('%HOMEPATH%'))
		task_file = os.path.join(home_path, 'tasks.tsk')
	elif platform.system() == 'Darwin' or platform.system() == 'Linux':
		task_file = os.path.join(os.path.expanduser('~'), 'tasks.tsk')
	else:
		print 'What OS are we on?'
		sys.exit(-2)

	task_file_exists = os.path.exists(task_file)


	if not task_file_exists and docopt_args['<Task>'] is None:
		print '\nThe file ' + task_file + ' does not exist. There are no tasks to display.\n'
		sys.exit(-1)
	elif task_file_exists:
		tasks.load_tasks(task_file)


	if docopt_args['modify']:
		if docopt_args['<Task>']:
			tasks.modify_task(docopt_args['<Task_ID>'], task_=docopt_args['<Task>'])
		elif docopt_args['-p']:
			tasks.modify_task(docopt_args['<Task_ID>'], priority=docopt_args['-p'])
		elif docopt_args['-d']:
			tasks.modify_task(docopt_args['<Task_ID>'], due_date=docopt_args['-d'])
		elif docopt_args['-n']:
			tasks.modify_task(docopt_args['<Task_ID>'], note=docopt_args['-n'])
		elif docopt_args['-t']:
			tasks.modify_task(docopt_args['<Task_ID>'], tags=docopt_args['-t'])
	elif docopt_args['<Task>']:
		if docopt_args['-p']:
			if docopt_args['-d']:
				if docopt_args['-n']:
					if docopt_args['-t']:
						tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'],
						               due_date=docopt_args['-d'], note=docopt_args['-n'], tags=docopt_args['-t'])
					else:
						tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'],
						               due_date=docopt_args['-d'], note=docopt_args['-n'])
				elif docopt_args['-t']:
					tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'],
					               due_date=docopt_args['-d'], tags=docopt_args['-t'])
				else:
					tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'], due_date=docopt_args['-d'])
			elif docopt_args['-n']:
				if docopt_args['-t']:
					tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'],
					               note=docopt_args['-n'], tags=docopt_args['-t'])
				else:
					tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'], note=docopt_args['-n'])
			elif docopt_args['-t']:
				tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'], tags=docopt_args['-t'])
			else:
				tasks.add_task(docopt_args['<Task>'], priority=docopt_args['-p'])
		elif docopt_args['-d']:
			tasks.add_task(docopt_args['<Task>'], due_date=docopt_args['-d'])
		elif docopt_args['-n']:
			tasks.add_task(docopt_args['<Task>'], note=docopt_args['-n'])
		elif docopt_args['-t']:
			tasks.add_task(docopt_args['<Task>'], tags=docopt_args['-t'])
		else:
			tasks.add_task(docopt_args['<Task>'])

	if docopt_args['-r']:
		tasks.delete_task(docopt_args['-r'])
	if docopt_args['-a']:
		tasks.show_tasks(date_format=docopt_args['-a'])
	elif docopt_args['display']:
		tasks.show_task(docopt_args['<Task_ID>'])
	elif docopt_args['priority']:
		tasks.show_tasks_by_priority(date_format=docopt_args['-a'])
	elif docopt_args['search']:
		tasks.search_tasks(docopt_args['<Search_String>'])
	else:
		tasks.show_tasks()

	tasks.save_tasks(task_file)


if __name__ == '__main__':
	args = docopt(__doc__)
	main(args)