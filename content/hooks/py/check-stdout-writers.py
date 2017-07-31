#!python
# -*- encoding: utf-8 -*-

import os
import re
import sys

BRIGHT = '\x1b[1m'

RED = '\x1b[31m'
BLUE = '\x1b[34m'
YELLOW = '\x1b[33m'
GREEN = '\x1b[32m'

RED_BRIGHT = RED + BRIGHT
GREEN_BRIGHT = GREEN + BRIGHT
BLUE_BRIGHT = BLUE + BRIGHT
RESET = '\x1b[0m'
NORMAL = '\x1b[22m'

cmd = os.popen('git diff --cached --name-only')
output = cmd.read().splitlines()

def stop(msg=None):
    with open('.git/prev_uncommitted_msg.txt', 'w') as fpw:
        with open(sys.argv[1], 'r') as fpr:
            fpw.write(fpr.read())
    if msg is not None:
        print(msg)
    sys.exit(1)


def confirm(text):
    ans = input(text + ' (y/n) ')
    if ans.lower() in ('y', 'yes'):
        return True
    elif ans.lower() in ('n', 'no'):
        return False
    else:
        return confirm(text)

def find(pattern, file, is_word=True):
    _pattern = re.escape(pattern)
    if is_word:
        _pattern = r'(CSW: ignore\n)?\s*(\W|^)' + _pattern + r'(\W|$)'
    try:
        with open(file, encoding='utf8') as fp:
            content = fp.read()
    except FileNotFoundError:
        if confirm(YELLOW + "CSW: The file {!r} wasn't found. Abort?".format(file) + RESET):
            stop(RED_BRIGHT + 'Abort')
    except UnicodeError:
        if confirm(YELLOW + 'CSW: Not able to read the file {!r} because of a unicode error. Abort?'.format(file) + RESET):
            stop(RED_BRIGHT + 'Abort')
    except Exception as e:
        if confirm(YELLOW + 'CSW: An unexpected error as occured: {!r}'.format(e.__class__.__name__) + RESET):
            stop(RED_BRIGHT + 'Abort')
    else:
        for line in content.splitlines()[:2]:
            if 'CSW: ignore *' in line:
                return None, content
        return re.finditer(_pattern, content, re.MULTILINE), content
    return None, None

def get_rowcol(content, point):
    """return a tuple: (<line>, <char_nb>) where char_nb is from the beginning of the line"""
    line = 0
    line_char = 0
    for i, char in enumerate(content):
        line_char += 1
        if char == '\n':
            line += 1
            line_char = 0
        if i == point:
            return line, line_char

def show_error(found, match, content, file):
    nb_line, nb_char = get_rowcol(content, match.start() + len(match.group(1) or '') + 1)
    print(RED + 'CSW: found a {bright}{!r}{normal} in {bright}{!r}{normal} '
        'line {bright}{!r}{normal}'.format(found, file, nb_line + 1, bright=BRIGHT, normal=NORMAL) + RESET)

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
    nb_error = 0
    name, ext = os.path.splitext(file)
    for checker in checkers:
        if ext[1:] in checker['ext']:
            for ow in checker['ows']:
                matches, content = find(ow, file)
                if matches is None: continue
                for match in matches:
                    if match.group(1) is not None:
                        continue # there is a CSW: ignore
                    show_error(ow, match, content, file)
                    nb_error += 1

    return nb_error

errors = 0
for line in output:
    errors += checkfile(line)

if errors > 0:
    print('Found {} stdout writer{}'.format(errors, 's' if errors > 1 else ''))
    stop()
