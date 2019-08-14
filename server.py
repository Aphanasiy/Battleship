def create_field():
	return [["~" for i in range(10)] for j in range(10)]

def print_field(field):
	print("  0123456789")
	c = ord("A")
	for i in field:
		print(chr(c)+' '+''.join(i))
		c += 1
	return

class Game:
	def __init__():
		f1 = create_field()
		f2 = create_field()
	def turn():
		q = input("Enter your shot: ")
		while (not (len(q) == 2 J and
			q[0] in "ABCDEFGHIJ" and
			q[1] in "0123456789")):
			q = input("Wrong position. Try again: ")
		send(q)
	


f = create_field()
print_field(f)