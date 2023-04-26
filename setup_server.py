from sample.multiplayer.server import Server

if __name__ == "__main__":
    server = Server()
    while True:
        server.reset_session()
        server.run()
        while server.player_count > 0:
            pass

 