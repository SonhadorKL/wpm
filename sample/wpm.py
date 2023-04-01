import curses
import time
from collections import Counter
from sample import constants

class WPMStatistics:
    """Store the data about test"""
    def __init__(self) -> None:
        self.wpm = 0.0
        self.errors = 0
        self.start_time = time.time()
        self.symbol_count = {}
        self.symbol_errors = {}

    def get_occurences(self, string : str) -> None:
        """Make a dictionaty of character occurrences"""
        self.symbol_count = Counter(string)

    def add_error_char(self, char : str) -> None:
        """Add symbol in which user make an error"""
        self.errors += 1
        if char in self.symbol_errors:
            self.symbol_errors[char] += 1
        else:
            self.symbol_errors[char] = 1

class WPM:
    """Class for the test of words per minute"""
    def __init__(self, target_text : str, window : curses.window) -> None:
        self.window = window.subwin(0, 0)
        self.target_text = target_text
        self.printed_text = ""
        self.stats = WPMStatistics()
        self.is_playing = True
        self.was_interrupted = False

    def reset(self) -> None:
        """Reset parameters"""
        self.stats.start_time = time.time()
        self.printed_text = ""
        self.stats = WPMStatistics()
        self.stats.get_occurences(self.target_text)
        self.is_playing = True

    def wpm_test(self) -> WPMStatistics:
        """Call to start the process of the test"""
        self.reset()
        self.process()
        if self.was_interrupted:
            return None
        self.end_screen()
        return self.stats

    def process(self) -> None:
        """Manage the wpm test process"""
        while self.is_playing:
            self.update_window()
            self.manage_inputs()

    def end_screen(self) -> None:
        """After test screen"""
        self.window.erase()
        self.put_info()
        cur_y_pos = self.window.getyx()[0] + 1
        self.window.addstr(cur_y_pos, 0, "You've completed the test!")
        self.window.addstr(cur_y_pos + 1, 0, "Press any key to continue")
        self.window.refresh()
        self.window.getch()

    def put_info(self) -> None:
        """put general info on the screen"""
        stats = self.get_stat()
        end_of_win = self.window.getmaxyx()[0] - constants.get_text_height(self.window, stats)
        self.window.addstr(end_of_win, 0, stats, constants.MAGENTA_BLACK)
        self.window.move(0, 0)
        self.window.addstr(0, 0, self.target_text, constants.GREY_BLACK)
        self.window.addstr(0, 0, self.printed_text, constants.GREEN_BLACK)

    def update_window(self) -> None:
        """Update text on the screen"""
        self.window.erase()
        self.put_info()
        self.window.refresh()

    def manage_inputs(self) -> None:
        "Manage players keyboard inputs"
        symbol = self.window.getch()
        expected_sym = self.target_text[len(self.printed_text)]
        if symbol == constants.ESCAPE:
            self.is_playing = False
            self.was_interrupted = True
        elif chr(symbol) != expected_sym:
            self.stats.add_error_char(expected_sym.lower())
            curses.beep()
        else:
            self.printed_text += chr(symbol)
        if len(self.printed_text) == len(self.target_text):
            self.is_playing = False
     
    def get_stat(self) -> str:
        """Return and update a string with current player statistics"""
        wpm = round(len(self.printed_text) * 60 / (time.time() - self.stats.start_time), 2)
        self.stats.wpm = wpm
        wpm_text = f"WPM: {wpm}"
        errors_text = f"Errors: {self.stats.errors}"
        done_text = f"Done: {len(self.printed_text)} / {len(self.target_text)}"
        time_text = f"Time: {round(time.time() - self.stats.start_time, 2)}"
        sp = " " * 4
        return f"{wpm_text}{sp}{errors_text}{sp}{done_text}{sp}{time_text}{sp}"
