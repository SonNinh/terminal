import subprocess
import os
from threading import Thread
import time
from datetime import datetime


def threadout(name, output):
    while True:
        print('fg')
        o = output.readline().decode()

        if o:
            print(o)
    # print('a')
    # for line in proc.stdout:
    #     print(line)
    # print('b')


def main():
<<<<<<< HEAD

=======
    # log = open('output_pipe', 'w+')
>>>>>>> 548ca1b5a13989189013e4511d3f8b69696aadc3
    proc = subprocess.Popen(['python3', '-i'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
<<<<<<< HEAD
    # proc.stdin.write('import os\n'.encode())
    # proc.stdin.flush()
    # print(proc.stdout.readline().decode())
    # # for _ in range(12):
    # proc.stdin.write('len("foasdobar")\n'.encode())
    # proc.stdin.flush()
    # print(proc.stdout.readline().decode())

    thread1 = Thread(target=threadout, args=('Thread-1', proc.stdout))
    thread1.start()

    # cmd = ['len("foasdobar")\nlen("foasdobar")\n', 'os.environ["HOME"]\n']

    cmd = ['len("foasdobar")\n', 'import os\n', 'import sys\n', 'len("foasdobar")\nlen("fsdobar")\n', 'os.environ["HOME"]\n']

    for c in cmd:
        proc.stdin.write(c.encode())
        proc.stdin.flush()
        # for line in proc.stdout:
        #     # print('b')
        #     print(line)
        # print(proc.stdout.readline().decode())
    while False:
        print("a")
        proc.stdin.write((input()+'\nprint("")\n').encode())
        proc.stdin.flush()
        # time.sleep(0.2)
        for line in proc.stdout:
            # print('b')
            print(line.decode())
        # print(proc.stdout.readline().decode())
        # for line in iter(proc.stdout.readline, ""):
        #     print(line)


    # proc.stdin.close()
    # proc.terminate()
    # proc.wait(timeout=0.2)
=======
    # proc.stdin.write(b'import os\n')
    # proc.stdin.flush()
    # ret_code = proc.wait()
    # while True:
    #     ret = proc.poll()
    #     if ret != None:
    #         break
    # log.flush()
    # print('hi')
    # print(proc.stdout)
    # ret = proc.poll()
    # print(ret)
    # print(proc.stdout.readline().decode())
    # proc.stdout.flush()
    # print(proc.stdout.readline().decode())
    # ret = proc.poll()
    # print(ret)
    
    # proc.stdin.write('import os\nos.environ[\'HOME\']\n'.encode())
    # proc.stdin.flush()
    # print(proc.stdout.readline().decode())

    # for _ in range(12):
    # proc.stdin.write(b'len("foasdobar")\n')
    # proc.stdin.flush()
    # print(proc.stdout.readline().decode())

    cmd = ['len("asd")\n', 'import os\n', 'os.environ["HOME"]\n']
    while True:
        proc.stdin.write((input()+'\n').encode())
        proc.stdin.flush()
        print(proc.stdout.readline().decode())
        
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)
>>>>>>> 548ca1b5a13989189013e4511d3f8b69696aadc3


main()
