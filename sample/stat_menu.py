import curses
from sample import menu
from sample import data_manager

class Statistics:
    """"Class to display user statistics"""
    def __init__(self, window : curses.window) -> None:
        self.window = window.subwin(0, 0)
        self._set_data()

    def _set_data(self):
        self.data = data_manager.DataManager.get_data()
        self.main_menu = menu.Menu(self.window, "Statistics", self._get_menu_options_())

    def process(self) -> None:
        """Main loop"""
        while True:
            user_option = self.main_menu.launch()
            if user_option == "Show mistakes":
                self._show_errors()
            elif user_option in ("Quit", ""):
                break
            elif user_option == "Reset statistics":
                data_manager.DataManager.reset_data()
                data_manager.TextDataManager.reset_data()
                self._set_data()

    def _get_menu_options_(self) -> str:
        options = []
        options += ["Best wpm: " + str(round(self.data["test.bestwpm"]))]
        compeleted_text = self.data["test.count"] if self.data["test.count"] != 0 else 1
        options += ["Average wpm: " + str(round(self.data["test.wpm"] / compeleted_text))]
        options += ["Training time: " + str(round(self.data["test.time"] / 60, 2)) + " min"]
        options += ["Show mistakes"]
        options += ["Reset statistics"]
        options += ["Quit"]
        return options

    def _show_errors(self):
        """Run a window with errors"""
        mistakes = self._get_mistakes() + ["Quit"]
        error_window = menu.Menu(self.window, "Most serious mistakes", mistakes)
        result = error_window.launch()
        while result not in ("Quit", ""):
            result = error_window.launch()

    def _get_mistakes(self, mistake_count = 10):
        """return <mistake_count> errors"""
        def get_perc(key, value, all_count : int):
            all_count = all_count if all_count != 0 else 1
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
