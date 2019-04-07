import curses
import curses.textpad
import subprocess


class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items):
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
        self.lk=65
        self.touch_ending = True
        self.last_char = -1
        self.up_last = -1
        self.down_last = -1
        self.command = ''
        self.lim_of_arrow = 0
        self.pos_cursor_str = 0
        self.run()

    def init_curses(self):
        """Setup the curses"""
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

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        self.window.clear()
        self.window.refresh()
        self.display()
        # self.window.addstr(0, 0, self.text[-self.height*self.width-1:], curses.color_pair(1))
        """Waiting an input and run a proper method according to type of input"""

        while True:
            # self.display()
            new_key = self.window.getch()

            self.lk = new_key
            if new_key == curses.KEY_UP:
                if self.touch_ending:
                    self.last_char = self.up_last      
                    self.display()       
            elif new_key == curses.KEY_DOWN:
                self.last_char = self.down_last
                self.display()
            elif new_key == curses.ascii.ESC:
                break
            elif new_key == 10:
                self.display()
                self.last_char = -1
                self.up_last = -1
                self.down_last = -1
                self.play_subprocess()
                self.display()
            elif new_key < 127 and new_key > 31:
                self.last_char = -1
                self.up_last = -1
                self.down_last = -1
                self.display_key(new_key)
                self.display()
            elif new_key == 260 and self.pos_cursor_str > self.lim_of_arrow:
                self.pos_cursor_str -= 1
                self.move_cursor_back()
            elif new_key == 261 and self.pos_cursor_str < 0:
                self.pos_cursor_str += 1
                self.move_cursor_forward()
            elif new_key == 127:
                self.delete_char()
                self.display()
            else:
                self.display()

    def display(self):
        """Display the items on window"""
        # self.window.clear()
        # self.window.refresh()
        self.height, self.width = self.window.getmaxyx()

        # self.window.move(0, 0)
        # self.window.deleteln()
        self.window.move(self.height-1, 0)
        self.window.deleteln()
        self.get_top_bottom()

        if self.last_char+1 >= 0: 
            self.window.addstr(0, 0, self.text[self.last_char-self.height*self.width:], curses.color_pair(1))
        else:
            self.window.addstr(0, 0, self.text[self.last_char-self.height*self.width:self.last_char+1], curses.color_pair(1))
        self.window.refresh()
        self.window.clrtobot()
        if curses.getsyx()[0] == self.height-1:
            self.touch_ending = True
        else:
            self.touch_ending = False

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

        for _ in range(-self.pos_cursor_str):
            self.move_cursor_back()
            self.window.refresh()
        # txt = str(self.last_char) + ' ' + str(self.up_last) + ' ' + str(self.down_last) + ' ' + str(curses.getsyx()[1])
        # self.window.addstr(0, self.width-len(txt)-1, txt, curses.color_pair(2))
        # self.window.refresh()

    def get_top_bottom(self):
        i = self.last_char + 1
        if self.text[i] == '\n':
            i += 1
        for n in range(self.width):
            if i+n < 0:
                self.down_last = i+n
                if self.text[i+n] == '\n':
                    self.down_last = i+n-1
                    break

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

    def display_key(self, new_key):
        self.lim_of_arrow -= 1
        if self.pos_cursor_str == 0:
            self.text += chr(new_key)
            self.command += chr(new_key)
        else:
            self.text = self.text[:self.pos_cursor_str] + chr(new_key) + self.text[self.pos_cursor_str:]
            self.command = self.command[:self.pos_cursor_str] + chr(new_key) + self.command[self.pos_cursor_str:]
    
            
    def play_subprocess(self):
        self.lim_of_arrow = 0
        self.pos_cursor_str = 0
        self.text += '\n'
        command_for_sub = self.command.split()
        self.command = ''
        if command_for_sub:
            self.text += subprocess.run(command_for_sub, stdout=subprocess.PIPE).stdout.decode()
            if self.text[-1] != '\n':
                self.text += '\n'
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
    items = ['{}. Itemfgndfrtdfvbar'.format(num) for num in range(10)]
    Screen(items)


if __name__ == '__main__':
    main()
