import curses
from sample import wpm
from sample import data_manager
from sample import constants
from sample import menu
from sample import text_manager

def main(stdscr):
    """Just testing"""
    constants.init_colors()
    is_playing = True
    while is_playing:
        men = menu.Menu(stdscr, "WPM-Test", ["Start test", "Text loading", "Quit"])
        result = men.launch()
        if result == "Start test":
            text = text_manager.choose_text(stdscr)
            test = wpm.WPM(text, stdscr)
            stats = test.wpm_test()
            data_manager.DataManager.update_data(stats)
        elif result == "Quit":
            is_playing = False
        elif result == "Text loading":
            text_manager.load_text(stdscr)

curses.wrapper(main)
