import curses
from sample import menu
from sample import data_manager

class Statistics:
    """"Class to display user statistics"""
    def __init__(self, window : curses.window) -> None:
        self.window = window.subwin(0, 0)
        self.data = data_manager.DataManager.get_data()
        self.main_menu = menu.Menu(window, "Statistics", self._get_menu_options_())

    def process(self):
        while True:
            user_option = self.main_menu.launch()
            if user_option == "Show mistakes":
                self._show_errors()
            elif user_option == "Quit" or user_option == "":
                break 

    def _get_menu_options_(self):
        options = []
        options += ["Best wpm: " + str(round(self.data["test.bestwpm"]))]
        options += ["Average wpm: " + str(round(self.data["test.wpm"] / self.data["test.count"]))]
        options += ["Training time: " + str(round(self.data["test.time"] / 60)) + " min"]
        options += ["Show mistakes"]
        options += ["Quit"]
        return options
    
    def _show_errors(self):
        mistakes = self._get_mistakes() + ["Quit"]
        error_window = menu.Menu(self.window, "Most serious mistakes (it u)", mistakes)
        result = error_window.launch()
        while result != "Quit" and result != "":
            result = error_window.launch()

    def _get_mistakes(self, mistake_count = 10):
        def get_perc(key, value, all_count : int):
            return str(key) + ": " + str(round(value / all_count * 100, 2)) + "%"

        most_freq_mistakes = []
        mistakes = self.data["letters.errors"]
        errors_count = sum(mistakes.values())
        mistakes = dict(sorted(mistakes.items(), key=lambda x:x[1], reverse=True))
        obj_count = 0
        for item in mistakes.items():
            obj_count += 1
            if obj_count > mistake_count:
                break
            key = item[0]
            val = item[1]
            if key.isalpha():
                most_freq_mistakes.append(get_perc(key, val, errors_count))
        return most_freq_mistakes

