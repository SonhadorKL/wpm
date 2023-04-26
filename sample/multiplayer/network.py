import socket
import curses
import pickle
from sample import text_manager
from sample import data_manager
from sample.plate import ShowPlate
from sample.multiplayer.data import SendData

IP = "127.0.0.1"

class Network:
    """Class to interact with the server"""
    def __init__(self) -> None:
        self.user_socket : socket

    def create_new_player(self, window : curses.window) -> str:
        """
        Run to connect to server
        Return connection result
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 5555))
        # Get the result of connection
        client_socket.recv(1024)
        ch_name, ch_text = text_manager.choose_text(window)
        
        # Send choosed text
        nick = data_manager.SettingsManager().get_nickname()
        text_data = SendData("text", text=ch_text, name=ch_name, nickname=nick)
        client_socket.sendall(pickle.dumps(text_data))
        waiting = ShowPlate(window, f"You've made your desicion: {ch_name}", "Waiting for opponent")
        waiting.print_screen()

        # Get system's text
        choosed_text = pickle.loads(client_socket.recv(1024))

        self.user_socket = client_socket
        return choosed_text.data

    def update_data(self, data : str):
        """Run to update data on server. Return other player's progress"""
        player_info = SendData("player", text=data)
        self.user_socket.send(pickle.dumps(player_info))
        response = self.user_socket.recv(1024)
        return pickle.loads(response).data["text"]

    # def update_data(self, data : SendData):
    #     """Run to update data on server. Return other player's progress"""
    #     player_info = SendData("player", text=data)
    #     self.user_socket.send(pickle.dumps(player_info))
    #     response = self.user_socket.recv(1024)
    #     return pickle.loads(response).data["text"]

    def kill_process(self):
        """Send signal to the server that player left"""
        signal = pickle.dumps(SendData("dead"))
        self.user_socket.send(signal)
        self.user_socket.close()
