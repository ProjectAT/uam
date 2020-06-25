#!/usr/bin/env python3

'''Report Aggregator.
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Modified by A.Tafliovich 2016, 2020.

Given individual JSON report files, create an aggregrated JSON report
file. Inject student/group information into the individual JSON report
files.

'''

import argparse
import datetime
import json
import os
import sys

from utils.defaults import DEFAULT_IN_JSON_FILE, DEFAULT_OUT_JSON_FILE
from utils.uam_utils import Groups
from utils.uam_utils import Students


class TestReport:
    '''An aggregated report.

    '''

    def __init__(self, submission_dirs_file, student_file, group_file,
                 assignment_name, json_file=DEFAULT_OUT_JSON_FILE,
                 aggregated_dict=None):
        '''Initialize an aggregated test report, with information on all
        results of all tests on all submissions.

        submission_dirs_file: file in the format
           submission_path,submission_dir_name
        where submission_dir_name is the name of the 'main' directory for
        a student/group submission. For example, if you're using MarkUs,
        then this is the name of the MarkUs repo.

        students_file: classlist file in the format
          student_id,first_names,last_name,student_number,email

        groups_file: file with student groups, in the format
          group_name,dir_name,student_id_1,student_id_2,...
        Again, if you're using MarkUs, dir_name is the group's repo name.

        assignment_name: name of assignment being marked

        json_file: name of json file to produce

        aggregated_dict: if provided, aggregation is not performed, and
        the report is initialized from this dict.

        '''

        # skip active aggregation if dict is provided
        if aggregated_dict:
            self._from_aggregated_dict(aggregated_dict)
            return

        # set up aggregation
        self.results, self.name, self.date, self.tests = (
            [],
            assignment_name,
            datetime.datetime.now().isoformat().split('.')[0],
            set())

        # set up Students
        try:
            students = Students(student_file)
        except FileNotFoundError as err:
            print('Cannot initialize students info. {}'.format(err),
                  file=sys.stderr)
            return

        # set up Groups, by repo_name
        try:
            groups = Groups(group_file, students).by_repo_name()
        except FileNotFoundError as err:
            print('Cannot initialize students info. {}'.format(err),
                  file=sys.stderr)
            return

        try:
            submission_dirs = open(submission_dirs_file)
        except IOError as err:
            print('Cannot open file w/ submission directories and directory names: {}'.format(err),
                  file=sys.stderr)
            return

        # go
        for line in submission_dirs:
            if not self._process_submission(line, groups, submission_dirs_file, json_file):
                return

    def _process_submission(self, line, groups, submission_dirs_file, json_file):
        '''Process one test result (one submission) during aggregation.'''

        try:
            [dirpath, repo_name] = line.strip().split(',')
        except ValueError as err:
            print(('The file {} that lists submission directories ' +
                   'and directory names is incorrectly formatted. {}').format(
                       submission_dirs_file, err),
                  file=sys.stderr)
            return False  # abort aggregation

        try:
            with open(os.path.join(dirpath, json_file)) as json_path:
                test_result = json.loads(json_path.read())
        except IOError as error:
            print('Warning: no JSON result file for {}: {}'.format(dirpath, error),
                  file=sys.stderr)
            return True  # skip this one and continue
        except ValueError as error:
            print('Warning: could not load JSON from {}: {}'.format(dirpath, error),
                  file=sys.stderr)
            return True  # skip this one and continue

        group = groups.get(repo_name)
        if group is None:
            print('Warning: no record of group {}.'.format(repo_name),
                  file=sys.stderr)
            return True  # skip this one and continue

        test_result['students'] = [student.to_json() for student in
                                   group.students]

        # update report time
        test_result['date'] = self.date

        # update assignment name
        test_result['assignment'] = self.name

        # inject origin path (for templating stage)
        test_result['origin'] = os.path.join(os.getcwd(), dirpath)

        # aggegration
        self.results.append(test_result)
        self.tests.update(test_result['tests'])

        # write injected result back out into source json file
        with open(os.path.join(dirpath, json_file), 'w') as filep:
            filep.write(json.dumps(test_result, indent=2)
                        if test_result else '{}')

        return True

    def _from_aggregated_dict(self, aggregated_dict):
        self.results, self.name, self.date, self.tests = (
            aggregated_dict['results'],
            aggregated_dict['name'],
            aggregated_dict['date'],
            aggregated_dict['tests'])

    def to_json(self):
        '''Return a standardized UAM compatible JSON used for producing HTML,
        text, and gf (or whatever template is available) reports.

        '''

        # TODO: the else part may lead to bugs
        return (json.dumps({'results': self.results,
                            'name': self.name, 'date': self.date,
                            'tests': sorted(self.tests)},
                           indent=2)
                if self.results else '{}')

    @staticmethod
    def from_json(json_str):
        ''' Create a TestReport from JSON str.
        '''

        return TestReport(None, None, None, None,
                          aggregated_dict=json.loads(json_str))


if __name__ == '__main__':

    # get options
    PARSER = argparse.ArgumentParser(
        description=('Produces an aggregated json report file from the '
                     'individual json report files.'))
    PARSER.add_argument('assignment',
                        help='Name of the assignment')
    PARSER.add_argument('submission_dirs_and_names',
                        help=('Path to a file with submission information in format:'
                              '\n\tsubmission_path,submission_name'))
    PARSER.add_argument('students_file',
                        help=('Path to a classlist file in format:\n\t'
                              'student_id,firstnames,lastname,student_number,email'))
    PARSER.add_argument('groups_file',
                        help=('Path to a file with groups information in format:\n\t'
                              'group_name,group_dir_name,student_id_1,student_id_2,...'))
    PARSER.add_argument('source_files_name', nargs='?',
                        help='Name of the source JSON input files',
                        default=DEFAULT_IN_JSON_FILE)
    PARSER.add_argument('output_file_name', nargs='?',
                        help='Name of the aggregated JSON output file',
                        default=DEFAULT_OUT_JSON_FILE)
    ARGS = PARSER.parse_args()

    # aggegate and write json out
    TEST_REPORT = TestReport(
        str(ARGS.submission_dirs_and_names),
        str(ARGS.students_file),
        str(ARGS.groups_file),
        str(ARGS.assignment),
        str(ARGS.source_files_name)
    ).to_json()
    with open(str(ARGS.output_file_name), 'w') as report:
        report.write('{}\n'.format(TEST_REPORT))
