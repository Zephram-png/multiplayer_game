import socket
from _thread import *

from player import Player
import sys
import pickle

server = "10.88.174.47"
port = 5553
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))



s.listen()
print("Waiting for a connection, Server Started")

current_player_turn = 0
true_current_player_turn = 0

players = [Player([(0, 100)], 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
           , Player([(0, 100)], 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0)]

def threaded_client(conn, player):
    global current_player_turn, true_current_player_turn
    conn.send(pickle.dumps((players[player], current_player_turn)))

    reply = ""
    while True:
        try:
            data, current_player_turn = pickle.loads(conn.recv(2048 * 1))
            players[player] = data

            # If the player hit confirm button
            if players[player].player_confirmed == 1:
                print(player, players[player].player_confirmed)
            if players[player].player_confirmed == 1:
                true_current_player_turn = current_player_turn

            if true_current_player_turn == 0:
                current_player_turn = 0
            else:
                current_player_turn = 1

            if not data:
                print("Disconnected")
                break

            if player == 1:
                reply = (players[0], current_player_turn)
            else:
                reply = (players[1], current_player_turn)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1