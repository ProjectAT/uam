#!/usr/bin/python3

# Modified by A. Tafliovich to use python 3 and to generate 10-digit
# student numbers.

# Read a Blackboard grade-centre file (saved as "Comma Separated Values") and
# write to standard output lines that would be the corresponding student
# records in a DCS grade file. The input file name is the single command-line
# argument:
#
#   bb2grade gradecentrefile.csv
#
# The input lines in the grade centre file are assumed to contain these
# fields, separated by commas:
# UTORid, given names, family name, student number, others.
# We don't need the others, so we just keep the UTORid as a "mark".
#
# Skips all malformed lines (including the BlackBoard header).
#
# Jim Clarke, Feb 2011

import sys, csv

if len(sys.argv) != 2:
    print('Usage: bb2grade bbgrades.csv [ > stdoutfile]', file=sys.stderr)
    sys.exit(1)

reader = csv.reader(open(sys.argv[1], 'U')) # 'U' is universal-newline mode

for line in reader:
    utorid, given, family, stunum = line[:4]
    if not stunum[0].isdigit():
        print('Warning: malformed line: %s' % line, file=sys.stderr)
        continue
    stunum = stunum.zfill(10)
    output_line = stunum + '    ' + family + '  ' + given + '\t' + utorid
    print(output_line)
