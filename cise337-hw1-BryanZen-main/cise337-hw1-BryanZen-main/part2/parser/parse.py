from db.manager import sort, search, create, get_all_tasks, add_task, remove_task, complete_task, change_priority, \
    update_desc
from utils.commands import sort_cmd, search_cmd, update_cmd, change_priority_cmd, complete_task_cmd, remove_task_cmd, \
    add_task_cmd, list_all_tasks_cmd, showhelp


# parse the command line arguments and execute the appropriate commands.
def parseArgs(args):
    n = len(args)
    if n == 1:
        return "Missing Required argument. Type -h to seek help"
    for i in range(1, n):
        a = args[i]
        if a == '-h':  # -h or --help to print this menu.
            showhelp()
        if a == '-l' or a == '--list':  # -l or --list to list all tasks.
            str = list_all_tasks_cmd().replace('ID: ', '').replace(' DESC: ', ',').replace(' PRIORITY: ', ',').replace(
                ' STATUS: ', ',')
            return str
        if a == '-a' or a == '--add':  # -a or --add <DESCRIPTION> to add a new task. -p or --priority <NUMBER> to assign a priority to a new task. Must use with -a or -s.
            for j in range(1, n):
                if j + 4 < n:
                    return 'Error: Found extraneous options'
                else:
                    if args[j + 2] == '-p' or args[j + 2] == '--priority':
                        if j + 3 < n:
                            if isinstance(args[j + 3], int):
                                return add_task_cmd(args[i + 1], args[i + 3])
                            else:
                                return 'Priority must be integer'
                        else:
                            return 'Error: Cannot add a task with empty priority'
                    else:
                        return 'Error: Incorrect priority option'
        if a == '-r' or a == '--remove':   #-r or --remove <ID> remove a task.
            for j in range(1, n):
                if i + 1 < n:
                    if i + 3 < n:
                        return 'Error: Found extraneous options'
                    else:
                        if isinstance(args[j + 1], int):
                            return remove_task_cmd(args[i + 1])
                        else:
                            return 'Task ID must be a number'
                else:
                    return 'Task ID missing'
        if a == '-c' or a == '--complete':#-c or --complete <ID> mark a task as complete.
            for j in range(1, n):
                if j + 1 < n:
                    if j + 2 < n:
                        return 'Error: Found extraneous options'
                    else:
                        if isinstance(args[j + 1], int):
                            return complete_task_cmd(args[i + 1])
                        else:
                            return 'Task ID must be a number'
                else:
                    return 'Task ID missing'

        if a == '-cp' or a == '--changepriority':#-cp or --changepriority <ID> <NUMBER> change an existing task\'s priority.
            for j in range(1, n):
                if j + 1 < n:
                    if j + 3 < n:
                        return 'Error: Found extraneous options'
                    else:
                        if isinstance(args[j + 1], int) and isinstance(args[j + 2], int):
                            return change_priority_cmd(args[i + 1], args[i + 2])
                        else:
                            return 'Task ID must be a number'
                else:
                    return 'Task ID or priority missing'
        if a == '-u' or a == '--update':#-u or --update <ID> <DESCRIPTION> update an existing task\'s description.
            for j in range(1, n):
                if j + 1 < n:
                    if j + 3 < n:
                        return 'Error: Found extraneous options'
                    else:
                        if isinstance(args[j + 1], int):
                            return update_cmd(args[i + 1], args[i + 2])
                        else:
                            return 'Task ID must be a number'
                else:
                    return 'Task ID or description missing'
        if a == '-s' or a == '--search':#-s or --search <OPTIONS> search a task by options. #-p or --priority <NUMBER> to assign a priority to a new task. Must use with -a or -s.
            for j in range(1, n):
                ty = ''
                if j + 1 < n:
                    ty = args[j + 1]
                    if ty == '-i' or ty == '--id':
                        pass  #incompleted
                else:
                    return 'Search Criteria Missing'

            return search_cmd()
        if a == '-t' or a == '--sort':#-t or --sort show sorted list of tasks by increasing order of priority.
            for j in range(1, n):
                if j + 2 < n:
                    return 'Error: Found extraneous options'
                else:
                    if j + 1 < n:
                        if args[j + 1] == '-d' or args[j + 1] == '--desc':
                            return sort_cmd(2)
                    else:
                        return sort_cmd(1)
        # if a == '-d' or a == '--desc':#-d or --desc decreasing order of priority. Must use with -t.
        # if a == '-i' or a == '--id':#-i or --id <ID> task ID. Must use with -s for search task with ID.
        # if a == '-dp' or a == '--description':#-dp or --description <TEXT> task description. Must use with -s for search task with description.
