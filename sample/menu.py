import curses
from sample import constants

class Menu:
    """Class for creating console menu"""
    def __init__(self, window : curses.window, menu_name : str, names : list, under_string = "") -> None:
        self.window = window.subwin(0, 0)
        self.items_name = names
        self.name = menu_name
        self.is_processing = True
        self.choosen_item = 0
        self.under_string = under_string

    def launch(self) -> str:
        """
        Launch menu
        Return choosen item in menu
        """
        curses.curs_set(0)
        while self.is_processing:
            self.print_menu()
            self.process_input()
        curses.curs_set(1)
        return self.items_name[self.choosen_item]


    def print_menu(self):
        """"Print menu in console"""
        self.window.erase()
        self.window.addstr(0, 0, self.name, curses.A_BOLD)
        self._print_all_items()
        # make 
        self.window.addstr(self.window.getmaxyx()[0] - self._get_height_of_string(self.under_string), 0, self.under_string, constants.GREY_BLACK)
        self.window.refresh()

    def process_input(self) -> None:
        """Process user input"""
        user_input = self.window.getch()
        if chr(user_input) == "w":
            self.choosen_item = (self.choosen_item - 1) % len(self.items_name)
        elif chr(user_input) == "s":
            self.choosen_item = (self.choosen_item + 1) % len(self.items_name)
        elif user_input == 10: # code of ENTER key
            self.is_processing = False


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
        window_height = self.window.getmaxyx()[0] - self._get_height_of_string(self.under_string)
        start_pos = max(0, self.choosen_item - window_height + 2)
        for item_name in self.items_name:
            if start_pos < num_item < window_height + start_pos:
                self._print_item(item_name, cur_pos, num_item)
                cur_pos += self._get_height_of_string(item_name)
            num_item += 1
