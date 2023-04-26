import curses
import time
from sample.wpm_stats import WPMStatistics
from sample.wpm_stats import TextStatistics
from sample.text_unit import TextUnit
from sample import data_manager
from sample import constants

def write_string_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print(f'Successfully wrote string to file: {file_path}')
    except Exception as e:
        print(f'Error writing string to file: {e}')



class WPMTest:
    """Class for the test of words per minute"""
    def __init__(self, window : curses.window, file_name : str) -> None:
        self.window = window.subwin(0, 0)
        self.is_playing = True
        self.was_interrupted = False
        self.stats = WPMStatistics()
        self.texts_stats = TextStatistics(file_name)
        self.headline = TextUnit()
        self.main_text = TextUnit()
        self.under_string = TextUnit()

    def set_headline(self) -> None:
        """Set headlines setting\nCalled first before window.refresh()"""

    def set_main_text(self) -> None:
        """
        Set main text\n
        Called after set_headline() and before window.refresh()\n
        """

    def set_under_text(self) -> None:
        """
        Set main text\n
        Called after set_main_text() and before window.refresh()\n
        """

    def wpm_test(self) -> WPMStatistics:
        """Call to start the process of the test"""
        self.process()
        if self.was_interrupted:
            return None
        self.texts_stats.fix_time()
        self.end_screen()
        data_manager.TextDataManager.update_text_data(self.texts_stats)
        return self.stats

    def put_info(self) -> None:
        """Reset content on the window"""
        self.set_headline()
        self.set_main_text()
        self.set_under_text()
        
        main_text_pos = self.headline.get_text_height(self.window)
        under_pos = self.window.getmaxyx()[0] - self.under_string.get_text_height(self.window)

        self.headline.print_on_screen(self.window, (0, 0))

        self.under_string.print_on_screen(self.window, (under_pos, 0))

        self.main_text.print_on_screen(self.window, (main_text_pos, 0))

    def update_window(self) -> None:
        """Update text on the screen"""
        self.window.erase()
        self.put_info()
        self.window.refresh()

    def manage_inputs(self) -> int:
        """
        Basic method to get user key
        Overload it to do something with key input
        """
        symbol = self.window.getch()
        return symbol

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


class ClassicWPM(WPMTest):
    """Original test: user have test to type, his statistics show in underline string"""
    def __init__(self, window: curses.window, target_text : str, file_name : str) -> None:
        super().__init__(window, file_name)
        self.target_text = target_text
        self.user_text = ""

    def set_headline(self) -> None:
        """Put file name in the headline"""
        self.headline.add_string(self.texts_stats.file_name, curses.A_BOLD, (0, 0))

    def set_main_text(self) -> None:
        """Put target text and user's above it"""
        self.main_text.add_string(self.target_text, constants.GREY_BLACK, (0,0))
        self.main_text.add_string(self.user_text, constants.GREEN_BLACK, (0,0))

    def set_under_text(self) -> None:
        """
        Set main text\n
        Called after set_main_text() and before window.refresh()\n
        """
        self.under_string.add_string(self.get_stat(), constants.MAGENTA_BLACK, (0, 0))

    def get_stat(self) -> str:
        """Return and update a string with current player statistics"""
        wpm = round(len(self.user_text) * 60 / (time.time() - self.stats.start_time), 2)
        self.stats.wpm = wpm
        wpm_text = f"WPM: {wpm}"
        errors_text = f"Errors: {self.stats.errors}"
        done_text = f"Done: {len(self.user_text)} / {len(self.target_text)}"
        time_text = f"Time: {round(time.time() - self.stats.start_time, 2)}"
        sp = " " * 4
        return f"{wpm_text}{sp}{errors_text}{sp}{done_text}{sp}{time_text}{sp}"

    def manage_inputs(self) -> int:
        "Manage players keyboard inputs"
        symbol = super().manage_inputs()
        expected_sym = self.target_text[len(self.user_text)]
        if symbol == constants.ESCAPE:
            self.is_playing = False
            self.was_interrupted = True
        elif chr(symbol) != expected_sym:
            self.stats.add_error_char(expected_sym.lower())
            curses.beep()
        else:
            self.user_text += chr(symbol)
            self.texts_stats.add_next_character()
        if len(self.user_text) == len(self.target_text):
            self.is_playing = False

class SpeedWPM(ClassicWPM):
    """WPM test where you can compete with yourself from the past"""
    def __init__(self, window: curses.window, target_text: str, file_name: str) -> None:
        super().__init__(window, target_text, file_name)
        self.best_speed_times = data_manager.TextDataManager.get_text_data(file_name)["times"]
        self.past_index = 0
        self.past_text = ""

    def set_main_text(self) -> None:
        """Put target text and user's above it"""
        self._update_past_text()
        past_attr = constants.YELLOW_BLACK | curses.A_DIM
        self.main_text.add_string(self.target_text, constants.GREY_BLACK, (0,0))
        self.main_text.add_string(self.past_text, past_attr, (0,0))
        self.main_text.add_string(self.user_text, constants.GREEN_BLACK, (0,0))

    def _update_past_text(self):
        if self.past_index >= len(self.target_text):
            return
        if constants.get_time(self.stats.start_time) < self.best_speed_times[self.past_index]:
            if self.past_index == 0:
                self.past_text = ""
                return
        past_time = self.best_speed_times[self.past_index]
        while past_time < constants.get_time(self.stats.start_time) and self.past_index < len(self.target_text):
            past_time = self.best_speed_times[self.past_index]
            self.past_index += 1
        self.past_text = self.target_text[:self.past_index + 1]

    def end_screen(self) -> None:
        """After test screen"""
        self.window.erase()
        self.put_info()
        cur_y_pos = self.window.getyx()[0] + 1
        cur_time = round(constants.get_time(self.stats.start_time), 2)
        prev_best = round(data_manager.TextDataManager.get_best_time(self.texts_stats.file_name), 2)
        if prev_best is None:
            self.window.addstr(cur_y_pos, 0, "You've completed the test!")
        if cur_time <= prev_best:
            self.window.addstr(cur_y_pos, 0, "Congrats, you broke your record!")
            self.window.addstr(cur_y_pos + 1, 0, "New record: " + str(cur_time) + " sec")
        else:
            self.window.addstr(cur_y_pos, 0, "Good try, fellow")
            self.window.addstr(cur_y_pos + 1, 0, "Current record: " + str(prev_best) + " sec")
        self.window.refresh()
        self.window.getch()

    def set_under_text(self) -> None:
        """Set current user's statistics and previous best score"""
        wpm_u = round(len(self.user_text) * 60 / (time.time() - self.stats.start_time))
        wpm_p = round(len(self.past_text) * 60 / (time.time() - self.stats.start_time))
        if self.past_text == self.target_text:
            best_time = data_manager.TextDataManager.get_best_time(self.texts_stats.file_name)
            wpm_p = round(len(self.past_text) * 60 / best_time)
        wpm_user = f"WPM: {wpm_u}"
        done_text = f"Done: {len(self.user_text)} / {len(self.target_text)}"
        wpm_past = f"WPM: {wpm_p}"
        done_past = f"Done: {len(self.past_text)} / {len(self.target_text)}"

        self.under_string.add_string(wpm_user + "\t\t" + done_text, constants.GREEN_BLACK, (0, 0))
        self.under_string.add_string(wpm_past + "\t\t" + done_past, constants.YELLOW_BLACK, (1, 0))
