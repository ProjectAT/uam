#!/usr/bin/python3

''' Markus Integration -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

Obtains a listing of all groups and repos for an assignment number
from Markus.
'''

import utils.markusapi
import argparse
import sys

def from_markus(api_key, url, assignment_number):
    ''' (str, str, int) -> (list of str, list of str)
    Gets a listing of all groups for an assignment assignment_number
    from Markus in a format resembling a CSV group list obtained
    from Markus directly.
    '''

    groups = list()
    repos = list()
    try:
        for group in utils.markusapi.Markus(
            api_key,
            url
        ).get_groups(assignment_number):
            try:
                groups.append(','.join([
                    group['student_memberships'][0]['user']['user_name'],

                    # generate group repo name
                    'group_%s' % str(group['id']).zfill(4),

                    # force unique students, because markus outputs duplicates
                    # for some odd reason
                    ','.join(set(
                        [
                            user['user']['user_name']
                            for user
                            in group['student_memberships']
                        ]
                    ))
                ]))

                # TODO: get SVN repo url in a non-hacky way
                repo = url.split('/')
                repo.insert(3, 'svn')
                repo = '/'.join(repo).strip('/')

                repos.append(','.join([
                    group['group_name'],
                    '%s/group_%s' % (
                        repo,
                        str(group['id']).zfill(4))
                ]))

            # group is broken and has no members
            except (KeyError, IndexError, TypeError):
                continue

    # connection error
    except ValueError:
        raise ValueError('Incorrect API Key (%s)' % api_key)

    return (groups, repos)

if __name__ == '__main__':
    # get args
    parser = argparse.ArgumentParser(
        description=(
            'Obtains a listing of all groups and repos for an assignment ' +
            'from Markus in a format resembling a CSV group list and ' +
            'stores it in groups_target and repos_target, respectively.'
        )
    )
    parser.add_argument(
        'groups_target',
        help='Path to write out groups list'
    )
    parser.add_argument(
        'repos_target',
        help='Path to write out groups list'
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
        groups, repos = from_markus(
           args.key,
           args.url,
           int(args.assignment)
        )

        # groups
        with open(args.groups_target, 'w') as tgt:
            tgt.write('\n'.join(groups))

        # repos
        with open(args.repos_target, 'w') as tgt:
            tgt.write('\n'.join(repos))

    except IOError as error:
        print('Could not write groups to file: %s' % error,
            file=sys.stderr)
    except ValueError as error:
        print('Could not connect to MarkUs: %s' % error,
            file=sys.stderr)
