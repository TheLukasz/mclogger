from mcstatus import JavaServer
from datetime import datetime
import time

class log:
    def __init__(self, name):
        self.file_name = name
        self.file = open(self.file_name,"a")
    def write(self, text):
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        to_print = f"[{dt_string}] " + text
        print(to_print,end="")
        self.file.write(to_print)
    def close(self):
        self.file.close()

server = JavaServer.lookup("******:25578")
status = server.status()

print(f"status: {status.version.name} {status.latency:8.2f}ms")

if status.players.sample:
    players_online = [x.name for x in status.players.sample]

    print("players online:")
    for player in players_online :
        print("\t* ",player)
else:
    players_online = []
    print("No players Online")


log = log("log.txt")
player_table = {}

for player in players_online :
    if player_table.get(player,0) == 0 :
        player_table[player] = 1

while(1):
    for player in players_online :
        if player_table.get(player,0) == 0 :
            player_table[player] = 1
            log.write(f"{player} joined\n")

    for player in player_table.keys():
        if player not in players_online and player_table[player] == 1:
            player_table[player] = 0
            log.write(f"{player} left\n")

    time.sleep(5)

    printed_shutdown = 0
    while(1):
        try:
            status = server.status()
            err = None
        except TimeoutError as e:
            err = e
            if not printed_shutdown:
                log.write("Server shutdown")
                printed_shutdown = 1
        if err:
            sleep(10)
        else:
            if printed_shutdown:
                log.write("Server online")
            break

    if status.players.sample:
        players_online = [x.name for x in status.players.sample]
    else:
        players_online = []

log.close()
