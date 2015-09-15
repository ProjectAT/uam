"""A set of utils to work with Markus grades."""

import csv
from uam_utils import Students, Student
import math

def read_csv_report(fileobject, roundup=False):
    """Read a MarkUs csv report and return a {utorid: [grades]} dict.
    If roundup, the marks are rounded up to the next integer.
    """

    def convert(s):
        return 

    grades = {}
    for rec in csv.reader(fileobject):
        grades[rec[0]] = (list(map(lambda s: str(math.ceil(float(s))) if s else s,
                                   rec[1:]))
                          if roundup else rec[1:])
    return grades


def read_markus_grades_file(fileobject, roundup=False):
    """Read a MarkUs grades reportfile and return a {utorid: [grades]}
    dict.
    If roundup, the marks are rounded up to the next integer.
    """

    fileobject.readline()  # skip first two lines
    fileobject.readline()
    return read_csv_report(fileobject, roundup)


def print_csv_report(grades, out):
    """Given a {utorid: [grades]} dict, print a MarkUs csv report to out."""

    for utorid, gradelist in grades.items():
        print(','.join([utorid] + gradelist), file=out)


def merge_grades(g1, g2):
    """Return a {utorid: [grades]} dict by appending all grades from
    {utorid: [grades]} dict g2 to the grades from {utorid: [grades]}
    dict g1, for each utorid in g1.

    """

    merged = {}
    for utorid, grades in g1.items():
        merged[utorid] = grades + g2.get(utorid, [])
    return merged


def select_grades(grades, select):
    selected = {}
    for utorid, grs in grades.items():
        selected[utorid] = [grs[i] for i in select]
    return selected


def print_gf_format(grades, students, out):
    """Print out the grades in {utorid: [grades]} dict 'grades' for
    uam_utils.Students students.

    """

    for utorid, grs in grades.items():
        student = students.get(utorid)
        if student is None:
            print('Warning: no student record for %s.' % utorid)
            continue
        stu_num, first, last = (student.student_number,
                                student.first,
                                student.last)
        print(('%s    %s %s,' % (stu_num, last, first) +
               ','.join([utorid] + grs)), file=out)


def read_gf(gf):
    """Read the given gf file and return a {utorid: [grades]} dict."""

    grades = {}
    lines = open(gf).readlines()
    blank_at = lines.index('\n')  # skip header
    for line in lines[blank_at+1:]:
        fs = line.strip().split(',')
        utorid = fs[1]
        grs = fs[2:]
        grades[utorid] = grs
    return grades
