import curses
from sample import plate
from sample.multiplayer import network
from sample.multiplayer.wpm_multiplayer import MultiplayerWPM
from sample.multiplayer.data import SendData

class MultiplayerConnection:
    """Just a class to run a multiplayer """
    def __init__(self, window : curses.window) -> None:
        self.window = window
        self.network = network.Network()

    def run(self):
        self.plate = plate.ShowPlate(self.window, "Connection...", "Waiting other players")
        self.plate.print_screen()
        try:
            got_data = self.network.create_new_player(self.window)
            name, text =  got_data["name"], got_data["text"]
        except Exception as _:
            return
        wpm = MultiplayerWPM(self.window, text, name, self.network)
        wpm.wpm_test()
        self.network.kill_process()