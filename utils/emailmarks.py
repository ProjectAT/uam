'''Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students.

'''

import argparse
import os
from utils import load_bb

DEFAULT_SENDER = 'atafliovich@utsc.utoronto.ca'
DEFAULT_SENDMAIL_LOC = '/usr/sbin/sendmail'


def send_mail(recipient, subject, message_body, sender=DEFAULT_SENDER,
              sendmail_loc=DEFAULT_SENDMAIL_LOC):
    '''(str, str, str) -> NoneType

    Send an email to recepient with subject line subject and message
    body message_body.

    '''

    # Build the message header
    header = ('From: %s\nTo: %s\nSubject: %s\r\n\r\n' %
              (sender, recipient, subject))

    # Actually send the message
    with os.popen('%s -t' % (sendmail_loc), 'w') as email:
        email.write(header + message_body)


def send_mails(students, subject, path_pref, path_suff):
    '''({str: Student}, str, str, str) -> NoneType

    Send an email to each student in the dictionary of Students (by
    student_id), with subject subject and the message body being the
    contents of a file path_pref/Student.utorid/path_suff.

    '''

    for student in students.values():
        try:
            with open(os.path.join(path_pref,
                                   student.student_id,
                                   path_suff)) as markfile:
                body = markfile.read()
        except IOError as error:
            print('No result for %s: %s' % (student.student_id, error))

        send_mail(student.email, subject, body)


if __name__ == '__main__':

    # get args
    PARSER = argparse.ArgumentParser(
        description=('Email contents of result files to students.\n'))
    PARSER.add_argument('-s', '--subject', help='The subject line.')
    PARSER.add_argument(
        '-c', '--classlist',
        help='Path to the classlist file in BlackBoard format.')
    PARSER.add_argument(
        '-p', '--path_prefix',
        help=('Prefix of the path to the file to email: ' +
              'up to student submission directory.'))
    PARSER.add_argument(
        '-s', '--path_suffix',
        help=('Sufffix of the path to the file to email: ' +
              'from the student submission directory.'))
    ARGS = PARSER.parse_args()

    # email
    with open(ARGS.classlist) as clslist:
        send_mails(load_bb(clslist),
                   ARGS.subject,
                   ARGS.path_prefix if ARGS.path_prefix else '',
                   ARGS.path_suffix if ARGS.path_suffix else '')
