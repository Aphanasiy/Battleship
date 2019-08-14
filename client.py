import socket
import sys


HOST = "localhost"
PORT = 1237
ENCODING = "utf-8"

cBASE = "~"
cMISS = "*"
cSHIP = "H"
cHURT = "X"
cDEAD = "F"

MISS = "MISS"
HURT = "HURT"
DEAD = "DEAD"

FIELD_FILE = "my_field.txt"

"""
It must contain field 10x10 like:
~~~~~~~~H~
~H~~~~~~~~
~H~~~HHH~~
~H~~~~~~~~
~H~~H~~~~~
~~~~~~~~~~
HH~~~~~HH~
~~~~~H~~~~
H~~H~~~~~~
~~~H~~~~~~

HHHH x1
HHH x2
HH x3
H x4

No side and diagonal contact
"""


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
		if (len(field[i]) != 10):
			print("There are {} != 10 cols in line {}".format(len(field[i]), i), file=sys.stderr)
			sys.exit(0)
	#There must be also a contact and fleet check
	

class Game:
	def __init__():
		my_field = check_field(FIELD_FILE)
		enemy_field = [[cBASE for i in range(10)] for j in range(10)]
		server = socket.socket()
		server.connect((HOST, PORT))
		finished = 0
		my_turn = 0
		send("OK")
		code = get_code()
		if (code == "ST_1"):
			my_turn = 1
		elif (code == "ST_2"):
			my_turn = 0
		else:
			print("Wrong code: {}", file=sys.stderr)
			sys.exit(0)
	def send(trn):
		server.send(bytes(trn), encoding=ENCODING)
	def get_code():
		msg = server.recv(1024)
		code = msg.decode(ENCODING)
	def print_fields():
		print("  0123456789\t\t  0123456789")
		c = ord("A")
		for i in range(10):
			print(chr(c)+' '+''.join(my_field[i])+"\t\t"+chr(c) + ' ' + ''.join(enemy_field[i]))
			c += 1
		return

	def fill_surroundings(field, pos):
		stack = [pos]
		while (len(stack) > 0):
			cur = stack.pop():
			for i in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
				new_y = cur[0] + i[0]
				new_x = cur[1] + i[1]
				if (not (0 <= x < 10 and 0 <= y < 10)):
					continue
				if (field[new_y][new_x] == cBASE):
					field[new_y][new_x] = cMISS
				elif (field[new_y][new_x] == cHURT):
					field[new_y][new_x] = cDEAD
					stack.append((new_y, new_x))
	def modify_enemy(code, y, x):
		if (code == MISS):
			enemy_field[y][x] = cMISS
		if (code == HURT):
			enemy_field[y][x] = cHURT
		if (code == DEAD):
			enemy_field[y][x] = cDEAD
			fill_surroundings(enemy_field, (y, x))
	def attack():
		q = input("Enter your shot: ")
		while (not (len(q) == 2 J and
			q[0] in "ABCDEFGHIJ" and
			q[1] in "0123456789")):
			q = input("Wrong position. Try again: ")
		y = ord(q[0]) - ord('A')
		x = ord(q[1]) - ord('0')
		send("SHOT {}".format(q))
		code = get_code()
		if (code == STOP):
			finished = 1
			return 0
		print(code)
		modify_enemy(code, y, x)
		print_fields()
		return code != MISS  # Your turn continues

	def modify_me(code, y, x):
		if (my_field[y][x] == cBASE):
			my_field[y][x] = cMISS
			return MISS
		elif (my_field[y][x] in {cMISS, cDEAD, cHURT}):
			return MISS
		else:
			my_field[y][x] = cHURT
			stack = [pos]
			# is dead check
			while (len(stack) > 0):
				cur = stack.pop():
				for i in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
					new_y = cur[0] + i[0]
					new_x = cur[1] + i[1]
					if (not (0 <= x < 10 and 0 <= y < 10)):
						continue
					if (field[new_y][new_x] == cSHIP):
						return HURT
					elif (field[new_y][new_x] == cHURT):
						stack.append((new_y, new_x))
			# is dead check end
			my_field[y][x] = cDEAD
			fill_surroundings(my_field, y, x)
			return DEAD
		


	def defence():
		code, q* = get_code().split()
		if (msg != SHOT):
			print("SHOT expected, but {} found".format(code), file=sys.stderr)
			sys.exit(0)
		y = ord(q[0]) - ord('A')
		x = ord(q[1]) - ord('0')
		code = modify_me(code, y, x)
		send(code)
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
