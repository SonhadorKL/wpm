import curses
import string
import time

# Constants for colors
COLOR_GREY = 240

GREY_BLACK = 0
MAGENTA_BLACK = 0
GREEN_BLACK = 0
YELLOW_BLACK = 0

def init_colors():
    """Should be called after init scr"""

    # Have to do it, because I have to create a window before initialising pairs
    global GREY_BLACK
    global MAGENTA_BLACK
    global GREEN_BLACK
    global YELLOW_BLACK
    curses.init_pair(1, COLOR_GREY, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    GREY_BLACK = curses.color_pair(1)
    MAGENTA_BLACK = curses.color_pair(2)
    GREEN_BLACK = curses.color_pair(3)
    YELLOW_BLACK = curses.color_pair(4)

# Paths
PATH_TO_DATA = "data/user_statistics.json"
PATH_TO_TEXT_DATA = "data/text_statistics.json"
PATH_TO_SETTINGS = "data/settings.json"

# KEYS
ESCAPE = 27
ENTER = 10
SPACE = 32
BACKSPACE = 127

def get_text_height(window : curses.window, text : str, start_pos_x = 0) -> int:
    """return the height of string in given window"""
    return (start_pos_x + len(text)) // window.getmaxyx()[1] + 1

def check_letter(char : str) -> bool:
    """Check if char is can be printed"""
    is_alpha = char.isalpha()
    is_digit = char.isdigit()
    is_space = char == " "
    is_punctiation = char in string.punctuation
    return is_alpha or is_digit or is_space or is_punctiation

def get_time(start_time):
    """Return time in seconds"""
    return time.time() - start_time
