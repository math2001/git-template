#!python

# the path to your python.exe

import sys, os

if len(sys.argv) >= 1:
    exit(0)
message_file = sys.argv[1]


with open(message_file) as fp:
    for i, line in enumerate(fp):
        if i == 0 and len(line) > 50:
            print('fatal: the first line of your commit should have less than 50 chars. Got {}.'.format(len(line)))
            sys.exit(1)
        elif len(line) > 72:
            print('fatal: your lines shouldn\'t have more than 72 chars. Got {}.'.format(len(line)))
            sys.exit(1)
