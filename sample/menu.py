import curses
from sample import commands
from sample import constants


class Menu:
    """Class for creating console menu"""
    def __init__(self, window : curses.window, menu_name : str, names : list, under_string = "") -> None:
        self.window = window.subwin(0, 0)
        self.items_name = names
        self.name = menu_name
        self.is_processing = True
        self.result = ""
        self.choosen_item = 0
        self.under_string = under_string

    def launch(self) -> str:
        """
        Launch menu\n
        Return choosen item in menu
        """
        curses.curs_set(0)
        self.reset(self.items_name)
        while self.is_processing:
            self.print_menu()
            self.process_input()
        curses.curs_set(1)
        return self.result

    def reset(self, names : list) -> None:
        self.is_processing = True
        self.result = ""
        self.choosen_item = 0

    def print_menu(self):
        """"Print menu in console"""
        self.window.erase()
        self.window.addstr(0, 0, self.name, curses.A_BOLD)
        self._print_all_items()
        self.window.addstr(self._get_pos_of_understr(), 0, self.under_string, constants.GREY_BLACK)
        self.window.refresh()

    def process_input(self) -> int:
        """Process user input"""
        user_input = self.window.getch()
        if chr(user_input) == "w":
            self.choosen_item = (self.choosen_item - 1) % len(self.items_name)
        elif chr(user_input) == "s":
            self.choosen_item = (self.choosen_item + 1) % len(self.items_name)
        elif user_input == constants.ENTER: # code of ENTER key
            self.is_processing = False
            self.result = self.items_name[self.choosen_item]
        return user_input

    def _get_height_of_string(self, line : str) -> int:
        return len(line) // self.window.getmaxyx()[1] + 1

    def _print_item(self, name : str, cur_pos : int, num_item : int):
        item_attribute = []
        if num_item - 1 == self.choosen_item:
            item_attribute.append(curses.A_REVERSE)
        self.window.addstr(cur_pos, 0, str(num_item) + ". " + name, *item_attribute)

    def _print_all_items(self):
        cur_pos = 0
        num_item = 1
        cur_pos += self._get_height_of_string(self.name)
        under_string_size = self._get_height_of_string(self.under_string)
        window_height = self.window.getmaxyx()[0] - under_string_size
        start_pos = max(0, self.choosen_item - window_height + 2)
        for item_name in self.items_name:
            if start_pos < num_item < window_height + start_pos:
                self._print_item(item_name, cur_pos, num_item)
                cur_pos += self._get_height_of_string(item_name)
            num_item += 1

    def _get_pos_of_understr(self) -> str:
        under_string_size = self._get_height_of_string(self.under_string)
        window_size = self.window.getmaxyx()[0]
        return window_size - under_string_size


class ConsoleMenu(Menu):
    """Menu with ability to get commands"""
    def __init__(self, window: curses.window, menu_name: str, names: list, commands_name: list) -> None:
        self.default_string = "Press <C> to enter COMMAND mode"
        super().__init__(window, menu_name, names, self.default_string)
        self.user_input = ""
        self.is_in_command = False
        self.commands = commands_name

    def process_input(self) -> None:
        if not self.is_in_command:
            curses.curs_set(0)
            user_input = super().process_input()
            if chr(user_input) == "c":
                self.is_in_command = True
                self.under_string = self.user_input
                self.window.move(self._get_pos_of_understr(), 0)
            return
        curses.curs_set(1)
        self.process_command_line()

    def process_command_line(self):
        """Process user input in menu's command line"""
        user_input = self.window.getch()
        if user_input == constants.ESCAPE:
            self.is_in_command = False
            self.under_string = self.default_string
            return

        if user_input == constants.BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif user_input == constants.ENTER and self.user_input != "":
            self.is_in_command = False
            if self.check_command(self.user_input):
                self.is_processing = False
                self.result = self.user_input
            else:
                error = self.check_wrong_argument(self.user_input)
                if error != "":
                    self.under_string = error
                else:
                    self.under_string = "Command not found"          
            return
        elif constants.check_letter(chr(user_input)):
            self.user_input += chr(user_input)
        self.under_string = self.user_input

    def check_command(self, command : str) -> bool:
        """Check if command is available"""
        return any(com.check_command(command) for com in self.commands)
    
    def check_wrong_argument(self, command : str) -> str:
        """Check if command is available but user gave wrong args"""
        for com in self.commands:
            if com.wrong_arguments(command):
                return com.error()
        return ""
