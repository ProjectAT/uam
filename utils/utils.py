"""A new set of utilities to work with MarkUs, Quercus, Intranet, CDF
grades files, CATME files, and what not.
Work in progress.

"""

import csv
import math
import re
from email_validator import validate_email, EmailNotValidError


MAX_UTORID_LENGTH = 8
STUDENT_NUMBER_LENGTH = 10
# str methods of Student and Students will use this as default format/ordering
# if any of these are not present, they are omitted from the str
DEFAULT_STUDENT_STR = ('last', 'first', 'student_number', 'utorid',
                       'gitid', 'email', 'lecture', 'tutorial', 'id1', 'id2')

# TODO Fix this
DEFAULT_FORMULA_OUTOF = 100


def DEFAULT_STUDENT_SORT(student): return student.last + student.first


def make_classlist(students, outfile, attrs=DEFAULT_STUDENT_STR,
                   header=False, key=DEFAULT_STUDENT_SORT):
    '''Write out a CSV classlist to outfile.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    attrs is an iterable of attributes of Student to include.
    key is the key for sorting Students.
    header is True/False: whether to write the header
    '''

    student_list = list(students)
    student_list.sort(key=key)
    if header:
        outfile.write(','.join(list(attrs)) + '\n')
    for student in student_list:
        outfile.write(student.full_str(attrs) + '\n')


def make_empty_gf(students, outfile, outofs=None,
                  utorid=True, key=DEFAULT_STUDENT_SORT):
    '''Write out an empty gf file.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    outofs is a Dict[asst:str, outof:int] for the header.
    key is the key for sorting Students.
    utorid is True/False: whether to include utorids.
    '''

    if outofs is None:
        outofs = {}

    student_list = list(students)
    student_list.sort(key=key)

    header = _make_gf_header(outofs, utorid)
    outfile.write(header + '\n')

    for student in student_list:
        line = _make_gf_student_line(student, utorid)
        outfile.write(line)


def make_gf_file(outfile, stnum_to_student_grades, outofs,
                 utorid=True, key=DEFAULT_STUDENT_SORT):
    '''Write a gf file to outfile.

    stnum_to_student_grades is Dict[stnum, Tuple(Student, Grades)]
    outofs is a List[(asst, grade)] since it must be ordered for gf.

    '''

    header = _make_gf_header(outofs, utorid)
    outfile.write(header + '\n')

    student_grades_list = _sorted_student_grades(stnum_to_student_grades, key)
    for student, grades in student_grades_list:
        line = _make_gf_student_line(student, utorid, grades, outofs)
        outfile.write(line)


def make_csv_submit_file(outfile, dict_key_to_student_grades, asst, exam_no_shows):
    '''Write a CSV submit file for eMarks to outfile.

    dict_key_to_student_grades maps some key (normally student_number
    or utorid) to Tuple(Student, Grades).
    asst is the name of the "final mark" assignment
    exam_no_shows is a list of keys into the dict of exam no shows.

    '''

    for key, (student, grades) in dict_key_to_student_grades.items():
        try:
            grade = grades.get_grade(asst)
        except KeyError:
            print('WARNING: No grade for assignment {} for this student:\n\t{}'.format(
                asst, student))
            continue

        outfile.write('{},{}{}\n'.format(student.student_number,
                                         # submit file needs integers
                                         math.ceil(grade),
                                         ',y' if key in exam_no_shows else ''))


def load_quercus_grades_file(infile, dict_key='student_number'):
    '''Read Quercus CSV Gradebook.
    Return (Dict[dict_key, Tuple(Student, Grades)], outofs).
    The default dictionary key is student_number. Another common use case would be 'utorid'.
    See also StudentGrades' staticmethod.
    '''

    student_grades = StudentGrades.load_quercus_grades_file(infile, dict_key)

    return (student_grades.studentgrades, student_grades.outofs)


def load_gf_file(infile, dict_key='student_number'):
    '''Read gf grades file.
    Return (Dict[dict_key, Tuple(Student, Grades)], outofs).
    The default dictionary key is student_number. Another common use case would be 'utorid'.
    See also StudentGrades' staticmethod.
    '''

    student_grades = StudentGrades.load_gf_file(infile, dict_key)

    return (student_grades.studentgrades, student_grades.outofs)


class Students:
    '''A collection of Students.'''

    def __init__(self, iterable=None):
        '''Initialize Students from iterable.'''

        if iterable:
            self.students = set(iterable)
        else:
            self.students = set()

    def add_student(self, student):
        '''Add new student.'''

        self.students.add(student)

    @staticmethod
    def load_intranet_classlist(infile):
        '''Return a new Students created from an Intranet classlist csv file.'''

        reader = csv.DictReader(infile)
        students = set()
        for row in reader:
            names = row['My Students (Lname, Fname)'].split(',')
            student = Student(student_number=row['StudentID'],
                              email=row['Email'],
                              first=names[1],
                              last=names[0],
                              lecture=row['Lecture'],
                              tutorial=row['Tutorial']
                              )
            students.add(student)
        return Students(students)

    @staticmethod
    def load_quercus_classlist(infile):
        '''Return a new Students created from a Quercus possibly empty gradebook
        csv file.'''

        reader = csv.DictReader(infile)
        students = set()
        for row in reader:
            if not _contains_student_data_quercus(row):
                continue
            student = _make_student_from_quercus_row(row)
            students.add(student)

        return Students(students)

    def __iter__(self):
        '''Return an Iterator over these Students.'''

        return iter(self.students)

    def by_utorid(self):
        '''Return a Dict[UTORID, Student]. Raises AttributeError if there is a
        Student with no utorid.'''

        return self._by_field('utorid')

    def by_student_number(self):
        '''Return a Dict[student_number, Student]. Raises AttributeError if there is a
        Student with no student_number.'''

        return self._by_field('student_number')

    def by_gitid(self):
        '''Return a Dict[gitid, Student]. Raises AttributeError if there is a
        Student with no gitid.'''

        return self._by_field('gitid')

    def _by_field(self, field):
        '''Return a Dict[field, Student].  Raises AttributeError if there is
        no attribute field in any of the Students.

        '''

        field2student = {}
        for student in self.students:
            attr = getattr(student, field)
            if attr is not None:
                field2student[attr] = student
            else:
                print('WARNING: This student\'s attribute {} is None!\n\t{}'.format(
                    field, student))
        return field2student

    def full_str(self, ordering=DEFAULT_STUDENT_STR, key=DEFAULT_STUDENT_SORT):
        '''Return a customized str representation of these Students.
        ordering is the other of Student attributes,
        key is the key for sorting Students.
        '''

        student_list = list(self.students)
        student_list.sort(key=key)
        return ('{' + str([student.full_str(ordering)
                           for student in student_list])[1:-1] + '}')

    def __str__(self):
        '''Return a default str representation of these Students.
        '''

        return self.full_str(DEFAULT_STUDENT_STR, DEFAULT_STUDENT_SORT)


class Student:
    """A representation of a student.
    """

    def __init__(self, **kwargs):
        """Instantiate this Student from given fields.
        """

        self.utorid = _clean(kwargs.get('utorid'))
        if self.utorid is not None and not _is_utorid(self.utorid):
            raise InvalidStudentInfoError('UTORID', self.utorid)

        self.student_number = _clean(kwargs.get('student_number'))
        if self.student_number is not None:
            if _is_student_number(self.student_number):
                self.student_number = self.student_number.zfill(10)
            else:
                raise InvalidStudentInfoError(
                    'student number', self.student_number)

        self.email = _clean(kwargs.get('email'))
        if self.email is not None and not _is_email(self.email):
            raise InvalidStudentInfoError('email', self.email)

        self.first = _clean(kwargs.get('first'))
        self.last = _clean(kwargs.get('last'))
        self.lecture = _clean(kwargs.get('lecture'))
        self.tutorial = _clean(kwargs.get('tutorial'))
        self.gitid = _clean(kwargs.get('gitid'))
        self.id1 = _clean(kwargs.get('id1'))
        self.id2 = _clean(kwargs.get('id2'))

    def __str__(self):
        '''Return the default str representation on this Student.'''

        return self.full_str(DEFAULT_STUDENT_STR)

    def full_str(self, ordering=DEFAULT_STUDENT_STR):
        '''Return a customized str representation of this Student.
        ordering is the other of Student attributes.
        '''

        attrs = []
        for attr_name in ordering:
            attr = getattr(self, attr_name)
            if attr:
                attrs.append(attr)
        return ','.join(attrs)


class Grades:
    '''Essentially a dictionary of grades.'''

    def __init__(self):
        self.grades = {}

    def __iter__(self):
        return iter(self.grades)

    def add_grade(self, assignment, grade=0):
        '''Add/update grade for assignment. Raise TypeError if assignment is
        not a str or if grade cannot be converted to float.

        '''

        grade = _clean_grade(grade)
        assignment = _clean_asst(assignment)
        self.grades[assignment] = grade

    def add_grades(self, grades):
        '''Add/update grades from dictionary grades.

        '''

        for assignment, grade in grades:
            self.add_grade(assignment, grade)

    def get_grade(self, assignment):
        '''Return the grade for assignment. Raise KeyError if no such
        assignment.

        '''

        try:
            return self.grades[assignment]
        except KeyError:
            raise KeyError('No such assignment: {}'.format(assignment))

    def __str__(self):
        return str(self.grades)


class StudentGrades:
    '''My own gradebook.'''

    def __init__(self, outofs=None, studentgrades=None, dict_key='student_number'):
        '''Init an empty Gradesfile.'''

        if outofs:
            self.outofs = dict(outofs)
        else:
            self.outofs = {}

        if studentgrades:
            self.studentgrades = dict(studentgrades)
        else:
            self.studentgrades = {}
        self.dict_key = dict_key

    def __iter__(self):
        return iter(self.studentgrades)

    def __str__(self):
        result = str(self.outofs) + '\n\n'

        student_list = _sorted_student_grades(self.studentgrades)
        for student, grades in student_list:
            result += '{}: {},{}\n'.format(student.student_number,
                                           student, grades)
        return result

    def get_students(self):
        '''Return a Students object with this StudentGrades' students.'''

        return Students(record[0] for record in self.studentgrades.values())

    @staticmethod
    def load_quercus_grades_file(infile, dict_key='student_number'):
        '''Read Quercus CSV Gradebook.
        The default dictionary key is student_number. Another common
        use case would be 'utorid'.

        '''

        reader = csv.DictReader(infile)
        dict_key_to_student_grades = {}

        for row in reader:
            first = row['Student'].strip()
            if first in ('', 'Student, Test'):
                continue
            if first == 'Points Possible':
                outofs = _make_out_of_from_quercus_row(row)
                continue

            student = _make_student_from_quercus_row(row)
            grades = _make_grades_from_quercus_row(row)

            try:
                key = getattr(student, dict_key)
                dict_key_to_student_grades[key] = (student, grades)
            except AttributeError:
                print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                    dict_key, student))

        return StudentGrades(outofs, dict_key_to_student_grades, dict_key)

    @staticmethod
    def load_gf_file(infile, dict_key='student_number'):
        '''Read gf grades file.

        The default dictionary key is student_number. Another common
        use case would be 'utorid'.

        '''

        dict_key_to_student_grades = {}

        lines = infile.readlines()
        sep = lines.index('\n')

        header = lines[:sep + 1]
        assts, outofs = _make_out_of_from_gf_header(header)

        for line in lines[sep + 1:]:
            student = _make_student_from_gf_line(line)
            grades = _make_grades_from_gf_line(line, assts)

            try:
                key = getattr(student, dict_key)
                dict_key_to_student_grades[key] = (student, grades)
            except AttributeError:
                print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                    dict_key, student))

        return StudentGrades(outofs, dict_key_to_student_grades, dict_key)


class InvalidStudentInfoError(Exception):
    '''Exception raised on attempt to create Student with invalid fields.
    '''

    def __init__(self, field, value):
        '''field: name of kwarg that is invalid
        value: value of kwarg that is invalid'''

        Exception.__init__(self)
        self.message = 'Cannot create Student with given {}: {}.'.format(
            field, value)


def _sorted_student_grades(stnum_to_student_grades, key=DEFAULT_STUDENT_SORT):
    student_grades_list = list(stnum_to_student_grades.values())
    def sort_key(record): return key(record[0])
    student_grades_list.sort(key=sort_key)
    return student_grades_list


def _make_student_from_gf_line(line):

    fields = line.strip().split(',')
    match = re.fullmatch(
        r'(\d+) [ dx][ dx] ([\w-]+)((\s+([\w-]+))+)', fields[0])

    stunum = match.group(1)
    last = match.group(2)
    first = match.group(3).strip()
    utorid = fields[1] if len(fields) > 1 and not fields[1].isdigit() else None

    return Student(student_number=stunum, first=first, last=last, utorid=utorid)


def _make_grades_from_gf_line(line, assts):
    grades = Grades()
    fields = line.strip().split(',')
    if len(fields) == 1:
        return grades

    if not fields[1].isdigit():
        fields = fields[2:]
    else:
        fields = fields[1:]

    grades.add_grades(zip(assts, fields))
    return grades


def _make_out_of_from_gf_header(header):
    # TODO FIX collecting calculated grades
    outofs = {}
    assts = []
    for line in header:
        match = re.fullmatch(r'(\w+)\s*/\s*(\d+)\n', line)
        if match:
            asst = _clean_asst(match.group(1))
            outof = _clean_grade(match.group(2))
            outofs[asst] = outof
            assts.append(asst)
            continue
        match = re.match(r'(\w+)\s*=', line)  # calculated grade
        if match:
            asst = _clean_asst(match.group(1))
            outof = DEFAULT_FORMULA_OUTOF
            outofs[asst] = outof
            assts.append(asst)
            continue
    return (assts, outofs)


def _clean_grade(grade):
    try:
        return float(grade)
    except ValueError:
        raise TypeError('Invalid type for grade: {} of type {}.'.format(
            grade, type(grade)))


def _clean_asst(assignment):
    if isinstance(assignment, str):
        return assignment.strip()
    raise TypeError('Invalid type for assignment: {} of type {}.'.format(
        assignment, type(assignment)))


def _make_student_from_quercus_row(row):
    '''Create and return a Student from a row of Quercus file.'''

    names = row['Student'].split(',')
    sections = row['Section'].split(' and ')
    student = Student(student_number=row['Integration ID'],
                      utorid=row['SIS User ID'],
                      first=names[1],
                      last=names[0],
                      lecture=sections[0],
                      tutorial=sections[1],
                      id1=row['ID']
                      )
    return student


def _make_grades_from_quercus_row(row):
    '''Create and return a Grades from a row of Quercus file.

    '''
    grades = Grades()
    for asst, grade in row.items():
        asst = _clean_asst(asst)
        if isinstance(grade, str) and grade.strip() == '':
            grade = 0
        if _is_quercus_asst_name(asst):
            grades.add_grade(asst, _clean_grade(grade))
    return grades


def _make_out_of_from_quercus_row(row):
    '''Create and return a dict mapping asst name to total points.'''

    outofs = {}
    for key, value in row.items():
        key = _clean_asst(key)
        if _is_quercus_asst_name(key):
            outofs[key] = _clean_grade(value)
    return outofs


def _is_quercus_asst_name(word):
    # assignments on Quercus are "AsstName (numericID)"

    match = re.fullmatch(r'\w+\s\(\d+\)', word.strip())
    return match is not None


def _clean(word):
    return word.strip() if word else word


def _is_utorid(word):
    '''Alphanumeric up to MAX_UTORID_LENGTH.'''

    return word.isalnum() and len(word) <= MAX_UTORID_LENGTH


def _is_student_number(word):
    return (word.isdigit() and
            STUDENT_NUMBER_LENGTH - 1 <= len(word) <= STUDENT_NUMBER_LENGTH)


def _is_email(word):
    try:
        validate_email(word)
    except EmailNotValidError:
        return False
    return True


def _contains_student_data_quercus(row):
    '''Does this row contain student info?'''

    names = row['Student']
    return (names is not None and
            names.strip() != '' and
            names.strip() != 'Points Possible' and
            names.strip() != 'Student, Test')


def _make_gf_header(outofs=None, utorid=False):
    '''outofs is a List[(asst, grade)], as it must be ordered for gf.'''

    if outofs is None:
        outofs = []
    header = '*/,\n'
    if utorid:
        header = header + 'utorid " ! , 9\n'
    for asst, outof in outofs:
        # gf does not like spaces and parens in asst names
        asst = asst.replace('(', '_').replace(')', '_').replace(' ', '_')
        header = header + \
            '{} / {}\n'.format(asst, int(outof))
    return header


def _make_gf_student_line(student, utorid=False, grades=None, outofs=None):
    '''outofs is a List[(asst, grade)], as it must be ordered for gf.
    Either both grades and outofs are None (no grades) or
    both are not None (grades recorded).'''

    if grades is None:
        grades = {}

    line = '{}    {} {}{}'.format(
        student.student_number,
        student.last if student.last else '',
        student.first if student.first else '',
        ',{}'.format(student.utorid) if utorid else '')

    line = (line + ',' +
            ','.join([str(round(grades.get_grade(asst), 1)) for (asst, grade) in outofs]) +
            '\n')

    return line
