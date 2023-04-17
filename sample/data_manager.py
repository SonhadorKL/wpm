import json
import time
from sample import constants
from sample.wpm_stats import WPMStatistics
from sample.wpm_stats import TextStatistics

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

class TextDataManager:
    """Class to update and load statistics of the text"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_text_data(file_name : str) -> dict:
        """
        Get information about text\n
        Return None if file not found
        """
        with open(constants.PATH_TO_TEXT_DATA, "r", encoding="utf8") as json_file:
            loaded_text = json.load(json_file)
            if file_name not in loaded_text:
                return None
            return loaded_text[file_name]

    @staticmethod
    def update_text_data(stats : TextStatistics) -> dict:
        """
        Update information about the text or add it
        """
        file_name = stats.file_name
        with open(constants.PATH_TO_TEXT_DATA, "r", encoding="utf8") as json_file:
            texts = json.load(json_file)
            if file_name not in texts or texts[file_name]["alltime"] > stats.all_time:
                texts[file_name] = {}
                texts[file_name]["alltime"] = stats.all_time
                texts[file_name]["times"] = stats.char_times
        with open(constants.PATH_TO_TEXT_DATA, "w", encoding="utf8") as json_file:
            json.dump(texts, json_file)

    @staticmethod
    def reset_data() -> None:
        """
        Delete all statistics about texts
        """
        with open(constants.PATH_TO_TEXT_DATA, "w", encoding="utf8") as json_file:
            json.dump({}, json_file)

    @staticmethod
    def get_best_time(file_name : str) -> float:
        """
        For given file name return best wpm
        """
        with open(constants.PATH_TO_TEXT_DATA, "r", encoding="utf8") as json_file:
            data = json.load(json_file)
            if file_name in data:
                return data[file_name]["alltime"]
        return None

class SettingsManager:
    """Class to control global test's settings"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_test_type() -> str:
        """Get user's test mode"""
        with open(constants.PATH_TO_SETTINGS, "r", encoding="utf8") as json_file:
            data = json.load(json_file)
            return data["test.type"]

    @staticmethod
    def set_test_type(test_type : str) -> None:
        """Set user's test mode"""
        with open(constants.PATH_TO_SETTINGS, "r", encoding="utf8") as json_file:
            data = json.load(json_file)
            data["test.type"] = test_type
        with open(constants.PATH_TO_SETTINGS, "w", encoding="utf8") as json_file:
            json.dump(data, json_file)
