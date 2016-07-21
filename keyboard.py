#! /usr/bin/env python3

# keyboard.py
#
# Routines for parsing keyboard input

import sys
import shlex
import textwrap
from mtcmds import MTBuffer
from collections import namedtuple


TableEntry = namedtuple("TableEntry",
                        "subsystem, type, command, help_text")

class UIHandler:
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
        self.sock = sock
        print("MTAPI Console Program")
        print()
        self.prompt()

    def prompt(self):
        print("> ", end="", flush=True)

    def __call__(self):
        inline = sys.stdin.readline()
        tokens = shlex.split(inline)
        if not tokens:
            self.prompt()
            return True
        if tokens[0] == '?':
            cmd = "help"
        else:
            cmd = tokens[0].lower()

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
            name = tokens[0].lower()
            if name not in UIHandler.COMMAND_TABLE:
                print("Command", tokens[0], "not found")
                return True
            entry = UIHandler.COMMAND_TABLE[name]
            print("Syntax:", name, end=" ")
            if entry.subsystem is not None:
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
