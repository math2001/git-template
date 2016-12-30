#!python
# -*- encoding: utf-8 -*-

import os
import sys

def insert_text(file_path, text, caret_pos):
    with open(file_path, 'r') as fp:
        content = fp.read()
    content = content[:caret_pos] + text + content[caret_pos:]
    with open(file_path, 'w') as fp:
        fp.write(content)

if os.path.isfile('.git/prev_uncommitted_msg.txt'):
    with open('.git/prev_uncommitted_msg.txt') as fp:
        insert_text(sys.argv[1], fp.read(), 0)
    os.remove('.git/prev_uncommitted_msg.txt')
