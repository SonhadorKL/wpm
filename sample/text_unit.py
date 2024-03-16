import curses
from sample import constants

class TextUnit:
    """Class to store textes, their attributes and positions"""
    def __init__(self) -> None:
        self.texts = []
        self.attrs = []
        self.poses = []

    def add_string(self, text : str, attr : int, pos = None) -> None:
        """Add texts with given parameters"""
        self.texts.append(text)
        self.attrs.append(attr)
        self.poses.append(pos)

    def print_on_screen(self, window : curses.window, start_pos : tuple) -> None:
        """Print striprint_on_screenngs on the screen"""
        for i in range(len(self.texts)):
            if self.poses[i]:
                pos = (start_pos[0] + self.poses[i][0], start_pos[1] + self.poses[i][1])
                window.addstr(*pos, self.texts[i], self.attrs[i])
            else:
                window.addstr(*start_pos, self.texts[i], self.attrs[i])
        # How does it even work before???
        self.texts.clear()
        self.attrs.clear()
        self.poses.clear()

    def get_text_height(self, win : curses.window) -> int:
        """Return height of the whole text"""
        ind = 0
        max_heig = 0
        cur_heig = 0
        for text in self.texts:
            if not self.poses[ind] is None:
                heigh = constants.get_text_height(win, text, self.poses[ind][1])
                max_heig = max(max_heig, self.poses[ind][0] + heigh)
                cur_heig = max_heig
            else:
                cur_heig += constants.get_text_height(win, text, win.getyx()[1])
                max_heig = max(max_heig, cur_heig)
            ind += 1
        return max_heig
