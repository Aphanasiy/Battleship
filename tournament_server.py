#!/usr/bin/python3

import sys
import socket
from config import *


def send(sock, what):
		sock.send(bytes(what, encoding=ENCODING))


def get(sock):
	msg = sock.recv(1024)
	msg = msg.decode(ENCODING)
	if (len(msg) == 0):
		print("Connection is closed.", file=sys.stderr)
		sys.exit(0)
	return msg


class Fields:
	def __init__(self, name1, name2):
		self.fields = [[[cBASE for i in range(10)] for j in range(10)] for k in range(2)]
		self.names = [name1, name2]
	def print_fields(self):
		print(self.names[0].rjust(12, ' ') + "\t\t" + self.names[1].rjust(12, ' '))
		print("  0123456789\t\t  0123456789")
		c = ord("A")
		for i in range(10):
			print(chr(c)+' '+''.join(self.fields[0][i])+"\t\t"+chr(c) + ' ' + ''.join(self.fields[1][i]))
			c += 1
		print("____________\t\t____________")
		return

	def fill_surroundings(self, field, pos):
		stack = [pos]
		used = set(stack)
		while (len(stack) > 0):
			cur = stack.pop()
			for i in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
				new_y = cur[0] + i[0]
				new_x = cur[1] + i[1]
				if (not (0 <= new_x < 10 and 0 <= new_y < 10)):
					continue
				if (field[new_y][new_x] == cBASE):
					field[new_y][new_x] = cMISS
				elif ((new_y, new_x) not in used and 
					   field[new_y][new_x] == cHURT):
					field[new_y][new_x] = cDEAD
					stack.append((new_y, new_x))
					used = set(pos)

	def modify_player(self, code, i, y, x):
		if (code == MISS):
			self.fields[i][y][x] = cMISS
		if (code == HURT):
			self.fields[i][y][x] = cHURT
		if (code == DEAD):
			self.fields[i][y][x] = cDEAD
			self.fill_surroundings(self.fields[i], (y, x))

	def attack(self, defender, q, code):
		if (code == STOP):
			print(self.name[defender^1] + " Won. Congrutulations to winner!")
			return
		y = ord(q[0]) - ord('A')
		x = ord(q[1]) - ord('0')
		self.modify_player(code, defender, y, x)
		self.print_fields()
		print(code)
		return code != MISS  # Your turn continues



def game(name1, conn1, addr1, name2, conn2, addr2):
	send(conn1, "ST_1 {}".format(name2))
	send(conn2, "ST_2 {}".format(name1))
	f = Fields(name1, name2)
	print("      |{} vs {}|".format(name1, name2))
	turn = 1
	while turn != -1:
		if (turn):
			shot = get(conn1)
			print("[1] " + name1 + " makes " + shot)
			send(conn2, shot)
			ans = get(conn2)
			print("[2] " + name2 + " answers: " + ans)
			f.attack((turn + 1) % 2, shot.split()[1], ans)
			if (ans not in {HURT, DEAD}):
				turn ^= 1
			send(conn1, ans)
		else:
			shot = get(conn2)
			print("[2] " + name2 + " makes " + shot)
			send(conn1, shot)
			ans = get(conn1)
			print("[1] " + name1 + " answers: " + ans)
			f.attack((turn + 1) % 2, shot.split()[1], ans)
			if (ans not in {HURT, DEAD}):
				turn ^= 1
			send(conn2, ans)


sock = socket.socket()
sock.bind(("", PORT))
sock.listen(2)

conn1, addr1 = sock.accept()
name1 = get(conn1)
print("[1] {} {} connected".format(name1, addr1))

conn2, addr2 = sock.accept()
name2 = get(conn2)
print("[2] {} {} connected".format(name2, addr2))

game(name1, conn1, addr1, name2, conn2, addr2)