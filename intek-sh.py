#!/usr/bin/python3

import sys
import os
import curses
from time import sleep


def shellLoop(stdscr):
    begin_x = 20
    begin_y = 7
    height = 5
    width = 40
    win = curses.newwin(height, width, begin_y, begin_x)

    promtName = 'intek-sh$ '
    lastKey = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    # stdscr.leaveok(1)
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (lastKey != 27):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        # curses.setsyx(1, 1)
        stdscr.refresh()
        # sleep(1)
        # if lastKey == 10:
        #     stdscr.addstr(curses.getsyx()[0]+1, 0, promtName, curses.color_pair(1))
        stdscr.addstr(0, 0, 'asdasdaaaaaaaaaaaaaaaaaaaaaaaaaaadfgfgfgdfgdgdg', curses.color_pair(1))
        stdscr.refresh()
        stdscr.addstr(4, 0, 'as{}'.format(stdscr.getmaxyx()[0]), curses.color_pair(1))
        # Refresh the screen
        stdscr.refresh()
        # sleep(1)

        # Wait for next input
        lastKey = stdscr.getch()


def main():
    curses.wrapper(shellLoop)


if __name__ == "__main__":
    main()
