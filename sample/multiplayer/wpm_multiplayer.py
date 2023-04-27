import curses
import time
from sample import constants
from sample import data_manager
from sample.multiplayer.network import Network
from sample.wpm import ClassicWPM


class MultiplayerWPM(ClassicWPM):
    """Compete with other people"""
    def __init__(self, window: curses.window, target_text: str, file_name: str, network: Network) -> None:
        super().__init__(window, target_text, file_name)
        self.other_user_text = ""
        self.other_user_wpm = None
        self.nickname = data_manager.SettingsManager.get_nickname()
        self.network = network
        self.window.nodelay(True)

    def set_main_text(self) -> None:
        """Put target text and user's above it"""
        other_user = constants.YELLOW_BLACK | curses.A_DIM
        self._update_text()
        self.main_text.add_string(self.target_text, constants.GREY_BLACK, (0,0))
        self.main_text.add_string(self.other_user_text, other_user, (0,0))
        self.main_text.add_string(self.user_text, constants.GREEN_BLACK, (0,0))

    def end_screen(self) -> None:
        """After test screen"""
        self.window.nodelay(False)
        self.window.erase()
        self.put_info()
        cur_y_pos = self.window.getyx()[0] + 1
        if self.other_user_wpm is None:
            self.window.addstr(cur_y_pos, 0, f"Congratulation! You beat {self._get_opponent_nickname()}!")
        else:
            self.window.addstr(cur_y_pos, 0, f"Unfortunately, {self._get_opponent_nickname()} beat your ass")
        self.window.refresh()
        self.window.getch()

    def manage_inputs(self) -> int:
        "Manage players keyboard inputs"
        try:
            symbol = self.window.getch()
        except Exception as err:
            raise err
        if symbol < 0 or symbol > 0x10FFFF:
            return
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

    def _update_text(self):
        self.other_user_text = self.network.update_data(self.user_text)["text"]
    
    def _get_opponent_nickname(self):
        return self.network.update_data(self.user_text)["nickname"]

    def set_under_text(self) -> None:
        """Set current user's statistics and previous best score"""
        wpm_u = round(len(self.user_text) * 60 / (time.time() - self.stats.start_time))
        wpm_p = round(len(self.other_user_text) * 60 / (time.time() - self.stats.start_time))
        if self.other_user_text == self.target_text and not self.other_user_wpm:
            self.fix_time()

        nickname = self.nickname + ":"
        opponent_nickname = self._get_opponent_nickname() + ":"
        wpm_user = f"WPM: {wpm_u}"
        done_text = f"Done: {len(self.user_text)} / {len(self.target_text)}"
        wpm_past = f"WPM: {wpm_p if self.other_user_wpm is None else self.other_user_wpm}"
        done_past = f"Done: {len(self.other_user_text)} / {len(self.target_text)}"
        
        self.under_string.add_string(nickname, constants.GREEN_BLACK | curses.A_BOLD, (0, 0))
        self.under_string.add_string(wpm_user, constants.GREEN_BLACK, (0, 16))
        self.under_string.add_string(done_text, constants.GREEN_BLACK, (0, 32))
        
        self.under_string.add_string(opponent_nickname, constants.YELLOW_BLACK | curses.A_BOLD, (1, 0))
        self.under_string.add_string(wpm_past, constants.YELLOW_BLACK, (1, 16))
        self.under_string.add_string(done_past, constants.YELLOW_BLACK, (1, 32))

    def fix_time(self):
        """Fix time of other person when he won"""
        self.other_user_wpm = round(len(self.target_text) * 60 / (time.time() - self.stats.start_time))