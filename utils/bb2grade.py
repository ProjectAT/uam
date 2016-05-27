#!/usr/bin/env python3

'''
Read a Blackboard file in format
    utorid, firstnames, lastname, studentnumber, anything else ...
and print to stdout the corresponding lines of a gf file.
'''

import sys
import csv

if len(sys.argv) != 2:
    print('Usage: bb2grade classlist.csv [ > stdoutfile]', file=sys.stdout)
    exit(1)

with open(sys.argv[1], 'U') as infile:
    for line in csv.reader(infile):
        if len(line) < 4:
            print('Invalid input file. Each line must have at least 4 values.')
            exit(1)
        utorid, first, last, stunum = line[:4]
        print('%s    %s %s,%s' % (stunum.zfill(10), first, last, utorid))
