## Compile JAM

 Make sure [compile_jam.sh](./compile_jam.sh) is executable. Then:

`./compile_jam.sh`

 You only need to do this once.


## Grade

1. Student submissions.

You need a file that lists all directories containing student
submissions.  The directory [examples](./examples) contains six
"student" submissions, from students *correct*, *failures*, *infloop*,
*nosubmissions*, *nullpointer*, and *syntax* (see directory
[examples/submissions](./examples/submissions)). Each submission is in
a folder named A1.  Therefore, you need the file (see
[directories.txt](./examples/directories.txt)) with the following
contents:

`jam/examples/submissions/correct/A1`  
`jam/examples/submissions/failures/A1`  
`jam/examples/submissions/infloop/A1`  
`jam/examples/submissions/nosubmission/A1`  
`jam/examples/submissions/nullpointer/A1`  
`jam/examples/submissions/syntax/A1`  


Note that all paths are relative to the location of
[test_runner.py](../test_runner.py).


2. Test file(s).

You need your JAM test files for testing each individual submission.
You also may need additional files to run your tests (for example,
starter files you distributed to students and instructed them to not
modify them).

**Requirements** for the test files:

Starting with your "normal" JUnit4 test file, you create a JAM test
file as follows:

`import edu.toronto.cs.jam.annotations.Description;`

For each @Test method, use the following annotations:

`@Test(timeout=XXX)`  
`@Description(description="description of your test method")`  


The directory [examples/tests](./examples/tests) contains a sample
test suit for A1.

3. Configure test_runner.py.

You need a configuration file. See
[examples/config.py](./examples/config.py).

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

`python3 aggregator.py A1 jam/examples/dirs_and_names.txt jam/examples/students.csv jam/examples/groups.txt`

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
