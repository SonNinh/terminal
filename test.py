import subprocess


def main():
    proc = subprocess.Popen(['python3', '-i'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # To avoid deadlocks: careful to: add \n to output, flush output, use
    # readline() rather than read()
    proc.stdin.write('print(123)\n'.encode())
    proc.stdin.flush()
    print(proc.stdout.readline().decode())
    # for _ in range(12):
    proc.stdin.write(b'len("foasdobar")\n')
    proc.stdin.flush()
    print(proc.stdout.readline().decode())

    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)


main()
