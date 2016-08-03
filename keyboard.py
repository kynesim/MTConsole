#! /usr/bin/env python3

# keyboard.py
#
# Routines for parsing keyboard input
#
# Author: Rhodri James (rhodri@kynesim.co.uk)
# Date: 12 May 2016
#
# Copyright 2016 Kynesim Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
import shlex
import textwrap
from mtcmds import MTBuffer
from collections import namedtuple


# Convenience class for entries in the command table.  Subject to
# change: in particular this may turn into a real class if we have
# lots of commands that aren't just covers for MTAPI packets, as will
# be inevitable.
#
# Currently a `subsystem` field of `None` indicates that the command
# is not an MTAPI packet.  The handling of these "specials" is
# entirely done by the UIHandler class.
TableEntry = namedtuple("TableEntry",
                        "subsystem, type, command, help_text")

class UIHandler:
    """User Interface Handler class, (very) loosely based on cmd.Cmd.
    This version uses a command table rather than implying one from
    from the class attributes, largely because the bulk of the early
    commands are going to be simple veneers to MTAPI commands, which
    all have a very similar form.  Additional commands are implemented
    as attributes: the "xxx" command is implemented by do_xxx().

    There is no equivalent of the help_xxx() attributes of cmd.Cmd;
    just use the `help_text` field of the command table entries.

    If the command entered does not match a key in the command table,
    the parser goes to some effort to determine if it is a substring
    of any key.  If it is a substring of a single key, that command is
    selected; if it is ambiguous (a substring of several keys), a
    helpful error message detailing the ambiguity is given.  Note that
    commands are not case sensitive, and all table keys should be
    lower case.

    (Why are we not using cmd.Cmd directly?  Because it's a pain when
    you are monitoring multiple inputs, and we are here.)"""
    COMMAND_TABLE = {
        "help" : TableEntry(None, None, None,
                            "Supply help on the commands"),
        "quit" : TableEntry(None, None, None,
                            "Exit the program"),
        "ping" : TableEntry("SYS", "SREQ", "SYS_PING",
                            "Send a SYS_PING command to the serial port"),
        "version" : TableEntry("SYS", "SREQ", "SYS_VERSION",
                               "Send a SYS_VERSION command to the"
                               " serial port"),
        "reset" : TableEntry("SYS", "AREQ", "SYS_RESET_REQ",
                             "Request the CC2538 to reset itself")
    }

    def __init__(self, sock):
        """Create the UI handler instance.  Requires a serial comms
        socket for communicating with the device under
        investigation.  Otherwise interacts via stdin/stdout"""
        self.sock = sock
        print("MTAPI Console Program")
        print()
        self.prompt()

    def prompt(self):
        "Write the interactive prompt to stdout."
        print("> ", end="", flush=True)

    def __call__(self):
        """Read a line of text from stdin and act on it.  This is a
        blocking read, so ensure that there is data to be read before
        calling, otherwise serial input may be lost."""
        inline = sys.stdin.readline()
        tokens = shlex.split(inline)
        if not tokens:
            self.prompt()
            return True
        if tokens[0] == '?':
            cmd = "help"
        else:
            cmd = tokens[0].casefold()

        if cmd in UIHandler.COMMAND_TABLE:
            entry = UIHandler.COMMAND_TABLE[cmd]
        else:
            # See if cmd is a unique substring of a command name
            cmds = []
            for name in UIHandler.COMMAND_TABLE.keys():
                if name.startswith(cmd):
                    cmds.append(name)
            if not cmds:
                print("Unrecognised command '%s'" % tokens[0])
                self.prompt()
                return True
            elif len(cmds) == 1:
                cmd = cmds[0]
                entry = UIHandler.COMMAND_TABLE[cmd]
            else:
                print("Ambiguous command: do you mean",
                      " ,".join(cmds[:-1]),
                      "or", cmds[-1])
                self.prompt()
                return True

        if entry.subsystem is None:
            # This is one of our specials, either help or quit
            fn = getattr(self, "do_" + cmd)
            result = fn(tokens[1:])
            if result:
                self.prompt()
            return result
        buf = MTBuffer(entry.subsystem, entry.type, entry.command)
        if buf.cmd.parse_tokens(tokens, buf):
            buf.send(self.sock)
        else:
            self.do_help([cmd])
        self.prompt()
        return True

    def do_help(self, tokens):
        "Supply help on the commands"
        wrapper = textwrap.TextWrapper(subsequent_indent='\t')
        if tokens:
            # Help required on a specific command
            name = tokens[0].casefold()
            if name not in UIHandler.COMMAND_TABLE:
                print("Command", tokens[0], "not found")
                return True
            entry = UIHandler.COMMAND_TABLE[name]
            print("Syntax:", name, end=" ")
            if entry.subsystem is not None:
                # Deduce the command parameters from the MTAPI command
                buf = MTBuffer(entry.subsystem,
                               entry.type,
                               entry.command)
                info = []
                for field in buf.cmd.fields:
                    info.extend(field.field_info())
                print(" ".join(i[0] for i in info))
                for i in info:
                    i[2].helper(i[0])
            print()
            paragraphs = entry.help_text.split("\n\n")
            wrapper.initial_indent = "\t"
            for p in paragraphs:
                print(wrapper.fill(p))
        else:
            # List all the commands and their help text
            for name, entry in UIHandler.COMMAND_TABLE.items():
                paragraphs = entry.help_text.split("\n\n")
                wrapper.initial_indent = name + ":\t"
                print(wrapper.fill(paragraphs[0]))
                wrapper.initial_indent = "\t"
                for p in paragraphs[1:]:
                    print(wrapper.fill(p))
        return True

    def do_quit(self, tokens):
        "Exit the program"
        return False
