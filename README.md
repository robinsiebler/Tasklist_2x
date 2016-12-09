# Tasklist_2x
My imitation of Task Warrior

A simple command-line based task maanager.

run 'tasks.py -h' for the complete help menu:

Usage: tasks.py command argument option

	   tasks.py priority [-a]
	   tasks.py display <Task_ID>
	   tasks.py search <Search_String>
	   tasks.py modify <Task_ID> ([<Task>] | [-c] | [-p <Priority>] | [-d=<Due_Date> --time=<Time_Due>] | [-n <Note>] | [-t <Tags>])
	   tasks.py [<Task>] [-a] ([-p <Priority>] [-d=<Due_Date> --time=<Time_Due>] [-n <Note>] [-t <Tags>]) | [-r <Task_ID>]


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
        -c                      Mark a task as completed
        -d <Due_Date>           Date the task is due (Ex: M/D/YY, MM-DD-YYYY, MM.DD.YY)
        -n <Note>               A lengthier description of the task
        -p <Priority>           Priority - L, M, H (Low, Medium or High)
        -r <Task_ID>            Remove a task
        -t <Tags>               Words you want to associate with this task
        --time <Time_Due>       Time the Task is due in the format h:mm AM/PM

    Note: The Task, the Note and any Tags need to be in double quotes if they contain spaces.
