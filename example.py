import curses
import curses.textpad
import subprocess
from threading import Thread
from time import sleep
from datetime import datetime

from os import environ, path
import cdCommand
import printenvCommand
import globbing
import dynamic
from math import fabs


class Screen(object):
    def __init__(self):
        self.window = None

        self.width = 0
        self.height = 0
        self.init_curses()
        self.prompt_name = 'intek-sh:{}$ '.format(environ['PWD'].replace(environ['HOME'], '~'))
        self.text = 'intek-sh:{}$ '.format(environ['PWD'].replace(environ['HOME'], '~'))
        self.lk = 0
        self.touch_ending = True
        self.last_char = -1
        self.up_last = -1
        self.down_last = -1
        self.command = ''
        self.lim_of_arrow = 0
        self.pos_cursor_str = 0
        self.in_sub = False
        self.p = None
        self.turnback = ''
        self.end_thread = False
        self.on_display = False

    def init_curses(self):
        self.window = curses.initscr()
        self.window.keypad(True)
        self.window.scrollok(True)
        self.window.timeout(50)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        self.current = curses.color_pair(2)
        self.height, self.width = self.window.getmaxyx()

    def input_stream(self):
        '''
        main function
        '''
        if not self.on_display:
            self.update_screen()
        new_key = self.window.getch()

        self.lk = new_key
        if new_key == curses.KEY_UP:
            if self.touch_ending:
                # if all line in window have been filled
                self.last_char = self.up_last
                # self.update_screen()
        elif new_key == curses.KEY_DOWN:
            self.last_char = self.down_last
            # self.update_screen()
        elif new_key == 9:
            # button 'tab'
            self.dynamic_completion()
        elif new_key == 10:
            # if button 'enter' was pressed
            # self.update_screen()
            self.last_char = -1
            self.up_last = -1
            self.down_last = -1
            self.play_subprocess()
            # self.update_screen()
        elif new_key < 127 and new_key > 31:
            # if normal key was pressed
            self.last_char = -1
            self.up_last = -1
            self.down_last = -1
            self.insert_new_key(new_key)
            # self.update_screen()
        elif new_key == 260 and self.pos_cursor_str > self.lim_of_arrow:
            # if left arrow was pressed and cursor's position has not been over upper limitation
            self.pos_cursor_str -= 1
            # self.move_cursor_back()
        elif new_key == 261 and self.pos_cursor_str < 0:
            # if left arrow was pressed and cursor's position has not been over lower limitation
            self.pos_cursor_str += 1
        elif new_key == 127:
            # ubuntu 263 Macos 127
            # if button 'delete' was pressed
            self.delete_char()
            # self.update_screen()
        elif new_key == 262:
            # home button
            self.pos_cursor_str = self.lim_of_arrow
        elif new_key == 360:
            self.pos_cursor_str = 0
        else:
            # any thing else was pressed
            self.update_screen()

    def dynamic_completion(self):
        start_idx, ls_of_possibles, complt_str = dynamic.complete(self.command, self.pos_cursor_str, environ)

        if complt_str:
            if self.pos_cursor_str != 0:
                self.command = self.command[:start_idx] + complt_str + self.command[self.pos_cursor_str:]
                self.text = self.text[:start_idx] + complt_str + self.text[self.pos_cursor_str:]
            else:
                self.command = self.command[:start_idx] + complt_str
                self.text = self.text[:start_idx] + complt_str
            self.lim_of_arrow = -len(self.command)
        if ls_of_possibles:
            for pos in ls_of_possibles:
                self.text += ('\n'+pos.strip('/').split('/')[-1])

            self.text += ('\n' + self.prompt_name + self.command)

    def update_screen(self):
        '''
        update window by new conntent
        '''
        self.on_display = True
        self.text += self.turnback
        self.turnback = ''
        self.height, self.width = self.window.getmaxyx()
        self.update_upper_line()

        win_area = self.height*self.width
        if self.last_char+1 >= 0:
            self.window.addstr(0, 0, self.text[self.last_char-win_area:],
                               curses.color_pair(1))
        else:
            self.window.addstr(0, 0, self.text[self.last_char-win_area:self.last_char+1],
                               curses.color_pair(1))
        self.window.refresh()
        self.window.clrtobot()
        if curses.getsyx()[0] == self.height-1:
            self.touch_ending = True
        else:
            self.touch_ending = False

        self.update_lower_line()

        self.move_cursor_back()
        self.window.refresh()
        self.on_display = False
        # txt = str(self.last_char) + ' ' + str(self.up_last) + ' ' + str(self.down_last) + ' ' + str(self.lk)
        # self.window.addstr(curses.getsyx()[0], curses.getsyx()[1], txt, curses.color_pair(2))
        # self.window.refresh()

    def update_upper_line(self):
        i = self.last_char + 1
        if self.text[i] == '\n':
            i += 1

        for n in range(self.width):
            if i+n < 0 and self.text[i+n] != '\n':
                pass
            else:
                self.down_last = i+n-1
                break

    def update_lower_line(self):
        if self.text[self.last_char] == '\n':
            self.up_last -= 1
        else:
            self.up_last = self.last_char - 1
            if self.text[self.up_last] != '\n':
                self.up_last = self.last_char - curses.getsyx()[1]
                try:
                    if self.up_last == self.last_char:
                        self.up_last -= self.width
                    if self.text[self.up_last] == '\n':
                        self.up_last -= 1
                except IndexError:
                    self.up_last = self.last_char

    def move_cursor_back(self):
        y_cursor, x_cursor = curses.getsyx()

        if -self.pos_cursor_str <= x_cursor:
            self.window.move(y_cursor, x_cursor+self.pos_cursor_str)
        else:
            a = fabs(self.pos_cursor_str + x_cursor) // (self.width+1)
            b = fabs(self.pos_cursor_str + x_cursor+1) % (self.width)
            self.window.move(y_cursor-1-int(a), self.width-int(b)-1)

    def insert_new_key(self, new_key):
        self.lim_of_arrow -= 1
        if self.pos_cursor_str == 0:
            self.text += chr(new_key)
            self.command += chr(new_key)
        else:
            self.text = self.text[:self.pos_cursor_str] + chr(new_key) +\
                        self.text[self.pos_cursor_str:]
            self.command = (self.command[:self.pos_cursor_str] + chr(new_key) +
                            self.command[self.pos_cursor_str:])

    def threadout(self, name, output):
        while not self.end_thread:
            o = output.readline().decode()
            if o:
                self.turnback += o
                if not self.on_display:
                    self.update_screen()
        self.end_thread = False

    def run_by_curses(self, command_ls):
        if command_ls[0] == 'cd':
            command_ls.pop(0)
            self.text += cdCommand.chDir(command_ls)
            self.prompt_name = 'intek-sh:{}$ '.format(environ['PWD'].replace(environ['HOME'], '~'))
        elif command_ls[0] == 'printenv':
            command_ls.pop(0)
            for env in printenvCommand.printEnv(command_ls):
                self.text += env
        else:
            # for path_name in globbing.main(self.command):
            #     self.text += path_name
            self.p = subprocess.Popen(command_ls,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      stdin=subprocess.PIPE)

            # if self.command == 'python3 -i':
            if 'python3' in self.command:
                self.in_sub = True
                self.thread1 = Thread(target=self.threadout, args=('Thread-1', self.p.stdout))
                self.thread1.start()
            else:
                self.text += self.p.communicate()[0].decode()
                self.p.terminate()

    def run_by_subshell(self):
        if self.command == 'exit()' or self.p.returncode != None:
            self.end_thread = True
            self.in_sub = False
            self.p.stdin.write(('print(" ")\n').encode())
            self.p.stdin.flush()
            sleep(0.5)
            self.p.stdin.close()
            self.p.terminate()
        else:
            self.p.stdin.write((self.command+'\n').encode())
            self.p.stdin.flush()

    def play_subprocess(self):
        self.lim_of_arrow = 0
        self.pos_cursor_str = 0
        self.text += '\n'
        command_ls = self.command.split()
        try:
            if not self.in_sub:
                self.run_by_curses(command_ls)
            else:
                self.run_by_subshell()

            if self.text[-1] != '\n':
                self.text += '\n'
        except Exception:
            pass
        self.command = ''
        if not self.in_sub:
            self.text += self.prompt_name

    def delete_char(self):
        if self.pos_cursor_str > self.lim_of_arrow:
            self.lim_of_arrow += 1
            if self.pos_cursor_str != 0:
                self.text = self.text[:self.pos_cursor_str-1] + self.text[self.pos_cursor_str:]
                self.command = self.command[:self.pos_cursor_str-1] + self.command[self.pos_cursor_str:]
            else:
                self.text = self.text[:self.pos_cursor_str-1]
                self.command = self.command[:self.pos_cursor_str-1]


def main():
    the_shell = Screen()
    the_shell.update_screen()
    while True:
        try:
            the_shell.input_stream()
            if the_shell.lk == curses.ascii.ESC:
                curses.endwin()
                break
        except KeyboardInterrupt:
            curses.endwin()
            break

    quit()

if __name__ == '__main__':
    main()
