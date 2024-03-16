import curses
from sample import constants

class Plate:
    """Simple window to manage text"""
    def __init__(self, window, name, text, return_key=constants.ESCAPE) -> None:
        self.name = name
        self.text = text
        self.return_key = return_key
        self.window = window.subwin(0, 0)
        self.is_processing = True
        self.name_attr = [curses.A_BOLD]
        self.text_attr = []

    def set_text_atr(self, atributes : list):
        """add atributes for main text"""
        self.text_attr = atributes

    def set_name_atr(self, atributes : list):
        """add atributes for headline"""
        self.name_attr = atributes

class WritablePlate(Plate):
    """Window with ability to write on it"""
    def __init__(self, window : curses.window, name, text, return_key=constants.ESCAPE) -> None:
        super().__init__(window, name, text, return_key)
        self.user_input = ""

    def process(self) -> str:
        """Draw on window and get users input"""
        while self.is_processing:
            self.window.erase()
            self._print_on_screen()
            self.window.refresh()
            self._process_input()
        return self.user_input

    def _process_input(self):
        user_char = self.window.getch()
        if user_char == constants.BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif user_char == self.return_key:
            self.is_processing = False
            self.user_input = ""
        elif user_char == constants.ENTER and self.user_input != "":
            self.is_processing = False
        elif constants.check_letter(chr(user_char)):
            self.user_input += chr(user_char)

    def _print_on_screen(self):
        self.window.addstr(0, 0, self.name, *self.name_attr)
        text_pos = constants.get_text_height(self.window, self.name)
        if self.user_input != "":
            self.window.addstr(text_pos, 0, self.user_input, *self.text_attr)
        else:
            self.window.addstr(text_pos, 0, self.text, *self.text_attr)
            self.window.move(text_pos, 0)

class ShowPlate(Plate):
    """Class to show text in console"""
    def __init__(self, window : curses.window, name, text, return_key=constants.ESCAPE) -> None:
        super().__init__(window, name, text, return_key)
        curses.curs_set(0)
        self.is_processing = True

    def update(self):
        """Draw text until user leave"""
        while self.is_processing:
            self.print_screen()
            self._get_input()
        curses.curs_set(1)
    
    def print_screen(self):
        """Distplay screen"""
        self.window.erase()
        self._print_on_screen()
        self.window.refresh()

    def _get_input(self):
        """Check if return button pressed"""
        if self.window.getch() == self.return_key:
            self.is_processing = False

    def _print_on_screen(self):
        self.window.addstr(0, 0, self.name, *self.name_attr)
        text_pos = constants.get_text_height(self.window, self.name)
        self.window.addstr(text_pos, 0, self.text, *self.text_attr)
