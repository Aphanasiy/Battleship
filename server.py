#!/usr/bin/python3

from Battleship import *
TOURNAMENT = False



def argparsing():
	global PORT, TOURNAMENT
	k = sys.argv
	if ("-h" in k or "--help" in k):
		print("""
    It's server for console Battleship.
    Look at config.py for more detailed settings.
    
    This app has some arguements:
    \t -h, --help               - printing this message
    \t -p, --port  =<PORT>      - changing of listened port
    \t -t, --tournament         - enable tournament mode
""")
		sys.exit(0)
		return 0

	for i in k:
		if (i[:2] == "-p" or i[:6] == "--port"):
			p = i.split("=")
			PORT = int(p[1])
		if (i == "-t" or i == "--tournament"):
			TOURNAMENT = True
			print("Tournament mode enabled")


argparsing()

			

sock = socket.socket()
sock.bind(("", PORT))
sock.listen(2)

print(f"Server has been started at port {PORT}")
conn1, addr1 = sock.accept()
name1 = get(conn1)
print(f"[1] {name1} {addr1} connected".format(name1, addr1))

conn2, addr2 = sock.accept()
name2 = get(conn2)
print(f"[2] {name2} {addr2} connected".format(name2, addr2))

game = ServerGame(name1, conn1, addr1, name2, conn2, addr2, tournament=TOURNAMENT)
game.start()