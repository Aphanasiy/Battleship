#!/usr/bin/python3

import sys
import socket
from config import *

sock = socket.socket()



PORT = 1237
ENCODING = "utf-8"
sock.bind(("", PORT))

sock.listen(2)
conn1, addr1 = sock.accept()
print("connected: {}".format(addr1))
conn2, addr2 = sock.accept()
print("connected: {}".format(addr2))


def send(sock, what):
		sock.send(bytes(what, encoding=ENCODING))

def get(sock):
	msg = sock.recv(1024)
	msg = msg.decode(ENCODING)
	return msg

send(conn1, "ST_1")
send(conn2, "ST_2")
if (get(conn1) != "OK" or get(conn2) != "OK"):
	print("OK FAIL", file=sys.stderr)
	sys.exit(0)
turn = 1
while turn != -1:
	if (turn):
		shot = get(conn1)
		print("1 shots to " + shot)
		send(conn2, shot)
		ans = get(conn2)
		print("2 answers: " + ans)
		send(conn1, ans)
	else:
		shot = get(conn2)
		print("2 shots to " + shot)
		send(conn1, shot)
		ans = get(conn1)
		print("1 answers: " + ans)
		send(conn2, ans)
	turn ^= 1
