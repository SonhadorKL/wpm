import curses
import time
from sample import constants

class WPM:
    """Class for the test of words per minute"""
    def __init__(self, target_text : str, window : curses.window) -> None:
        self.window = window.subwin(0, 0)
        self.target_text = target_text
        self.start_time = 0
        self.printed_text = ""
        self.error_count = 0
        self.is_playing = True

    def start_wpm_test(self) -> None:
        """Call to start the process of the test"""
        self.start_time = time.time()
        self.printed_text = ""
        self.error_count = 0
        self.is_playing = True
        self.process()

    def process(self) -> None:
        """Manage the wpm test process"""
        while self.is_playing:
            self.update_window()
            self.manage_inputs()

    def update_window(self) -> None:
        """Update text on the screen"""
        self.window.erase()
        end_of_win = self.window.getmaxyx()[0] - 1
        self.window.addstr(end_of_win, 0, self.get_stat(), constants.MAGENTA_BLACK)
        self.window.move(0, 0)
        self.window.addstr(0, 0, self.target_text, constants.GREY_BLACK)
        self.window.addstr(0, 0, self.printed_text)
        self.window.refresh()

    def get_stat(self) -> str:
        """Return a string with current player statistics"""
        wpm = round(len(self.printed_text) * 60 / (time.time() - self.start_time), 2)
        return f"WPM: {wpm}\tERRORS: {self.error_count}"

    def manage_inputs(self) -> None:
        "Manage players keyboard inputs"
        symbol = self.window.getch()
        if chr(symbol) != self.target_text[len(self.printed_text)]:
            self.error_count += 1
            curses.beep()
        else:
            self.printed_text += chr(symbol)
        if len(self.printed_text) == len(self.target_text):
            self.is_playing = False
        