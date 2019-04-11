import subprocess


def main():
    # log = open('output_pipe', 'w+')
    proc = subprocess.Popen(['python3', '-i'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
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


main()
