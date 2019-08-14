# User configs

NAME = "Aphanasiy"
FIELD_FILE = "my_field.txt"
FLEET = {
	1: 4,
	2: 3,
	3: 2,
	4: 1,
}

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

# Network config

HOST = "192.168.43.14"
PORT = 1237
ENCODING = "utf-8"

## Field display config

cBASE = "~"
cMISS = "*"
cSHIP = "H"
cHURT = "X"
cDEAD = "F"

## TO-SERVER config

SHOT = "SHOT"
STOP = "STOP"
MISS = "MISS"
HURT = "HURT"
DEAD = "DEAD"

