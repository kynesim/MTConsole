#! /usr/bin/env python3

# base_test.py
#
# Unit test classes for MTConsole unit tests
#
# Author: Rhodri James (rhodri@kynesim.co.uk)
# Date: 18 July 2016
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


import mtcmds
from mtapi import MTAPIType, MTAPISubsystem, ParseError
import unittest
import random
from test import support
import sys
import textwrap
import contextlib


class MockSock:
    "Mocked-up socket class to stress-test mtcmds.MTAPI"
    def __init__(self, input_bytes=None, chop_max=None):
        """Creates the mock socket.  If `input_bytes` is not None,
        uses that as the input stream to read; otherwise it creates
        an empty bytearray() that can be added to later.  `input_bytes`
        should be a mutable byte type such as bytearray, otherwise the
        various add_ methods will raise an exception.

        If `chop_max` is not None, the input will be chopped into
        smaller segments to simulate partial reads.  Each read will
        be a random length, up to `chop_max` bytes long (unless the
        request is for fewer bytes, obviously)."""
        if input_bytes is None:
            input_bytes = bytearray()
        self.bytes = input_bytes
        self.bytes_read = 0
        self.chop_max = chop_max

    def reset(self):
        "Resets the input stream to read from the start"
        self.bytes_read = 0

    def load_bytes(self, input_bytes):
        """Accepts `input_bytes` as the bytestream to use, and resets
        the read pointers.  Note that it does not take a copy of the
        input bytes, so bytearray parameters must not be fiddled with
        after loading.  Conversely, immutable byte types will cause the
        various add_ methods to raise an exception."""
        self.bytes = input_bytes
        self.bytes_read = 0

    def load_header(self, subsystem_name, type_name, command):
        """Creates a new four byte MTAPI header bytearray, assembles the
        subsystem, type and command passed as parameters into it, and
        resets the read pointers.  The `subsystem_name` and `type_name`
        parameters must be strings as defined in the MTAPISubsystem
        and MATPIType classes respectively."""
        self.bytes = bytearray(4)
        self.bytes[0] = 0xfe # SOF
        self.bytes[2] = (MTAPIType.to_number(type_name) |
                         MTAPISubsystem.to_number(subsystem_name))
        self.bytes[3] = command
        self.bytes_read = 0

    def add_byte(self, byte):
        """Append a byte to the existing bytestream, keeping the header
        length field in step.  The byte is assumed to belong to the body
        of the MTAPI packet; if not, the length field will be incorrectly
        updated."""
        self.bytes.append(byte)
        self.bytes[1] += 1

    def add_hword(self, hword):
        """Append a two-byte value to the existing bytestream in little
        endian order, keeping the header length field in step.  The bytes
        are assumed to belong to the body of the MTAPI packet; if not,
        the length field will be incorrectly updated."""
        self.bytes += bytearray((hword & 0xff, (hword >> 8) & 0xff))
        self.bytes[1] += 2

    def add_word(self, word):
        """Append a four-byte value to the existing bytestream in
        little endian order, keeping the header length field in step.
        The bytes are assumed to belong to the body of the MTAPI
        packet; if not, the length field will be incorrectly
        updated."""
        self.bytes += bytearray((word & 0xff,
                                 (word >> 8) & 0xff,
                                 (word >> 16) & 0xff,
                                 (word >> 24) & 0xff))
        self.bytes[1] += 4

    def add_bytes(self, bytestream):
        """Append a list of bytes to the existing bytestream, in the
        order presented.  The bytes are assumed to belong to the body
        of the MTAPI packet; if not, the header length field will be
        incorrectly updated.  `bytestream` will be passed through the
        `bytearray()` constructor, so any value that bytearray can
        handle can be used."""
        bytestream = bytearray(bytestream)
        self.bytes += bytestream
        self.bytes[1] += len(bytestream)

    def eof(self):
        "Returns True if all the bytes in the input buffer have been read."
        return self.bytes_read == len(self.bytes)

    def read(self, nbytes):
        """Reads up to `nbytes` from the buffer, possibly not all of
        them if the mock socket is simulating partial reads.  At least
        one byte will always be returned as long as there is any data
        left in the buffer."""
        if self.chop_max is not None:
            limit = min(self.chop_max,
                        len(self.bytes) - self.bytes_read)
            if limit > 1:
                limit = random.randint(1, limit)
            bytes_to_read = min(limit, nbytes)
        else:
            bytes_to_read = nbytes
        result = bytes(self.bytes[self.bytes_read :
                                  self.bytes_read + bytes_to_read])
        self.bytes_read += bytes_to_read
        return result

    def dump(self, outfile=sys.stderr):
        "Print debug output of current state of the mocket"
        print("Input buffer:", file=outfile)
        print("  Chop Max =", self.chop_max, file=outfile)
        print("  Bytes Read =", self.bytes_read, file=outfile)
        print("  Buffer Len =", len(self.bytes), file=outfile)
        data = " ".join("%02x" % b for b in self.bytes)
        print(textwrap.fill(data, width=58,
                            initial_indent="\t",
                            subsequent_indent="\t"), file=outfile)


def field_output(field_name, field_value, indent=1):
    "Format a line in the manner normally output by the parsers"
    return "%s%s : %s" % ("  " * indent, field_name, field_value)


class BaseTest(unittest.TestCase):
    """Abstract class for basing tests off

    Concrete subclasses must have the following class variables:
    * SUBSYSTEM: the MTAPI subsystem as a string, e.g. "AF"
    * TYPE: the MTAPI type as a string, e.g. "SREQ"
    * COMMAND: the subsystem command tested by this class, as
    *   an integer.
    * COMMAND_NAME: the subsystem command name tested by this class,
    *   e.g. "AF_REGISTER" (for which COMMAND = 0x00)

    The general form of tests in the subclass is then to construct
    an input buffer and expected output results using the "add_"
    functions below, then call "self.run_test()" to run the test.
    """
    def setUp(self):
        self.sock = MockSock()
        self.sock.load_header(self.SUBSYSTEM, self.TYPE, self.COMMAND)
        self.expected_output = [
            "%s %s Cmd = %02x" % (self.TYPE,
                                  self.SUBSYSTEM,
                                  self.COMMAND),
            "  " + self.COMMAND_NAME ]
        self.expected_parse_errors = []

    def add_byte(self, name, value, int_value=None):
        """Add a single byte value to the input buffer and the
        corresponding field to the expected parse output.  The
        input `value` is given as the expected output string; if
        this can be converted to an input byte by `int(value, 0)`
        then the separate `int_value` parameter is unnecessary.
        """
        self.expected_output.append(field_output(name, value))
        if int_value is None:
            int_value = int(value, 0)
        self.sock.add_byte(int_value)

    def add_hword(self, name, value, int_value=None):
        """Add a two-byte value to the input buffer, little-endian,
        and the corresponding field to the expected parse output.
        The input `value` is given as the expected output string;
        if this can be converted to an input byte by `int(value, 0)`
        then the separate `int_value` parameter is unnecessary.
        """
        self.expected_output.append(field_output(name, value))
        if int_value is None:
            int_value = int(value, 0)
        self.sock.add_hword(int_value)

    def add_word(self, name, value, int_value=None):
        """Add a four-byte value to the input buffer, little-endian,
        and the corresponding field to the expected parse output.  The
        input `value` is given as the expected output string; if this
        can be converted to an input byte by `int(value, 0)` then the
        separate `int_value` parameter is unnecessary.
        """
        self.expected_output.append(field_output(name, value))
        if int_value is None:
            int_value = int(value, 0)
        self.sock.add_word(int_value)

    def add_list(self, name, value, value_list):
        """Add a list of two-byte values to the input buffer,
        little-endian, and the corresponding field to the expected
        parse output.  `value` is a string containing the list as it
        will appear in the output; `value_list` is a sequence of
        two-byte integers to feed into the input buffer.
        """
        self.expected_output.append(field_output(name, value))
        for v in value_list:
            self.sock.add_hword(v)

    def add_bytes(self, name, bytestream, leading_0x=False):
        """Add a list of one-byte values to the input buffer, and the
        corresponding field to the expected parse output.  `bytestream`
        is a sequence of single byte values; they are presumed to appear
        in the output with no leading '0x' and in the order
        presented."""
        fmt = "0x%02x" if leading_0x else "%02x"
        value = " ".join(fmt % b for b in bytestream)
        self.expected_output.append(field_output(name, value))
        self.sock.add_bytes(bytestream)

    def add_ieee(self, name, bytestream):
        """Add a sequence of bytes to the input buffer, and a field
        consisting of the bytes in reverse order separated by colons
        to the expected parse output.  As the name suggests, this is
        intended primarily for 64-bit IEEE addresses."""
        value = ":".join("%02x" % b for b in reversed(bytestream))
        self.expected_output.append(field_output(name, value))
        self.sock.add_bytes(bytestream)

    def add_padding(self, padding_length, padding=0x00):
        """Add a number of padding bytes to the input buffer that have
        no corresponding parse output.  By default, the `padding` byte
        added is 0x00."""
        bytestream = (padding,) * padding_length
        self.sock.add_bytes(bytestream)

    def add_text(self, name, text):
        """Add a text field to the expected parse output that has no
        corresponding input bytes.  Commonly used for empty data fields.
        """
        self.expected_output.append(field_output(name, text))

    def add_bstring(self, len_name, string_name, string_chars):
        string_bytes = string_chars.encode()
        length = len(string_bytes)
        self.add_byte(len_name, str(length), length)
        self.add_bytes(string_name, string_bytes)

    def add_parse_error(self, text):
        """Add the text of a ParseError that the test should raise."""
        self.expected_parse_errors.append(text)

    def run_test(self, leftovers=False, dump=False, verbose=False):
        """Parse the input buffer prepared through the 'add_' functions
        and compare the results to the expected output.  `leftovers`
        should be `True` if the input buffer is expected to have excess
        data in it.  If `dump` is `True`, the state of the mock socket
        will be dumped after parsing."""
        if verbose:
            print("Initial state of socket")
            self.sock.dump()
        self.expected_output.append("")
        with contextlib.ExitStack() as stack:
            for parse_error in self.expected_parse_errors:
                stack.enter_context(self.assertRaises(ParseError,
                                                      msg=parse_error))
            with support.captured_stdout() as stdout:
                mtapi = mtcmds.MTAPI(self.sock)
                mtapi()
                while mtapi.state != mtapi.read_sof:
                    mtapi()
        if dump:
            print("Final state of socket")
            self.sock.dump()
        if leftovers:
            self.assertFalse(self.sock.eof())
        else:
            self.assertTrue(self.sock.eof())
        if verbose:
            print("Parse output:")
            print(stdout.getvalue())
        actual_output = stdout.getvalue().split("\n")
        for (expected, actual) in zip(self.expected_output, actual_output):
            self.assertEqual(expected, actual)
