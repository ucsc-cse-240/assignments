# Assignments
These are the assignments for CSE240 at UCSC.  They are:
- [Assignment1](Assignment1/)
- [Assignment2](Assignment2/) 
- [Assignment3](Assignment3/)
- [Assignment4](Assignment4/)
- [Assignment5](Assignment5/)
  
# Installing the Autograder package
Install the autograder with `pip3 install autograder-py` on the command line.  

# Submitting and using the Autograder in CSE 240

Make sure that the autograder is installed on your local machine by
typing: `python3 -m autograder.cli`.  If you see the `--help` option:

```nil
python -m autograder.cli
The autograder CLI package contains several tools for interacting with the autograder.
The following is a non-exhaustive list of CLI tools.
Invoke each command with the `--help` option for more details.
```
## Using the autograder

The autograder command line interface (cli) is [documented](https://github.com/eriq-augustine/autograder-py).  As a
student in the class, the main commands you will use are:

-   `python3 -m autograder.run.submit`: this will submit an assignment
    for a particular class and assignment.
-   `python3 -m autograder.run.peek`: this will show you your last submission
-   `python3 -m autograder.run.history`: this will show a summary of all
    your past submission
