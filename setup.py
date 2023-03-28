import curses
from sample import wpm

def main(stdscr):
    """Just testing"""
    with open("text_example.txt", "r", encoding="utf8") as file:
        test = wpm.WPM(file.readline(), stdscr)
        test.start_wpm_test()

curses.wrapper(main)
