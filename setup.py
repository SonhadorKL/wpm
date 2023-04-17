import curses

from sample import wpm
from sample import data_manager
from sample import constants
from sample import menu
from sample import text_manager
from sample import stat_menu
from sample import settings

def main(stdscr):
    """Main body of the application"""
    constants.init_colors()
    is_playing = True
    while is_playing:
        options = ["Start test", "Text loading", "Statistics", "Settings", "Quit"]
        men = menu.Menu(stdscr, "WPM-Test", options)
        result = men.launch()
        if result == "Start test":
            text_info = text_manager.choose_text(stdscr)
            text_found = data_manager.TextDataManager.get_text_data(text_info[0]) is not None
            is_type_speed = data_manager.SettingsManager.get_test_type() == "Speed"
            if text_found and is_type_speed:
                test = wpm.SpeedWPM(stdscr, text_info[1], text_info[0])
                stats = test.wpm_test()
                data_manager.DataManager.update_data(stats)
            else:
                test = wpm.ClassicWPM(stdscr, text_info[1], text_info[0])
                stats = test.wpm_test()
                data_manager.DataManager.update_data(stats)
        elif result == "Quit":
            is_playing = False
        elif result == "Text loading":
            text_manager.load_text(stdscr)
        elif result == "Statistics":
            stats = stat_menu.Statistics(stdscr)
            stats.process()
        elif result == "Settings":
            settings.launch_settings(stdscr)

curses.wrapper(main)
