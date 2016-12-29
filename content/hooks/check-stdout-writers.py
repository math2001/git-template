#!python
# -*- encoding: utf-8 -*-

import os
import re
import sys

RED = '\x1b[31m'
BRIGHT = '\x1b[1m'
RED_BRIGHT = RED + BRIGHT
GREEN_BRIGHT = '\x1b[32m' + '\x1b[1m'
RESET = '\x1b[0m'
NORMAL = '\x1b[22m'

cmd = os.popen('git ls-files')
output = cmd.read().splitlines()

def find(pattern, file, is_word=True):
    _pattern = re.escape(pattern)
    if is_word:
        _pattern = r'(\W|^)' + _pattern + r'(\W|$)'
    with open(file) as fp:
        content = fp.read()
        for line in content.splitlines()[:2]:
            if 'CSW: ignore' in line:
                return None, content
        return re.finditer(_pattern, content, re.MULTILINE), content

def get_rowcol(content, point):
    """return a tuple: (<line>, <char_nb>) where char_nb is from the beginning of the line"""
    line = 0
    line_char = 0
    for i, char in enumerate(content):
        if i == point:
            return line, line_char
        line_char += 1
        if char == '\n':
            line += 1
            line_char = 0

def show_error(found, match, content, file):
    nb_line, nb_char = get_rowcol(content, match.start() + 1)
    print(RED + 'CSW: found a {bright}{!r}{normal} line {bright}{!r}{normal} '
        'in {bright}{!r}{normal}'.format(found, nb_line + 1, file, bright=BRIGHT, normal=NORMAL) + RESET)

def checkfile(file):
    checkers = [
        {
            'ext': ['js', 'coffee'],
            'ows': ['console.log']
        },
        {
            'ext': ['py'],
            'ows': ['print']
        },
        {
            "ext": ["php"],
            "ows": ["echo", "print", "var_dump"]
        }
    ]
    valid = True
    name, ext = os.path.splitext(file)
    for checker in checkers:
        if ext[1:] in checker['ext']:
            for ow in checker['ows']:
                matches, content = find(ow, file)
                if matches is None: continue
                for match in matches:
                    show_error(ow, match, content, file)
                    valid = False

    return valid


errors = 0
for line in output:
    if not checkfile(line):
        errors += 1

if errors > 0:
    print('Found {} stdout writer{}'.format(errors, 's' if errors > 1 else ''))
    with open('.git/prev_uncommitted_msg.txt', 'w') as fpw:
        with open(sys.argv[1], 'r') as fpr:
            fpw.write(fpr.read())
    exit(1)
else:
    print(GREEN_BRIGHT + 'CSW: OK' + RESET)
