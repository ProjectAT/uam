"""Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students."""

import os
import sys
import time
from loadclasslist import load_by_utorid

sender = "atafliovich@utsc.utoronto.ca"
sendmail_loc = "/usr/sbin/sendmail"
path_pref = "/cmshome/tafliovi/at/scheme/submissions"

def send_mail(recipient, subject, message_body):
    """ (str, str, str) -> NoneType

    Send an email to recepient with subject subject and message body
    message_body.
    """
    
    # Build the message header
    header = ("From: %s\nTo: %s\nSubject: %s\r\n\r\n" %
              (sender, recipient, subject))

    # Actually send the message
    email = os.popen("%s -t" % (sendmail_loc), "w")
    email.write(header + message_body)
    email_status = email.close()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "python emailmarks.py <classlist> <item>"
        sys.exit(0)

    classlist = sys.argv[1]
    item = sys.argv[2]
    subject = "CSC C24: Marked " + item + " (cycle.py)"

    students = load_by_utorid(classlist)
    #students = load_by_utorid(classlist, "dirsnew.txt")

    for student in students.values():
        result_file = os.path.join(path_pref, item, student.utorid, item, 'result_e4.txt')
        try:
            markfile = open(result_file)
            body = markfile.read()
            markfile.close()
            send_mail(student.email, subject, body)
        except:
            print "No result file for %s." % student.utorid
