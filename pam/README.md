## Grade

1. Student submission(s).

You need a file that lists all directories containing student
submissions.  The demo contains seven "student" submissions, from
students named *correct*, *errors*, *failures*, *infloop*,
*outofstack*, *pep8fail*, and *syntax* (see directory
[examples/submissions](./examples/submissions)). Each submission in
our example is in a folder named *A1*.  Therefore, you need the file
(see [directories.txt](./examples/directories.txt)) with
the following contents:

`pam/examples/submissions/correct/A1`  
`pam/examples/submissions/errors/A1`  
`pam/examples/submissions/failures/A1`  
`pam/examples/submissions/infloop/A1`  
`pam/examples/submissions/outofstack/A1`  
`pam/examples/submissions/pep8fail/A1`  
`pam/examples/submissions/syntax/A1`  

Notice that all paths are relative to the location of [test_runner.py](../test_runner.py).

2. Test file(s).

You need unittest test file(s) that will be used to test the student
submissions.

See [examples/test_asst.py](./examples/test_asst.py) and
    [examples/test_2_asst.py](./examples/test_2_asst.py).

Look carefully at the way you need to import student files in your
unittest files: see [test_asst.py](./examples/test_asst.py) and/or
[test_2_asst.py](./examples/test_2_asst.py).


3. Configure test_runner.py.

You need a configuration file. See [examples/config.py](./examples/config.py).


4. Finally,

`python3 test_runner.py path/to/configfile`

If everything went well, you should have a .json file in each student
submission directory.


## Aggregate


1. Student information.

You need a classlist (see [students.csv](./examples/students.csv)) in
the following format:

`student-id,first-name,last-name,student-number,email`

TIP: if you are at UofT, you can get this list from
Quercus/Intranet/your-dept-sysadmin.

2. Group information.

If your students were working in groups and submitted one solution per
group, then you need a file that records this information. It should
be in the format (see [groups.txt](./examples/groups.txt)):

`group-name,dir-name,student-id-1,student-id-2,...`

Actually, even if your students were working individually, you still
need this file. In other words, we assume that students *always* work
in groups. When they work individually, the group size is 1, and you
have a group per student.

TIP: If you are using MarkUs, you can download this file from your
MarkUs web interface.

3. Name matching.

You need a file that matches submission directories with group
names. See [dirs_and_names.txt](./examples/dirs_and_names.txt) for an
example.

4. Finally,

`python3 aggregator.py A1 pam/examples/dirs_and_names.txt pam/examples/students.csv pam/examples/groups.txt`

See
  `python3 aggregator.py --help`
for more options and full documentation.

If all went well, you should have a file `aggregated.json` that contains
full results of running all tests on all student submissions.


##  Format.

JSONs are great, but we want good looking summaries.

1. In the configuration file, specify where your templates are. See
sample [config.py](./examples/config.py).

The templates we currently provide are: HTML (aggregate), txt (both
individual and aggregate), markus that contains a csv grades table
(aggregate), and a .gf file (aggregate). We are working on many more.

You are welcome to contribute your own templates!

2. Some examples:

`python3 templator.py aggregated.json html`  
`python3 templator.py aggregated.json txt`  
`python3 templator.py aggregated.json markus`  

See 
  `python3 templator.py --help`
for full information and more options.


## Support

Please send comments, feedback and bugs to
[anya@cs.utoronto.ca](mailto:anya@cs.utoronto.ca). Currently, there is
very limited support provided. We hope to improve.
