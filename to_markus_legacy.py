#!/usr/bin/python3

''' Markus Integration -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

Submits grades for an assignment to Markus v1.3 
through previously created rubrics from an Aggregate json file
containing grades.
'''

import uam_utils
import requests
import re
from bs4 import BeautifulSoup as bs
import random
import argparse
import json
import sys

def to_markus(username, password, url, assignment_number, aggregate):
    ''' (str, str, str, int, dict) -> NoneType
    Transmits grades from an Aggregated json dict of Reports
    to MarkUs v1.3.

    REQ: Markus has Rubric names previously created, matching
    TestCase (not methods, but TestCases) exactly.
    '''

    # start session with cookies enabled and login
    s = requests.session()
    login = s.post(url, data={
        'user_login': username,
        'user_password': password,
        'commit': 'Log in',
        'authenticity_token': get_auth_token(s, url)
    })

    # get group submission ids
    reports = uam_utils.Reports.from_json(aggregate)
    submissions = bs(
        s.get(
            '%s/assignments/%s/submissions/browse?per_page=99999'
            % (url, assignment_number)
        ).text,
        'html.parser'
    ).find(id="submissions").find_all('a')[:-7]
    submission_map = {}
    while submissions:
        group_id = str(submissions.pop()).split('>')[-2].split('<')[0]
        submission_id = str(submissions.pop()).split('/')[-3]

        print('Uploading %s\'s grade to Markus..' % group_id)

        # get rubric mark_id's
        criteria = bs(
            s.get(
                '%s/assignments/%s/submissions/%s/results/%s/edit'
                % (url, assignment_number, submission_id, submission_id)
            ).text,
            'html.parser'
        ).find_all(class_='criterion_title')

        for criterion in criteria:
            test_name = criterion.find(
                'div',
                class_='mark_criterion_title_div_level'
            ).b.text
            criteria_id = ''.join(
                filter(
                    lambda x: x.isdigit(),
                    criterion.find(class_='mark_grade_input')['id']
                )
            )

            # upload
            s.post(
                (
                    '%s/assignments/%s/submissions/%s/results/update_mark'
                    + '?mark_id=%s'
                )
                % (url, assignment_number, submission_id, criteria_id),
                data={
                    'mark': reports
                        .get_report_by_group(group_id)
                        .get_test_passes(test_name),
                    'authenticity_token': get_auth_token(s, url)
                }
            )

        # and finally, set as complete
        s.post(
            '%s/assignments/%s/submissions/%s/results/%s/update_marking_state'
            % (url, assignment_number, submission_id, submission_id),
            data={
                'value': 'complete',
                'authenticity_token': get_auth_token(s, url)
            }
        )
    
def get_auth_token(session, url):
    return re.findall('const AUTH_TOKEN = "(.*)"', session.get(url).text)[0]

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
        'username',
        help='An username from Markus'
    )
    parser.add_argument(
        'password',
        help='The password for the specified username'
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
                args.username,
                args.password,
                args.url,
                int(args.assignment),
                json.loads(aggregated.read().strip())
            )

    except IOError as error:
        print('Could not read Aggregated json file')
