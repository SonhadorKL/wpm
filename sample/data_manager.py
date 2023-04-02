import json
import time
from sample.wpm import WPMStatistics
from sample import constants

class DataManager:
    """Class to update and load user statistics"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def update_data(statistics : WPMStatistics):
        """Update data in user statistics"""
        if statistics is None:
            return
        user_stat = {}
        with open(constants.PATH_TO_DATA, "r", encoding="utf8") as json_file:
            user_stat = json.load(json_file)
            user_stat["test.wpm"] += statistics.wpm
            user_stat["test.count"] += 1
            user_stat["test.time"] += time.time() - statistics.start_time
            user_stat["test.bestwpm"] = max(user_stat["test.bestwpm"], statistics.wpm)
            for letter in statistics.symbol_count:
                if letter in user_stat["letters.count"]:
                    user_stat["letters.count"][letter] += statistics.symbol_count[letter]
                else:
                    user_stat["letters.count"][letter] = statistics.symbol_count[letter]

            for letter in statistics.symbol_errors:
                if letter in user_stat["letters.errors"]:
                    user_stat["letters.errors"][letter] += statistics.symbol_errors[letter]
                else:
                    user_stat["letters.errors"][letter] = statistics.symbol_errors[letter]
        with open(constants.PATH_TO_DATA, "w", encoding="utf8") as json_file:
            json.dump(user_stat, json_file)

    @staticmethod
    def get_data() -> dict:
        """Returt dictionaty with all user's statistics"""
        with open(constants.PATH_TO_DATA, "r", encoding="utf8") as json_file:
            return json.load(json_file)

    @staticmethod
    def reset_data() -> None:
        """Set statistics to start values"""
        data = {}
        with open(constants.PATH_TO_DATA, "r", encoding="utf8") as json_file:
            data = json.load(json_file)
            for key in data:
                if isinstance(data[key], dict):
                    data[key] = {}
                elif isinstance(data[key], (int, float)):
                    data[key] = 0
        with open(constants.PATH_TO_DATA, "w", encoding="utf8") as json_file:
            json.dump(data, json_file)
