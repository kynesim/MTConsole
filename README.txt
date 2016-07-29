MTConsole
=========

A serial terminal for talking TI's Monitor Test API to CC2538 and
similar chips.  MTConsole is distributed under version 2.0 of the
Apache License: see http://www.apache.org/licenses/LICENSE-2.0 for
details, but in summary you can use and redistribute it as long as due
credit is given.

MTConsole is a Python3 program; you will need to download the Python3
interpreter from www.python.org if you haven't already.

MTConsole consists of a command-line parser (keyboard.py) and a serial
input parser (mtcmds.py).  The former is currently trivial (supporting
Ping, Version and Reset), but the latter will parse the documented
MTAPI packet types and commands.  A large suite of unit tests ensure
the serial input parser conforms to the MTAPI documentation; tweaking
may be needed as undocumented issues appear or the meanings of
enumerated fields become clear.

The serial input parser outputs values in hexadecimal or as text.  It
is a little inconsistent about whether the hexadecimal is given with a
leading "0x" or not.  This is partially deliberate: I am used to
seeing short network addresses, cluster IDs and the like as four
unadorned hex digits.  This will probably get tweaked as it causes me
confusion or decimal output is more sensible.

Note that the command-line parser is currrently very primative and
incomplete.  Only the most basic field types support it, and only for
numeric input.  This, obviously, is the next target.

-- Rhodri James, 28/7/16
