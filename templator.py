#!/usr/bin/env python3

'''Report Templator.
Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich
Author: Anya Tafliovich 2015, 2016

Given template file(s), create individual and/or aggregrated human
readable reports from an aggregrated JSON report file.

'''

import argparse
import json
import os
import sys

import jinja2

from utils.defaults import (DEFAULT_TEMPLATE_TYPE, DEFAULT_AGGREGATE_TEMPLATE,
                            DEFAULT_INDIVIDUAL_TEMPLATE, DEFAULT_JINJA_EXTENSIONS,
                            DEFAULT_TEMPLATE_DIR, DEFAULT_REPORT_NAME)
from utils.plugins import (student_list, get_all_counts, get_counts, ljust,
                           to_gf_names, exclude, passed, get_balanced_weight)


class TemplatedReport:
    '''Parent class.'''

    def __init__(self,
                 report,
                 template_file,
                 template_dir=DEFAULT_TEMPLATE_DIR,
                 env=None,
                 plugins=None,
                 jinja_extns=None,
                 origin=None):
        '''
        TODO
        report is Dict[str, dict] maps ?
        template_file is the name of the file to use for templating
        template_dir is the directory that contains template files
        env id a jinja environment
        plugins is a list of functions
        jinja_extns is jinja extensions
        '''

        self._report = report

        if plugins is None:
            plugins = []

        self._template = _load_template(env, template_dir,
                                        template_file, plugins, jinja_extns)

        if origin:
            self._report['origin'] = origin  # inject origin

    def write(self, target):
        '''Write this TemplatedReport out to target.
        target is a path to the output file.
        '''

        if self._template:
            try:
                with open(target, 'w') as trgt:
                    trgt.write(str(self))
            except IOError as err:
                print('Cannot generate report {}: {}'.format(target, err))
        else:
            print('Warning: cannot generate report {}. No template file.'.format(target),
                  file=sys.stderr)

    def __str__(self):

        return self._template.render(result=self._report)


class IndividualReport(TemplatedReport):
    ''' A human readable, templated, individual report of test results.
    '''

    def __init__(self,
                 report,
                 template_file,
                 template_dir=DEFAULT_TEMPLATE_DIR,
                 env=None,
                 plugins=None,
                 jinja_extns=None,
                 origin=None):
        '''
        TODO
        '''

        TemplatedReport.__init__(self, report, template_file, template_dir,
                                 env, plugins, jinja_extns, origin)

    def write(self, target):
        '''Write this IndividualReport out to target.
        target is a path to the output file.
        '''

        TemplatedReport.write(self,
                              os.path.join(self._report['origin'], target))

    @staticmethod
    def from_json(source_json,
                  template_file,
                  template_dir=DEFAULT_TEMPLATE_DIR,
                  plugins=None,
                  jinja_extns=None,
                  origin=None):
        '''Create an IndividualReport from the individual JSON file at
        source_json, using template_file for templating.

        '''

        try:
            with open(source_json) as source:
                json_report = json.loads(source.read())
        except IOError as err:
            print('Cannot open individual json file: {}'.format(err),
                  file=sys.stderr)
            raise err

        return IndividualReport(json_report,
                                template_file,
                                template_dir,
                                None,
                                plugins,
                                jinja_extns,
                                origin)


class AggregateReport(TemplatedReport):
    '''A human readable, templated, aggregated report (of all test
    results for all student submissions).

    '''

    def __init__(self,
                 report_dict,
                 template_file,
                 template_dir=DEFAULT_TEMPLATE_DIR,
                 plugins=None,
                 jinja_extns=None):
        '''
        TODO
        '''

        TemplatedReport.__init__(self, report_dict, template_file,
                                 template_dir, None, plugins, jinja_extns,
                                 None)

    @staticmethod
    def from_json(source_json,
                  template_file,
                  template_dir=DEFAULT_TEMPLATE_DIR,
                  plugins=None,
                  jinja_extns=None):
        '''Create an AggregatelReport from aggregate JSON file at source_json,
        using template_file for templating.

        '''

        try:
            with open(source_json) as source:
                json_report = json.loads(source.read())
        except IOError as err:
            print('Cannot open aggregate json file: {}'.format(err),
                  file=sys.stderr)
            raise err

        return AggregateReport(json_report,
                               template_file,
                               template_dir,
                               plugins,
                               jinja_extns)


class IndividualReports:
    '''A collection of human readable, templated, individual reports (of
    test results).

    '''

    def __init__(self,
                 report_dict,
                 template_file,
                 template_dir=DEFAULT_TEMPLATE_DIR,
                 plugins=None,
                 jinja_extns=None):
        '''
        TODO
        '''

        self._individual_reports = {
            report['origin']: IndividualReport(report,
                                               template_file,
                                               template_dir,
                                               None,
                                               plugins,
                                               jinja_extns,
                                               None)
            for report in report_dict['results']}

    def write(self, target):
        '''Write all individual reports to target.
        target is a file object.
        '''

        for report in self._individual_reports.values():
            report.write(target)

    @staticmethod
    def from_json(source_json,
                  template_file,
                  template_dir=DEFAULT_TEMPLATE_DIR,
                  plugins=None,
                  jinja_extns=None):
        '''CreateIndividualReports from aggregate JSON file at source_json,
        using template_file for templating.

        '''

        try:
            with open(source_json) as source:
                json_report = json.loads(source.read())
        except IOError as err:
            print('Cannot open aggregate json file: {}'.format(err),
                  file=sys.stderr)
            raise err

        return IndividualReports(json_report,
                                 template_file,
                                 template_dir,
                                 plugins,
                                 jinja_extns)


def _load_template(env, template_dir, template_file, plugins, jinja_extns):
    if env is None:
        env = _set_up_jinja_env(template_dir, plugins, jinja_extns)

    try:
        return env.get_template(template_file)
    except jinja2.TemplateNotFound:
        return None


def _set_up_jinja_env(template_dir, plugins, jinja_exts):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=jinja_exts)

    # populate jinja environment with our custom filters
    for plugin in plugins:
        env.filters[plugin.__name__.lower()] = plugin

    return env


def individual_report(source, plugins, template_file,
                      template_dir, jinja_extns, origin, output):
    '''Template an individual report given an individual json.'''

    report = IndividualReport.from_json(source,
                                        template_file,
                                        template_dir,
                                        plugins,
                                        jinja_extns,
                                        origin)
    report.write(output)


def aggregate_report(source, plugins, template_file, template_dir,
                     jinja_extns, output):
    '''Template an aggregate report given an aggregate json.'''

    report = AggregateReport.from_json(source,
                                       template_file,
                                       template_dir,
                                       plugins,
                                       jinja_extns)
    report.write(output)


def individual_reports(source, plugins, template_file,
                       template_dir, jinja_extns, output):
    '''Template all individual reports given an aggregate json.'''

    reports = IndividualReports.from_json(source,
                                          template_file,
                                          template_dir,
                                          plugins,
                                          jinja_extns)
    reports.write(output)


def check_arguments(args):
    '''TODO: write me.'''

    pass


def arguments():
    '''Parse command line arguments.'''

    help_all = 'If neither -i nor -a are specified, all reports are generated.'

    # get options
    parser = argparse.ArgumentParser(
        description=('Convert JSON file(s) (individual, aggregated or both) '
                     'into human readable format using templates.'))
    parser.add_argument('-i', '--individual', action='store_true',
                        help='Produce a single individual report. {}'.format(help_all))
    parser.add_argument('-a', '--aggregate', action='store_true',
                        help='Produce a single aggregated report. {}'.format(help_all))
    parser.add_argument('-o', '--output',
                        help='Filepath for templated report output.',
                        default=DEFAULT_REPORT_NAME)
    parser.add_argument('--template_dir',
                        help='Directory that contains the templates. {}'.format(
                            help_all),
                        default=DEFAULT_TEMPLATE_DIR)
    parser.add_argument('--template_individual',
                        help=('Filepath for template file to use for templating individual '
                              'reports. {}').format(help_all),
                        default=DEFAULT_INDIVIDUAL_TEMPLATE)
    parser.add_argument('--template_aggregate',
                        help=('Filepath for template file to use for templating aggregate '
                              'reports. {}').format(help_all),
                        default=DEFAULT_AGGREGATE_TEMPLATE)
    parser.add_argument('--jinja_extensions', help='Jinja extensions.',
                        default=DEFAULT_JINJA_EXTENSIONS)
    parser.add_argument('source_json',
                        help='Path to (aggregated or individual) JSON file.')
    parser.add_argument('template_type', nargs='?',
                        help='Type of template to use (txt/gf/markus/html).',
                        default=DEFAULT_TEMPLATE_TYPE)
    return parser.parse_args()


if __name__ == '__main__':

    PLUGINS = [student_list, get_all_counts, get_counts, ljust,
               to_gf_names, exclude, passed, get_balanced_weight]

    ARGS = arguments()
    check_arguments(ARGS)

    OUTPUT = '{}.{}'.format(ARGS.output, ARGS.template_type)

    if ARGS.individual:
        individual_report(ARGS.source_json,
                          PLUGINS,
                          os.path.join(ARGS.template_type,
                                       ARGS.template_individual),
                          ARGS.template_dir,
                          ARGS.jinja_extensions,
                          os.path.dirname(ARGS.source_json),
                          OUTPUT)
        exit(0)

    aggregate_report(ARGS.source_json,
                     PLUGINS,
                     os.path.join(ARGS.template_type, ARGS.template_aggregate),
                     ARGS.template_dir,
                     ARGS.jinja_extensions,
                     OUTPUT)

    if not ARGS.aggregate and not ARGS.individual:
        individual_reports(ARGS.source_json,
                           PLUGINS,
                           os.path.join(ARGS.template_type,
                                        ARGS.template_individual),
                           ARGS.template_dir,
                           ARGS.jinja_extensions,
                           OUTPUT)
