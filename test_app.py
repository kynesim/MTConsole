#! /usr/bin/env python3

# test_app.py
#
# Unit tests for MT APP command and response parsing.
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


class TestAppMsgSReq(base_test.BaseTest):
    SUBSYSTEM = "APP"
    TYPE = "SREQ"
    COMMAND = 0x00
    COMMAND_NAME = "APP_MSG"

    def test_short_message(self):
        self.add_byte("AppEndpoint", "0x01")
        self.add_hword("DstAddr", "0204", 0x0204)
        self.add_byte("DstEndpoint", "0x08")
        self.add_hword("ClusterId", "1020", 0x1020)
        self.add_byte("MsgLen", "3")
        self.add_bytes("Message", (0x40, 0x80, 0x00))
        self.run_test()

    def test_no_message(self):
        self.add_byte("AppEndpoint", "0xfe")
        self.add_hword("DstAddr", "fdfb", 0xfdfb)
        self.add_byte("DstEndpoint", "0xf7")
        self.add_hword("ClusterId", "efdf", 0xefdf)
        self.add_byte("MsgLen", "0")
        self.add_bytes("Message", ())
        self.run_test()


class StatusResponse:
    SUBSYSTEM = "APP"
    TYPE = "SRSP"

    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_fail(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestAppMsgSRsp(StatusResponse, base_test.BaseTest):
    COMMAND = 0x00
    COMMAND_NAME = "APP_MSG"


class TestAppUserTestSReq(base_test.BaseTest):
    SUBSYSTEM = "APP"
    TYPE = "SREQ"
    COMMAND = 0x01
    COMMAND_NAME = "APP_USER_TEST"

    def test_command(self):
        self.add_byte("SrcEndpoint", "0xbf")
        self.add_hword("CommandId", "7fff", 0x7fff)
        self.add_hword("Parameter1", "0001", 0x0001)
        self.add_hword("Parameter2", "0204", 0x0204)
        self.run_test()


class TestAppUserTestSRsp(StatusResponse, base_test.BaseTest):
    COMMAND = 0x01
    COMMAND_NAME = "APP_USER_TEST"


if __name__ == "__main__":
    unittest.main()
