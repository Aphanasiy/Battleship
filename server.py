#!/usr/bin/python3

import sys
import socket
from config import *


def send(sock, what):
		sock.send(bytes(what, encoding=ENCODING))


def get(sock):
	msg = sock.recv(1024)
	msg = msg.decode(ENCODING)
	return msg


def game(name1, conn1, addr1, name2, conn2, addr2):
	send(conn1, "ST_1 {}".format(name2))
	send(conn2, "ST_2 {}".format(name1))

	print("|{} vs {}|".format(name1, name2))
	turn = 1
	while turn != -1:
		if (turn):
			shot = get(conn1)
			print("[1] " + name1 + " shots to " + shot)
			send(conn2, shot)
			ans = get(conn2)
			if (ans == ""):
				print("Connection with [2] {}{} is failed".format(name2, addr2))
				conn1.close()
				conn2.close()
				return
			print("[2] " + name2 + " answers: " + ans)
			if (ans not in {HURT, DEAD}):
				turn ^= 1
			send(conn1, ans)
		else:
			shot = get(conn2)
			print("[2] " + name2 + " shots to " + shot)
			send(conn1, shot)
			ans = get(conn1)
			if (ans == ""):
				print("Connection with [1] {}{} is failed".format(name1, addr1))
				conn1.close()
				conn2.close()
				return
			print("[1] " + name1 + " answers: " + ans)
			if (ans not in {HURT, DEAD}):
				turn ^= 1
			send(conn2, ans)


sock = socket.socket()
sock.bind(("", PORT))
sock.listen(2)

conn1, addr1 = sock.accept()
name1 = get(conn1)
print("{} {} connected".format(name1, addr1))

conn2, addr2 = sock.accept()
name2 = get(conn2)
print("{} {} connected".format(name2, addr2))

game(name1, conn1, addr1, name2, conn2, addr2)