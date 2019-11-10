import sys
import socket
from config import *


def send(sock, message):
        sock.send(bytes(message, encoding=ENCODING))


def get(sock):
    raw = sock.recv(1024)
    msg = raw.decode(ENCODING)
    if (len(raw) == 0):
        print("Connection is closed.", file=sys.stderr)
        sys.exit(0)
    return msg


class Fields:
    def __init__(self, name1, name2):
        self.fields = [[[cBASE for i in range(10)] for j in range(10)] for k in range(2)]
        self.names = [name1, name2]
    def print_fields(self):
        print(self.names[1].rjust(12, ' ') + "\t\t" + self.names[0].rjust(12, ' '))
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
        if (code == DEAD or code == STOP):
            self.fields[i][y][x] = cDEAD
            self.fill_surroundings(self.fields[i], (y, x))

    def attack(self, defender, q, code):
        if (code == STOP):
            print(self.names[defender] + " Won. Congrutulations to winner!")
        y = ord(q[0]) - ord('A')
        x = ord(q[1]) - ord('0')
        self.modify_player(code, defender, y, x)
        self.print_fields()
        print(code)
        return code != MISS  # Your turn continues


class ServerGame:
    def __init__(self, 
                 name1, conn1, addr1,
                 name2, conn2, addr2,
                 tournament=False):
        self.name = [name1, name2]
        self.conn = [conn1, conn2]
        self.tournament=tournament
        send(conn1, "ST_1 {}".format(name2))
        send(conn2, "ST_2 {}".format(name1))
        if (self.tournament): self.field = Fields(name2, name1)
        print("      |{} vs {}|".format(name1, name2))
        print("      Tournament mode is " + ("en" if self.tournament else "dis") + "abled")

    def start(self):
        turn = 0
        while turn != -1:
            shot = get(self.conn[turn])
            if (self.tournament): 
                print("[{}] {} makes {}".format(
                       turn+1, self.name[turn], shot))
            send(self.conn[turn^1], shot)
            ans = get(self.conn[turn^1])
            if (self.tournament):
                print("[{}] {} answers: {}".format(
                   (turn^1)+1, self.name[turn^1], ans))
                self.field.attack(turn^1, shot.split()[1], ans)
            send(self.conn[turn], ans)
            if (ans not in {HURT, DEAD}):
                turn ^= 1
            if (ans == STOP):
                sys.exit(0)


class ClientGame:
    def __init__(self):
        settings_check()
        self.my_field = field_check(FIELD_FILE)
        self.enemy_field = [[cBASE for i in range(10)] for j in range(10)]
        self.server = socket.socket()
        self.server.connect((HOST, PORT))
        self.finished = 0
        self.my_turn = 0
        self.alive = sum([FLEET[x] * x for x in FLEET])
        send(self.server, NAME)
        code, *opponent = get(self.server).split()
        self.opponent = ' '.join(opponent)
        print("Your opponent is {}".format(self.opponent))
        if (code == "ST_1"):
            self.my_turn = 1
        elif (code == "ST_2"):
            self.my_turn = 0
        else:
            print("Wrong code: {}", file=sys.stderr)
            sys.exit(0)
        print("You are the {} player".format(code[-1]))

    def print_fields(self):
        print(self.opponent.rjust(12, ' ') + "\t\t" + NAME.rjust(12, ' '))
        print("  0123456789\t\t  0123456789")
        c = ord("A")
        for i in range(10):
            print(chr(c)+' '+''.join(self.enemy_field[i])+"\t\t"+chr(c) + ' ' + ''.join(self.my_field[i]))
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

    def modify_enemy(self, code, y, x):
        if (code == MISS):
            self.enemy_field[y][x] = cMISS
        if (code == HURT):
            self.enemy_field[y][x] = cHURT
        if (code == DEAD or code == STOP):
            self.enemy_field[y][x] = cDEAD
            self.fill_surroundings(self.enemy_field, (y, x))

    def attack(self):
        print("We are shooting, my captain!")
        ## BE AWARE OF MISSSHOT PROBLEM!!!
        q = input("Enter your shot: ")
        while (not (len(q) == 2 and
            q[0] in "ABCDEFGHIJ" and
            q[1] in "0123456789")):
            q = input("Wrong position. Try again: ")
        y = ord(q[0]) - ord('A')
        x = ord(q[1]) - ord('0')
        send(self.server, "SHOT {}".format(q))
        code = get(self.server)
        self.modify_enemy(code, y, x)
        self.print_fields()
        print(code)
        if (code == STOP):
            print("CONGRATULATIONS, MY COMMANDER!")
            print("YOU WON!")
            self.finished = 1
            return 0
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
        y = ord(q[0]) - ord('A')
        x = ord(q[1]) - ord('0')
        code = self.modify_me(code, y, x)
        if (code != MISS):
            self.alive -= 1
        if (not self.alive):
            code = STOP
            self.finished = 1
        send(self.server, code)

        self.print_fields()
        print("SHOT   >===> {} >===> {}  ".format(q, code))
        if (not self.alive):
            print("Sorry, comander, we losed...")
            print("Next time the faith will be on our side!")
            sys.exit(0)
        return code != MISS


def settings_check():
    global NAME
    if (len(NAME) > 12):
        print("Your name is too long. Shrink it to 12 symbols!")
        sys.exit(0)


def field_check(file):
    try:
        fld = open(file, 'r')
    except:
        print("No file {} in directory".format(FIELD_FILE), file=sys.stderr)
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
    # There must be also a contact and fleet check
    # Contact check
    for i in range(10 - 1):
        for j in range(10 - 1):
            if (field[i][j] == cSHIP and field[i + 1][j + 1] == cSHIP):
                print("CONTACT CHECK FAILED at field[{}][{}] and field[{}][{}]".format(i, j, i + 1, j + 1), file=sys.stderr)
                print('.' * 4 + '\n' + '.' + field[i][j] + field[i][j + 1] + '.\n.' + field[i + 1][j] + field[i + 1][j + 1] + '.\n' + '....')
                sys.exit(0)
    for i in range(10 - 1):
        for j in range(1, 10):
            if (field[i][j] == cSHIP and field[i + 1][j - 1] == cSHIP):
                print("CONTACT CHECK FAILED at field[{}][{}] and field[{}][{}]".format(i, j, i + 1, j - 1), file=sys.stderr)
                print('.' * 4 + '\n' + '.' + field[i][j - 1] + field[i][j] + '.\n.' + field[i + 1][j - 1] + field[i + 1][j] + '.\n' + '....')
                sys.exit(0)
    
    used_pos = set()
    used_sz = dict()
    def dfs(field, pos):
        stack = [(pos)]
        used_pos.add(pos)
        cnt = 0
        while (len(stack) > 0):
            cur = stack.pop()
            cnt += 1
            for i in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_y = cur[0] + i[0]
                new_x = cur[1] + i[1]
                if (not (0 <= new_x < 10 and 0 <= new_y < 10)):
                    continue
                if ((new_y, new_x) not in used_pos and 
                    field[new_y][new_x] == cSHIP):
                    stack.append((new_y, new_x))
                    used_pos.add((new_y, new_x))
        return cnt

    for i in range(10):
        for j in range(10):
            if (field[i][j] == cSHIP and (i, j) not in used_pos):
                cnt = dfs(field, (i, j))
                if cnt not in used_sz:
                    used_sz[cnt] = 0
                used_sz[cnt] += 1
    if (used_sz != FLEET):
        print("Your fleet isn't standart\n", file=sys.stderr)
        print("You have: ", used_sz, file=sys.stderr)
        print("Must be: ", FLEET, file=sys.stderr)
        sys.exit(0)
    return field
