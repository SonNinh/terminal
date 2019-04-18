import subprocess
from time import sleep


def main():

    p = subprocess.Popen("python3 -i".split(),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    p.stdin.write(("exit()"+'\n').encode())
    p.stdin.flush()
    # sleep(1)
    # p.stdin.write(("sfsf"+'\n').encode())
    # p.stdin.flush()
    # p.wait()
    while p.poll() is None:
        print("running")
    print("end")
    p.terminate()

main()
