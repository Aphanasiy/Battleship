# Network config

HOST = "localhost"
PORT = 1237
ENCODING = "utf-8"


# User configs

NAME = "Aphanasiy"
FIELD_FILE = "fields/main.txt"
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

No side and diagonal contact
"""


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

