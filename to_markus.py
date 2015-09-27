#!/usr/bin/python3

''' Markus Integration -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

Submits grades for an assignment to Markus (through previously created
rubrics) from an Aggregate json file containing grades.
'''

import utils.markusapi
import uam_utils
import argparse
import json
import sys

def to_markus(api_key, url, assignment_number, aggregate):
    ''' (str, str, int, dict) -> NoneType
    Transmits grades from an Aggregated json dict of Reports
    to MarkUs.

    REQ: Markus has Rubric names previously created, matching
    TestCase (not methods, but TestCases) exactly.
    '''

    # create Reports object first
    reports = uam_utils.Reports.from_json(aggregate)
    markus = utils.markusapi.Markus(api_key, url)
    group_ids = markus.get_groups_by_name(assignment_number)

    for report in reports.get_reports():
        try:
            markus.update_marks_single_group(
                grades_map_from_report(report, reports.get_test_names()),
                assignment_number,
                group_ids[report.get_group()]['id']
            )

        # TODO: a hacky fix for Markus hacky stuff with group names/userids
        except KeyError as e:
            for student in report.get_students():
                try:
                    markus.update_marks_single_group(
                        grades_map_from_report(
                            report, reports.get_test_names()
                        ),
                        assignment_number,
                        group_ids[student.student_id]['id']
                    )
                except Exception as e:
                    print(
                        'Warning: Markus Update for student_id %s failed: %s'
                        % (student.student_id, e)
                    )
    
def grades_map_from_report(report, tests):
    ''' (uam_utils.Report, list of str) -> dict of str:int
    Produces a map of TestCase names to numeric grades from 
    a Report report.
    '''

    return {
        test_name: report.get_test_passes(test_name)
        for test_name in tests
    }

if __name__ == '__main__':

    # get args
    parser = argparse.ArgumentParser(
        description=(
            'Uploads grades to Markus from an Aggregated json file.'
        )
    )
    parser.add_argument(
        'aggregated',
        help='Path containing Aggregated json file'
    )
    parser.add_argument(
        'key',
        help='An API key obtained from Markus'
    )
    parser.add_argument(
        'url',
        help='Base URL for Markus installation'
    )
    parser.add_argument(
        'assignment',
        help='The assignment number to obtain a listing for'
    )
    args = parser.parse_args()

    # write out listing
    try:
        with open(args.aggregated) as aggregated:
            to_markus(
                args.key,
                args.url,
                int(args.assignment),
                json.loads(aggregated.read().strip())
            )

    except IOError as error:
        print('Could not read Aggregated json file')
