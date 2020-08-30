'''A wrapper around test_runner that runs the tester on individual
submissions given on the command line.

Also takes a file that maps directories to repo_names, in the format:
dirpath,repo_name

TODO: perhaps add an option to specify group names instead of repo
names?

Anya Tafliovich 2015, 2016, 2019

'''

import argparse
import importlib
import os
import sys
import test_runner


def read_repodirs(repo_dirs_file):
    '''Return a Dict[repo_name, dirpath] collected from info in repo_dirs_file.

    repo_dirs_file is a path to a file in format:
        dirpath,repo_name
    '''

    return dict((repo_name, dirpath) for [dirpath, repo_name]
                in (line.strip().split(',') for line in repo_dirs_file))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Run tests on selected repos.')

    PARSER.add_argument('directories_and_names',
                        help='File in format dirpath,repo_name.')

    PARSER.add_argument('config',
                        help='Config file for test_runner')

    PARSER.add_argument('repo_name', nargs='+',
                        help='Names of student repos to test.')

    ARGS = PARSER.parse_args()

    HEAD, TAIL = os.path.split(ARGS.config)
    sys.path.append(HEAD)
    CONFIG = importlib.import_module(TAIL.split('.')[0])

    # read the dirpath,repo_name file
    with open(ARGS.directories_and_names) as rdf:
        REPODIRS = read_repodirs(rdf)

    # run tester on all given repos
    for repo in ARGS.repo_name:
        test_runner.execute_tests(REPODIRS[repo], CONFIG)
