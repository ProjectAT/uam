GRADE (relative paths)
===

Introduction
---
These instructions pertain to the example contained in `example_reldir`. The instructions here remove the need to place a `config.py` file in uam's directory. This has the benefit of enabling quickly running different sets of tests; it also allows the installation of uam in a read-only directory. Furthermore, this set of examples removes the fragility of unittest configurations being filesystem-location dependent. This means that sets of unittests are self-contained units and can be shared (e.g., via `git`) without modifying the associated `config.py`.

Grading Instructions
---
1. Student submission(s).

   You need a file that lists all directories containing student submissions.  The demo contains seven "student" submissions, from students "correct", "errors", "failures", "infloop", "outofstack",
"pep8fail", and "syntax" (see directory `pam/example_reldir/submissions`). Each submission in our example is in a folder named `A1`.  Therefore, for this example, `directories.txt` must contain the following:

   ```
    submissions/correct/A1
    submissions/errors/A1
    submissions/failures/A1
    submissions/infloop/A1
    submissions/outofstack/A1
    submissions/pep8fail/A1
    submissions/syntax/A1
   ```
   Notice that all paths are relative to the location of `config.py`.

2. Test file(s).

   You need unittest test file(s) that will be used to test the student submissions.
   
   See `test_asst.py` and `test_2_asst.py` in the `example_reldir` directory.

   Look carefully at the way you need to import student files in your unittest files: see `test_asst.py` and/or `test_2_asst.py`.

   You are free to put these files in a location of your choice.

3. Configure `test_runner.py`.

   See `example_reldir/config.py`.

4. Finally, run

    `PYTHONPATH=. python3 path/to/test_runner.py`

   The absolute path of `test_runner.py` is not required if it is in your path. If everything went well, you should have a `.json` file in each student submission directory.


Result aggregation instructions
---
After running tests, it is sometimes helpful to combine results into a single file. This section on result aggregation demonstrates how uam can aggregate the results of test that were run.

1. Student information.

   You need a classlist (see `students.csv`) in the following format:

        student-id,first-name,last-name,student-number,email

   TIP: if you are at the University of Toronto, you can get this list from [Blackboard](https://portal.utoronto.ca).

2. Group information.

   If your students were working in groups and submitted one solution per group, then you need a file that records this information. It should be in the format (see `groups.txt`):

        group-name,dir-name,student-id-1,student-id-2,...

   Actually, even if your students were working individually, you still need this file. In other words, we assume that students ALWAYS work in groups. When they work individually, the group size is 1, and you have a group per student.

   TIP: If you are using [MarkUs](https://github.com/MarkUsProject/Markus), you can download this file from your MarkUs web interface.

3. Name matching.

   You need a file that matches submission directories with group
names. See `dirs_and_names.txt` for an example.

4. Finally, for the grading of `A1`, run

        path/to/aggregator.py A1 path/to/dirs_and_names.txt path/to/students.csv path/to/groups.txt

   If all went well, you should have a file named `aggregated.json` that contains
full results of running all tests on all student submissions. For more options, run

        path/to/aggregator.py --help
    

Format
---

JSONs are great, but we want good looking summaries.

1. In the `config.py` file, specify where your templates are. See sample `config.py`.

   The templates we currectly provide are

     * HTML (aggregate)
     * txt (both individual and aggregate),
     * markus that contains a csv grades table (aggregate), and
     * a .gf file (aggregate).

   You are welcome to contribute your own templates, or to request us to
produce some!

2. Some examples:

   ```
   python3 templator.py aggregated.json html 
   python3 templator.py aggregated.json txt
   python3 templator.py aggregated.json markus
   ```

   For more options, run

        python3 templator.py --help

Support
---

Please send comments, feedback and bugs to [anya@cs.utoronto.ca](mailto:anya@cs.toronto.edu).
