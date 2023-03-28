import curses
from sample import wpm
from sample import data_manager
from sample import constants

def main(stdscr):
    """Just testing"""
    constants.init_colors()
    with open("text_example.txt", "r", encoding="utf8") as file:
        test = wpm.WPM(file.readline(), stdscr)
        stats = test.wpm_test()
        data_manager.DataManager.update_data(stats)

curses.wrapper(main)
