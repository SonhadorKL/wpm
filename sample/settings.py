import curses
from sample import menu
from sample import data_manager

def launch_settings(stdscr : curses.window):
    """
    Launch menu to get change settings
    """
    while True:
        men = menu.Menu(stdscr, "Settings", ["Test mode", "Quit"], allow_quit=True)
        result = men.launch()
        if result in ("", "Quit"):
            return
        if result == "Test mode":
            choose_mode(stdscr)

def choose_mode(stdscr : curses.window):
    """Set new game mode"""
    men = menu.Menu(stdscr, "Choose test mode", ["Classic", "Speeed test", "Quit"], allow_quit=True)
    result = men.launch()
    if result == "Classic":
        data_manager.SettingsManager.set_test_type("Classic")
    elif result == "Speeed test":
        data_manager.SettingsManager.set_test_type("Speed")
