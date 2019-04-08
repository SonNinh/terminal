import sys
from subprocess import Popen, PIPE

with Popen(['python3'], stdin=PIPE, stdout=PIPE,
           universal_newlines=True, bufsize=1) as cat:
    for input_string in ["print(\'sdfsndf\')", "print(12)", ""]:
        print(input_string, file=cat.stdin, flush=True)
        print(cat.stdout.readline(), end='')
