import time
from collections import Counter

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

class TextStatistics:
    """Collect data about the text"""
    def __init__(self, file_name : str):
        self.file_name = file_name
        self.char_times = []
        self.start_time = time.time()
        self.all_time = float('inf')

    def add_next_character(self):
        """Call to register a new character"""
        self.char_times.append(time.time() - self.start_time)

    def fix_time(self):
        """Call to set spend time on the text"""
        self.all_time = time.time() - self.start_time

    def was_fixed(self):
        """Return if time was fixed"""
        return self.all_time != float('inf')
