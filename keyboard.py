#! /usr/bin/env python3

# keyboard.py
#
# Routines for parsing keyboard input

import sys
import shlex
import textwrap
from mtcmds import MTBuffer


class UIHandler:
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
            cmd = "do_help"
        else:
            cmd = "do_" + tokens[0].lower()

        try:
            fn = getattr(self, cmd)
        except AttributeError:
            # See if cmd is a unique substring of a command name
            cmds = []
            for name in dir(self.__class__):
                if name.startswith(cmd):
                    cmds.append(name)
            if not cmds:
                print("Unrecognised command '%s'" % cmd)
                self.prompt()
                return True
            elif len(cmds) == 1:
                fn = getattr(self, cmds[0])
            else:
                print("Ambiguous command: do you mean",
                      " ,".join(c[3:] for c in cmds[:-1]),
                      "or", cmds[-1][3:])
                self.prompt()
                return True

        result = fn(tokens)
        if result:
            self.prompt()
        return result

    def do_help(self, tokens):
        "Supply help on the commands"
        wrapper = textwrap.TextWrapper(subsequent_indent='\t')
        if tokens:
            name = tokens[1].lower()
            try:
                fn = getattr(self, "help_" + name)
            except AttributeError:
                try:
                    fn = getattr(self, "do_" + name)
                except AttributeError:
                    print("Command", tokens[1], "not found")
                    return True
                print("Syntax:", tokens[1])
                help_text = getattr(self, "do_" + name).__doc__
                paragraphs = help_text.split("\n\n")
                wrapper.initial_indent = "\t"
                for p in paragraphs:
                    print(wrapper.fill(p))
                return True

            # There is an explicit help function, call it!
            fn(tokens[1:])
        else:
            for name in dir(self.__class__):
                if name.startswith("do_"):
                    help_text = getattr(self, name).__doc__
                    paragraphs = help_text.split("\n\n")
                    wrapper.initial_indent = name[3:] + ":\t"
                    print(wrapper.fill(paragraphs[0]))
                    wrapper.initial_indent = "\t"
                    for p in paragraphs[1:]:
                        print(wrapper.fill(p))
        return True

    def do_quit(self, tokens):
        "Exit the program"
        return False

    def do_ping(self, tokens):
        "Send a SYS_PING command to the serial port"
        buf = MTBuffer("SYS", "SREQ", "SYS_PING")
        buf.send(self.sock)
        return True

    def do_version(self, tokens):
        "Send a SYS_VERSION command to the serial port"
        buf = MTBuffer("SYS", "SREQ", "SYS_VERSION")
        buf.send(self.sock)
        return True

    def do_reset(self, tokens):
        "Request the CC2538 to reset itself"
        buf = MTBuffer("SYS", "AREQ", "SYS_RESET_REQ")
        #buf.send(self.sock)
        return True

    def help_reset(self, tokens):
        buf = MTBuffer("SYS", "AREQ", "SYS_RESET_REQ")
        print("Syntax: %s" % tokens[0], end="")
        info = []
        for field in buf.cmd.fields:
            info.extend(field.field_info())
        print(" ".join(i[0] for i in info))
        for i in info:
            i[2].helper(i[0])
