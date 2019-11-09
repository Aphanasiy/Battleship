#!/usr/bin/python3

from Battleship import *


def argparsing():
	global PORT, FIELD_FILE
	k = sys.argv
	if ("-h" in k or "--help" in k):
		print("""
    It's client for console Battleship.
    Look at config.py for more detailed settings.
    
    This app has some arguements:
    \t -h, --help               - printing this message
    \t -p, --port    =<PORT>    - changing of listened port
    \t     --field   =<FILE>    - set the file with your map
""")
		sys.exit(0)
		return 0

	for i in k:
		if (i[:2] == "-p" or i[:6] == "--port"):
			p = i.split("=")
			PORT = int(p[1])
		if (i[:7] == "--field"):
			p = i.split("=")
			FIELD_FILE = p[1]


argparsing()


game = ClientGame()
while (not game.finished):
	if (game.my_turn):
		while game.attack():
			pass
	else:
		while game.defence():
			pass
	game.my_turn ^= 1
