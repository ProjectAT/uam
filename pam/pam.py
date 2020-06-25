'''Python Auto Marker.
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Author: Anya Tafliovich 2015, 2016, 2020

Grade an individual student submission in the current working
directory with given files containing unittest.TestCases and produce a
UAM compatible JSON string, suitable for templating and aggregation
stages.

'''

import argparse
import io
import json
import os
import signal
import sys
import traceback
import unittest

import testtools

from utils.defaults import DEFAULT_TIMEOUT, DEFAULT_VERBOSITY


def _default_formatter(exc):
    (ex_type, ex_value, ex_traceback) = exc[1]
    return {'description': exc[0].shortDescription() or '',
            'message': str(ex_value),
            'details': '\n'.join(traceback.format_exception(
                ex_type, ex_value, ex_traceback))}


class TestResult:
    '''A result containing information (passes, failures, and errors) of
    the all test runs.
    '''

    def __init__(self, test_files=None, timeout=DEFAULT_TIMEOUT,
                 verbosity=DEFAULT_VERBOSITY, from_json=None,
                 formatter=_default_formatter):
        '''TODO: Document me.'''

        print('Grading {}..'.format(os.getcwd()))

        self._timeout = timeout
        self._test_suite, self._result, self._buffer = \
            None, None, io.StringIO()

        # if no tests files specified: try to load results from JSON,
        # complain and return if load unsuccessful.
        if test_files is None:
            if from_json is None:
                print('Error: cannot init a TestResult ' +
                      'with no test files and no JSON result file',
                      file=sys.stderr)
            else:
                try:
                    self.results = json.loads(from_json)
                except ValueError as error:
                    print('Could not load a JSON result file. {}'.format(error),
                          file=sys.stderr)
            return

        # load tests from test_files
        self._load_tests(test_files)

        # run loaded tests with our custom result object
        self._result = unittest.TextTestRunner(
            verbosity=verbosity,
            stream=self._buffer,
            resultclass=PAMTestResult
        ).run(self._test_suite)

        # make result dict for JSON
        self.results = {'students': [],
                        'results': self._format_results(formatter),
                        'date': 'N/A',
                        'assignment': 'N/A'}

    def get_results(self):
        ''' (TestResult) -> dict
        Return a copy of this TestResult's results.
        '''

        return dict(self.results)

    def to_json(self):
        '''Produce a UAM compatible JSON result string, suitable for
        templating and aggregating.

        '''

        try:
            return json.dumps(self.results)
        except TypeError as err:
            print('Cannot generate a JSON string from test results. {}'.format(err),
                  file=sys.stderr)
            return '{}'

    @staticmethod
    def from_json(json_str):
        ''' (str) -> TestResult
        Instantiate and return a new TestResult from a json string
        jsonStr.
        '''

        return TestResult(json_str)

    def _load_tests(self, test_files):
        '''Load all tests from list of file names test_files (without running
        them).

        TODO: If test_files not given, discover and load all unittests
        in the current directory. Or not.

        '''

        # get TestSuites from test files
        test_loader = unittest.defaultTestLoader
        self._test_suite = unittest.TestSuite(
            (test_loader.discover(os.getcwd(), test_file)
             for test_file in test_files))

        # wrap all test methods with Timeout
        for test in testtools.testsuite.iterate_tests(self._test_suite):
            test.run = Timeout(test.run, self._timeout)

    def _format_results(self, formatter=_default_formatter):
        '''(TestResult) -> dict{str: dict{str: list of str or dict{str: str}}}

        Order passes, failures, and errors by their parent TestCase
        name.  Uses TestCase's fully qualified name instead of the
        TestCase itself in a dictionary.

        '''

        results = {}

        # passes
        for success in self._result.pam_successes():
            results.setdefault(_fully_qualified_name(success), {}).setdefault(
                'passes', {}).update({success.id():
                                      success.shortDescription() or ''})

        # failures
        for fail in self._result.pam_failures():
            results.setdefault(_fully_qualified_name(fail[0]), {}).setdefault(
                'failures', {}).update({fail[0].id(): {
                    'description': formatter(fail)['description'],
                    'message': formatter(fail)['message'],
                    'details': formatter(fail)['details']}})

        # errors
        for err in self._result.pam_errors():
            results.setdefault(_fully_qualified_name(err[0]), {}).setdefault(
                'errors', {}).update({err[0].id(): {
                    'description': formatter(err)['description'],
                    'message': formatter(err)['message'],
                    'details': formatter(err)['details']}})

        return results


class PAMTestResult(unittest.TextTestResult):
    '''An extension of TextTestResult that collects all successes, errors,
    and failures, including the (type, value, traceback) tuples
    returned by sys.exc_info().

    '''

    def __init__(self, stream, descriptions, verbosity):
        unittest.TextTestResult.__init__(self, stream, descriptions, verbosity)
        self._pam_successes, self._pam_errors, self._pam_failures = [], [], []

    def pam_successes(self):
        '''Return the successes.'''

        return self._pam_successes

    def pam_failures(self):
        '''Return the Failures.'''

        return self._pam_failures

    def pam_errors(self):
        '''Return the Errors.'''

        return self._pam_errors

    def addError(self, test, err):

        # don't really need to call parent's method
        # this is just in case we will want all standard
        # TextTestResult features in the future
        unittest.TextTestResult.addError(self, test, err)
        self._pam_errors.append((test, err))

    def addFailure(self, test, err):

        # don't really need to call parent's method
        # this is just in case we will want all standard
        # TextTestResult features in the future
        unittest.TextTestResult.addFailure(self, test, err)
        self._pam_failures.append((test, err))

    def addSuccess(self, test):

        self._pam_successes.append(test)


class TimeoutError(Exception):
    '''TODO: does it have to shadow the built-in?'''

    pass


class Timeout:
    ''' A wrapper class to prevent functions from infinite loops.
    '''

    def __init__(self, action, timeoutLimit=DEFAULT_TIMEOUT):
        ''' (Timeout, function) -> NoneType
        Wraps a function action to prevent it from timing out when called.
        '''

        self._action, self._limit = action, timeoutLimit

    @staticmethod
    def _timeout(signum, frame):
        ''' (int, str) -> NoneType
        Raises a TimeoutError.
        '''

        raise TimeoutError('Test timed out.')

    def __call__(self, *argss, **kwargss):
        ''' (Timeout, ..) -> object
        Calls the wrapped function.
        '''

        signal.signal(signal.SIGALRM, Timeout._timeout)
        signal.alarm(self._limit)

        try:
            return self._action(*argss, **kwargss)
        finally:
            signal.alarm(0)


def _fully_qualified_name(obj):
    '''There must be a better way. TODO: find it.'''

    return '{}.{}'.format(type(obj).__module__, type(obj).__name__)


if __name__ == '__main__':

    # get args
    PARSER = argparse.ArgumentParser(
        description=('Grades an individual student submission ' +
                     'in the current directory.'))
    PARSER.add_argument('target',
                        help='Path to write out resulting JSON string')
    PARSER.add_argument('-t',
                        '--timeout',
                        nargs='?',
                        help='Number of seconds before timing out testMethod',
                        default=DEFAULT_TIMEOUT)
    PARSER.add_argument('-v',
                        '--verbosity',
                        nargs='?',
                        help='The level of verbosity of test results required',
                        default=DEFAULT_VERBOSITY)
    PARSER.add_argument('unittestfile',
                        nargs='+',
                        help='Test files to run')
    ARGS = PARSER.parse_args()

    # create TestResult
    RESULT = TestResult(ARGS.unittestfile,
                        int(ARGS.timeout),
                        int(ARGS.verbosity))
    # write json out
    try:
        with open(ARGS.target, 'w') as tgt:
            tgt.write('{}\n'.format(RESULT.to_json()))
    except IOError as error:
        print('Could not write JSON result to file. {}'.format(error),
              file=sys.stderr)
