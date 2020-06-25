'''Utilities for UAM.

TODO: cleanup and modernize
'''

import sys


class Student:
    '''A representation of a student.

    '''

    def __init__(self, line):
        '''Instantiate this Student from a line in BlackBoard generated
        student file:
             student_id,first,last,student_number,email

        '''

        [self.student_id, self.first, self.last,
         self.student_number, self.email] = line.strip().split(',')
        self.student_number = self.student_number.zfill(10)

        # used to determine a single student-to-group relationship
        self.in_groups = []

        self.source, self.section = 'N/A', 'N/A'

    def to_json(self):
        '''Return a dictionary of this Student to be injected into a
        TestResult JSON string.

        '''

        return {'student_id': self.student_id, 'first': self.first, 'last':
                self.last, 'student_number': self.student_number.zfill(10),
                'section': self.section, 'source': self.source, 'email':
                self.email}

    def __str__(self):
        return ','.join([self.student_id, self.first, self.last,
                         self.student_number, self.email])


class Students:
    '''A collection of Students.
    '''

    def __init__(self, student_file=None):
        '''Initialize Students.  Raises FileNotFoundError is student_file
        cannot be opened.

        '''

        self._students = {}
        if student_file is not None:
            self.load_students(student_file)

    def load_students(self, student_file):
        '''Given student_file, a path to a file in the format
            student_id,first,last,student_number,email
        load all Students in this file into this Students.
        Raises FileNotFoundError is student_file cannot be opened.
        '''

        with open(student_file) as st_file:
            for line in st_file:
                try:
                    student = Student(line)
                    self._students[student.student_id] = student
                except ValueError:
                    print('Warning: could not create Student from %s' % line,
                          file=sys.stderr)
                    continue

    def get(self, student_id):
        '''Return a Student with the given student_id, or None if no such
        Student.

        '''

        return self._students.get(student_id)

    def add(self, student):
        '''Add a given Student. Complain on stderr yet proceed if a Student
        with student's student_id already exists.

        '''

        if student.student_id in self._students:
            print('Warning: %s is an existing student. ' +
                  'Adding/updating its record.' % student.student_id)
        self._students[student.student_id] = student

    def __iter__(self):
        return iter(self._students)

    def __str__(self):
        return '\n'.join([str(student) for student in self._students.values()])


class Group:
    '''A representation of a Group containing Students working together on
    an assignment to be graded. These groups are synonymous to the
    groups on MarkUs.

    '''

    def __init__(self, group_id, repo_name=None, students=None):
        '''Instantiate this Group with the given group_id, and associate the
        given list of Students, students, with this Group.

        '''

        self.group_id = group_id
        self.repo_name = repo_name
        if students is None:
            self.students = []
        else:
            self.students = students

    def add(self, student):
        '''Add Student student to this Group.'''

        self.students.append(student)

    def __str__(self):
        return (self.group_id + ',' + self.repo_name + ': ' +
                ';'.join([str(student)for student in self.students]))


class Groups:
    '''A collection of Student Groups.'''

    def __init__(self, group_file=None, students=None):
        '''Raises FileNotFoundError is student_file cannot be opened.

        '''

        self._groups = {}
        if group_file is not None:
            self.load_groups(group_file, students)

    def load_groups(self, group_file, students):
        '''Load all Groups from group_file, a path to a file in the format
          group_id,repo_name,student_id1,...  and Students students.
          Raises FileNotFoundError is student_file cannot be opened.

        '''

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
                                  (student_id, ', '.join(student.in_groups)),
                                  file=sys.stderr)
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
        '''Add a given Group. Complain on stderr yet proceed if a Group with
        group's group_id already exists.

        '''

        if group.group_id in self._groups:
            print('Warning: %s is an existing group. ' +
                  'Adding/updating its students.' % group.group_id)
        self._groups[group.group_id] = group

    def get(self, group_id):
        '''Return a Group with group_id, or None if it doesn't exixt.

        '''

        return self._groups.get(group_id)

    def by_repo_name(self):
        '''Return a dict of this Groups' object Groups, by repo_name.

        '''

        groups = {}
        for group in self._groups.values():
            groups[group.repo_name] = group
        return groups

    def __iter__(self):
        return iter(self._groups)

    def __str__(self):
        return '\n'.join(str(grp) for grp in self._groups.values())
