#!/usr/bin/python3

''' Report Templator -- a part of the UAM project at UofT
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Author: Anya Tafliovich 2015

Creates both individual and aggregrated human readable reports from an
aggregrated JSON report file given a template file (text, html, gf, etc).
'''

import json
import jinja2
import argparse
import os
import sys
import re
import config

DEFAULT_TEMPLATE_TYPE = 'txt'
DEFAULT_AGGREGATE_TEMPLATE = 'aggregated.tpl'
DEFAULT_INDIVIDUAL_TEMPLATE = 'individual.tpl'
DEFAULT_JINJA_EXTENSIONS = ['jinja2.ext.do']
DEFAULT_REPORT_NAME = 'report.txt'


class AggregatedReport:
    '''A human readable, templated, aggregated report (of all test
    results for all student submissions).

    '''

    def __init__(self, reports, plugins=None,
                 templateType=DEFAULT_TEMPLATE_TYPE,
                 aggregateTemplateFile=DEFAULT_AGGREGATE_TEMPLATE,
                 individualTemplateFile=DEFAULT_INDIVIDUAL_TEMPLATE):

        if plugins is None:
            plugins = []

        self._data, self._type = reports, templateType

        # set up jinja2 environment
        self._env = _set_up_jinja_env(templateType, plugins)

        # load template
        try:
            self._template = self._env.get_template(aggregateTemplateFile)
        except Exception as e:
            self._template_error = e
            self._template = None

        # build a dict of all IndividualReports
        self._individualReports = {
            report['origin']: IndividualReport(report,
                                               self._env,
                                               plugins,
                                               templateType,
                                               individualTemplateFile)
            for report in reports['results']}

    def write_aggregate(self, target):
        ''' (AggregatedReport, str) -> NoneType
        Writes this AggregatedReport out to the file specified by target.
        '''

        if self._template:
            open(target, 'w').write(str(self))
        else:
            raise self._template_error

    def write_individual(self, target):
        ''' (AggregatedReport, str) -> NoneType
        Write all individual reports to target.
        '''

        for report in self._individualReports.values():
            report.write(target)

    def __str__(self):
        ''' (AggregatedReport) -> str
        Renders this AggregatedReport.
        '''

        try:
            return self._template.render(result=self._data)
        except Exception as e:
            print('Error: Unable to generate aggregated report. %s' % e,
                  file=sys.stderr)

    @staticmethod
    def fromJson(sourceJson, templateType, plugins=None):
        '''Produces an AggregatedReport from the given aggregated JSON file at
        sourceJson using the given templateType.
        '''

        if plugins is None:
            plugins = []

        try:
            json_report = json.loads(open(sourceJson).read())
        except IOError as e:
            print("Cannot open json file. %s" % e, file=sys.stderr)
            raise e
        except Exception as e:
            print("Cannot load json file. %s" % e, file=sys.stderr)
            raise e

        return AggregatedReport(json_report,
                                plugins,
                                templateType)


class IndividualReport:
    ''' A human readable, templated, individual report of test results.
    '''

    def __init__(self, report, env=None, plugins=None,
                 templateType=DEFAULT_TEMPLATE_TYPE,
                 templateFile=DEFAULT_INDIVIDUAL_TEMPLATE,
                 origin=None):

        if plugins is None:
            plugins = []

        if env is None:
            self._env = _set_up_jinja_env(templateType, plugins)
        else:
            self._env = env

        self._data, self._type = report, templateType

        # load template
        try:
            self._template = self._env.get_template(templateFile)
        except Exception as e:
            self._template_error = e
            self._template = None

        if origin:  # in case this report was not "aggregated"
            self._data['origin'] = origin

    def write(self, target):
        ''' (IndividualReport, str) -> NoneType
        Writes this IndividualReport out to the file specified by target.
        '''

        if self._template:
            open(os.path.join(self._data['origin'], target),
                 'w').write(str(self))
        else:
            raise self._template_error

    def __str__(self):
        ''' (IndividualReport) -> str
        Renders this IndividualReport.
        '''

        try:
            return self._template.render(result=self._data)
        except Exception as e:
            print('Warning: Unable to generate individual report for %s: %s.'
                  % (self._data['origin'], e),
                  file=sys.stderr)

    @staticmethod
    def fromJson(sourceJson, plugins=None,
                 templateType=DEFAULT_TEMPLATE_TYPE,
                 templateFile=DEFAULT_INDIVIDUAL_TEMPLATE,
                 origin=None):
        '''Produces an IndividualReport from the given aggregated JSON file at
        sourceJson using the given templateType.
        '''

        if plugins is None:
            plugins = []

        try:
            json_report = json.loads(open(sourceJson).read())
        except IOError as e:
            print("Cannot open json file. %s" % e, file=sys.stderr)
            raise e
        except Exception as e:
            print("Cannot load json file. %s" % e, file=sys.stderr)
            raise e

        return IndividualReport(json_report,
                                None,
                                plugins,
                                templateType,
                                templateFile,
                                origin)


def _set_up_jinja_env(templateType, plugins):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(config.template_dir, templateType)),
        extensions=DEFAULT_JINJA_EXTENSIONS)

    # populate jinja environment with our custom filters
    for plugin in plugins:
        env.filters[plugin.__name__.lower()] = plugin

    return env

###############################################################################
# custom filters for jinja2 defined below
# TODO: clean up hacky stuff!


def studentList(students, format_str, fields):
    ''' (list of dict, str, list of str) -> list of str
    Prepares a list of student fields from a list of dictionaries representing
    aggregator.UTSCStudents in the given format with respective fields.
    '''

    return [format_str % tuple([student.get(field) for field in fields])
            for student in students]


def getAllCounts(results, select):
    ''' (dict of dicts) -> int
    Gets either the number of passes, failures, errors, and total of the given
    results dictionary depending on select (from the respective order) for all
    TestCases.
    '''

    return sum([getCounts(test, select) for test in results.values()])


def getCounts(results, select):
    ''' (dict of dicts/lists) -> int
    Gets either the number of passes, failures, errors, or total of the given
    results dictionary depending on select (from the respective order) for a
    single TestCase.
    '''
    select = ['passes', 'failures', 'errors', 'total'][select]

    return (len(results.get(select)) if results.get(select) else 0
            if select != 'total' else
            sum([getCounts(results, i) for i in range(3)]))


def ljust(text, amount, offsetAfterFirst=0):
    ''' (str, int) -> str
    Pads the given text with spaces on the left until its length is the given
    amount -- in otherwords, right justify text. Every line after the first
    will be offset to the left offsetAfterFirst spaces.
    '''

    return '\n'.join([line.ljust(amount + int(bool(i)) * offsetAfterFirst)
                      for i, line in enumerate(text.split('\n'))])


def toGfNames(name):
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

    return [element for element in collection
            if not _isExcluded(element, exclusions)]


def _isExcluded(word, exclusions):
    ''' (str, list of str) -> bool
    Determines whether word contains any string from exclusions.
    '''

    return any([exclusion in word for exclusion in exclusions])


def passed(testName, results):
    ''' (str, dict{str:dict{str: dict{str: str or dict}}}) -> int
    Returns 1 if the test testName is a key in any TestCase's passes dict
    in results and 0 otherwise.
    '''

    # flatten passes from all TestCases
    passes = set()
    [passes.update((testCase.get('passes') or {}).keys())
     for testCase in results.values()]

    return int(testName in passes)


def getBalancedWeight(tests):
    ''' (list) -> int
    Calculates the equally weighted value of an individual test from a
    collection of tests.
    '''

    return round(1 / len(tests) * 100, 3)


if __name__ == '__main__':

    help_all = 'If neither -i nor -a are specified, all reports are generated.'

    # get options
    parser = argparse.ArgumentParser(
        description=('Convert an aggregated JSON file ' +
                     'into human readable format'))
    parser.add_argument('-i', '--individual', action="store_true",
                        help=('Produce a single individual report. ' +
                              help_all))
    parser.add_argument('-a', '--aggregate', action="store_true",
                        help=('Produce a single aggregated report. ' +
                              help_all))
    parser.add_argument('source_json',
                        help='Path to (aggregated or individual) JSON file')
    parser.add_argument('template_type',
                        help='Type of template to use (txt/gf/markus)')
    parser.add_argument('output_file_name', nargs='?',
                        help='Filename for templated report output',
                        default=DEFAULT_REPORT_NAME)
    args = parser.parse_args()

    plugins = [studentList, getAllCounts, getCounts, ljust,
               toGfNames, exclude, passed, getBalancedWeight]

    if args.individual:
        try:
            individual_report = IndividualReport.fromJson(
                args.source_json,
                plugins,
                args.template_type,
                DEFAULT_INDIVIDUAL_TEMPLATE,
                os.path.dirname(args.source_json))
            individual_report.write(args.output_file_name)
            exit(0)
        except Exception as e:
            print("Cannot create an Individual report. %s" % e,
                  file=sys.stderr)

    try:
        aggregate_report = AggregatedReport.fromJson(args.source_json,
                                                     args.template_type,
                                                     plugins)
    except Exception as e:
        print("Cannot create an Aggregate report. %s" % e, file=sys.stderr)
        exit(1)

    try:
        aggregate_report.write_aggregate(args.output_file_name)
    except jinja2.exceptions.TemplateSyntaxError as e:
        print('Could not write aggregate report. ' +
              'Template has syntax issues. %s' % e,
              file=sys.stderr)
    except jinja2.exceptions.TemplateNotFound as e:
        print('Could not write aggregate report. ' +
              'Template is not installed. %s' % e,
              file=sys.stderr)

    try:
        if not args.aggregate and not args.individual:
            aggregate_report.write_individual(args.output_file_name)
    except jinja2.exceptions.TemplateSyntaxError as e:
        print('Could not write individual report(s). ' +
              'Template has syntax issues. %s' % e,
              file=sys.stderr)
    except jinja2.exceptions.TemplateNotFound as e:
        print('Could not write individual report(s). ' +
              'Template is not installed. %s' % e,
              file=sys.stderr)
