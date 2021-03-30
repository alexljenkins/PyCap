---
title: Workflow - Unit Testing
description: This session will focus on how to utilise Pytest to write effective unit tests and we'll look at how to generate a code coverage report to ensure all your code has been tested
prev_know: None
skills:
  - Unit Tests
  - TDD
  - Code coverage

date: 08/03/2021
mentors: 
  - TimSando
  - ghandic
links:
  - '[Coursera follow along course](https://www.coursera.org/learn/python-data?specialization=python#syllabus){target=_blank}'
  - '[Pytest documentation](https://docs.pytest.org/en/stable/index.html){target=_blank}'
  - '[Pytest-cov documentation](https://pytest-cov.readthedocs.io/en/latest/){target=_blank}'

---

{{ course_summary(title, date, description=description, prev_know=prev_know, skills=skills, mentors=mentors, links=links) }}

## What is test driven development?

Test driven development is a software development methodology that requires a developer to convert requirements into unit tests before the code has actually been completed and iteratively test written code against these unit tests to ensure it meets expectations. This approach to software development ensures a developer is building code that actively addresses requirements from the client or product owner and gives everyone involved in the development life cycle confidence in what is being built. Test driven development is in contrast to writing unit tests at the end of the development life cycle where original requirements/scenarios may accidentally fall through the cracks and be forgotten, which can result in more bugs appearing in the code and the product not performing to expectations.

## What are Unit Tests?

When you write a piece of code, you consider all the ways the code might fail (incorrect data, format of the incoming data is wrong, people submitting silly values etc.) and you build your code to handle them. Unit tests are a way to guarantee your code works in the way you expect and handles these edge cases/possible exceptions gracefully by passing in different parameters to each function and checking the output is what is expected.

## Why Unit Tests?

Unit tests are implemented to give you confidence that when your code is pushed to production or other people are using your code, it's functioning correctly. It also allows other people to verify that you're code is functioning as expected without an in-depth understanding of the code itself. As your program develops, unit tests allow you to keep track of any changes in upstream or systems that may be sending different information and ensure that any changes maintain the integrity and functioning of the program. As such, unit tests are important for pull requests and code reviews when you've modified code and want to merge it back into the main development branch. It shows the person undertaking the code review that what you've written doesn't break the existing code/unit tests, and you can show that you've written new unit tests to cover the functions you've developed or changes you've made.

Another benefit to unit testing your code is that when someone else picks up your code, they can determine what each function should be expecting and what it should return. This helps other developers understand your code and allows them to improve and build upon what you've designed and developed which is a core component of open source development.

## Installing, importing and using Pytest

Now we know what unit tests are and why we use them, how do we actually design them for a Python program?

The most common library used for python unit tests is called Pytest. This can be installed using pip in your terminal:

```bash
# When python3 is the only version installed
pip install pytest
```

```bash
# When multiple versions of python are installed
pip3 install pytest
```

Pytest can then be imported into a python file by simply calling:

```python
import pytest
```

Pytest can then be called using the command line where it will iterate through all files within the current directory and sub-directories to find files that start with "test_" and then any functions within those files that begin with "test_" i.e **test_process.py** for a file or **test_check_status** for a function.

```bash
pytest
```

## Writing Pytest unit tests

Simple pytest unit tests are functions that call specific portions of your code, pass in defined variables and then check the output, verifying it's what should be expected. 

Lets define a simple function that we want to test that has an input and an output.

```python
# Define a simple function
def check_status(status):
  if status == "Red":
    check = True
  else:
    check = False
  return check
```

And now we want to define a unit test that will check that it's functioning correctly.

```python
# If the function as in another file, we'd need to import it first
from file import check_status

def test_check_status():
  status = "Red"
  result = check_status(status)
  assert result == True
```

If we look at the above function, we're defining a variable (status = "Red"), calling the function we want to test (result = check_status(status)) and then we're using a new concept "assert" to check the output of the function. Assert is an inbuilt python keyword that tests whether a statement is True and if not, returns an AssertionError. If we're running Pytest and the statement we're asserting isn't True, it will fail the test. In our case however, this particular unit test will always return true unless the check_status function is changed.

The assert statement can be used to check any statement. Some examples of statements that will pass are:

```python
assert 10/5 == 2
# Check whether a math function is returning the correct value

word = "Syd"
assert word in "Sydney"
# Check whether a string contains a substring
```

Some examples of statements that will fail are:

```python
# Check whether a particular value is an integer
value = 10.5
assert isinstance(value, int)

score = "Blue"
assert "Red" == "Blue"
```

## Passing in multiple variables to a unit test

The above example was just passing in a single variable to our function, but what if we want to pass in multiple variables or run multiple tests on the same function but tweak each variable? We can use '[Pytest parametrization](https://docs.pytest.org/en/stable/parametrize.html){target=_blank}' to test our original function.

```python
import pytest

@pytest.mark.parametrize("status, expected", [("Red", True), ("Blue", False), ("Green", False), ("red", False)])
def test_check_status_multiple_variables(status, expected):
  result = check_status(status)
  assert result == expected
```

In this example we're using the parametrize decorator to define our 2 variables that we want to pass into our unit test, status and expected. We're then setting 4 different values for status and what is the expected value coming back from our function that is being tested. Because we've used the parametrize decorator, this lets Pytest know that we want to run the unit test with each of those sets of variables to validate our function.

## Checking for exceptions

We don't only want to check whether a particular function will operate perfectly, but often we want to check that our code handles errors and bad variables in the right way by raising the correct exceptions. If we change our original function to raise an exception when the incorrect value is provided:

```python
def check_status(status):
  assert status == "Red":
    check = True
  else:
    raise ValueError
    # ValueError is a built-in python exception raised when the type is correct but the value itself isn't.
  return check
```

Then we can do that our function will raise the right exception through pytest by using pytest.raises.

```python
@pytest.mark.parametrize("status, expected", [("Red", True), ("Blue", False), ("Green", False), ("red", False)])
def test_check_status_exception(status, expected):
  if expected == True:
    result = check_status(status)
    assert result == expected
  else:
    with pytest.raises(ValueError):
      result = check_status(status)
```

In this function, we're still passing in all our variables and whether we expect them to fail or not, but we're not only checking a True or False statement, we're also checking that a particular exception is being raised when it should be (ValueError).

To summarise, if unit tests are written correctly then we can check our functions and verify if they're working and we have a number of tools within Pytest at our disposal to successfully achieve this. More detailed information and examples can be found in the pytest documentation linked at the top of the page. The next step is to generate coverage reports to ensure we have written tests for all of our code.

## Code coverage reports

Pytest-cov is a nice library that can be used for generating coverage reports, integrates with pytest and can be installed using pip.

```bash
pip3 install pytest-cov
```

You can then call:

```bash
pytest --cov=myproject
```

(where myproject is the name of the directory that you want to run the coverage report and pytest on) and it will go through and generate a coverage report in the terminal and summarise what % code is being tested by all our unit tests. If we want to save this out to an html file that can be referenced later or uploaded somewhere, we can pass in:

```bash
pytest --cov=myproject --cov-report html
```

We have included a bash script in each of our capstone repos which you can run to generate a code coverage report. This script will also check the type annotation coverage and docstring coverage which we'll cover in the next section.
