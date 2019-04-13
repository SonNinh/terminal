from subprocess import *
import sys
import threading
import time
import pty, os


def daemon():
    p = Popen('python3',
              stdout=PIPE,
              stderr=STDOUT,
              stdin=PIPE,
              universal_newlines=True, bufsize=1)
    # p.communicate('print(\'helloWorld\')'.encode())
    # res = p.communicate(input='print(\'helloWorld\')'.encode())
    # print(res[0])
    # p = Popen('ls',
    #           stdout=PIPE,
    #           stderr=STDOUT,
    #           stdin=PIPE)
    # res = p.communicate(input='python3 fucker.py'.encode())\
    command = ['import os\n', 'print(os.environ[\'HOME\'])\n', 'print(\'SONNinh\')\n', 'print(\'helloWorld\')\n']
    for c in command:
        print(c, file=p.stdin, flush=True)
        print(p.stdout.readline(), end='')
        # stdin_handle.write(c.encode())
        # res = p.stdout.readline()
        # p.stdin.close()
        # res = p.stdout.read()
        # print(stdout_handle.read().decode())
        # p.stdin.open()
    # res = p.communicate()
    # for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
    #     print(line)


daemon()
