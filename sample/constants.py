import curses

# Have to add this lines of code to initialise curses.COLORS
curses.initscr()
curses.start_color()

COLOR_GREY = 240
curses.init_pair(1, COLOR_GREY, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

GREY_BLACK = curses.color_pair(1)
MAGENTA_BLACK = curses.color_pair(2)
