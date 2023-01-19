import sys, os
sys.path.insert(1, os.path.join(os.getcwd(), 'part2'))
# sys.path.insert(1, os.getcwd())
from parser.parse import parseArgs
from utils.commands import sort_cmd, search_cmd, update_cmd, change_priority_cmd, complete_task_cmd, remove_task_cmd, add_task_cmd, list_all_tasks_cmd
from db.manager import sort, search, create, get_all_tasks, add_task, remove_task, complete_task, change_priority, update_desc

tasks_file = os.path.join(os.getcwd(), 'part2', 'db', 'tasks.csv')

class TestTodoManager:

    def setup_method(self):
        if os.path.exists(tasks_file):
            os.remove(tasks_file)

    def test_parse_args_no_args(self):
        assert parseArgs(['main.py']) == 'Missing Required argument. Type -h to seek help'

    def test_db_manager_create(self):
        assert create()
        assert not create()
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n']

    def test_get_all_tasks(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Buy Eggs,2,Incomplete\n')
            f.write('2,Go to class,5,Incomplete\n')
            f.write('3,Finish Hw,1,Complete\n')
        assert get_all_tasks() == ['1,Buy Eggs,2,Incomplete\n', '2,Go to class,5,Incomplete\n', '3,Finish Hw,1,Complete\n']

    def test_list_all_tasks_cmd_empty(self):
        assert list_all_tasks_cmd() == 'TODO List empty. Add some tasks.'

    def test_list_all_tasks_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Buy Eggs,2,Incomplete\n')
            f.write('2,Go to class,5,Incomplete\n')
            f.write('3,Finish Hw,1,Complete\n')
        assert list_all_tasks_cmd().split('\n') == ['ID: 1 DESC: Buy Eggs PRIORITY: 2 STATUS: Incomplete', 'ID: 2 DESC: Go to class PRIORITY: 5 STATUS: Incomplete', 'ID: 3 DESC: Finish Hw PRIORITY: 1 STATUS: Complete','']

    def test_add_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,1,Complete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,5,Incomplete\n')
        assert 4 == add_task('Meet Friends', 10)
        with open(tasks_file, 'r') as f:
            assert f.readlines() ==  ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,1,Complete\n', '2,Eat food,1,Incomplete\n', '3,Write journal,5,Incomplete\n', '4,Meet Friends,10,Incomplete\n']

    def test_add_task_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Breathe Air,1,Complete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Exercise,3,Incomplete\n')
            f.write('4,Go running,3,Complete\n')
        assert 'Task added and assigned ID 5'== add_task_cmd('Go to work', 6)

    def test_add_task_cmd_fail_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Eat food,1,Incomplete\n')
            f.write('2,Exercise,4,Incomplete\n')
            f.write('3,Go running,3,Complete\n')
        assert 'Failed to add task'== add_task_cmd('', 10)

    def test_add_task_cmd_fail_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Eat food,1,Incomplete\n')
            f.write('2,Exercise,4,Incomplete\n')
            f.write('3,Go running,3,Complete\n')
        assert 'Failed to add task'== add_task_cmd('x', -10)

    def test_remove_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert remove_task(3)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Incomplete\n', '3,Party,1,Complete\n', '4,Go to class,10,Incomplete\n']

    def test_remove_absent_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert remove_task(13) != None
        assert not remove_task(13)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Incomplete\n', '3,Write journal,5,Incomplete\n', '4,Party,1,Complete\n', '5,Go to class,10,Incomplete\n']

    def test_remove_task_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,12,Incomplete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,2,Complete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,5,Incomplete\n')
        assert 'Removed task ID 2'== remove_task_cmd(2)

    def test_remove_task_cmd_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,12,Incomplete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,2,Complete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,5,Incomplete\n')
        assert 'Failed to remove task ID 6'== remove_task_cmd(6)

    def test_complete_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Incomplete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        complete_task(5)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Incomplete\n', '3,Write journal,5,Incomplete\n', '4,Party,1,Complete\n', '5,Go to class,10,Complete\n']

    def test_complete_absent_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert complete_task(7) != None
        assert not complete_task(7)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Complete\n', '3,Write journal,5,Incomplete\n', '4,Party,1,Complete\n', '5,Go to class,10,Incomplete\n']


    def test_complete_compltd_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert complete_task(2)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Complete\n', '3,Write journal,5,Incomplete\n', '4,Party,1,Complete\n', '5,Go to class,10,Incomplete\n']

    def test_complete_task_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
            f.write('6,Call Mom,1,Incomplete\n')
        assert 'Task 6 completed' == complete_task_cmd(6)

    def test_complete_task_cmd_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
            f.write('6,Call Mom,1,Incomplete\n')
        assert 'Task 8 could not be completed' == complete_task_cmd(8)

    def test_change_task_priority(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert change_priority(4, 3)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Complete\n', '3,Write journal,5,Incomplete\n', '4,Party,3,Complete\n', '5,Go to class,10,Incomplete\n']

    def test_change_absent_task_priority(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,3,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert change_priority(14, 3) != None
        assert not change_priority(14, 3)
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,2,Complete\n', '2,Eat food,1,Complete\n', '3,Write journal,5,Incomplete\n', '4,Party,3,Complete\n', '5,Go to class,10,Incomplete\n']

    def test_change_task_priority_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert 'Changed priority of task 4 to 4' == change_priority_cmd(4, 4)

    def test_change_task_priority_cmd_fail_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert 'Priority of task -4 could not be changed' == change_priority_cmd(-4, 4)

    def test_change_task_priority_cmd_fail_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert 'Priority of task 4 could not be changed' == change_priority_cmd(4, -4)

    def test_change_task_desc(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take Mecine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy tickets,4,Complete\n')
        assert update_desc(2, 'Take medicine')
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,See Jane,2,Incomplete\n', '2,Take medicine,1,Incomplete\n', '3,Write paper,3,Complete\n', '4,Buy tickets,4,Complete\n']

    def test_change_task_desc_cmd(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take Mecine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy ticket,4,Complete\n')
        assert 'Task 4 updated' == update_cmd(4, 'Buy tickets')

    def test_change_task_desc_cmd_fail_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take Mecine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy ticket,4,Complete\n')
        assert 'Failed to update task 0' == update_cmd(0, 'Buy tickets')

    def test_change_task_desc_cmd_fail_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take Mecine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy ticket,4,Complete\n')
        assert 'Failed to update task 2' == update_cmd(2, '')

    def test_change_absent_task_desc(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take Mecine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy tickets,4,Complete\n')
        assert update_desc(21, 'Take medicine') != None
        assert not update_desc(21, 'Take medicine')
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,See Jane,2,Incomplete\n', '2,Take Mecine,1,Incomplete\n', '3,Write paper,3,Complete\n', '4,Buy tickets,4,Complete\n']

    def test_search_by_id(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(4, None, None) == '4,Buy 5 tickets,4,Complete\n'

    def test_search_by_id_priority(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(4, None, 4) == '4,Buy 5 tickets,4,Complete\n'

    def test_search_by_id_desc(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(5, 'Print documents', None) == '5,Print documents,4,Complete\n'

    def test_search_by_id_desc_priority(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(5, 'Print documents', 4) == '5,Print documents,4,Complete\n'

    def test_search_empty_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(5, 'Print documents', 5) == ''

    def test_search_empty_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(None, 'Print documents', 5) == ''

    def test_search_empty_3(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,2,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(None, 'Print ', 5) == ''

    def test_search_by_priority(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(None, None, 4) == '1,See Jane,4,Incomplete\n4,Buy 5 tickets,4,Complete\n5,Print documents,4,Complete\n'

    def test_search_by_desc(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take Medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search(None, 'take medicine', None) == '2,Take Medicine,1,Incomplete\n'

    def test_search_cmd_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search_cmd(None, None, 4) ==  '1,See Jane,4,Incomplete\n4,Buy 5 tickets,4,Complete\n5,Print documents,4,Complete\n'

    def test_search_cmd_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search_cmd(1, None, 4) == '1,See Jane,4,Incomplete\n'

    def test_search_cmd_3(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search_cmd(5, 'Print documents', 4) == '5,Print documents,4,Complete\n'

    def test_search_cmd_fail_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search_cmd(5, 'Print documents', 1) == 'Task not found'

    def test_search_cmd_fail_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert search_cmd(None, None, -1) == 'Task not found'

    def test_sort_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take Medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert sort() == '2,Take Medicine,1,Incomplete\n3,Write paper,3,Complete\n1,See Jane,4,Incomplete\n4,Buy 5 tickets,4,Complete\n5,Print documents,4,Complete\n'

    def test_sort_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,See Jane,4,Incomplete\n')
            f.write('2,Take Medicine,1,Incomplete\n')
            f.write('3,Write paper,3,Complete\n')
            f.write('4,Buy 5 tickets,4,Complete\n')
            f.write('5,Print documents,4,Complete\n')
        assert sort(2) == '1,See Jane,4,Incomplete\n4,Buy 5 tickets,4,Complete\n5,Print documents,4,Complete\n3,Write paper,3,Complete\n2,Take Medicine,1,Incomplete\n'

    def test_sort_cmd_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Meet Jane,4,Incomplete\n')
            f.write('2,Take Medicines,1,Incomplete\n')
            f.write('3,Write papers,3,Complete\n')
            f.write('4,Buy 3 tickets,4,Incomplete\n')
            f.write('5,Print documents,4,Complete\n')
        assert sort_cmd('') == '2,Take Medicines,1,Incomplete\n3,Write papers,3,Complete\n1,Meet Jane,4,Incomplete\n4,Buy 3 tickets,4,Incomplete\n5,Print documents,4,Complete\n'

    def test_sort_cmd_2(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Meet Jane,4,Incomplete\n')
            f.write('2,Take Medicines,1,Incomplete\n')
            f.write('3,Write papers,3,Complete\n')
            f.write('4,Buy 3 tickets,4,Incomplete\n')
            f.write('5,Print documents,4,Complete\n')
        assert sort_cmd('-d') == '1,Meet Jane,4,Incomplete\n4,Buy 3 tickets,4,Incomplete\n5,Print documents,4,Complete\n3,Write papers,3,Complete\n2,Take Medicines,1,Incomplete\n'

    def test_parse_args_list_tasks(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert parseArgs(['main.py', '-l']).split('\n') == ['1,Exercise,2,Complete', '2,Eat food,1,Complete', '3,Write journal,5,Incomplete', '4,Party,1,Complete', '5,Go to class,10,Incomplete', '']
        assert parseArgs(['main.py', '--list']).split('\n') == ['1,Exercise,2,Complete', '2,Eat food,1,Complete', '3,Write journal,5,Incomplete', '4,Party,1,Complete', '5,Go to class,10,Incomplete', '']

    def test_parse_args_add_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert parseArgs(['main.py', '-a', 'Finish HW1', '-p', 1]) == 'Task added and assigned ID 6'
        assert parseArgs(['main.py', '--add', 'Finish HW2', '-p', 1]) == 'Task added and assigned ID 7'
        assert parseArgs(['main.py', '-a', 'Finish HW3', '--priority', 3]) == 'Task added and assigned ID 8'
        assert parseArgs(['main.py', '--add', 'Finish HW4', '--priority', 2]) == 'Task added and assigned ID 9'

    def test_parse_args_add_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,1,Complete\n')
            f.write('3,Write journal,5,Incomplete\n')
            f.write('4,Party,1,Complete\n')
            f.write('5,Go to class,10,Incomplete\n')
        assert parseArgs(['main.py', '-a', 'Finish HW1', '-p']) == 'Error: Cannot add a task with empty priority'
        assert parseArgs(['main.py', '-a', '-p', 2]) == 'Error: Incorrect priority option'
        assert parseArgs(['main.py', '-a', 'HW', '-p', 'Two']) == 'Priority must be integer'
        assert parseArgs(['main.py', '--add', 'HW', '-p', 2, '-i']) == 'Error: Found extraneous options'

    def test_parse_args_remove_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-r', 5]) == 'Removed task ID 5'
        assert parseArgs(['main.py', '--remove', 1]) == 'Removed task ID 1'
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Eat food,2,Complete\n', '2,Write journal,1,Incomplete\n', '3,Party,10,Complete\n']

    def test_parse_args_remove_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
        assert parseArgs(['main.py', '-r', 'five']) == 'Task ID must be a number'
        assert parseArgs(['main.py', '-r']) == 'Task ID missing'
        assert parseArgs(['main.py', '-r', 4, '-desc', 'HW']) == 'Error: Found extraneous options'
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,5,Complete\n', '2,Eat food,2,Complete\n', '3,Write journal,1,Incomplete\n', '4,Party,10,Complete\n']

    def test_parse_args_complete_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-c', 3]) == 'Task 3 completed'
        assert parseArgs(['main.py', '--complete', 1]) == 'Task 1 completed'

    def test_parse_args_complete_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
        assert parseArgs(['main.py', '-c', 'five']) == 'Task ID must be a number'
        assert parseArgs(['main.py', '--complete']) == 'Task ID missing'
        assert parseArgs(['main.py', '-c', '--complete', 4, 'HW']) == 'Error: Found extraneous options'
        with open(tasks_file, 'r') as f:
            assert f.readlines() == ['ID,DESCRIPTION,PRIORITY,STATUS\n', '1,Exercise,5,Complete\n', '2,Eat food,2,Complete\n', '3,Write journal,1,Incomplete\n', '4,Party,10,Complete\n']

    def test_parse_args_change_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,3,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,4,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-cp', 3, 4]) == 'Changed priority of task 3 to 4'
        assert parseArgs(['main.py', '--changepriority', 1, 1]) == 'Changed priority of task 1 to 1'
        with open(tasks_file, 'r') as f:
            lines = f.readlines()
            assert lines[3] == '3,Write journal,4,Incomplete\n'
            assert lines[1] == '1,Exercise,1,Complete\n'

    def test_parse_args_change_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
        assert parseArgs(['main.py', '-cp', 'five']) == 'Task ID must be a number'
        assert parseArgs(['main.py', '--changepriority']) == 'Task ID or priority missing'
        assert parseArgs(['main.py', '-cp', '', 4, 'HW']) == 'Error: Found extraneous options'

    def test_parse_args_update_task(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,3,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,4,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-u', 2, 'Eat Apple']) == 'Task 2 updated'
        assert parseArgs(['main.py', '--update', 4, 'Party with Jill']) == 'Task 4 updated'
        with open(tasks_file, 'r') as f:
            lines = f.readlines()
            assert lines[2] == '2,Eat Apple,3,Complete\n'
            assert lines[4] == '4,Party with Jill,4,Complete\n'

    def test_parse_args_update_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,5,Complete\n')
            f.write('2,Eat food,2,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,10,Complete\n')
        assert parseArgs(['main.py', '--update', '-i', 2]) == 'Task ID must be a number'
        assert parseArgs(['main.py', '-u']) == 'Task ID or description missing'
        assert parseArgs(['main.py', '-u', 2, 'Eat Apple', 'Take Meds']) == 'Error: Found extraneous options'

    def test_parse_args_search_task_1(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,3,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,4,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-s', '-i', 2]) == '2,Eat food,3,Complete\n'
        assert parseArgs(['main.py', '-s', '--id', 2]) == '2,Eat food,3,Complete\n'
        assert parseArgs(['main.py', '-s', '--id', 12]) == 'Task not found'
        assert parseArgs(['main.py', '--search', '-dp', 'Write journal']) == '3,Write journal,1,Incomplete\n'
        assert parseArgs(['main.py', '-s', '--description', 'Write journal']) == '3,Write journal,1,Incomplete\n'
        assert parseArgs(['main.py', '--search', '-p', 1, '-dp', 'Write journals']) == 'Task not found'
        assert parseArgs(['main.py', '--search', '-dp', 'Party', '-p', 4,]) == '4,Party,4,Complete\n'
        assert parseArgs(['main.py', '-s', '-p', 4,]) == '4,Party,4,Complete\n5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '-s', '--priority', 4,'--id',5]) == '5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '--search', '-i', 5, '--priority', 4]) == '5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '-s', '-id', 5, '--priority', 4]) == '1,Exercise,2,Complete\n2,Eat food,3,Complete\n3,Write journal,1,Incomplete\n4,Party,4,Complete\n5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '-s', '-priority', 4, '-dp', 'Party']) == '1,Exercise,2,Complete\n2,Eat food,3,Complete\n3,Write journal,1,Incomplete\n4,Party,4,Complete\n5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '-s', '-i', 4, '--dp', 'Party']) == '4,Party,4,Complete\n'

    def test_parse_args_search_task_fail(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,3,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,4,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-s', '-i', 'Two', '-p', 4]) == 'search ID and priority must be integer.'
        assert parseArgs(['main.py', '-s', '-i', 3, '--priority', 'Two']) == 'search ID and priority must be integer.'
        assert parseArgs(['main.py', '-s', '-i', 3, '-dp', 'HW', '--priority', 'Two']) == 'search ID and priority must be integer.'
        assert parseArgs(['main.py', '--search']) == 'Search Criteria Missing'

    def test_parse_args_sort(self):
        with open(tasks_file, 'w') as f:
            f.write('ID,DESCRIPTION,PRIORITY,STATUS\n')
            f.write('1,Exercise,2,Complete\n')
            f.write('2,Eat food,3,Complete\n')
            f.write('3,Write journal,1,Incomplete\n')
            f.write('4,Party,4,Complete\n')
            f.write('5,Go to class,4,Incomplete\n')
        assert parseArgs(['main.py', '-t']) == '3,Write journal,1,Incomplete\n1,Exercise,2,Complete\n2,Eat food,3,Complete\n4,Party,4,Complete\n5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '--sort']) == '3,Write journal,1,Incomplete\n1,Exercise,2,Complete\n2,Eat food,3,Complete\n4,Party,4,Complete\n5,Go to class,4,Incomplete\n'
        assert parseArgs(['main.py', '-t', '-d']) == '4,Party,4,Complete\n5,Go to class,4,Incomplete\n2,Eat food,3,Complete\n1,Exercise,2,Complete\n3,Write journal,1,Incomplete\n'
        assert parseArgs(['main.py', '--sort', '-d']) == '4,Party,4,Complete\n5,Go to class,4,Incomplete\n2,Eat food,3,Complete\n1,Exercise,2,Complete\n3,Write journal,1,Incomplete\n'

    def test_parse_args_sort_fail(self):
        assert parseArgs(['main.py', '-t','-d',2]) == 'Error: Found extraneous options'
        assert parseArgs(['main.py', '--sort','-d',2]) == 'Error: Found extraneous options'
