import curses
import string

# Constants for colors
COLOR_GREY = 240

GREY_BLACK = 0
MAGENTA_BLACK = 0
GREEN_BLACK = 0

def init_colors():
    """Should be called after init scr"""

    # Have to do it, because I have to create a window before initialising pairs
    global GREY_BLACK
    global MAGENTA_BLACK
    global GREEN_BLACK
    curses.init_pair(1, COLOR_GREY, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    GREY_BLACK = curses.color_pair(1)
    MAGENTA_BLACK = curses.color_pair(2)
    GREEN_BLACK = curses.color_pair(3)

# Paths
PATH_TO_DATA = "data/user_statistics.json"

# KEYS
ESCAPE = 27
ENTER = 10
SPACE = 32
BACKSPACE = 127

def get_text_height(window : curses.window, text : str) -> int:
    """return the height of string in given window"""
    return (len(text)) // window.getmaxyx()[1] + 1

def check_letter(char : str) -> bool:
    """Check if char is can be printed"""
    is_alpha = char.isalpha()
    is_digit = char.isdigit()
    is_space = char == " "
    is_punctiation = char in string.punctuation
    return is_alpha or is_digit or is_space or is_punctiation
