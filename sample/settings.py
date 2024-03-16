import curses
from sample import menu
from sample import data_manager
from sample import plate

def launch_settings(stdscr : curses.window):
    """
    Launch menu to get change settings
    """
    while True:
        men = menu.Menu(stdscr, "Settings", ["Test mode", "Nickname", "Quit"], allow_quit=True)
        result = men.launch()
        if result in ("", "Quit"):
            return
        if result == "Test mode":
            choose_mode(stdscr)
        elif result == "Nickname":
            choose_nickname(stdscr)

def choose_mode(stdscr : curses.window):
    """Set new game mode"""
    men = menu.Menu(stdscr, "Choose test mode", ["Classic", "Speeed test", "Quit"], allow_quit=True)
    result = men.launch()
    if result == "Classic":
        data_manager.SettingsManager.set_test_type("Classic")
    elif result == "Speeed test":
        data_manager.SettingsManager.set_test_type("Speed")

def choose_nickname(stdscr : curses.window):
    """Set new nickname of the player"""
    cur_nick = data_manager.SettingsManager.get_nickname()
    write_nick = plate.WritablePlate(stdscr, "Write new nickname", cur_nick)
    nick = write_nick.process()
    if nick != "":
        data_manager.SettingsManager.set_nickname(nick)
