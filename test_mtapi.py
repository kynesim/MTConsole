#! /usr/bin/env python3

# Unit tests for MTAPI Parser classes

import unittest
from test import support
import mtapi
import sys

class TestParseField(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseField("Test", 2)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test is missing"):
            offset = field.parse(b'\x01\x02', 2)

    def test_short_field(self):
        field = mtapi.ParseField("Test", 3)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test is missing"):
            offset = field.parse(b'\x01\x02', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test is missing"):
            offset = field.parse(b'\x01\x02', 1)

    def test_byte_field(self):
        field = mtapi.ParseField("Test", 1)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x10\x11\x12', 2)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(), "  Test : 0x12\n")

    def test_wide_field(self):
        field = mtapi.ParseField("Test", 2)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x20\x21\x22\x23', 0)
        self.assertEqual(offset, 2)
        self.assertEqual(stdout.getvalue(), "  Test : 0x20 0x21\n")

    def test_indented_field(self):
        field = mtapi.ParseField("Test", 1)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x30', 0, indent=2)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(), "      Test : 0x30\n")


class TestParseClusterList(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseClusterList("TestCount", "TestList")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field TestCount is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field TestCount is missing"):
            offset = field.parse(b'\x01\x02\x03', 3)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field TestList is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x10', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field TestList is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x20\x21', 0)

    def test_ok_field(self):
        field = mtapi.ParseClusterList("TestCount", "TestList")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "  TestCount : 0\n"
                         "  TestList : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x01\x02\x03\x04', 1)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "  TestCount : 1\n"
                         "  TestList : 0302\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x33\x44\x55\x66', 1)
        self.assertEqual(offset, 6)
        self.assertEqual(stdout.getvalue(),
                         "  TestCount : 2\n"
                         "  TestList : 4433, 6655\n")

    def test_indented_field(self):
        field = mtapi.ParseClusterList("TestCount", "TestList")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x01\x05', 0, indent=1)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "    TestCount : 1\n"
                         "    TestList : 0501\n")


class TestParseVariable(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseVariable("Len", "Data")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing"):
            offset = field.parse(b'\x00\x01', 2)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\10', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x21\x22', 0)

    def test_missing_wide_field(self):
        field = mtapi.ParseVariable("Len", "Data", len_bytes=2)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing"):
            offset = field.parse(b'\x30', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x40\x41', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x02\x00\x50', 0)

    def test_ok_field(self):
        field = mtapi.ParseVariable("Len", "Data")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x51\x00\x00', 1)
        self.assertEqual(offset, 2)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 0\n"
                         "  Data : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x60', 0)
        self.assertEqual(offset, 2)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 1\n"
                         "  Data : 60\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x02\x71\x72\x73', 1)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 2\n"
                         "  Data : 71 72\n")

    def test_ok_wide_field(self):
        field = mtapi.ParseVariable("Len", "Data", len_bytes=2)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x51\x00\x00', 1)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 0\n"
                         "  Data : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x00\x60', 0)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 1\n"
                         "  Data : 60\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x02\x00\x71\x72\x73', 1)
        self.assertEqual(offset, 5)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 2\n"
                         "  Data : 71 72\n")

    def test_limited_field(self):
        field = mtapi.ParseVariable("Count", "Data", limit=5)
        with self.assertRaises(
                mtapi.ParseError,
                msg="Variable field Len exceeds limit (6 > 5)"):
            offset = field.parse(b'\x06\x11\x22\x33\x44\x55\x66', 0)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x05\x11\x22\x33\x44\x55\x66', 0)
        self.assertEqual(offset, 6)
        self.assertEqual(stdout.getvalue(),
                         "  Count : 5\n"
                         "  Data : 11 22 33 44 55\n")

    def test_limited_wide_field(self):
        field = mtapi.ParseVariable("Count", "Data", len_bytes=2, limit=4)
        with self.assertRaises(
                mtapi.ParseError,
                msg="Variable field Len exceeds limit (5 > 4)"):
            offset = field.parse(b'\x05\x00\x11\x22\x33\x44\x55', 0)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x04\x00\x11\x22\x33\x44\x55', 0)
        self.assertEqual(offset, 6)
        self.assertEqual(stdout.getvalue(),
                         "  Count : 4\n"
                         "  Data : 11 22 33 44\n")

    def test_indented_field(self):
        field = mtapi.ParseVariable("Count", "Data")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x02\x03\x04', 1, indent=2)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "      Count : 2\n"
                         "      Data : 03 04\n")


class TestParseExtData(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseExtData("Len", "Data", 10)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing or short"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing or short"):
            offset = field.parse(b'\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Len is missing or short"):
            offset = field.parse(b'\x00', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x00\x01\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Data is missing or short"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x02\x00\x01', 0)

    def test_ok_field(self):
        field = mtapi.ParseExtData("Len", "Data", 10)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x00', 0)
        self.assertEqual(offset, 2)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 0\n"
                         "  Data : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x10\x02\x00\x11\x12', 1)
        self.assertEqual(offset, 5)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 2\n"
                         "  Data : 11 12\n")

    def test_limited_field(self):
        field = mtapi.ParseExtData("Len", "Data", 10)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x00\x0b\x00', 2)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 11\n"
                         "  Data : Blank\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x0a\x00'
                                 b'\x20\x21\x22\x23\x24\x25\x26\x27'
                                 b'\x28\x29', 0)
        self.assertEqual(offset, 12)
        self.assertEqual(stdout.getvalue(),
                         "  Len : 10\n"
                         "  Data : 20 21 22 23 24 25 26 27 28 29\n")

    def test_indented_field(self):
        field = mtapi.ParseExtData("Len", "Data", 10)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x02\x00\x03\x04', 0, indent=2)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "      Len : 2\n"
                         "      Data : 03 04\n")


class TestParseRemaining(unittest.TestCase):
    def test_empty_field(self):
        field = mtapi.ParseRemaining("Data")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'', 0)
        self.assertEqual(offset, 0)
        self.assertEqual(stdout.getvalue(), "  Data : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x03', 3)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(), "  Data : \n")

    def test_ok_field(self):
        field = mtapi.ParseRemaining("Data")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x10\x11\x12\x13', 1)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(), "  Data : 11 12 13\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x20\x21\x22\x23\x24\x25', 0)
        self.assertEqual(offset, 6)
        self.assertEqual(stdout.getvalue(),
                         "  Data : 20 21 22 23 24 25\n")

    def test_indented_field(self):
        field = mtapi.ParseRemaining("Data")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x30\x31\x32', 1, indent=1)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(), "    Data : 31 32\n")


class TestParseAddress(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseAddress("Mode", "Addr")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Mode is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Mode is missing"):
            offset = field.parse(b'\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x00', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x02\x12\x34', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x03\x11\x22\x33\x44\x55\x66\x77', 0)

    def test_no_address(self):
        field = mtapi.ParseAddress("Mode", "Addr")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88', 0)
        self.assertEqual(offset, 9)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : Address not present\n")

    def _test_2_byte_address(self, mode_byte, mode_string):
        field = mtapi.ParseAddress("Mode", "Addr")
        with support.captured_stdout() as stdout:
            offset = field.parse(mode_byte +
                                 b'\x11\x22\x33\x44\x55\x66\x77\x88',
                                 0)
        self.assertEqual(offset, 9)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : " + mode_string + "\n" +
                         "  Addr : 2211\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xaa' + mode_byte +
                                 b'\xfe\xdc\xba\x98\x76\x54\x32\x10' +
                                 b'\x00\x00\x00',
                                 1)
        self.assertEqual(offset, 10)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : " + mode_string + "\n" +
                         "  Addr : dcfe\n")

    def test_group_address(self):
        self._test_2_byte_address(b'\x01', "Group address")

    def test_network_address(self):
        self._test_2_byte_address(b'\x02', "16-bit")

    def test_broadcast_address(self):
        self._test_2_byte_address(b'\xff', "Broadcast")

    def test_ieee_address(self):
        field = mtapi.ParseAddress("Mode", "Addr")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xff\xee\x03'
                                 b'\x01\x23\x45\x67\x89\xab\xcd\xef', 2)
        self.assertEqual(offset, 11)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : 64-bit\n"
                         "  Addr : ef:cd:ab:89:67:45:23:01\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x03'
                                 b'\x88\x77\x66\x55\x44\x33\x22\x11', 0)
        self.assertEqual(offset, 9)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : 64-bit\n"
                         "  Addr : 11:22:33:44:55:66:77:88\n")

    def test_unknown_mode(self):
        field = mtapi.ParseAddress("Mode", "Addr")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22'
                                 b'\x33\x44\x55\x66\x77\x88\x99\xaa', 2)
        self.assertEqual(offset, 11)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : Unknown(22)\n"
                         "  Addr : 0x33 0x44 0x55 0x66 "
                         "0x77 0x88 0x99 0xaa\n")

    def test_indented_address(self):
        field = mtapi.ParseAddress("Mode", "Addr")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88',
                                 0, indent=2)
        self.assertEqual(offset, 9)
        self.assertEqual(stdout.getvalue(),
                         "      Mode : Address not present\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x02\x11\x22\x33\x44\x55\x66\x77\x88',
                                 0, indent=1)
        self.assertEqual(offset, 9)
        self.assertEqual(stdout.getvalue(),
                         "    Mode : 16-bit\n"
                         "    Addr : 2211\n")


class TestBindAddress(unittest.TestCase):
    def test_bad_mode_field(self):
        field = mtapi.ParseBindAddress("Mode", "Addr", "EP")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Mode is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Mode is missing"):
            offset = field.parse(b'\x11', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Invalid field Mode (17)"):
            offset = field.parse(b'\x17', 0)

    def test_no_address(self):
        field = mtapi.ParseBindAddress("Mode", "Addr", "EP")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xff\xff\x00\x11\x22', 2)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : Address not present\n")


    def _test_2_byte_address(self, mode_byte, mode_string):
        field = mtapi.ParseBindAddress("Mode", "Addr", "EP")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x00' + mode_byte, 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(mode_byte + b'\x00', 0)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\xfe' + mode_byte + b'\x02\x01', 2)
        self.assertEqual(offset, 5)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : " + mode_string + "\n" +
                         "  Addr : 0102\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(mode_byte + b'\x99\x88\x77\x66', 0)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : " + mode_string + "\n" +
                         "  Addr : 8899\n")

    def test_group_address(self):
        self._test_2_byte_address(b'\x01', "Group address")

    def test_network_address(self):
        self._test_2_byte_address(b'\x02', "16-bit")

    def test_broadcast_address(self):
        self._test_2_byte_address(b'\xff', "Broadcast")

    def test_ieee_address(self):
        field = mtapi.ParseBindAddress("Mode", "Addr", "EP")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x03', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Addr is missing or short"):
            offset = field.parse(b'\x00\x03\x11\x22\x33\x44\x55\x66\x77',
                                 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field EP is missing"):
            offset = field.parse(b'\x03'
                                 b'\x20\x21\x22\x23\x24\x25\x26\x27', 0)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x03'
                                 b'\x30\x31\x32\x33\x34\x35\x36\x37\x48', 0)
        self.assertEqual(offset, 10)
        self.assertEqual(stdout.getvalue(),
                         "  Mode : 64-bit\n"
                         "  Addr : 37:36:35:34:33:32:31:30\n"
                         "  EP : 48\n")

    def test_indented_address(self):
        field = mtapi.ParseBindAddress("Mode", "Addr", "EP")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x03', 0, indent=1)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "    Mode : Group address\n"
                         "    Addr : 0302\n")


class TestInterPan(unittest.TestCase):
    def test_bad_command_field(self):
        field = mtapi.ParseInterPan()
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Command is missing"):
            offset = field.parse(b'\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Unknown InterPan command 0x23"):
            offset = field.parse(b'\x23', 1)

    def test_clear_command(self):
        field = mtapi.ParseInterPan()
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(), "  Command : InterPanClr\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xfd\xfe\xff\x00\x01\x02', 3)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(), "  Command : InterPanClr\n")

    def test_set_command(self):
        field = mtapi.ParseInterPan()
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Channel is missing"):
            offset = field.parse(b'\x00\x01', 1)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x03', 0)
        self.assertEqual(offset, 2)
        self.assertEqual(stdout.getvalue(),
                         "  Command : InterPanSet\n"
                         "  Channel : 2\n")

    def test_register_command(self):
        field = mtapi.ParseInterPan()
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Endpoint is missing"):
            offset = field.parse(b'\x02', 0)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x03', 1)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  Command : InterPanReg\n"
                         "  Endpoint : 0x03\n")

    def test_check_command(self):
        field = mtapi.ParseInterPan()
        with self.assertRaises(mtapi.ParseError,
                               msg="Field PanId is missing or short"):
            offset = field.parse(b'\x03', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field PanId is missing or short"):
            offset = field.parse(b'\x55\x03\xfe', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="FieldEndpoint is missing"):
            offset = field.parse(b'\x01\x02\x03\x04\x05', 2)
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x03\x55\xaa\x0a', 0)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "  Command : InterPanChk\n"
                         "  PanId : aa55\n"
                         "  Endpoint : 0x0a\n")

    def test_indented(self):
        field = mtapi.ParseInterPan()
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00', 0, indent=2)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "      Command : InterPanClr\n")


class TestBitField(unittest.TestCase):
    def test_bad_description(self):
        with self.assertRaises(mtapi.ParseError,
                               msg="Empty mask illegal in bitfield 'Test'"):
            bitfield = mtapi.BitField(("Test", 0x00))

    def test_parsing(self):
        bitfield = mtapi.BitField(("Test", 0x0c))
        with support.captured_stdout() as stdout:
            bitfield.parse(0)
        self.assertEqual(stdout.getvalue(), "  Test : 00\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x01, indent=1)
        self.assertEqual(stdout.getvalue(), "    Test : 00\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x02)
        self.assertEqual(stdout.getvalue(), "  Test : 00\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x04)
        self.assertEqual(stdout.getvalue(), "  Test : 01\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x08)
        self.assertEqual(stdout.getvalue(), "  Test : 02\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x0c)
        self.assertEqual(stdout.getvalue(), "  Test : 03\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0x10)
        self.assertEqual(stdout.getvalue(), "  Test : 00\n")
        with support.captured_stdout() as stdout:
            bitfield.parse(0xff)
        self.assertEqual(stdout.getvalue(), "  Test : 03\n")

class TestBitFields(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseBitFields((("A", 0xff),))
        with self.assertRaises(mtapi.ParseError,
                               msg="Field A is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field A is missing"):
            offset = field.parse(b'\x01\x02', 2)

    def test_ok_field(self):
        # It is not technically wrong to define a bitfield with no
        # subfields, though it is pretty pointless.  Test that here.
        field = mtapi.ParseBitFields((()))
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xff', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(), "   : \n")

        # Now try more complex fields
        field = mtapi.ParseBitFields((("A", 0x03),
                                      ("B", 0x1c),
                                      ("C", 0x60),
                                      ("D", 0x80)))
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x06\x07', 2)
        self.assertEqual(offset, 3)
        self.assertEqual(stdout.getvalue(),
                         "  A/B/C/D : \n"
                         "    A : 02\n"
                         "    B : 01\n"
                         "    C : 00\n"
                         "    D : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xc0', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "  A/B/C/D : \n"
                         "    A : 00\n"
                         "    B : 00\n"
                         "    C : 02\n"
                         "    D : 01\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\xff', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "  A/B/C/D : \n"
                         "    A : 03\n"
                         "    B : 07\n"
                         "    C : 03\n"
                         "    D : 01\n")

    def test_indented(self):
        field = mtapi.ParseBitFields((("A", 0x0f), ("B", 0xf0)))
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x5a', 0, indent=1)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "    A/B : \n"
                         "      A : 0a\n"
                         "      B : 05\n")


class TestRepeated(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseRepeated("Count", "Data",
                                    (mtapi.ParseField("Test1", 1),
                                     mtapi.ParseField("Test2", 2)))
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Count is missing"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Count is missing"):
            offset = field.parse(b'\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test1 is missing"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x01', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test2 is missing"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x00\x01\x02', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test2 is missing"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x01\x02\x03', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Test1 is missing"):
            with support.captured_stdout() as stdout:
                offset = field.parse(b'\x01\x02\x03\x04\x05', 1)

    def test_ok_fields(self):
        field = mtapi.ParseRepeated("Count", "Data",
                                    (mtapi.ParseField("Test1", 1),
                                     mtapi.ParseField("Test2", 2)))
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00', 0)
        self.assertEqual(offset, 1)
        self.assertEqual(stdout.getvalue(),
                         "  Count : 0\n"
                         "  Data : \n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x01\x02\x03\x04\x05', 1)
        self.assertEqual(offset, 5)
        self.assertEqual(stdout.getvalue(),
                         "  Count : 1\n"
                         "  Data : \n"
                         "    Test1 : 0x02\n"
                         "    Test2 : 0x03 0x04\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x02\x11\x22\x33\x44\x55\x66', 0)
        self.assertEqual(offset, 7)
        self.assertEqual(stdout.getvalue(),
                         "  Count : 2\n"
                         "  Data : \n"
                         "    Test1 : 0x11\n"
                         "    Test2 : 0x22 0x33\n"
                         "    Test1 : 0x44\n"
                         "    Test2 : 0x55 0x66\n")

    def test_indented(self):
        field = mtapi.ParseRepeated("Count", "Data",
                                    (mtapi.ParseField("Test1", 1),
                                     mtapi.ParseField("Test2", 2)))
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\xfe\xdc\xba', 0, indent=2)
        self.assertEqual(offset, 4)
        self.assertEqual(stdout.getvalue(),
                         "      Count : 1\n"
                         "      Data : \n"
                         "        Test1 : 0xfe\n"
                         "        Test2 : 0xdc 0xba\n")


class TestSecurityKey(unittest.TestCase):
    def test_missing_field(self):
        field = mtapi.ParseKey("Source", "Level", "Id", "Index")
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Source is missing or short"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Source is missing or short"):
            offset = field.parse(b'\x00\x10\x20\x30\x40\x50\x60\x70', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Level is missing"):
            offset = field.parse(b'\x00\x01\x02\x03\x04\x05\x06\x07', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Id is missing"):
            offset = field.parse(b'\x10\x20\x30\x40\x50\x60\x70\x80\x90', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Index is missing"):
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x88\x99', 0)

    def test_ok_fields(self):
        field = mtapi.ParseKey("Source", "Level", "Id", "Index")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x23\x45\x67\x89\xab\xcd\xef'
                                 b'\x00\x00\x00', 0)
        self.assertEqual(offset, 11)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 01 23 45 67 89 ab cd ef\n"
                         "  Level : No Security\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x23\x45\x67\x89\xab\xcd\xef\x00'
                                 b'\x01\x01\x01\x02\x03', 1)
        self.assertEqual(offset, 12)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 23 45 67 89 ab cd ef 00\n"
                         "  Level : MIC_32_AUTH\n"
                         "  Id : KEY_1BYTE_INDEX\n"
                         "  Index : 01\n")

    def test_security_field(self):
        field = mtapi.ParseKey("Source", "Level", "Id", "Index")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x01\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : MIC_32_AUTH\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x02\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : MIC_64_AUTH\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x03\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : MIC_128_AUTH\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x04\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : AES_ENCRYPTION\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x05\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : AES_ENCRYPTION_MIC_32\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x06\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : AES_ENCRYPTION_MIC_64\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x07\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : AES_ENCRYPTION_MIC_128\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x08\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : Invalid(08)\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")

    def test_id_mode_field(self):
        field = mtapi.ParseKey("Source", "Level", "Id", "Index")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x00\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : Not Used\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x01\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : KEY_1BYTE_INDEX\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x02\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : KEY_4BYTE_INDEX\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x03\x00', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : KEY_8BYTE_INDEX\n"
                         "  Index : 00\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x04\xff', 0)
        self.assertEqual(stdout.getvalue(),
                         "  Source : 00 11 22 33 44 55 66 77\n"
                         "  Level : No Security\n"
                         "  Id : Invalid(04)\n"
                         "  Index : ff\n")

    def test_indented(self):
        field = mtapi.ParseKey("Source", "Level", "Id", "Index")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x00\x11\x22\x33\x44\x55\x66\x77'
                                 b'\x00\x00\x00', 0, indent=1)
        self.assertEqual(stdout.getvalue(),
                         "    Source : 00 11 22 33 44 55 66 77\n"
                         "    Level : No Security\n"
                         "    Id : Not Used\n"
                         "    Index : 00\n")


class TestTime(unittest.TestCase):
    def test_missing_fields(self):
        field = mtapi.ParseTime()
        with self.assertRaises(mtapi.ParseError,
                               msg="Field UTCTime is missing or short"):
            offset = field.parse(b'', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field UTCTime is missing or short"):
            offset = field.parse(b'\x00', 1)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field UTCTime is missing or short"):
            offset = field.parse(b'\x05\x00\x00', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Hour is missing"):
            offset = field.parse(b'\x05\x00\x00\x00', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Minute is missing"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Second is missing"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Day is missing"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Month is missing"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b'
                                 b'\x11', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Year is missing or short"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b'
                                 b'\x11\x03', 0)
        with self.assertRaises(mtapi.ParseError,
                               msg="Field Year is missing or short"):
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b'
                                 b'\x11\x03\x07', 0)

    def test_ok_fields(self):
        field = mtapi.ParseTime()
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b'
                                 b'\x03\x11\xd1\x07', 0)
        self.assertEqual(offset, 11)
        self.assertEqual(stdout.getvalue(),
                         "  UTCTime : 5\n"
                         "  Hour : 10\n"
                         "  Minute : 15\n"
                         "  Second : 27\n"
                         "  Month : 3\n"
                         "  Day : 17\n"
                         "  Year : 2001\n")
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x01\x02\x56\x41\x45\x00\x07\x32\x18'
                                 b'\x04\x04\xd2\x07\x03\x04', 2)
        self.assertEqual(offset, 13)
        self.assertEqual(stdout.getvalue(),
                         "  UTCTime : 4538710\n"
                         "  Hour : 7\n"
                         "  Minute : 50\n"
                         "  Second : 24\n"
                         "  Month : 4\n"
                         "  Day : 4\n"
                         "  Year : 2002\n")

    def test_indented(self):
        field = mtapi.ParseTime()
        with support.captured_stdout() as stdout:
            offset = field.parse(b'\x05\x00\x00\x00\x0a\x0f\x1b'
                                 b'\x03\x11\xd1\x07', 0, indent=2)
        self.assertEqual(offset, 11)
        self.assertEqual(stdout.getvalue(),
                         "      UTCTime : 5\n"
                         "      Hour : 10\n"
                         "      Minute : 15\n"
                         "      Second : 27\n"
                         "      Month : 3\n"
                         "      Day : 17\n"
                         "      Year : 2001\n")

class TestParseHword(unittest.TestCase):
    def test_hword(self):
        field = mtapi.ParseField("Test", 2,
                                 parser=mtapi.field_parse_hword)
        buf = b'\x01\x02'
        result_hex = mtapi.field_parse_hword(buf)
        result_decimal = mtapi.field_parse_hword(buf, as_decimal=True)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, 2)
        self.assertEqual(result_hex, "0201")
        self.assertEqual(result_decimal, "513")
        self.assertEqual(stdout.getvalue(), "  Test : 0201\n")


class TestParseWord(unittest.TestCase):
    def test_word(self):
        field = mtapi.ParseField("Test", 4,
                                 parser=mtapi.field_parse_word)
        buf = b'\x78\x56\x34\x12'
        result_hex = mtapi.field_parse_word(buf)
        result_decimal = mtapi.field_parse_word(buf, as_decimal=True)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, 4)
        self.assertEqual(result_hex, "12345678")
        self.assertEqual(result_decimal, "305419896")
        self.assertEqual(stdout.getvalue(), "  Test : 12345678\n")


class TestParseColonSep(unittest.TestCase):
    def test_colon_sep(self):
        field = mtapi.ParseField("Test", 8,
                                 parser=mtapi.field_parse_colon_sep)
        buf = b'\x11\x22\x33\x44\x55\x66\x77\x88'
        result = mtapi.field_parse_colon_sep(buf)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, 8)
        self.assertEqual(result, "88:77:66:55:44:33:22:11")
        self.assertEqual(stdout.getvalue(),
                         "  Test : 88:77:66:55:44:33:22:11\n")


class TestParseScanChannels(unittest.TestCase):
    def _test_scan_channels(self, buf, expected_result):
        field = mtapi.ParseField("Test", 4,
                                 parser=mtapi.field_parse_scan_channels)
        result = mtapi.field_parse_scan_channels(buf)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, 4)
        self.assertEqual(result, expected_result)
        self.assertEqual(stdout.getvalue(),
                         "  Test : " + expected_result + "\n")

    def test_scan_channels(self):
        self._test_scan_channels(b'\x00\x00\x00\x00', "None")
        self._test_scan_channels(b'\x00\xf8\xff\x07', "All")
        self._test_scan_channels(b'\x00\x10\x00\x00', "12")
        self._test_scan_channels(b'\x00\xd0\x00\x00', "12,14,15")


class TestParseDict(unittest.TestCase):
    def _test_dictionary(self, buf, parser, expected_result):
        field = mtapi.ParseField("Test", len(buf), parser=parser)
        result = parser(buf)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, len(buf))
        self.assertEqual(result, expected_result)
        self.assertEqual(stdout.getvalue(),
                         "  Test : " + expected_result + "\n")

    def test_dictionary(self):
        dictionary = { 0x0001 : "One", 0x0100 : "Two" }
        default = "Bad(%04x)"
        parser = lambda d : mtapi.field_parse_dict(d, dictionary, default)
        self._test_dictionary(b'\x01\x00', parser, "One")
        self._test_dictionary(b'\x00\x01', parser, "Two")
        self._test_dictionary(b'\x10\x00', parser, "Bad(0010)")


class TestParseBitfield(unittest.TestCase):
    def _test_bitfield(self, buf, parser, expected_result):
        field = mtapi.ParseField("Test", len(buf), parser=parser)
        result = parser(buf)
        with support.captured_stdout() as stdout:
            offset = field.parse(buf, 0)
        self.assertEqual(offset, len(buf))
        self.assertEqual(result, expected_result)
        self.assertEqual(stdout.getvalue(),
                         "  Test : " + expected_result + "\n")

    def test_bitfield(self):
        bitfield = ("Zero", "One", "Two", "Three",
                    "Four", "Five", "Six", "Seven",
                    "Eight", "Nine", "Ten", "Eleven",
                    "Twelve", "Thirteen", "Fourteen", "Fifteen")
        offfield = ("~0", "~1", "~2", "~3",
                    None, None, None, None,
                    None, None, None, None,
                    None, None, None, None)
        parser_on = lambda d : mtapi.field_parse_bitfield(d, bitfield)
        parser_off = lambda d : mtapi.field_parse_bitfield(d, bitfield,
                                                           offfield)
        self._test_bitfield(b'\x01\x00', parser_on,
                            "0001 (Zero)")
        self._test_bitfield(b'\x01\x00', parser_off,
                            "0001 (Zero, ~1, ~2, ~3)")
        self._test_bitfield(b'\x00\x00', parser_on,
                            "0000 ()")
        self._test_bitfield(b'\x00\x00', parser_off,
                            "0000 (~0, ~1, ~2, ~3)")
        self._test_bitfield(b'\x00\x02', parser_on,
                            "0200 (Nine)")
        self._test_bitfield(b'\x00\x02', parser_off,
                            "0200 (~0, ~1, ~2, ~3, Nine)")
        self._test_bitfield(b'\x04\x02', parser_on,
                            "0204 (Two, Nine)")
        self._test_bitfield(b'\x04\x02', parser_off,
                            "0204 (~0, ~1, Two, ~3, Nine)")


class TestParseStatus(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_status, "Success")
        self._test_dictionary(b'\x01', mtapi.field_parse_status, "Failed")
        self._test_dictionary(b'\xff', mtapi.field_parse_status,
                              "Failure(0xff)")


class TestParseLatency(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_latency,
                              "No latency")
        self._test_dictionary(b'\x01', mtapi.field_parse_latency,
                              "Fast beacons")
        self._test_dictionary(b'\x02', mtapi.field_parse_latency,
                              "Slow beacons")
        self._test_dictionary(b'\x03', mtapi.field_parse_latency,
                              "Invalid(0x03)")


class TestParseOptions(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_options, "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_options,
                            "01 ((Reserved))")
        self._test_bitfield(b'\x02', mtapi.field_parse_options,
                            "02 (Wildcard Profile Id)")
        self._test_bitfield(b'\x10', mtapi.field_parse_options,
                            "10 (APS ACK)")
        self._test_bitfield(b'\x20', mtapi.field_parse_options,
                            "20 (Discover Route)")
        self._test_bitfield(b'\x40', mtapi.field_parse_options,
                            "40 (APS Security)")
        self._test_bitfield(b'\x80', mtapi.field_parse_options,
                            "80 (Skip Routing)")


class TestParseAddressMode(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_address_mode,
                              "Address not present")
        self._test_dictionary(b'\x01', mtapi.field_parse_address_mode,
                              "Group address")
        self._test_dictionary(b'\x02', mtapi.field_parse_address_mode,
                              "16-bit address")
        self._test_dictionary(b'\x03', mtapi.field_parse_address_mode,
                              "64-bit address")
        self._test_dictionary(b'\x04', mtapi.field_parse_address_mode,
                              "Invalid(0x04)")
        self._test_dictionary(b'\xff', mtapi.field_parse_address_mode,
                              "Broadcast")


class TestParseTxOption(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_tx_option, "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_tx_option,
                            "01 (Ack)")
        self._test_bitfield(b'\x02', mtapi.field_parse_tx_option,
                            "02 (GTS)")
        self._test_bitfield(b'\x04', mtapi.field_parse_tx_option,
                            "04 (Indirect)")
        self._test_bitfield(b'\x10', mtapi.field_parse_tx_option,
                            "10 (No Retransmission)")
        self._test_bitfield(b'\x20', mtapi.field_parse_tx_option,
                            "20 (No Confirms)")
        self._test_bitfield(b'\x40', mtapi.field_parse_tx_option,
                            "40 (Alternate Backoff Exponent)")
        self._test_bitfield(b'\x80', mtapi.field_parse_tx_option,
                            "80 (Power/Channel)")


class TestParseCap(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_capabilities,
                            "00 (End Device, Battery Powered)")
        self._test_bitfield(b'\x01', mtapi.field_parse_capabilities,
                            "01 (Alternative PAN Coord, End Device, "
                            "Battery Powered)")
        self._test_bitfield(b'\x02', mtapi.field_parse_capabilities,
                            "02 (Zigbee Router, Battery Powered)")
        self._test_bitfield(b'\x04', mtapi.field_parse_capabilities,
                            "04 (End Device, Mains Powered)")
        self._test_bitfield(b'\x08', mtapi.field_parse_capabilities,
                            "08 (End Device, Battery Powered, "
                            "Rx On When Idle)")
        self._test_bitfield(b'\x40', mtapi.field_parse_capabilities,
                            "40 (End Device, Battery Powered, "
                            "Security)")
        self._test_bitfield(b'\x80', mtapi.field_parse_capabilities,
                            "80 (End Device, Battery Powered, "
                            "Allocate Address)")


class TestParseAssocStatus(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_assoc_status,
                              "Success")
        self._test_dictionary(b'\x01', mtapi.field_parse_assoc_status,
                              "PAN at capacity")
        self._test_dictionary(b'\x02', mtapi.field_parse_assoc_status,
                              "PAN access denied")
        self._test_dictionary(b'\x03', mtapi.field_parse_assoc_status,
                              "Unknown(0x03)")


class TestParseDisassoc(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_disassoc_reason,
                              "Reserved")
        self._test_dictionary(b'\x01', mtapi.field_parse_disassoc_reason,
                              "Coord wishes device to leave")
        self._test_dictionary(b'\x02', mtapi.field_parse_disassoc_reason,
                              "Device wishes to leave")
        self._test_dictionary(b'\x03', mtapi.field_parse_disassoc_reason,
                              "Unknown(0x03)")


class TestParseMacAttr(TestParseDict):
    def test_dictionary(self):
        for byte, reason in ((b'\x00', "Unknown(0x00)"),
                             (b'\x40', "ZMAC_ACK_WAIT_DURATION"),
                             (b'\x41', "ZMAC_ASSOCIATION_PERMIT"),
                             (b'\x42', "ZMAC_AUTO_REQUEST"),
                             (b'\x43', "ZMAC_BATT_LIFE_EXT"),
                             (b'\x44', "ZMAC_BATT_LEFT_EXT_PERIODS"),
                             (b'\x45', "ZMAC_BEACON_MSDU"),
                             (b'\x46', "ZMAC_BEACON_MSDU_LENGTH"),
                             (b'\x47', "ZMAC_BEACON_ORDER"),
                             (b'\x48', "ZMAC_BEACON_TX_TIME"),
                             (b'\x49', "ZMAC_BSN"),
                             (b'\x4a', "ZMAC_COORD_EXTENDED_ADDRESS"),
                             (b'\x4b', "ZMAC_COORD_SHORT_ADDRESS"),
                             (b'\x4c', "ZMAC_DSN"),
                             (b'\x4d', "ZMAC_GTS_PERMIT"),
                             (b'\x4e', "ZMAC_MAX_CSMA_BACKOFFS"),
                             (b'\x4f', "ZMAC_MIN_BE"),
                             (b'\x50', "ZMAC_PANID"),
                             (b'\x51', "ZMAC_PROMISCUOUS_MODE"),
                             (b'\x52', "ZMAC_RX_ON_IDLE"),
                             (b'\x53', "ZMAC_SHORT_ADDRESS"),
                             (b'\x54', "ZMAC_SUPERFRAME_ORDER"),
                             (b'\x55', "ZMAC_TRANSACTION_PERSISTENCE_TIME"),
                             (b'\x56', "ZMAC_ASSOCIATED_PAN_COORD"),
                             (b'\x57', "ZMAC_MAX_BE"),
                             (b'\x58', "ZMAC_FRAME_TOTAL_WAIT_TIME"),
                             (b'\x59', "ZMAC_MAC_FRAME_RETRIES"),
                             (b'\x5a', "ZMAC_RESPONSE_WAIT_TIME"),
                             (b'\x5b', "ZMAC_SYNC_SYMBOL_OFFSET"),
                             (b'\x5c', "ZMAC_TIMESTAMP_SUPPORTED"),
                             (b'\x5d', "ZMAC_SECURITY_ENABLED"),
                             (b'\xe0', "ZMAC_PHY_TRANSMIT_POWER"),
                             (b'\xe1', "ZMAC_LOGICAL_CHANNEL"),
                             (b'\xe2', "ZMAC_EXTENDED_ADDRESS"),
                             (b'\xe3', "ZMAC_ALT_BE"),
                             (b'\xff', "Unknown(0xff)")):
            self._test_dictionary(byte, mtapi.field_parse_mac_attr, reason)


class TestParseScanType(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_scan_type,
                              "Energy Detect")
        self._test_dictionary(b'\x01', mtapi.field_parse_scan_type,
                              "Active")
        self._test_dictionary(b'\x02', mtapi.field_parse_scan_type,
                              "Passive")
        self._test_dictionary(b'\x03', mtapi.field_parse_scan_type,
                              "Orphan")
        self._test_dictionary(b'\x04', mtapi.field_parse_scan_type,
                              "Unknown(0x04)")


class TestParseResetType(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_reset_type,
                              "Hardware")
        self._test_dictionary(b'\x01', mtapi.field_parse_reset_type,
                              "Software")
        self._test_dictionary(b'\x02', mtapi.field_parse_reset_type,
                              "Unknown(0x02)")


class TestParseResetReason(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_reset_reason,
                              "Power-up")
        self._test_dictionary(b'\x01', mtapi.field_parse_reset_reason,
                              "External")
        self._test_dictionary(b'\x02', mtapi.field_parse_reset_reason,
                              "Watchdog")
        self._test_dictionary(b'\x03', mtapi.field_parse_reset_reason,
                              "Unknown(0x03)")


class TestParseSysCap(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00\x00', mtapi.field_parse_sys_capabilities,
                            "0000 ()")
        self._test_bitfield(b'\x01\x00', mtapi.field_parse_sys_capabilities,
                            "0001 (MT_CAP_SYS)")
        self._test_bitfield(b'\x02\x00', mtapi.field_parse_sys_capabilities,
                            "0002 (MT_CAP_MAC)")
        self._test_bitfield(b'\x04\x00', mtapi.field_parse_sys_capabilities,
                            "0004 (MT_CAP_NWK)")
        self._test_bitfield(b'\x08\x00', mtapi.field_parse_sys_capabilities,
                            "0008 (MT_CAP_AF)")
        self._test_bitfield(b'\x10\x00', mtapi.field_parse_sys_capabilities,
                            "0010 (MT_CAP_ZDO)")
        self._test_bitfield(b'\x20\x00', mtapi.field_parse_sys_capabilities,
                            "0020 (MT_CAP_SAPI)")
        self._test_bitfield(b'\x40\x00', mtapi.field_parse_sys_capabilities,
                            "0040 (MT_CAP_UTIL)")
        self._test_bitfield(b'\x80\x00', mtapi.field_parse_sys_capabilities,
                            "0080 (MT_CAP_DEBUG)")
        self._test_bitfield(b'\x00\x01', mtapi.field_parse_sys_capabilities,
                            "0100 (MT_CAP_APP)")
        self._test_bitfield(b'\x00\x10', mtapi.field_parse_sys_capabilities,
                            "1000 (MT_CAP_ZOAD)")
        self._test_bitfield(b'\x00\x80', mtapi.field_parse_sys_capabilities,
                            "8000 ((Reserved))")


class TestParseAdcChannel(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_adc_channel,
                              "AIN0")
        self._test_dictionary(b'\x01', mtapi.field_parse_adc_channel,
                              "AIN1")
        self._test_dictionary(b'\x02', mtapi.field_parse_adc_channel,
                              "AIN2")
        self._test_dictionary(b'\x03', mtapi.field_parse_adc_channel,
                              "AIN3")
        self._test_dictionary(b'\x04', mtapi.field_parse_adc_channel,
                              "AIN4")
        self._test_dictionary(b'\x05', mtapi.field_parse_adc_channel,
                              "AIN5")
        self._test_dictionary(b'\x06', mtapi.field_parse_adc_channel,
                              "AIN6")
        self._test_dictionary(b'\x07', mtapi.field_parse_adc_channel,
                              "AIN7")
        self._test_dictionary(b'\x08', mtapi.field_parse_adc_channel,
                              "Invalid(0x08)")
        self._test_dictionary(b'\x0e', mtapi.field_parse_adc_channel,
                              "Temperature Sensor")
        self._test_dictionary(b'\x0f', mtapi.field_parse_adc_channel,
                              "Voltage Reading")
        self._test_dictionary(b'\x10', mtapi.field_parse_adc_channel,
                              "Invalid(0x10)")


class TestParseAdcResolution(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_adc_resolution,
                              "8-bit")
        self._test_dictionary(b'\x01', mtapi.field_parse_adc_resolution,
                              "10-bit")
        self._test_dictionary(b'\x02', mtapi.field_parse_adc_resolution,
                              "12-bit")
        self._test_dictionary(b'\x03', mtapi.field_parse_adc_resolution,
                              "14-bit")
        self._test_dictionary(b'\x04', mtapi.field_parse_adc_resolution,
                              "Invalid(0x04)")


class TestParseGpioOperation(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_gpio_operation,
                              "Set direction")
        self._test_dictionary(b'\x01', mtapi.field_parse_gpio_operation,
                              "Set input mode")
        self._test_dictionary(b'\x02', mtapi.field_parse_gpio_operation,
                              "Set")
        self._test_dictionary(b'\x03', mtapi.field_parse_gpio_operation,
                              "Clear")
        self._test_dictionary(b'\x04', mtapi.field_parse_gpio_operation,
                              "Toggle")
        self._test_dictionary(b'\x05', mtapi.field_parse_gpio_operation,
                              "Read")
        self._test_dictionary(b'\x06', mtapi.field_parse_gpio_operation,
                              "Invalid(0x06)")


class TestParseDeviceType(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_device_type,
                            "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_device_type,
                            "01 (Coordinator)")
        self._test_bitfield(b'\x02', mtapi.field_parse_device_type,
                            "02 (Router)")
        self._test_bitfield(b'\x03', mtapi.field_parse_device_type,
                            "03 (Coordinator, Router)")
        self._test_bitfield(b'\x04', mtapi.field_parse_device_type,
                            "04 (End Device)")
        self._test_bitfield(b'\x05', mtapi.field_parse_device_type,
                            "05 (Coordinator, End Device)")
        self._test_bitfield(b'\x06', mtapi.field_parse_device_type,
                            "06 (Router, End Device)")
        self._test_bitfield(b'\x07', mtapi.field_parse_device_type,
                            "07 (Coordinator, Router, End Device)")
        self._test_bitfield(b'\x08', mtapi.field_parse_device_type,
                            "08 ((Reserved))")


class TestParseDeviceTypeAndInfo(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_type_and_info,
                            "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_type_and_info,
                            "01 (Coordinator)")
        self._test_bitfield(b'\x02', mtapi.field_parse_type_and_info,
                            "02 (Router)")
        self._test_bitfield(b'\x04', mtapi.field_parse_type_and_info,
                            "04 (End Device)")
        self._test_bitfield(b'\x08', mtapi.field_parse_type_and_info,
                            "08 (Complex Descriptor Available)")
        self._test_bitfield(b'\x10', mtapi.field_parse_type_and_info,
                            "10 (User Descriptor Available)")
        self._test_bitfield(b'\x20', mtapi.field_parse_type_and_info,
                            "20 ((Reserved))")


class TestParseDeviceState(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_device_state,
                              "Unstarted")
        self._test_dictionary(b'\x01', mtapi.field_parse_device_state,
                              "Not connected")
        self._test_dictionary(b'\x02', mtapi.field_parse_device_state,
                              "Nothing to join")
        self._test_dictionary(b'\x03', mtapi.field_parse_device_state,
                              "Joining")
        self._test_dictionary(b'\x04', mtapi.field_parse_device_state,
                              "Rejoining")
        self._test_dictionary(b'\x05', mtapi.field_parse_device_state,
                              "Unauthenticated")
        self._test_dictionary(b'\x06', mtapi.field_parse_device_state,
                              "Authenticated")
        self._test_dictionary(b'\x07', mtapi.field_parse_device_state,
                              "Routing")
        self._test_dictionary(b'\x08', mtapi.field_parse_device_state,
                              "Starting as Coordinator")
        self._test_dictionary(b'\x09', mtapi.field_parse_device_state,
                              "Started as Coordinator")
        self._test_dictionary(b'\x0a', mtapi.field_parse_device_state,
                              "Lost Parent Info")
        self._test_dictionary(b'\x0b', mtapi.field_parse_device_state,
                              "Unknown(0x0b)")


class TestParseSubsystemId(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00\x00', mtapi.field_parse_subsystem_id,
                              "Reserved(0x0000)")
        self._test_dictionary(b'\x00\x01', mtapi.field_parse_subsystem_id,
                              "MT_SYS")
        self._test_dictionary(b'\x00\x02', mtapi.field_parse_subsystem_id,
                              "MT_MAC")
        self._test_dictionary(b'\x00\x03', mtapi.field_parse_subsystem_id,
                              "MT_NWK")
        self._test_dictionary(b'\x00\x04', mtapi.field_parse_subsystem_id,
                              "MT_AF")
        self._test_dictionary(b'\x00\x05', mtapi.field_parse_subsystem_id,
                              "MT_ZDO")
        self._test_dictionary(b'\x00\x06', mtapi.field_parse_subsystem_id,
                              "MT_SAPI")
        self._test_dictionary(b'\x00\x07', mtapi.field_parse_subsystem_id,
                              "MT_UTIL")
        self._test_dictionary(b'\x00\x08', mtapi.field_parse_subsystem_id,
                              "MT_DEBUG")
        self._test_dictionary(b'\x00\x09', mtapi.field_parse_subsystem_id,
                              "MT_APP")
        self._test_dictionary(b'\xff\xff', mtapi.field_parse_subsystem_id,
                              "ALL_SUBSYSTEMS")
        self._test_dictionary(b'\x00\x0a', mtapi.field_parse_subsystem_id,
                              "Reserved(0x0a00)")


class TestParseEnable(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_enable,
                              "Disable")
        self._test_dictionary(b'\x01', mtapi.field_parse_enable,
                              "Enable")
        self._test_dictionary(b'\x02', mtapi.field_parse_enable,
                              "Unexpected(0x02)")


class TestParseKeys(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_keys,
                            "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_keys,
                            "01 (Key 1)")
        self._test_bitfield(b'\x02', mtapi.field_parse_keys,
                            "02 (Key 2)")
        self._test_bitfield(b'\x04', mtapi.field_parse_keys,
                            "04 (Key 3)")
        self._test_bitfield(b'\x08', mtapi.field_parse_keys,
                            "08 (Key 4)")
        self._test_bitfield(b'\x10', mtapi.field_parse_keys,
                            "10 (Key 5)")
        self._test_bitfield(b'\x20', mtapi.field_parse_keys,
                            "20 (Key 6)")
        self._test_bitfield(b'\x40', mtapi.field_parse_keys,
                            "40 (Key 7)")
        self._test_bitfield(b'\x80', mtapi.field_parse_keys,
                            "80 (Key 8)")
        self._test_bitfield(b'\x31', mtapi.field_parse_keys,
                            "31 (Key 1, Key 5, Key 6)")


class TestParseShift(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_shift,
                              "No shift")
        self._test_dictionary(b'\x01', mtapi.field_parse_shift,
                              "Shift")
        self._test_dictionary(b'\x02', mtapi.field_parse_shift,
                              "Unexpected(0x02)")


class TestParseOnOff(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_onoff,
                              "OFF")
        self._test_dictionary(b'\x01', mtapi.field_parse_onoff,
                              "ON")
        self._test_dictionary(b'\x02', mtapi.field_parse_onoff,
                              "Unexpected(0x02)")


class TestParseRelation(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_relation,
                              "Parent")
        self._test_dictionary(b'\x01', mtapi.field_parse_relation,
                              "Child RFD")
        self._test_dictionary(b'\x02', mtapi.field_parse_relation,
                              "Child RFD RxIdle")
        self._test_dictionary(b'\x03', mtapi.field_parse_relation,
                              "Child FFD")
        self._test_dictionary(b'\x04', mtapi.field_parse_relation,
                              "Child FFD RxIdle")
        self._test_dictionary(b'\x05', mtapi.field_parse_relation,
                              "Neighbour")
        self._test_dictionary(b'\x06', mtapi.field_parse_relation,
                              "Other")
        self._test_dictionary(b'\x07', mtapi.field_parse_relation,
                              "Invalid(0x07)")


class TestParseLeaveAction(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_leave_action,
                            "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_leave_action,
                            "01 (Rejoin)")
        self._test_bitfield(b'\x02', mtapi.field_parse_leave_action,
                            "02 (Remove Children)")
        self._test_bitfield(b'\x03', mtapi.field_parse_leave_action,
                            "03 (Rejoin, Remove Children)")
        self._test_bitfield(b'\x04', mtapi.field_parse_leave_action,
                            "04 ((Reserved))")


class TestParseStartupStatus(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_startup_status,
                              "Restored network state")
        self._test_dictionary(b'\x01', mtapi.field_parse_startup_status,
                              "New network state")
        self._test_dictionary(b'\x02', mtapi.field_parse_startup_status,
                              "Leave and not Started")
        self._test_dictionary(b'\x03', mtapi.field_parse_startup_status,
                              "Unexpected(0x03)")


class TestParseServerMask(TestParseBitfield):
    def test_bitfield(self):
        self._test_bitfield(b'\x00', mtapi.field_parse_server_mask,
                            "00 ()")
        self._test_bitfield(b'\x01', mtapi.field_parse_server_mask,
                            "01 (Primary Trust Centre)")
        self._test_bitfield(b'\x02', mtapi.field_parse_server_mask,
                            "02 (Backup Trust Centre)")
        self._test_bitfield(b'\x04', mtapi.field_parse_server_mask,
                            "04 (Primary Binding Table Cache)")
        self._test_bitfield(b'\x08', mtapi.field_parse_server_mask,
                            "08 (Backup Binding Table Cache)")
        self._test_bitfield(b'\x10', mtapi.field_parse_server_mask,
                            "10 (Primary Discovery Cache)")
        self._test_bitfield(b'\x20', mtapi.field_parse_server_mask,
                            "20 (Backup Discovery Cache)")
        self._test_bitfield(b'\x40', mtapi.field_parse_server_mask,
                            "40 ((Reserved))")


class TestParseRoutingStatus(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_routing_status,
                              "Active")
        self._test_dictionary(b'\x01', mtapi.field_parse_routing_status,
                              "Discovery Underway")
        self._test_dictionary(b'\x02', mtapi.field_parse_routing_status,
                              "Discovery Failed")
        self._test_dictionary(b'\x03', mtapi.field_parse_routing_status,
                              "Inactive")
        self._test_dictionary(b'\x04', mtapi.field_parse_routing_status,
                              "Invalid(0x04)")


class TestParseJoinDuration(TestParseDict):
    def test_dictionary(self):
        self._test_dictionary(b'\x00', mtapi.field_parse_join_duration,
                              "Disabled")
        self._test_dictionary(b'\x01', mtapi.field_parse_join_duration,
                              "0x01")
        self._test_dictionary(b'\xfe', mtapi.field_parse_join_duration,
                              "0xfe")
        self._test_dictionary(b'\xff', mtapi.field_parse_join_duration,
                              "Enabled")


if __name__ == "__main__":
    unittest.main()
