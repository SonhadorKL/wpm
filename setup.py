import curses
from sample import wpm
from sample import data_manager
from sample import constants
from sample import menu

def main(stdscr):
    """Just testing"""
    constants.init_colors()
    is_playing = True
    while is_playing:
        men = menu.Menu(stdscr, "WPM-Test", ["Start test", "Quit"])
        result = men.launch()
        if result == "Start test":
            with open("text_example.txt", "r", encoding="utf8") as file:
                test = wpm.WPM(file.readline(), stdscr)
                stats = test.wpm_test()
                data_manager.DataManager.update_data(stats)
        elif result == "Quit":
            is_playing = False

curses.wrapper(main)
