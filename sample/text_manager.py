import curses
import os
import string
import random
from sample import menu
from sample import commands


def choose_text(stdscr : curses.window) -> str:
    """Launch menu to get text"""
    files = get_files("texts")
    start_game_commands = [
        commands.Command("random", 0)
    ]
    new_menu = menu.ConsoleMenu(stdscr, "Choose the file", files, start_game_commands)
    chosen_one = new_menu.launch().split()
    match chosen_one[0]:
        case "random":
            file_name = random.choice(files)
        case _:
            file_name = chosen_one[0]
    with open("texts/" + file_name, "r", encoding="utf8") as file:
        return "".join(file.readlines())

def load_text(stdscr : curses.window):
    """Launch menu to load new files"""
    files = get_files("texts")
    loading_commands = [
        commands.Command("quit", 0),
        commands.Command("addtext", 2, "Could not add text."),
        commands.Command("load", 1, "You did not provide path to file")
    ]
    while True:
        load_menu = menu.ConsoleMenu(stdscr, "Saved files", files, loading_commands)
        user_input = load_menu.launch().split()
        match user_input[0]:
            case "quit":
                return
            case "addtext":
                add_text(user_input[1], " ".join(user_input[2:]))
            case "load":
                pass

def get_files(path : str) -> list:
    """Simple function to get all files from directory"""
    files = []
    for file in os.scandir(path):
        if file.is_file():
            files.append(file.name)
    return files

def add_text(name: str, text: str):
    """Create a new file with given name and text"""
    with open("texts/" + name + ".txt", "w", encoding="utf8") as file:
        file.write(text)

def check_letter(char : str) -> bool:
    """Check if char is can be printed"""
    is_alpha = char.isalpha()
    is_digit = char.isdigit()
    is_space = char == " "
    is_punctiation = char in string.punctuation
    return is_alpha or is_digit or is_space or is_punctiation
