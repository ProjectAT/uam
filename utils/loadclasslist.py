"""Get a map of Students: by utorid or by student number."""

import re

class Student(object):
    """A Student has a utor id (str), student number (str), last name
    (str), first name(s) (str), and email (str)."""
    
    def __init__(self, fields):
        self.utorid = fields[0]
        self.lastname = fields[1]
        self.firstnames = fields[2]
        self.st_num = fields[3]
        self.email = fields[4]

def load_by_st_num(filename, select=None):
    """Create from the input class list 'filename' and return a
    dictionary of Students by student number.  If select is specified,
    include only students with utorids mentioned in that file."""

    return load_by(filename, 'st_num', select)
	
def load_by_utorid(filename, select=None):
    """Create from the input class list 'filename' and return a
    dictionary of Students by utorid.  If select is specified, include
    only students with utorids mentioned in that file."""

    return load_by(filename, 'utorid', select)

def load_by(filename, by_what, select):
   
    students = {}
    for line in open(filename):
        s = Student(line.strip().split(','))
        students[getattr(s, by_what)] = s

    if select:
        toselect = [re.findall(r"[\w]+", line) for line in open(select).readlines()]
        selected = {}
        for (utorid, student) in students.items():
            if any([utorid in toselectitem for toselectitem in toselect]):
                selected[utorid] = student
        students = selected
    return students
