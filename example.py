import curses
import curses.textpad
import subprocess


class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items):
        """ Initialize the screen window

        Attributes
            window: A full curses screen window

            width: The width of `window`
            height: The height of `window`

            max_lines: Maximum visible line count for `result_window`
            top: Available top line position for current page (used on scrolling)
            bottom: Available bottom line position for whole pages (as length of items)
            current: Current highlighted line number (as window cursor)
            page: Total page count which being changed corresponding to result of a query (starts from 0)

            ┌--------------------------------------┐
            |1. Item                               |
            |--------------------------------------| <- top = 1
            |2. Item                               |
            |3. Item                               |
            |4./Item///////////////////////////////| <- current = 3
            |5. Item                               |
            |6. Item                               |
            |7. Item                               |
            |8. Item                               | <- max_lines = 7
            |--------------------------------------|
            |9. Item                               |
            |10. Item                              | <- bottom = 10
            |                                      |
            |                                      | <- page = 1 (0 and 1)
            └--------------------------------------┘

        Returns
            None
        """
        self.window = None

        self.width = 0
        self.height = 0

        self.init_curses()

        self.items = items

        self.max_lines = curses.LINES
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines
         
        # self.text = subprocess.run('ls', stdout=subprocess.PIPE).stdout.decode()
        f = open('text', 'r')
        self.text = f.read()
        f.close()
        self.last_char = -1
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
        # result = run("ls", stdout=subprocess.PIPE)

        """Waiting an input and run a proper method according to type of input"""
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.ascii.ESC:
                break

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def display(self):
        """Display the items on window"""
        self.height = self.window.getmaxyx()[0]
        self.width = self.window.getmaxyx()[1]
        self.window.clear()
        self.window.refresh()
        lim_top, lim_bottom = self.get_top_bottom()

        self.window.addstr(0, 0, self.text[lim_top:lim_bottom], curses.color_pair(1))
        self.window.refresh()
        
        # txt = self.text[lim_top:lim_top+5]
        # self.window.addstr(self.window.getmaxyx()[0]-1, 0, txt, curses.color_pair(1))
        # self.window.refresh()

    def get_top_bottom(self):
        filled_line = 0
        i = self.last_char
        j = self.last_char
        while i > -len(self.text):
            if self.text[i] == '\n':
                filled_line += (j-i)//self.width + 1
                j = i
                if filled_line > self.height:
                    diff = filled_line - self.height
                    i += diff*self.width
                    break
                
            i -= 1
        
        return i, self.last_char




def main():
    items = ['{}. Itemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmsdfgndfrtdfvbar'.format(num) for num in range(10)]
    Screen(items)


if __name__ == '__main__':
    main()
