#! /usr/bin/env python3

# test_debug.py
#
# Unit tests for MT DEBUG command and response parsing
#
# Author: Rhodri James (rhodr@kynesim.co.uk)
# Date: 15 July 2016
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
