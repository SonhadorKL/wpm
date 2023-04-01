"""Module which contains some useful functions to manipulate with texts"""
import curses
import os
import random
from sample import menu
from sample import plate


def choose_text(stdscr : curses.window) -> str:
    """Launch menu to get text file"""
    random_file_case = "RANDOM FILE"
    files = get_files("texts")
    options = [random_file_case] + files
    new_menu = menu.Menu(stdscr, "Choose the file", options)
    chosen_option = new_menu.launch()
    if chosen_option == random_file_case:
        file_name = random.choice(files)
    else:
        file_name = chosen_option
    with open("texts/" + file_name, "r", encoding="utf8") as file:
        return "".join(file.readlines())

def load_text(stdscr : curses.window):
    """Launch menu to load new files"""
    options = ["Show files", "Load file", "Write text", "Delete file", "Quit"]
    load_menu = menu.Menu(stdscr, "Loading menu", options)
    while True:
        result = load_menu.launch()
        if result == "Quit":
            return
        if result == "Show files":
            file_preview(stdscr)
        elif result == "Load file":
            file_loading(stdscr)
        elif result == "Write text":
            file_creating(stdscr)
        elif result == "Delete file":
            delete_file(stdscr)

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

def get_file_text(path : str):
    """Return text from file"""
    with open(path, "r", encoding="utf8") as file:
        return "".join(file.readlines())

def file_preview(window : curses.window):
    """Show names of texts as a menu with ability to watch texts itself"""
    is_processing = True
    options = ["QUIT"] + get_files("texts")
    preview_menu = menu.Menu(window, "Loaded files", options)
    while is_processing:
        user_input = preview_menu.launch()
        if user_input == "QUIT":
            is_processing = False
        else:
            show_plate = plate.ShowPlate(window, user_input, get_file_text("texts/" + user_input))
            show_plate.update()

def file_loading(window : curses.window):
    """Show the window to get path to the file"""
    is_processing = True
    headline = "Enter the path to the file you want to copy"
    example = "Example: /home/name/projects/python/test.txt"
    while is_processing:
        write_path = plate.WritablePlate(window, headline, example)
        result = write_path.process()
        if result == "":
            return
        if load_new_file(result) == "":
            is_processing = False

def delete_file(window : curses.window):
    """Menu to delete file"""
    files = get_files("texts")
    options = ["QUIT"] + files
    men = menu.Menu(window, "Choose file tou want to delete", options)
    result = men.launch()
    if result == "QUIT":
        return
    os.remove("texts/" + result)

def file_creating(window : curses.window):
    """Create a new file with writing name and text"""
    # Get name of new file
    name_headline = "Write a name for the file"
    name_example = "Example: HardText"
    file_name = ""
    while file_name == "":
        write_name = plate.WritablePlate(window, name_headline, name_example)
        file_name = write_name.process()
    # get content of file
    text_headline = "Write a text (or just paste it using <Ctrl + V>)"
    file_content = ""
    while file_content == "":
        write_text = plate.WritablePlate(window, text_headline, "")
        file_content = write_text.process()
    add_text(file_name, file_content)



def load_new_file(path: str) -> str:
    """
    Copy txt file from given path\n
    Return empty string on success
    """
    if not path.endswith(".txt"):
        return "ERROR: inappropriate file type"
    try:
        with open(path, "r", encoding="utf8") as file:
            name_of_file = "".join(path.split('/')[-1].split('.')[:-1])
            add_text(name_of_file, "".join(file.readlines()))
            return ""
    except FileNotFoundError:
        return "ERROR: file not found"
