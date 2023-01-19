import os
from db.manager import sort, search, create, get_all_tasks, add_task, remove_task, complete_task, change_priority, update_desc

tasks_file = os.path.join(os.getcwd(), 'part2', 'db', 'tasks.csv')


def showhelp():
    print('usage: python main.py <options>')
    print('===== options =====')
    print('-h or --help to print this menu.')
    print('-l or --list to list all tasks.')
    print('-a or --add <DESCRIPTION> to add a new task')
    print('-p or --priority <NUMBER> to assign a priority to a new task. Must use with -a or -s.')
    print('-r or --remove <ID> remove a task.')
    print('-c or --complete <ID> mark a task as complete.')
    print('-cp or --changepriority <ID> <NUMBER> change an existing task\'s priority.')
    print('-u or --update <ID> <DESCRIPTION> update an existing task\'s description.')
    print('-s or --search <OPTIONS> search a task by options.')
    print('-t or --sort show sorted list of tasks by increasing order of priority.')
    print('-d or --desc decreasing order of priority. Must use with -t.')
    print('-i or --id <ID> task ID. Must use with -s for search task with ID.')
    print('-dp or --description <TEXT> task description. Must use with -s for search task with description.')


# command to list all tasks
def list_all_tasks_cmd():
    create()
    f = open(tasks_file, 'r')
    str = ''
    i = 0
    for line in f:
        i += 1
        if i > 1:
            spl = line.split(",")
            new = 'ID: {d} DESC: {desc} PRIORITY: {prior} STATUS: {status}'.format(d=spl[0], desc=spl[1], prior=spl[2],
                                                                                   status=spl[3])
            str += new
    if i == 1:
        return 'TODO List empty. Add some tasks.'
    else:
        return str


# command to add a task
def add_task_cmd(task, priority):
    create()
    if len(task) == 0 or int(priority) <= 0:
        return 'Failed to add task'
    create()
    id = add_task(task, priority)
    return 'Task added and assigned ID {k}'.format(k=id)


# command to delete a task
def remove_task_cmd(id):
    create()
    if remove_task(id):
        return 'Removed task ID {x}'.format(x=str(id))
    else:
        return 'Failed to remove task ID {x}'.format(x=str(id))

# command to complete a task
def complete_task_cmd(id):
    create()
    if complete_task(id):
        return 'Task {x} completed'.format(x=str(id))
    else:
        return 'Task {x} could not be completed'.format(x=str(id))

# command to edit task priority
def change_priority_cmd(id, priority):
    create()
    if int(id) < 1 or int(priority) < 1:
        return 'Priority of task {x} could not be changed'.format(x=str(id))
    if change_priority(id, priority):
        return 'Changed priority of task {a} to {b}'.format(a=str(id), b=str(priority))
    else:
        return 'Priority of task {x} could not be changed'.format(x=str(id))

# command to edit task description
def update_cmd(id, desc):
    create()
    if int(id) < 1 or len(desc) == 0:
        return 'Failed to update task {x}'.format(x=str(id))
    if update_desc(id, desc):
        return 'Task {x} updated'.format(x=str(id))
    else:
        return 'Failed to update task {x}'.format(x=str(id))


# command to search a task by id, description, or priority
def search_cmd(id, desc, priority):
    create()
    x = search(id, desc, priority)
    if len(x) == 0:
        return 'Task not found'
    else:
        return x

# command to sort the tasks in specified order
def sort_cmd(order):
    create()
    return sort(order)
