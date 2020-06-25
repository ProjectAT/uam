#!/usr/bin/env python3

''' Report Templator -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Author: Anya Tafliovich 2015, 2016

TODO: Needs some serious clean-up. Lots of hacks.
'''

import re


def student_list(students, format_str, fields):
    ''' (list of dict, str, list of str) -> list of str
    Prepares a list of student fields from a list of dictionaries representing
    aggregator.UTSCStudents in the given format with respective fields.
    '''

    return [format_str % tuple([student.get(field) for field in fields])
            for student in students]


def get_all_counts(results, select):
    ''' (dict of dicts) -> int
    Gets either the number of passes, failures, errors, and total of the given
    results dictionary depending on select (from the respective order) for all
    TestCases.
    '''

    return sum([get_counts(test, select) for test in results.values()])


def get_counts(results, select):
    ''' (dict of dicts/lists) -> int
    Gets either the number of passes, failures, errors, or total of the given
    results dictionary depending on select (from the respective order) for a
    single TestCase.
    '''
    select = ['passes', 'failures', 'errors', 'total'][select]

    return (len(results.get(select)) if results.get(select) else 0
            if select != 'total' else
            sum([get_counts(results, i) for i in range(3)]))


def ljust(text, amount, offset_after_first=0):
    ''' (str, int) -> str
    Pads the given text with spaces on the left until its length is the given
    amount -- in otherwords, right justify text. Every line after the first
    will be offset to the left offsetAfterFirst spaces.
    '''

    return '\n'.join([line.ljust(amount + int(bool(i)) * offset_after_first)
                      for i, line in enumerate(text.split('\n'))])


def to_gf_names(name):
    ''' (str) -> str
    Converts all non-compliant (non alphanumeric including the underscore)
    characters to underscores for usage as a grade name in a standard .gf
    file as specified by:

    http://www.cdf.toronto.edu/~clarke/grade/fileformat.shtml
    '''

    return re.sub('[^A-Za-z0-9_]', '_', name)


def exclude(collection, exclusions):
    ''' (list, list) -> list
    Removes any elements that contain exclusions from collection.
    '''

    return [element for element in collection if all(exclusion not in element for exclusion in exclusions)]


def _is_excluded(word, exclusions):
    ''' (str, list of str) -> bool
    Determines whether word contains any string from exclusions.
    '''

    return any([exclusion in word for exclusion in exclusions])


def passed(test_name, results):
    ''' (str, dict{str:dict{str: dict{str: str or dict}}}) -> int
    Returns 1 if the test testName is a key in any TestCase's passes dict
    in results and 0 otherwise.
    '''

    # flatten passes from all TestCases
    passes = set()
    for test_case in results.values():
        passes.update((test_case.get('passes') or {}).keys())

    return int(test_name in passes)


def get_balanced_weight(tests):
    '''(list) -> int

    Calculate the equally weighted value of an individual test from a
    collection of tests.

    '''

    return round(1 / len(tests) * 100, 3)
