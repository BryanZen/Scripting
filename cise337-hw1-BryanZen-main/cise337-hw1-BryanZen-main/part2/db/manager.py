import os

tasks_file = os.path.join(os.getcwd(), 'part2', 'db', 'tasks.csv')


# creates tasks file is none exists
def create():
    if is_tasks_file_exists():
        return False
    else:
        new = open(tasks_file, 'w')
        new.writelines(['ID,DESCRIPTION,PRIORITY,STATUS\n'])
        new.close()
        return True


# check if tasks file exists
def is_tasks_file_exists():
    return os.path.exists(tasks_file)


# adds a task to the task file and returns the task id.
def add_task(desc, priority):
    f = open(tasks_file, 'r')
    id = sum(1 for _ in f)
    add = open(tasks_file, 'a')
    add.writelines(['{a},{b},{c},Incomplete\n'.format(a=str(id), b=desc, c=str(priority))])
    f.close()
    add.close()
    return id


# returns list of tasks in the task file.
def get_all_tasks():
    f = open(tasks_file, 'r')
    l = list()
    i = 0
    for line in f:
        i += 0
        l.append(line)
    f.close()
    if i == 1:
        return 'TODO List empty. Add some tasks.'
    return l[1:len(l)]


# remove a task from the task file.
def remove_task(id):
    s = str(id)
    f = open(tasks_file, 'r')
    l = ['ID,DESCRIPTION,PRIORITY,STATUS\n']
    found = False
    i = 0
    for line in f:
        spl = line.split(",")
        if spl[0] == s:
            found = True
        if not spl[0] == s and i > 0:
            if int(spl[0]) < id:
                l.append('{a},{b},{c},{d}'.format(a=spl[0], b=spl[1], c=spl[2], d=spl[3]))
            else:
                newid = str(int(spl[0]) - 1)
                l.append('{a},{b},{c},{d}'.format(a=newid, b=spl[1], c=spl[2], d=spl[3]))
        i += 1
    new = open(tasks_file, 'w')
    new.writelines(l)
    f.close()
    new.close()
    if found:
        return True
    else:
        return False


# complete a task in the task file.
def complete_task(id):
    s = str(id)
    f = open(tasks_file, 'r')
    l = []
    found = False
    for line in f:
        spl = line.split(",")
        if spl[0] == s:
            found = True
            l.append('{a},{b},{c},{d}'.format(a=spl[0], b=spl[1], c=spl[2], d='Complete\n'))
        else:
            l.append(line)
    new = open(tasks_file, 'w')
    new.writelines(l)
    f.close()
    new.close()
    if not found:
        return False
    else:
        return True


# change the priority of a task in the task file.
def change_priority(id, priority):
    s = str(id)
    p = str(priority)
    f = open(tasks_file, 'r')
    l = []
    found = False
    for line in f:
        spl = line.split(",")
        if spl[0] == s:
            found = True
            l.append('{a},{b},{c},{d}'.format(a=spl[0], b=spl[1], c=p, d=spl[3]))
        else:
            l.append(line)
    new = open(tasks_file, 'w')
    new.writelines(l)
    f.close()
    new.close()
    if not found:
        return False
    else:
        return True


# update the task description of a task in the task file.
def update_desc(id, desc):
    s = str(id)
    p = str(desc)
    f = open(tasks_file, 'r')
    l = []
    found = False
    for line in f:
        spl = line.split(",")
        if spl[0] == s:
            found = True
            l.append('{a},{b},{c},{d}'.format(a=spl[0], b=desc, c=spl[2], d=spl[3]))
        else:
            l.append(line)
    new = open(tasks_file, 'w')
    new.writelines(l)
    f.close()
    new.close()
    x = open(tasks_file, 'r')
    print(x.read())
    x.close()
    if not found:
        return False
    else:
        return True


# search for a task in the task file.
def search(id, desc, priority):
    nullid = False
    if id is None:
        nullid = True
    s = str(id)
    d = str(desc)
    p = str(priority)
    f = open(tasks_file, 'r')
    l = ''
    for line in f:
        spl = line.split(",")
        if spl[0] == s and not nullid:
            if desc is None and priority is None:
                return line
            if desc is None and spl[2] == p:
                return line
            if spl[1].lower() == d.lower() and priority is None:
                return line
            if spl[1].lower() == d.lower() and spl[2] == p:
                return line
        if nullid:
            if desc is None and spl[2] == p:
                l += line
            if spl[1].lower() == d.lower() and priority is None:
                l += line
            if spl[1].lower() == d.lower() and spl[2] == p:
                l += line
    f.close()
    return l


# sort the tasks in the task file. Default order is 1.
def sort(order=1):
    f = open(tasks_file, 'r')
    l = []
    i = 0
    for line in f:
        if i != 0:
            spl = line.split(",")
            spl[0] = int(spl[0])
            spl[2] = int(spl[2])
            l.append(spl)
        i += 1
    if order == 1 or order == '':
        l.sort(key=lambda row: (row[2], row[0]))
    if order == 2 or order == '-d':
        l.sort(key=lambda row: (-row[2], row[0]))
    out = ''
    for list in l:
        temp = ''
        h = 0
        for p in list:
            p = str(p)
            if h < 3:
                temp += (p + ',')
            else:
                temp += p
            h += 1
        out += temp
    print(out)
    return out