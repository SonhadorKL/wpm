import json
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
