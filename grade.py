"""A wrapper around test_runner that runs the tester on individual
submissions given on the command line.

Needs a file tht maps directories to repo_names, in the format
dirpath,repo_name

TODO: perhaps add an option to specify group names instead of
repo names?

Anya Tafliovich June 2015

"""

import test_runner
import argparse


def read_repodirs(repo_dirs_file):
    """Read the file in the format
    dirpath,repo_name
    and return a repo_name->dirpath dict.
    """

    repodirs = {}
    with open(repo_dirs_file) as rdf:
        for line in rdf:
            dirpath, repo_name = line.strip().split(',')
            repodirs[repo_name] = dirpath
    return repodirs


if __name__ == '__main__':
    # Arguments #
    parser = argparse.ArgumentParser(
        description='Executes unit tests on student code in given repos.')

    parser.add_argument("directories_and_names",
                        help="File in format dirpath,repo_name.")

    parser.add_argument("repo_name", nargs="+",
                        help="Names of student repos to test.")

    args = parser.parse_args()

    # read the dirpath,repo_name file
    repodirs = read_repodirs(args.directories_and_names)

    # run tester on all given repos
    for repo in args.repo_name:
        test_runner.execute_tests(repodirs[repo])
