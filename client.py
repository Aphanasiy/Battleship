#!/usr/bin/python3


import socket
import sys
from config import *


def check_field(file):
	try:
		fld = open(file, 'r')
	except:
		print("No file {} in directory", file=sys.stderr)
		sys.exit(0)
	field = fld.readlines()
	fld.close()
	if (len(field) != 10):
		print("There are {} != 10 lines in file".format(len(field)), file=sys.stderr)
		sys.exit(0)
	for i in range(10):
		field[i] = list(field[i].strip())
		if (len(field[i]) != 10):
			print("There are {} != 10 cols in line {}".format(len(field[i]), i), file=sys.stderr)
			sys.exit(0)
	#There must be also a contact and fleet check
	return field


def send(server, trn):
	server.send(bytes(trn, encoding=ENCODING))
def get(server):
	msg = server.recv(1024)
	code = msg.decode(ENCODING)
	return code


class Game:
	def __init__(self):
		self.my_field = check_field(FIELD_FILE)
		self.enemy_field = [[cBASE for i in range(10)] for j in range(10)]
		self.server = socket.socket()
		self.server.connect((HOST, PORT))
		self.finished = 0
		self.my_turn = 0
		send(self.server, "OK")
		code = get(self.server)
		if (code == "ST_1"):
			self.my_turn = 1
		elif (code == "ST_2"):
			self.my_turn = 0
		else:
			print("Wrong code: {}", file=sys.stderr)
			sys.exit(0)
		print("You are the {} player".format(code[-1]))

	def print_fields(self):
		print("  0123456789\t\t  0123456789")
		c = ord("A")
		for i in range(10):
			print(chr(c)+' '+''.join(self.my_field[i])+"\t\t"+chr(c) + ' ' + ''.join(self.enemy_field[i]))
			c += 1
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

	def modify_enemy(self, code, y, x):
		if (code == MISS):
			self.enemy_field[y][x] = cMISS
		if (code == HURT):
			self.enemy_field[y][x] = cHURT
		if (code == DEAD):
			self.enemy_field[y][x] = cDEAD
			self.fill_surroundings(self.enemy_field, (y, x))

	def attack(self):
		print("We are shooting, my captain!")
		q = input("Enter your shot: ")
		while (not (len(q) == 2 and
			q[0] in "ABCDEFGHIJ" and
			q[1] in "0123456789")):
			q = input("Wrong position. Try again: ")
		y = ord(q[0]) - ord('A')
		x = ord(q[1]) - ord('0')
		send(self.server, "SHOT {}".format(q))
		code = get(self.server)
		if (code == STOP):
			self.finished = 1
			return 0
		print(code)
		self.modify_enemy(code, y, x)
		self.print_fields()
		return code != MISS  # Your turn continues

	def modify_me(self, code, y, x):
		if (self.my_field[y][x] == cBASE):
			self.my_field[y][x] = cMISS
			return MISS
		elif (self.my_field[y][x] in {cMISS, cDEAD, cHURT}):
			return MISS
		else:
			self.my_field[y][x] = cHURT
			pos = (y, x)
			stack = [pos]
			used = set(stack)
			# is dead check
			while (len(stack) > 0):
				cur = stack.pop()
				for i in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
					new_y = cur[0] + i[0]
					new_x = cur[1] + i[1]
					if (not (0 <= new_x < 10 and 0 <= new_y < 10)):
						continue
					if (self.my_field[new_y][new_x] == cSHIP):
						return HURT
					elif ((new_y, new_x) not in used and 
						  self.my_field[new_y][new_x] == cHURT):
						stack.append((new_y, new_x))
						used.add((new_y, new_x))
			# is dead check end
			self.my_field[y][x] = cDEAD
			self.fill_surroundings(self.my_field, (y, x))
			return DEAD
		
	def defence(self):
		print("Now we are waiting for enemy attack!")
		code, *q = get(self.server).split()
		if (code != SHOT):
			print("SHOT expected, but {} found".format(code), file=sys.stderr)
			sys.exit(0)
		q = q[0]
		print("SHOT   >===> {} >===>".format(q))
		y = ord(q[0]) - ord('A')
		x = ord(q[1]) - ord('0')
		code = self.modify_me(code, y, x)
		send(self.server, code)
		self.print_fields()
		return code != MISS


game = Game()
while (not game.finished):
	if (game.my_turn):
		while game.attack():
			pass
	else:
		while game.defence():
			pass
	game.my_turn ^= 1
