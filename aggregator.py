#!/usr/bin/python3

"""Report Aggregator -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Modified by A.Tafliovich 2015.
"""

import sys
import os
import json
import argparse
import datetime
from uam_utils import Student, Students
from uam_utils import Group, Groups

DEFAULT_JSON_FILE = 'result.json'


class TestReport:
    """An aggregated report.
    """

    def __init__(self, submission_dirs_file, student_file, group_file,
                 assignment_name, json_file=DEFAULT_JSON_FILE,
                 aggregated_dict=None):
        """Initialize an aggregated test report, with information on all
        results of all tests on all submissions.

        submission_dirs_file: file in the format
           submission_path,submission_dir_name
        where submission_dir_name is the name of the "main" directory for
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
        """

        # skip active aggregation if json is provided
        if aggregated_dict:
            _from_aggregated_dict()
            return

        # aggregate
        self.results, self.name, self.date, self.tests = (
            [],
            assignment_name,
            datetime.datetime.now().isoformat().split('.')[0],
            set())

        # set up Students
        try:
            students = Students(student_file)
        except FileNotFoundError as e:
            print("Cannot initialize students info. %s " % e,
                  file=sys.stderr)
            return

        # set up Groups, by repo_name
        try:
            groups = Groups(group_file, students).by_repo_name()
        except FileNotFoundError as e:
            print("Cannot initialize students info. %s " % e,
                  file=sys.stderr)
            return

        try:
            submission_dirs = open(submission_dirs_file)
        except IOError as e:
            print("Cannot open file that lists submission directories " +
                  "and directory names. %s" % e,
                  file=sys.stderr)
            return

        # go
        for line in submission_dirs:
            try:
                [dirpath, repo_name] = line.strip().split(',')
            except ValueError as e:
                print("The file %s that lists submission directories " +
                      "and directory names is incorrectly formatted. %s" %
                      (submission_dirs_file, e),
                      file=sys.stderr)
                return

            try:
                test_result = json.loads(open(os.path.join(dirpath,
                                                           json_file)).read())
            except Exception as ex:
                print("Warning: could not load json from %s. %s" %
                      (dirpath, ex))
                continue

            group = groups.get(repo_name)
            if group is None:
                print("Warning: no record of group %s." % repo_name,
                      file=sys.stderr)
                continue

            test_result['students'] = [student.to_json() for student in
                                       group.students]

            # update report time
            test_result['date'] = self.date

            # update assignment name
            test_result['assignment'] = assignment_name

            # inject origin path (for templating stage)
            test_result['origin'] = os.path.join(os.getcwd(), dirpath)

            # aggegration
            self.results.append(test_result)

            # TODO: I don't think we need this anymore. Anya.
            # cycle through tests to keep track of test names performed
            for (test_case, test_case_result) in test_result['results'].items():
                self.tests = (self.tests |
                              set(test_case_result.get('passes', {}).keys()) |
                              set(test_case_result.get('failures', {}).keys()) |
                              set(test_case_result.get('errors', {}).keys()))

            # write injected result back out into source json file
            with open(os.path.join(dirpath, json_file), 'w') as fp:
                fp.write(json.dumps(test_result) if test_result else '{}')

    def _from_aggregated_dict(self, aggregated_dict):
        self.results, self.name, self.date, self.tests = (
            aggregated_dict['results'],
            aggregated_dict['name'],
            aggregated_dict['date'],
            aggregated_dict['tests'])

    def to_json(self):
        """Return a standardized UAM compatible JSON string used for producing
        HTML, text, and gf (or whatever template is available)
        reports.

        """

        # TODO: the else part may lead to bugs
        return (json.dumps({'results': self.results,
                            'name': self.name, 'date': self.date,
                            'tests': sorted(self.tests)})
                if self.results else '{}')

    @staticmethod
    def fromJson(jsonStr):
        ''' (str) -> TestReport
        Instatiates a new TestReport from a json string.
        '''

        return TestReport(None, None, None, None,
                          aggregatedJson=json.loads(jsonStr))


if __name__ == '__main__':

    # get options
    parser = argparse.ArgumentParser(
        description=('Produces an aggregated json report file from the ' +
                     'individual json report files.'))
    parser.add_argument('assignment',
                        help='Name of the assignment')
    parser.add_argument('submission_dirs_and_names',
                        help=('Path to a file that contains submission ' +
                              'information. This file must be in the format:' +
                              '\n\tsubmission_path,submission_name'))
    parser.add_argument('students_file',
                        help=('Path to a classlist file. This file must be ' +
                              'in the following format:\n\t' +
                              'student_id,firstnames,lastname,' +
                              'student_number,email'))
    parser.add_argument('groups_file',
                        help=('Path to a file with groups information. This ' +
                              'file must be in the following format:\n\t' +
                              'group_name,group_dir_name,student_id_1,' +
                              'student_id_2,...'))
    parser.add_argument('output_file_name', nargs='?',
                        help='Name of the aggregated JSON output file',
                        default='aggregated.json')
    args = parser.parse_args()

    # aggegate and write json out
    test_report = TestReport(
        str(args.submission_dirs_and_names),
        str(args.students_file),
        str(args.groups_file),
        str(args.assignment)
    ).to_json()
    with open(str(args.output_file_name), 'w') as report:
        report.write('%s\n' % test_report)
