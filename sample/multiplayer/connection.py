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
        """Connect to the server"""
        connection_plate = plate.ShowPlate(self.window, "Connection...", "Waiting other players")
        connection_plate.print_screen()
        server_ip = self._get_server_ip()
        if not self._check_connection(server_ip):
            return
        try:
            got_data = self.network.create_new_player(server_ip, self.window)
            name, text =  got_data["name"], got_data["text"]
        except Exception as _:
            return
        wpm = MultiplayerWPM(self.window, text, name, self.network)
        wpm.wpm_test()
        self.network.kill_process()

    def _get_server_ip(self) -> str:
        """Return chosen server IP"""
        header = "Enter server IP (0 for connection to local server)"
        ip_example = "Example: 192.168.0.1"
        get_ip_plate = plate.WritablePlate(self.window, header, ip_example)
        server_ip = get_ip_plate.process()
        if server_ip == "0":
            server_ip = "127.0.0.1"
        return server_ip

    def _check_connection(self, server_ip : str) -> bool:
        """Chech if IP is valid"""
        values = server_ip.split('.')
        return len(values) == 4 and all(0 <= int(value) <= 255 for value in values)
