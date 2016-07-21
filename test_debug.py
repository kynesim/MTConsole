#! /usr/bin/env python3

# Unit tests for MT DEBUG command and response parsing

import base_test
import unittest


class TestDebugSetThresholdSReq(base_test.BaseTest):
    SUBSYSTEM = "DEBUG"
    TYPE = "SREQ"
    COMMAND = 0x00
    COMMAND_NAME = "DEBUG_SET_THRESHOLD"

    def test_threshold(self):
        self.add_byte("ComponentId", "0x01")
        self.add_byte("Threshold", "0x7e")
        self.run_test()


class TestDebugSetThresholdSRsp(base_test.BaseTest):
    SUBSYSTEM = "DEBUG"
    TYPE = "SRSP"
    COMMAND = 0x00
    COMMAND_NAME = "DEBUG_SET_THRESHOLD"

    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_fail(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestDebugMsg(base_test.BaseTest):
    SUBSYSTEM = "DEBUG"
    TYPE = "AREQ"
    COMMAND = 0x00
    COMMAND_NAME = "DEBUG_MSG"

    def test_short_string(self):
        self.add_bstring("Length", "String", 'A short message')
        self.run_test()

    def test_empty_string(self):
        self.add_bstring("Length", "String", '')
        self.run_test()


if __name__ == "__main__":
    unittest.main()
