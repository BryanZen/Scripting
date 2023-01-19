# Homework 1

This homework assignment has two parts. In the first part, we will implement the RSA encryption algorithm in Python. In the second part, we will develop command line Python application to automatically maintain a TODO list.

## Learning Outcomes

After completion of this assignment, you should be able to:

- Define functions and classes in Python.

- Write command line applications in Python.

- Use the Python data structures.

- Use File I/O in Python.

## Getting Started

You will need to have *Python3.8 or higher* and *pytest* installed.

You should have already setup Git and configured it to work with SSH. If you haven't then do Homework 0 first!

Download or clone this repository to your local system. Use the following command:

`$ git clone <ssh-link>`

After you clone, you will see a directory of the form *cise337-hw1-\<username\>*, where *username* is your GitHub username.


## How to read the test cases

The *part1/tests* and *part2/tests* directories contain test files, which contains tests to verify your implementations. In each test function, you will find one or more assert statements that need to be true for the test to pass. These asserts compare the expected result with the output of your program. If a test fails, the name of the failing test will be reported with an error message. You can use the error message from the failing test to diagnose and fix your errors.

*Do not change any files in the tests directory. If you do, then you won't receive any credit for this homework assignment*.

## Part 1

RSA Encryption.

### Problem Specification

The RSA algorithm is an encryption algorithm used to generate a pair of public and private keys, which are further used for secure transmission (e.g., HTTPS). Here is how it works informally. Suppose Alice and Bob want to communicate securely. Alice uses the RSA algorithm to generate a public-private key and broadcasts the public key to the world. Alice keeps the private key a secret and stores it securely in some place. If Bob wants to communicate with Alice, Bob gets hold of Alice's public public key, encrypts a secret message with the public key, sends it to Alice, and challenges Alice to decrypt it. If Alice has the corresponding private key, which she has, she will successfully decrypt Bob's secret, thereby proving to Bob that she is indeed Alice. The RSA algorithm is relatively slow. Hence, instead of directly encrypting data with it, it is used by involved parties to exchange a shared secret key, which is used for further encryption and decryption.

The steps in the RSA algorithm are as follows:

1. Choose two distinct prime numbers `p` and `q` and compute `n = p * q`.
2. Compute `K = lcm(p-1, q-1)`.
3. Choose an integer `1 < e < K` such that `e` and `K` are *coprimes*, i.e,   `gcd(e, K) = 1`. `K` must kept secret and `e` is released as the public key.
4.  Compute the private key `d`, where `d` is the [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of `e modulo K`. One efficient way to calculate `d` is to use the [Extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm). The private key must kept a secret.
5. A message `m` is encrypted to a ciphertext `c` using the formula `c = m^e (mod n)`. The numbers `m`, `e` and `n` can get large, occupying vast amounts of memory. A memory-efficient way to generate the ciphertext is to use the [Modular Exponentiation algorithm](https://en.wikipedia.org/wiki/Modular_exponentiation).
6. Given a ciphertext `c`, the original message, `m`, can be extracted using the private key, `e`, with the formula `m = c^d (mod n)`.

Here is an example of the RSA algorithm in action:

1. Choose `p = 61` and `q = 53`. Hence, `n = 61 * 53 = 3233`.
2. `K = lcm(60, 52) = 780`.
3. Suppose `e = 17` as `1 < e < K` and `e` and `K` are coprimes.
4. `d = 413`, the modulo multiplicative inverse of `17 (mod 780)`.
5. Suppose m = 65, then
    1. ciphertext, `c = 65^17 (mod 3233) = 2790`.
    2. on decryption, `m = 2790^413 (mod 3233)`.

### Implementation Details.

Define a **class Rsa** with an initial state comprising the numbers `p,q` and `n`, where `q = p + 1000`. The value in `p` will be provided when creating an instance of **class Rsa**. This class must have methods *encrypt* and *decrypt* to create a cipher text and to get the original message back. The *encrypt* and *decrypt* methods work with hash values of string messages. To this end, a one-way hash function must be defined in the **mymath** module, which returns the sum of ascii values of the corresponding characters in the string message. Further, all arithmetic operations required to implement the RSA algorithm should be defined as functions in the **mymath** module.

### Directory Structure

The **crypt/rsa.py** has the **class Rsa** definition. You should complete the method stubs in the class along with any other methods you deem necessary. The **mymath/mymath.py** has the function stubs of the necessary arithmetic operations you will need to implement the RSA. Complete the function stubs. You can add other functions that you deem necessary. The **tests** directory contains the tests to verify the correctness of your implementation. To run the tests, you will need the test runner **pytest**. With pytest you can run the tests using the following command `$ pytest part1/tests/`. Your goal is to pass all the tests.

## Part 2

The TODO Manager app.

### Problem Specification

The TODO list manager is a Python command line application that helps users manage their TODO lists. A user can do the following using this application:

#### Create a new task

A user can create a new task and add it to the TODO list. The new task must have an unique ID, a description, a priority to indicate its urgency, and status to denote whether the task is complete or yet to be completed.

#### Edit an existing task

A user can change specific properties of an existing task in the TODO list such as its description, priority, or status.

#### Remove tasks from the TODO list

A user can delete a task from the TODO list.

#### Display Tasks

A user can list all the tasks in the TODO list at any point.

#### Search Tasks

A user can search for tasks in the TODO list based on the task ID, description, priority or some combination of the three.

#### Sort Tasks

A user can list all tasks in the TODO list in increasing or decreasing order of priority.

### Implementation Details

Write a Python script called **main.py** which takes the following command line arguments from the user:

  1. *-h* or *--help* to print a help menu. Ignore additional arguments.

  2. *-l* or *--list* to list all tasks in the TODO list. Ignore additional arguments if present and print the list of all tasks. Each task must be printed in a new line and must have the form ID,DESCRIPTION,PRIORITY,STATUS.

  3. *-a* or *--add* \<TASK-DESCRIPTION\> \<PRIORITY\> to add a new task with a priority. \<TASK-DESCRIPTION\> is a string that describes the task. \<PRIORITY\> corresponds to bullet 4. The task ID is auto-generated. The user does not need to provide this.

  If the task is added to the TODO list then print the message 'Task added and assigned ID <NUMBER>'. If the priority number is not greater than 0 print the message 'Failed to add task'.

  Further, if \<PRIORITY\> is absent print the error message 'Error: Cannot add a task with empty priority'. If \<PRIORITY\> is is not an integer then print the message 'Priority must be integer'. If the expected \<PRIORITY\> option is not used then print the error message 'Error: Incorrect priority option'. If additional arguments are found print the error message 'Error: Found extraneous options'.

  4. *-p* or *--priority* \<NUMBER\> to assign a priority to a new task. \<NUMBER\> is an integer. This option must be used with options *-a* or *-s*.

  5. *-r* or *--remove* \<NUMBER\> remove a task with task ID \<NUMBER\>. If the task exists in TODO list and is successfully removed then print the message 'Removed task ID <NUMBER>', otherwise print 'Failed to remove task ID <NUMBER>'.

  Further, \<NUMBER\> must be an integer, otherwise print the message 'Task ID must be a number'. If \<NUMBER\> absent then print the message 'Task ID missing'. If additional arguments are found print the error message 'Error: Found extraneous options'.

  6. *-c* or *--complete* \<NUMBER\> set the status of a task with task ID \<NUMBER\> to "Complete". Print the message 'Task \<NUMBER\> completed' when this is done. If the task is not found then print the message 'Task \<NUMBER\> not completed'.

  Further, \<NUMBER\> must be an integer, otherwise print the message 'Task ID must be a number'. If \<NUMBER\> absent then print the message 'Task ID missing'. If additional arguments are found print the error message 'Error: Found extraneous options'.

  7. *-cp* or *--changepriority* \<TNUM\> \<PNUM\> change an existing task's (with ID \<TNUM\>) priority to \<PNUM\>. If the priority is changed then print the message 'Changed priority of task \<TNUM\> to \<PNUM\>'. If the task is not found or the priority is not greater than 0 then print the message 'Priority of task \<TNUM\> could not be changed'.

  Moreover, \<TNUM\> and \<PNUM\> must be integers. If \<TNUM\> is not an integer then print the message 'Task ID must be a number'. If \<PNUM\> is not an integer then print the message 'Priority must be a number'. If either of them are absent then print the message 'Task ID or priority missing'. If additional arguments are found print the error message 'Error: Found extraneous options'.

  8. *-u* or *--update* \<NUMBER\> \<DESCRIPTION\> update an existing task\'s description. If the task exists in the TODO list and the description is not empty then update the task and print the message 'Task \<NUMBER\> updated'; otherwise, print the message 'Failed to update task \<NUMBER\>'.

  Also, \<NUMBER\> must be an integer, otherwise print the message 'Task ID must be a number'. \<DESCRIPTION\> is a string to describe the task. If either option is missing print the message 'Task ID or description missing'. If additional arguments are found print the error message 'Error: Found extraneous options'.

  9. *-s* or *--search* \<CRITERIA\> search a task based a criteria. \<CRITERIA\> must be either \<ID\> or \<DESCRIPTION\> or \<PRIORITY\>, where \<ID\> is the option in bullet 12, \<DESCRIPTION\> is the option in bullet 13, and \<PRIORITY\> is the option in bullet 4. At least one search criteria must be present. A combination of any 2 of the 3 or all 3 search criteria is also allowed. If the task ID or the priority are not integers then print the message 'search ID and priority must be integer'. When searching by description, the task description should match exactly with the search parameter and should be case-insensitive. Ignore additional arguments.

  The list of tasks matching the search criteria should be displayed with each task in a new line. Each task must be of the form ID,DESCRIPTION,PRIORITY,STATUS.

  10. *-t* or *--sort* show sorted list of tasks by increasing order of priority. Each task must be of the form ID,DESCRIPTION,PRIORITY,STATUS and in a new line. Further, print the error message 'Error: Found extraneous options' if more than 2 arguments are given. If the argument after *-t* is not *-d* then print the tasks in increasing order.

  11. *-d* or *--desc* decreasing order. Must use with *-t*.

  12. *-i* or *--id* \<NUMBER\> task ID. Must use with *-s* for search task with ID.

  13. *-dp* or *--description* <TEXT> task description. Must use with *-s* for search task with description.

### Directory Structure

The file **part2/main.py** should read the arguments and call **parseArgs** in **parser/parse.py** to process the arguments. Based on the provided arguments the parser should execute the functions defined in **utils/commands.py**. The **db** directory contains a csv file **tasks.csv** to store the contents of the TODO list. The **tasks.csv** has a header ID,DESCRIPTION,PRIORITY,STATUS and tasks in the following lines. The **db/manager.py** defines functions to read/write the **tasks.csv** file. The **tests** directory contains the tests to verify the correctness of your implementation. To run the tests, you will need the test runner **pytest**. With pytest you can run the tests using the following command `$ pytest part2/tests/`. Your goal is to pass all the tests.

## Grading

If you pass all tests in *part1/tests/* and *part2/tests/*, you will get 50% of the credit. The remaining grade will be based on another set of tests with the same specs but different set of inputs.

Also, **note that you cannot use any library that is not specified in the README. If you do, you will not receive any credit for your submission.**
