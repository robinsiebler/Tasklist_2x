#------------------------------------------
# Name:     tests
# Purpose:  Unit tests will go here
#
# Author:   Robin Siebler
# Created:  7/14/13
#------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/14/13'

# TODO: add unit tests
import pytest

from command_line import validate_args

@pytest.fixture
def setup():
	pass

def test_date_format_1():
	"""Test that the right date format is returned."""

	docopt_args = {'--time': None,
               '-a': True,
               '-c': False,
               '-d': '5/23/2015',
               '-n': None,
               '-p': None,
               '-r': None,
               '-t': None,
               '<Search_String>': None,
               '<Task>': 'Sleep',
               '<Task_ID>': None,
               'display': False,
               'modify': False,
               'priority': False,
               'search': False
               }

	docopt_args = validate_args(docopt_args)
	assert docopt_args['-d'] == ['5/23/2015 11:59 PM -0800', 'M/DD/YYYY h:mm A Z']

def test_date_format_2():
	"""Test that the right date format is returned."""

	docopt_args = {'--time': None,
               '-a': True,
               '-c': False,
               '-d': '5-23-15',
               '-n': None,
               '-p': None,
               '-r': None,
               '-t': None,
               '<Search_String>': None,
               '<Task>': 'Sleep',
               '<Task_ID>': None,
               'display': False,
               'modify': False,
               'priority': False,
               'search': False
               }

	docopt_args = validate_args(docopt_args)
	assert docopt_args['-d'] == ['5-23-15 11:59 PM -0800', 'M-DD-YY h:mm A Z']

def test_date_format_3():
	"""Test that the right date format is returned."""

	docopt_args = {'--time': '7:30 PM',
               '-a': True,
               '-c': False,
               '-d': '6.2.2015',
               '-n': None,
               '-p': None,
               '-r': None,
               '-t': None,
               '<Search_String>': None,
               '<Task>': 'Sleep',
               '<Task_ID>': None,
               'display': False,
               'modify': False,
               'priority': False,
               'search': False
               }

	docopt_args = validate_args(docopt_args)
	assert docopt_args['-d'] == ['6.2.2015 7:30 PM -0800', 'M.D.YYYY h:mm A Z']


def test_invalid_date_format(capsys):
	"""Test that an invalid date format is caught."""

	docopt_args = {'--time': None,
               '-a': True,
               '-c': False,
               '-d': '5-23.15',
               '-n': None,
               '-p': None,
               '-r': None,
               '-t': None,
               '<Search_String>': None,
               '<Task>': 'Sleep',
               '<Task_ID>': None,
               'display': False,
               'modify': False,
               'priority': False,
               'search': False
               }

	with pytest.raises(SystemExit):
		docopt_args = validate_args(docopt_args)
	out, err = capsys.readouterr()
	assert out == '\n5-23.15 is not a valid date\n\n'

