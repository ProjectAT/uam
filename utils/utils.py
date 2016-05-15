'''A set of utilities to work with MarkUs, BlackBoard, Intranet, CDF
grades files (gf), CATME files, and what not.

'''

import sys
import csv
import datetime
import io


# Multiply by this const to get the grade on MarkUs.
# can't figure out why it should sometimes be 1 and
# sometimes 4 ?!
MARKUS_MULT_CONST = 1.0


def load_bb(bb_file):
    '''(reader) -> {str: Student}

    File reader is for a BlackBoard (BB file) -- see FORMATS.  Load
    all Students in reader into a dict {student_id: Student} and
    return this dict.

    '''

    students = {}

    for line in bb_file:
        try:
            student = Student.make_student_from_bb(line)
            students[student.student_id] = student
        except ValueError:
            print('Warning: could not create Student from %s' % line,
                  file=sys.stderr)
            continue

    return students


def load_intranet(intranet_file):
    '''(reader) -> {str: Student}

    Given a file reader for the Intranet students file, return a dict
    {student_number : Student}.

    '''

    reader = csv.reader(intranet_file)
    students = {}
    for record in reader:
        st_record = {'student_number': record[0],
                     'last': record[1].split(',')[0],
                     'first': record[1].split(',')[1],
                     'lecture': record[3],
                     'tutorial': record[5],
                     'email': record[-1]}
        student = Student(**st_record)
        students[student.student_number] = student
    return students


def load_bb_intranet(bb_file, intranet_file):
    '''(reader, reader) -> {str: Student}

    Given a BB file reader (see FORMATS) and an Intranet file, load
    all Students information into a {student_id: Student} dict and
    return the dict.

    '''

    students = load_bb(bb_file)
    intranet_students = load_intranet(intranet_file)
    for student_id in students.keys():
        try:
            student = students[student_id]
            intranet_student = intranet_students[student.student_number]
            students[student_id].lecture = intranet_student.lecture
            students[student_id].tutorial = intranet_student.tutorial
        except KeyError:
            print('Warning: no record for %s %s in intranet file.' %
                  (student_id, student.student_number),
                  file=sys.stderr)
    return students


def load_git_teams_by_team(gitteams_file):
    '''(reader) -> {str: [str]}

    Read a file in the teachers_pet git teams format and return a dict
    {team_name: [gitid]}

    '''

    gitteams = {}
    for line in gitteams_file:
        info = line.strip().split()
        gitteams[info[0]] = info[1:]
    return gitteams


def load_git_teams_by_id(gitteams_file):
    '''(reader) -> {str: [str]}

    Read a file in the teachers_pet git teams format and return a dict
    {gitid: team_name}

    '''

    gitteams = {}
    for line in gitteams_file:
        info = line.strip().split()
        for gitid in info[1:]:
            gitteams[gitid] = info[0]
    return gitteams


def add_git_ids(student_file, students):
    '''(reader, {str: Student}) -> {str: Student}

    Given a file in format
       first,last,student_id,gitid,email,team

    and a {student_id: Student} dict, return an updated {student_id:
    Student} dict that includes git_id's as Student.id1 and team
    numbers as Student.id2.

    '''

    for line in csv.reader(student_file):
        if len(line) > 1:  # non-empty line
            try:
                students[line[2]].id1 = line[3]  # git id
                students[line[2]].id2 = line[5]  # team
            except KeyError:
                print('Warning: no record for %s.' % line[2], file=sys.stderr)
    return students


def make_git_lists(student_responses, gitteams, gitids):
    '''(csv reader, file writer, file writer) -> None

    student_responses: reader for csv file of the team formation
    Google forms
    gitteams: writer to create teams file for GitHub
    gitids: writer to create ids file for GitHub

    '''

    lines = [' '.join([line[i] for i in range(2, len(line), 2)])
             for line in student_responses]

    for (i, line) in enumerate(lines):
        print('team%s %s' % (str(i).zfill(2), line), file=gitteams)
    gitteams.close()

    for line in lines:
        for gitid in line.split()[1:]:
            print(gitid, file=gitids)
    gitids.close()


def load_markus_students(markus_students):
    '''(reader) -> [str]

    Given a file reader for the MarkUs students file, return a list of
    student_ids.

    '''

    return [line.split(',')[0] for line in markus_students]


def load_marks(markus_file):
    '''(reader) -> {str: [float]}

    Given a file reader for the MarkUs grades file, return a dict that
    maps student_id to a list of grades.

    '''

    all_marks = {}
    for line in markus_file:
        parsed = _check_and_parse_line(line)
        all_marks[parsed[0]] = parsed[1]
    return all_marks


def load_groups_by_student(groups_file):
    '''(reader) -> {str: str}

    Given a file reader for the MarkUs groups file, return a dict of
    student_id to group_name.

    '''

    groups = {}
    for line in groups_file:
        fields = line.strip().split(',')
        for student_id in fields[2:]:
            groups[student_id] = fields[0]
    return groups


def load_groups_by_group(groups_file):
    '''(file reader) -> {str: (str[, str, ...])}

    Given a file reader for the MarkUs groups file, return a dict of
    group_name to a tuple of student IDs.

    '''

    groups = {}
    for line in groups_file:
        fields = line.strip().split(',')
        groups[fields[0]] = tuple(fields[2:])
    return groups


def load_catme_teams(catme_file):
    '''(reader) -> {str: [str, str, ...])}

    Given a file reader in a csv format, generated by catme team
    maker, produce a dictionary of {team_name: [utorid, utorid, ...]}.

    '''

    reader = csv.reader(catme_file)
    groups = {}
    for record in reader:
        utorid = record[2]
        team = record[-2]
        groups[team] = groups.get(team, []) + [utorid]
    return groups


def list_dropped(bb_file, catme_file):
    '''(reader, reader) -> [str]

    Given a BB file reader (see FORMATS) and CATME file reader, return
    a list of student_id's that are present in the CATME file but not
    in the BB file.

    '''

    students = load_bb(bb_file)
    catme = [line.split(',')[0] for line in catme_file.readlines()]
    dropped = [student_id for student_id in catme
               if student_id not in students]
    return dropped


def load_catme_adj(catme):
    '''(reader) -> {student_id: [float]}

    Given a file reader for a file generated by CATME for results of
    peer evaluation, record and return CATME adjustment factors
    (without self).  The value list is just a list of one float, the
    adjustment factor.

    '''

    adj = {}
    for record in csv.reader(catme):
        try:
            adj[record[1]] = [float(record[-2])]
        except ValueError:
            print('Warning: non-float value for %s: %s' %
                  (record[1], record[-2]),
                  file=sys.stderr)
    return adj


def load_student_number2gitid(bb_file, gitid2utorid_file):
    '''(reader, reader) -> {str: str}

    Load and return a dict {student_number: gitid}.
    bb_file is a BlackBoard file.
    gitid2utorid_ file is in format
      gitid,utorid

    '''

    utorid2gitid = \
        dict((line.strip().split(',')[1], line.strip().split(',')[0])
             for line in gitid2utorid_file)
    students = load_bb(bb_file)
    return dict((student.student_number, utorid2gitid[utorid])
                for (utorid, student) in students.items())


def add_project_bonus(
        gf_file, bonus_file, gitid2team, student_number2gitid, outfile=None):
    '''(reader, reader, {str: str}, {str:str}, writer) -> None

    Write out the gf file with added project bonus marks and updated
    team project marks (including the bonus).  Assumes the last grade
    in the gf file is the team grade.

    The bonus_file is in format:
    team_name, ..., bonus
    gitid2team maps {gitid : team_name}
    student_number2gitid maps {student_number: gitid}

    '''

    if outfile is None:
        outfile = sys.stdout

    bonus = {}  # {team_name: bonus}
    for record in csv.reader(bonus_file):
        try:
            bonus[record[0]] = float(record[-1])
        except KeyError:
            print('Warning: no bonus mark for %s.' % record[0],
                  file=sys.stderr)
            continue

    for line in gf_file:
        print(line, end='', file=outfile)
        if line.strip() == '':  # done reading header
            break

    for line in gf_file:
        student_number = line.strip().split()[0]
        team_grade = float(line.strip().split(',')[-1])
        try:
            team_name = gitid2team[student_number2gitid[student_number]]
            bonus_grade = bonus.get(team_name, 0)
        except KeyError:
            print('Warning: no record for %s.' % student_number,
                  file=sys.stderr)
            continue

        withbonus = team_grade * (float(bonus_grade) / 100 + 1)
        print('%s,%.2f,%.2f' % (line.strip(), bonus_grade, withbonus),
              file=outfile)


def add_catme_adj(gf_file, catme):
    '''(reader, reader) -> None

    Print out the gf file with added adjustment factors and calculated
    individual marks.  Assumes the last grade in the gf file is the
    team grade. The catme file is in format:
      student_id,adj1,adj2,...,adj
    Takes the last adj on the line.

    '''

    adj = {}
    for record in csv.reader(catme):
        adj[record[0]] = float(record[-1])

    for line in gf_file:
        print(line, end='')
        if line.strip() == '':  # done reading header
            break

    for line in gf_file:
        student_id = line.strip().split(',')[1]
        team = float(line.strip().split(',')[-1])
        indiv = team * adj[student_id]
        print('%s,%.2f,%.2f' % (line.strip(), adj[student_id], indiv))


def make_gf(bb_file, markus_file):
    '''(reader, reader) -> (str, str)

    Given two file readers, one for the claslist file from Blackboard,
    and one for the MarkUs grades file, return a pair (header, body)
    for the gf file.

    '''

    students = load_bb(bb_file)
    marks = load_marks(markus_file)
    _check_input(students, marks)

    markus_file.seek(0)
    header = _make_gf_header(markus_file.readline())
    body = _make_gf_body(students, marks)

    return (header, body)


def _make_gf_header(line):
    '''Return a header for a gf file from the given line of a MarkUs file.

    '''

    header = ('*/,\n' +
              '*Grades file generated by markus2gf on %s' %
              datetime.datetime.today() +
              '\nutorid " ! , 9')

    parsed = _check_and_parse_line(line)

    for (i, out_of) in enumerate(parsed[2]):
        header += 'm%s / %s\n' % (i, out_of)

    return header


def _make_gf_body(students, all_marks):
    '''({str: Student}, {str: [float]}) -> str

    Return a body for a gf file given two dicts, of students and
    marks.

    '''

    body = ''

    for (student_id, student) in students.items():

        try:
            marks = all_marks[student_id]
        except KeyError:
            print('Warning: no record for student %s in the MarkUs file' %
                  student_id,
                  file=sys.stderr)
            marks = []

        body += ('%s    %s %s,%s,' %
                 (student.student_number, student.last,
                  student.first, student_id) +
                 ','.join([str(mark) for mark in marks]) +
                 '\n')
    return body


def _check_and_parse_line(line):
    '''(str) -> (str, [float], [float])

    Given a line from a MarkUs file, return a tuple of a str and two
    lists of floats (student_id, marks, out_ofs). In case of an
    invalid line, print an error message to stderr and return [] in
    place of a list (or both lists) that could not be produced.

    '''

    parsed = next(csv.reader(io.StringIO(line)))
    marks_list = parsed[2:-3]

    if len(parsed) < 5 or len(marks_list) % 2 != 0:
        print('Ill-formatted MarkUs line: %s' % line, file=sys.stderr)
        return ('', [], [])

    if marks_list == []:
        print('Warning: no marks from line %s' % line)

    student_id = parsed[0]

    marks = []
    for i in range(0, len(marks_list), 2):
        if marks_list[i] == '':
            marks.append(0)
            continue
        try:
            marks.append(float(marks_list[i]))
        except ValueError:
            print('Non-number and non-"" mark on MarkUs line: %s' % line,
                  file=sys.stderr)
            marks = []
            break

    out_ofs = []
    for i in range(1, len(marks_list), 2):
        try:
            out_ofs.append(float(marks_list[i]) * MARKUS_MULT_CONST)
        except ValueError:
            print('Non-number out-of value on MarkUs line: %s' % line,
                  file=sys.stderr)
            out_ofs = []
            break

    return (student_id, marks, out_ofs)


def _check_input(students, marks):
    '''({str: Student}, {str: [float]}) -> NoneType

    Report to stderr if there are any records in marks with no
    corresponding records in students.

    '''

    for student in marks:
        if student not in students:
            print(('Warning: no record of %s in classlist file, ' +
                   'but marks present in Marks file.') % student,
                  file=sys.stderr)


class Student:
    '''A representation of a student.
    '''

    @staticmethod
    def make_student_from_bb(bb_line):
        '''Instantiate a return a Student from a line in BlackBoard generated
        csv student file:
        student_id,first,last,student_number,email

        '''

        dct = zip(['student_id', 'first', 'last', 'student_number', 'email'],
                  next(csv.reader(io.StringIO(bb_line))))
        return Student(**dict(dct))

    def __init__(self, **kwargs):
        '''Instantiate this Student from given fields.

        '''

        self.student_id = kwargs.get('student_id')
        self.first = kwargs.get('first')
        self.last = kwargs.get('last')
        self.student_number = kwargs.get('student_number')
        self.email = kwargs.get('email')
        self.lecture = kwargs.get('lecture')
        self.tutorial = kwargs.get('tutorial')
        self.id1 = kwargs.get('id1')
        self.id2 = kwargs.get('id2')
        if self.student_number:
            self.student_number = self.student_number.zfill(10)

    def __str__(self):
        return ','.join([self.student_id, self.first, self.last, self.email])
