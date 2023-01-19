# Homework Assignment 2

## Learning Outcomes

After completion of this assignment, you should be able to:

- work with regular expressions in Python.

- automate basic file management tasks in Python.

- analyze datasets using Python libraries NumPy and Pandas.

## Getting Started

To complete this homework assignment, you will need [Python3.8](https://www.python.org/downloads/) and above and the testing framework [pytest](https://docs.pytest.org/en/7.1.x/getting-started.html). If you still do not have them configured (highly unlikely), then do homework 0 and come back here. You can use any test editor or IDE (e.g., Pycharm) to write your python code.

Download or clone this repository to your local system using the following command:

`$ git clone <ssh-link>`

After you clone, you will see a directory of the form *cise337-hw2-python-application-\<username\>*, where *username* is your GitHub username.

In this directory, you will find a sub-directory *src* with the following files:

- **numsAnalyzer.py**
- **movieAnalyzer.py**
- **rename_files.py**

Your job is to complete the function definitions in these files.

The *tests/* directory has three test files, which are currently empty. Fill these files with tests for the corresponding parts. The tests should be executable from the repository's root directory using pytest.

You cannot use any additional modules other than the ones already imported in the *src* files. You are allowed to use additional modules in the *tests* files.

Install [NumPy](https://numpy.org/install/) and [Pandas](https://pandas.pydata.org/docs/getting_started/install.html) if you don't already have them.

## Problem Specification

### Part 1 -- Analyze NumPy Arrays

Define functions in the file *src/numsAnalyzer.py* to analyze numpy arrays.

#### Count Missing Values

Define a function **countMissingValues(x, k)** to count the missing values in a NumPy array. Parameter `x` is a N-dimensional numpy array and `k` is an integer. The default value of `k` is `0`. The function should return a numpy array containing the number of `Nan` values in `x` along axis `k`. For example, if `x` is a 2D array of shape *(4,5)* as shown below and `k=0`, then the function should return the numpy array `[0 2 0 3 0]` since column 1 has no NaN values, column 2 has 2 NaN values, column 3 has no NaN values, column 4 has 3 NaN values, and column 5 has no NaN values.

```
array[
  [100.0, 87.3, 94.5, 99.0, 78.4],
  [82.6, 71.3, 99.9, np.NaN, 48.0],
  [92.6, np.NaN, 43.5, np.NaN, 80.0],
  [97.0, np.NaN, 98.5, np.NaN, 65.3]
]
```

However, if `k=1` then it should return the numpy array `[0 1 2 2]` since `k=1` indicates the row axis. If `k` is an invalid axis or is not an int then the function should raise a *ValueError*. Parameter `k` can be a negative integer. A negative axis is the reverse of a positive axis. For example, in a 2D array, the axis 0 is the same as the axis -2 and the axis 1 is the same as the axis -1.

Note `x` can be more than 2 dimensions. Suppose `x` is a 3 dimensional array of shape *(2,2,5)* as follows

```
[
  [[100.0, 87.3, 94.5, 99.0, 78.4],[82.6, 71.3, 99.9, np.NaN, 48.0]],
  [[92.6, np.NaN, 43.5, np.NaN, 80.0],[97.0, np.NaN, 98.5, np.NaN, 65.3]]
]
```      

In this case, the function should return the numpy array `[[0 1 0 1 0] [0 1 0 2 0]]` if the axis `k = 0`. If `k = 1`, then the number of `Nan` values along axis 1 is the numpy array `[[0 0 0 1 0] [0 2 0 2 0]]`. If the axis is 2, then the number of `Nan` values along axis 2 is the numpy array `[[0 1][2 2]]`.

#### Analyze Test Scores

Suppose that we have a *two-dimensional `M X N` matrix*, where a row indicates the final exam score of all students in a semester. Following is an example:

```
100.0, 87.3, 94.5, 99.0, 78.4
82.6, 71.3, 99.9, NaN, 48.0
92.6, NaN, 43.5, NaN, 80.0
97.0, NaN, 98.5, NaN, 65.3
```

In the example, the 4 X 5 2D array captures the final test scores of 5 students in 4 semesters.

Assume that a final test score is of type float and must be in the interval [0.0, 100.0] (inclusive). However, it can also be a `NaN` to account for students who did not take the test.

Also, assume that the `M X N` matrix is a two-dimensional numpy array of `dtype` float.

Define a function **exams_with_median_gt_K(x, k)** to determine the number of semesters where the median test score was higher than a certain `k`. The parameter `x` is a 2D numpy array of shape *(M, N)*, same as the example outlined above. The parameter `k` is an integer that indicates a threshold median test score. The function should return the number of rows in `x` with a median greater than `k`. For example, if `x` is the array outlined above and `k`is 70, then the function should return 2 since there are only two semesters/rows in which the median test score is above 70. Note `Nan` values in the array should be treated as 0s. Raise a *ValueError* exception if `k` is negative or is greater than 100. Also raise a *ValueError* if `x` has negative numbers or numbers greater than 100. Further, raise a TypeError if `k` is not an integer.

Define a function **curve_low_scoring_exams(x, k)** to curve the final scores in a semester if the average final score in that semester is less than a threshold `k`. *A curved test score in a semester is obtained by subtracting the highest test score in that semester from 100 and adding the difference to each test score in that semester*. The parameter `x` is a 2D numpy array of shape *(M, N)*. The parameter `k` is an integer that indicates a threshold average test score. Raise a *ValueError* exception if `k` is negative or is greater than 100. Also raise a *ValueError* if `x` has negative numbers or numbers greater than 100. The function should return a modified `x`, where `x` is sorted in increasing order of the average test score in a semester and each test score in a semester with average test score less than `k` should be curved. The scores should be rounded up to a precision of 1 decimal digit (e.g., 93.483 should be 98.5). For example, if `k = 95` and `x`:

```
100.0, 87.3, 94.5, 99.0, 78.4
82.6, 71.3, 99.9, NaN, 48.0
92.6, NaN, 43.5, NaN, 80.0
97.0, NaN, 98.5, NaN, 65.3
```

then the function should return:

```
100.0, 7.4, 50.9, 7.4, 87.4
98.5, 1.5, 100.0, 1.5, 66.8
82.7, 71.4, 100.0, 0.1, 48.1
100.0, 87.3, 94.5, 99.0, 78.4
```

Note the following in this example:
1. The numpy array returned is sorted in increasing order of the average test scores.
2. In the array that was returned, all semesters with average test score less than 95 have curved test scores.
3. `Nan` values are treated as 0s.

### Part 2 -- Analyze with Pandas

Define functions using Pandas in the file *src/movieAnalyzer.py* to analyze a dataset containing information about the highly rated movies of all time `(src/data/Top_200_Movies.csv)`. The file *src/movieAnalyzer.py*, already has the function **get_movies_data()**. It returns a DataFrame with all the contents in the `csv` file.

Define a function **get_movies_interval(y1, y2)** to find all movies that were released between years `y1` and `y2` (inclusive). The function should return a `Series` object with movie names as the values and the indices of the movies in the dataframe from **get_movies_data()** as the indices in the `Series` object. Raise a `ValueError` if `y1 < y2`. If no movies are found in the given interval then return an empty Series. For example, **get_movies_interval(1992, 1993)** should return the following `Series` object:

```
5               Schindler's List
88                Reservoir Dogs
131                   Unforgiven
141                Jurassic Park
177    In the Name of the Father
205                Groundhog Day
Name: Title, dtype: object
```
Note the indices are the same as the indices of the movies in the DataFrame constructed from the csv file.

Define a function **get_rating_popularity_stats(index, type)** to calculate descriptive statistics of the rating and popularity index of all movies in the dataset. The parameter *index* should be *"Rating"* or *"Popularity Index"*. The parameter *type* can be one of the following strings:
- *"count"*. Total number of movies for an index.
- *"mean"*. Average of all movies for an index.
- *"median"*. Median of all movies for an index.
- *"min"*. The lowest movie for an index.
- *"max"*. The highest movie for an index.
The function returns a string formatted to two decimal places based on the index and type provided as arguments. For example, **get_rating_popularity_stats('Popularity Index', 'mean')** should return '1091.92' since the average popularity index of the top movies of all time is 1091.92. If an unexpected *index* and *type* is provided as argument then return the error message 'Invalid index or type'.   

Define a function **get_actor_movies_release_year_range(actor, upper, lower)** to determine all movies of an actor that released in a year interval *[lower, upper]* (inclusive). The parameter *actor* is an actor's name of type string, the parameters *upper* and *lower* are integers and indicate the upper and lower bounds of the year interval, respectively. The default value of *lower* is 0. Raise a *ValueError* if the interval is invalid, i.e., *lower* > *upper*. The function should return a `Series` object with the movie names as indices and the year of release as the values. If an actor did not have a movie released in a year interval then it should return an empty Series. For example, **get_actor_movies_release_year_range('Leonardo DiCaprio', 2022, 2010)** should return the following series:

```
Inception                  2010
Django Unchained           2012
The Wolf of Wall Street    2013
Shutter Island             2010
dtype: int64
```    
If an actor is not found in the csv file then return an empty Series.

Define a function **get_actor_median_rating(actor)** to calculate the median rating of all the movies by an actor. The parameter *actor* is an actor's name of type string. Raise a *ValueError* if *actor* is an empty string. Raise a *TypeError* if *actor* is a non-string. The function should return the median rating of type float. If an actor does not exist in the dataset then the function should return `None`.

Define a function **get_directors_median_reviews()** to calculate the median reviews (in million) of all movies grouped by the director of that movie. The function should return a `Series` object where the director name is an index and median reviews (in million) is the value. For example, for the given dataset, the function should return the following:

```
Director
Aamir Khan           0.190
Akira Kurosawa       0.124
Alfred Hitchcock     0.397
Andrew Stanton       1.050
Anthony Russo        1.050
                     ...  
Tony Kaye            1.100
Victor Fleming       0.353
Wes Anderson         0.790
William Wyler        0.237
Wolfgang Petersen    0.248
```

Note that the indices are director names and the values are the median reviews in million. For example, the director Aamir Khan has 0.19 million reviews.

### Part 3 -- Renaming Files

Define function in the file *src/rename_files.py* to rename files that match a pattern in a given directory.

Consider a directory with thousands of files and directories. Many of the files in the directory have names with the prefix `snap` followed by *exactly three digits* and end with the extension `.txt`. However, while inspecting the file names with the aforementioned pattern, we find that there are gaps. For example, the directory has `snap001.txt` and `snap003.txt` but no `snap002.txt`.

Define a function `rename(path)` that takes the path (type string) to a directory and renames all the snap files in the directory such that there are no gaps in the numbering of the snap files. For example, if the directory (passed as argument) has *snap001.txt*, *snap002.txt*, *snap004.txt*, and *snap005.txt*, then *snap001.txt* and *snap002.txt* should remain unchanged. However, *snap004.txt* should be renamed to *snap003.txt* and *snap005.txt* to *snap004.txt*.

The directory could have other files and folders that do not have the desired pattern in their names. The names of such files and directories should be preserved. For example, if the directory (passed as argument) has *snap001.txt*, *snap002.txt*, *snp003.jpg*, *snap004.txt*, and *snap005.txt*. then the directory should have the files snap001.txt, snap002.txt, snap003.txt, snap004.txt, and snp003.jpg.

The directory can have subdirectories. All files in the subdirectories including the subdirectory name should remain unchanged.

## Testing and Coverage

You are expected to write automated tests to verify the correctness of the scripts in *src*. The *tests* directory has three test scripts. The *tests/numsAnalyzer_test.py* should have tests for the *src/numsAnalyzer.py* script. The *tests/movieAnalyzer_test.py* should have tests for the *src/movieAnalyzer.py* script. The *tests/rename_file_test.py* should have tests for the *src/rename_files.py* script. The test scripts should be executed from the repository's root directory.

At the very least, your *src* scripts should pass all the tests defined by you. However, even if all your tests pass, that does not mean that the tests comprehensively verify all statements in your code. One way to measure this is to determine [code coverage](https://en.wikipedia.org/wiki/Code_coverage). Code coverage tells us what percentage of our code is executed by our tests. Ideally, this should be close to 100\%, which means that are tests execute all statements in our code. Use Pytest coverage to measure your tests' coverage. Read the documentation at https://pytest-cov.readthedocs.io/en/latest/index.html to install the package and its usage. One of the most common commands to measure coverage and determine which statements are not executed by the tests is:

`$ pytest --cov-report term-missing --cov=src tests/`

You should run this command from the repository's root. Also, you should run all tests from the repository's root as well using the command:

`$ pytest tests/`

## Submission instructions

Submit code to your GitHub repository as many times as you want till the deadline. After the deadline, any code you try to submit will be rejected. To submit a file to the remote repository, you first need to add it to the local git repository in your system, that is, directory where you cloned the remote repository initially. Use following commands from your terminal:

`$ cd /path/to/cise337-hw2-python-application-<username>` (skip if you are already in this directory)

`$ git add src/`

`$ git add tests/`

To submit your work to the remote GitHub repository, you will need to commit the file (with a message) and push the file to the repository. Use the following commands:

`$ git commit -m "<your-custom-message>"`

`$ git push`

**Submit your GitHub username to Brightspace under Assignment 2 as a comment**. Without this your work may not be graded.

## Grading

You are expected to write the implementation and test scripts to verify the correctness of your implementations. You will earn 25\% of the credit, if your implementations passes all checks w.r.t to the tests you defined. You will earn an additional 25\% if your tests have a coverage of 95\% or more. The remaining 50\% will be based on the graders' tests. You will get credit for each passing test.

**Do not change or remove data/Top_200_Movies.csv**

**Remember to submit your GitHub username to Brightspace under Assignment 2 as a comment**. Without this your work may not be graded.

## References

Some useful links:

- NumPy API Reference: https://numpy.org/doc/stable/reference/index.html
- Pandas API Reference: https://pandas.pydata.org/docs/reference/index.html
- `pytest` API Reference: https://docs.pytest.org/en/7.1.x/reference/reference.html
- `shutil` reference: https://docs.python.org/3/library/shutil.html
- `os` API reference: https://docs.python.org/3/library/os.html
- `re` API reference: https://docs.python.org/3/library/re.html
