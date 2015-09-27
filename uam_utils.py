""" Utilities for UAM.
"""
import sys
import os
import datetime

EXCLUDED_TESTS = ['unittest.loader.ModuleImportFailure']

class Student:
    """ A representation of a student.
    """

    def __init__(self, line):
        """ Instantiate this Student from a line in BlackBoard generated
        student file:
         student_id,first,last,student_number,email

        """

        [self.student_id, self.first, self.last,
         self.student_number, self.email] = line.strip().split(',')
        self.student_number = self.student_number.zfill(10)

        # used to determine a single student-to-group relationship
        self.in_groups = []

        self.source, self.section = 'N/A', 'N/A'

    def to_json(self):
        """ Return a dictionary of this Student to be injected into a
        TestResult JSON string.

        """

        return {'student_id': self.student_id, 'first': self.first, 'last':
                self.last, 'student_number': self.student_number.zfill(10),
                'section': self.section, 'source': self.source, 'email':
                self.email}

    def __str__(self):
        return ','.join([self.student_id, self.first, self.last,
                         self.student_number, self.email])


class Students:
    """ A collection of Students.
    """

    def __init__(self, student_file=None):
        """ Initialize Students.
        Raises FileNotFoundError is student_file cannot be opened.
        """

        self._students = {}
        if student_file is not None:
            self.load_students(student_file)

    def load_students(self, student_file):
        """ Given student_file, a path to a file in the format
            student_id,first,last,student_number,email
        load all Students in this file into this Students.
        Raises FileNotFoundError is student_file cannot be opened.
        """

        for line in open(student_file):
            try:
                student = Student(line)
                self._students[student.student_id] = student
            except ValueError:
                print('Warning: could not create Student from %s' % line,
                      file=sys.stderr)
                continue

    def get(self, student_id):
        """ Return a Student with the given student_id, or None if no such Student.
        """

        return self._students.get(student_id)

    def add(self, student):
        """ Add a given Student. Complain on stderr yet proceed if a Student
        with student's student_id already exists.
        """

        if student.student_id in self._students:
            print('Warning: %s is an existing student. ' +
                  'Adding/updating its record.' % student.student_id)
        self._students[student.student_id] = student

    def __iter__(self):
        return iter(self._students)

    def __str__(self):
        return '\n'.join([str(student) for student in self._students.values()])


class Group:
    """ A representation of a Group containing Students working together on
    an assignment to be graded. These groups are synonymous to the
    groups on MarkUs.
    """

    def __init__(self, group_id, repo_name=None, students=None):
        """ Instantiate this Group with the given group_id, and associate the
        given list of Students, students, with this Group.
        """

        self.group_id = group_id
        self.repo_name = repo_name
        if students is None:
            self.students = []
        else:
            self.students = students

    def add(self, student):
        """ Add Student student to this Group.
        """

        self.students.append(student)

    def __str__(self):
        return (self.group_id + ',' + self.repo_name + ': ' +
                ';'.join(list(map(str, self.students))))


class Groups:
    """ A collection of Student Groups.
    """

    def __init__(self, group_file=None, students=None):
        """ Raises FileNotFoundError is student_file cannot be opened.
        """

        self._groups = {}
        if group_file is not None:
            self.load_groups(group_file, students)

    def load_groups(self, group_file, students):
        """Load all Groups from group_file, a path to a file in the format
          group_id,repo_name,student_id1,...
        and Students students.
        Raises FileNotFoundError is student_file cannot be opened.
        """

        for line in open(group_file):
            try:
                splt = line.strip().split(',')
                group_id, repo_name, student_ids = splt[0], splt[1], splt[2:]
                group = Group(group_id, repo_name)
                for student_id in student_ids:
                    if student_id in students:
                        student = students.get(student_id)

                        # warn if student belongs in another group
                        if student.in_groups:
                            print('Warning: %s already belongs to groups: %s' %
                                (student_id, 
                                    ', '.join(student.in_groups)
                                ), file=sys.stderr)
                        student.in_groups.append(group_id)
                        group.add(student)
                    else:
                        print(('Warning: no record of student %s. ' +
                               'Omitting from group.') % student_id)
                self._groups[group_id] = group
            except ValueError as error:
                print(('Warning: could not process line %s. %s' %
                       (line, error)),
                      file=sys.stderr)
                continue

    def add(self, group):
        """ Add a given Group. Complain on stderr yet proceed if a Group with
        group's group_id already exists.
        """

        if group.group_id in self._groups:
            print('Warning: %s is an existing group. ' +
                  'Adding/updating its students.' % group.group_id)
        self._groups[group.group_id] = group

    def get(self, group_id):
        """ Return a Group with group_id, or None if it doesn't exixt.
        """

        return self._groups.get(group_id)

    def by_repo_name(self):
        """ Return a dict of this Groups' object Groups, by repo_name.
        """

        groups = {}
        for group in self._groups.values():
            groups[group.repo_name] = group
        return groups

    def __iter__(self):
        return iter(self._groups)

    def __str__(self):
        return '\n'.join(str(grp) for grp in self._groups.values())

class Report:
    ''' A representation of a Report in UAM.
    '''

    def __init__(self, results, students, assignment, origin, date=None):
        ''' (Report, dict of str:dict, list of Student, str, datetime.datetime)
            -> NoneType
        Creates a Report with results (a dict of TestCase names: dict of
        passes, failures, and errors: all dicts of TestCase method names
        -- essentially the format used in individual json result files),
        students, and the assignment name. If date is not provided,
        then the current time is assumed.
        '''

        self.results, self.students, self.assignment, self.origin = (
            results, students, assignment, origin
        )

        self.date = date if date else datetime.datetime.now()

    def to_json(self):
        ''' (Report) -> dict
        Returns a dict representing this Report.
        '''

        return {
            'students': [student.to_json() for student in self.students],
            'results': self.results,
            'date': self.date,
            'origin': self.origin,
            'assignment': self.assignment
        }

    @staticmethod
    def from_json(json):
        ''' (dict) -> Report
        Creates a Report from a json dict containing a Report.
        '''

        return Report(
            json['results'],
            [
                Student(
                    ','.join([
                        student['student_id'],
                        student['first'],
                        student['last'],
                        student['student_number'],
                        student['email']
                    ])
                ) for student in json['students']
            ],
            json['assignment'],
            json['origin'],
            json['date']
        )

    def get_test_passes(self, test_name):
        ''' (Report, str) -> int
        Get the number of passes for the given TestCase name test_name.
        '''

        try:
            return len(self.results[test_name]['passes'])
        except KeyError:
            return 0

    def get_total_passes(self):
        ''' (Report) -> int
        Get the total number of passes in all TestCases in this Report.
        '''

        return sum([
            self.get_test_passes(test_name)
            for test_name
            in self.get_test_names()
        ])

    def get_test_names(self):
        ''' (Report) -> list of str
        Gets a list of all the TestCase names in this Report.
        '''

        return list(self.results.keys())

    def get_students(self):
        ''' (Report) -> list of Student
        Gets a list of all Students in this Report.
        '''

        return self.students

    def get_group(self):
        ''' (Report) -> str
        Gets the group name for this Report.
        '''

        # TODO: hacky, relies on the structure of origin which can change
        return self.origin.split(os.sep)[-2]

class Reports:
    ''' A collection of Reports.
    '''

    def __init__(self, name, test_methods=None, reports=None, date=None):
        ''' (Reports, str, list of str, list of Report, datetime.datetime)
            -> NoneType
        Creates a collection of Reports.
        '''

        self.name = name
        self.date = date if date else datetime.datetime.now()
        self.test_methods = test_methods if test_methods else []
        self.tests = []
        self.reports = []
        [self.add(report) for report in reports] if reports else None

    def add(self, report):
        ''' (Reports, Report) -> Report
        Adds a Report to this Reports. Append any TestCase names to
        this Reports list of TestCase names that aren't known.
        '''

        # add unknown test_names
        for test_name in report.get_test_names():
            if test_name not in self.tests and test_name not in EXCLUDED_TESTS:
                self.tests.append(test_name)

        self.reports.append(report)
        return report

    def to_json(self):
        ''' (Reports) -> dict
        Returns a dict representing this Reports.
        '''

        return {
            'name': self.name,
            'date': self.date,
            'tests': self.tests,
            'results': [report.to_json() for report in self.reports]
        }

    @staticmethod
    def from_json(json):
        ''' (dict) -> Reports
        Returns a collection of Report from a json dict.
        '''

        return Reports(
            json['name'],
            json['tests'],
            [
                Report.from_json(report)
                for report in json['results']
            ],
            json['date']
        )

    def get_students(self):
        ''' (Reports) -> list of Student
        Gets all Students in all Report in this Reports.
        '''

        return sum([report.get_students() for report in self.reports], [])

    def get_test_names(self):
        ''' (Reports) -> list of str
        Gets all names of TestCases in this Reports.
        '''

        return list(self.tests)

    def get_reports(self):
        ''' (Reports) -> list of Report
        Gets all Report in this Reports.
        '''

        return list(self.reports)
