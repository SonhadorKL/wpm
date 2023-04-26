import socket
import threading
import random
import pickle
from sample.multiplayer.data import SendData

class Server:
    """Just a server. Run if you want to be able to play with your friends"""
    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_data = []
        self.players_sockets = []
        self.choosed_texts = []
        self.nicknames = []
        self.player_count = 0
        self.is_running = False
        self._open_server() 
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f'Server {ip_address} is open. Waiting for connection...')

    def reset_session(self):
        """Restart data about users"""
        for socket in self.players_sockets:
            socket.close()
        self.players_sockets = []
        self.choosed_texts = []
        self.nicknames = []
        self.user_data = [SendData("player", nick="player1", text=""),
                          SendData("player", nick="player2", text="")]
        self.player_count = 0
        self.is_running = False


    def _open_server(self):
        """It's fine"""
        # Not sure about IP-adress
        self.server_socket.bind(('0.0.0.0', 5555))
        # Maximum two players
        self.server_socket.listen(2)

    def connect_player(self, player_socket, player_num):
        """A thread for a new player. Get data - send data back until it dead"""
        while True:
            try:
                # recved_data = player_socket.recv(1024).decode()
                recved_data = player_socket.recv(4096)
                if not recved_data:
                    break
                data = pickle.loads(recved_data)
                # Get basic information about user
                if data.tag == "text":
                    self.choosed_texts.append((data.data["name"], data.data["text"]))
                    self.nicknames.append(data.data["nickname"])
                    print("Connected:",data.data["nickname"])
                    continue
                # Dead
                if data.tag == "dead":
                    break
                # Update data about players
                if player_num == 1:
                    self.user_data[0].data["text"] = data.data["text"]
                    reply = pickle.dumps(self.user_data[1])
                elif player_num == 2:
                    self.user_data[1].data["text"] = data.data["text"]
                    reply = pickle.dumps(self.user_data[0])
                player_socket.sendall(reply)
            except Exception as exc:
                print(exc)
                break

        print(f"Lost connection with {player_num}")
        self.player_count -= 1
        if self.player_count == 0:
            self.reset_session()


    def run(self):
        """
        Run to start connection
        Wait for two players and start the game
        """
        players_threads = []
        while self.player_count != 2:
            client_socket, client_address = self.server_socket.accept()
            self.players_sockets.append(client_socket)
            print(f"{client_address} connected")
            thread = threading.Thread(target = self.connect_player, args = (client_socket, self.player_count + 1, ))
            players_threads.append(thread)
            thread.start()
            self.player_count += 1
            to_send = SendData("info", message="Connected. Waiting for other person")
            client_socket.sendall(pickle.dumps(to_send))

        while len(self.choosed_texts) != 2:
            pass
        text = random.choice(self.choosed_texts)
        choosed_text = SendData("text", text=text[1], name=f"{self.nicknames[0]} vs. {self.nicknames[1]}")
        for sockets in self.players_sockets:
            sockets.sendall(pickle.dumps(choosed_text))
        print("Start the game!")

    def __del__(self):
        self.server_socket.close()
