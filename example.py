import curses
import curses.textpad
import subprocess


class Screen(object):
    def __init__(self):
        self.window = None

        self.width = 0
        self.height = 0

        self.init_curses()

        # self.text = subprocess.run('python3', stdout=subprocess.PIPE).stdout.decode()
        # f = open('text', 'r')
        # self.text = f.read()
        # f.close()
        self.prompt_name = 'intek-sh$ '
        self.text = 'intek-sh$ '
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

    def init_curses(self):
        self.window = curses.initscr()
        self.window.keypad(True)
        self.window.scrollok(True)
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
        new_key = self.window.getch()

        self.lk = new_key
        if new_key == curses.KEY_UP:
            if self.touch_ending:
                # if all line in window have been filled
                self.last_char = self.up_last
                self.update_screen()
        elif new_key == curses.KEY_DOWN:
            self.last_char = self.down_last
            self.update_screen()
        elif new_key == 10:
            # if button 'enter' was pressed
            self.update_screen()
            self.last_char = -1
            self.up_last = -1
            self.down_last = -1
            self.play_subprocess()
            self.update_screen()
        elif new_key < 127 and new_key > 31:
            # if normal key was pressed
            self.last_char = -1
            self.up_last = -1
            self.down_last = -1
            self.insert_new_key(new_key)
            self.update_screen()
        elif new_key == 260 and self.pos_cursor_str > self.lim_of_arrow:
            # if left arrow was pressed and cursor's position has not been over upper limitation
            self.pos_cursor_str -= 1
            self.move_cursor_back()
        elif new_key == 261 and self.pos_cursor_str < 0:
            # if left arrow was pressed and cursor's position has not been over lower limitation
            self.pos_cursor_str += 1
            self.move_cursor_forward()
        elif new_key == 127:
            #263 ubuntu
            # if button 'delete' was pressed
            self.delete_char()
            self.update_screen()
        else:
            # any thing else was pressed
            self.update_screen()

    def update_screen(self):
        '''
        update window by new conntent
        '''
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

        for _ in range(-self.pos_cursor_str):
            self.move_cursor_back()
            self.window.refresh()

        # txt = str(self.last_char) + ' ' + str(self.up_last) + ' ' + str(self.down_last) + ' ' + str(self.lk)
        # self.window.addstr(0, self.width-len(txt)-1, txt, curses.color_pair(2))
        # self.window.refresh()

    def update_upper_line(self):
        i = self.last_char + 1
        if self.text[i] == '\n':
            i += 1
        for n in range(self.width):
            if i+n < 0:
                self.down_last = i+n
                if self.text[i+n] == '\n':
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
        if x_cursor == 0:
            if y_cursor != 0:
                self.window.move(y_cursor-1, self.width-1)
        else:
            self.window.move(y_cursor, x_cursor-1)

    def move_cursor_forward(self):
        y_cursor, x_cursor = curses.getsyx()
        if x_cursor == self.width-1:
            self.window.move(y_cursor+1, 0)
        else:
            self.window.move(y_cursor, x_cursor+1)

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

    def play_subprocess(self):
        self.lim_of_arrow = 0
        self.pos_cursor_str = 0
        self.text += '\n'
        command_for_sub = self.command.split()

        if command_for_sub:
            # try:
            if not self.in_sub:
                self.p = subprocess.Popen(command_for_sub,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
                # res_from_sub = self.p.stdout.read().decode()
                # self.text += res_from_sub

            else:
                # self.p.stdin.write('print(123)\n'.encode())
                self.p.stdin.write((self.command+'\n').encode())
                self.p.stdin.flush()
                res_from_sub = self.p.stdout.readline().decode()
                self.text += res_from_sub

            if self.command == 'python3 -i':
                self.in_sub = True
            elif self.command == 'exit()':
                self.in_sub = False
                # res_from_sub = self.p.communicate(self.command.encode())

            # if self.in_sub:
            #     self.p.stdin.write('print(123)\n'.encode())
            #     self.p.stdin.write((self.command+'\n').encode())
            #     self.p.stdin.flush()
            #     res_from_sub = self.p.stdout.readline().decode()
            #     # res_from_sub = p.communicate()

            # self.text += res_from_sub
            # except Exception:
            #     pass

            if self.text[-1] != '\n':
                self.text += '\n'
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
        the_shell.input_stream()
        if the_shell.lk == curses.ascii.ESC:
            curses.endwin()
            break


if __name__ == '__main__':
    main()
