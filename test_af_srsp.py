#! /usr/bin/env python3

# test_af_srsp.py
#
# Unit tests for MT AF SRSP command (response) parsing
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


class BaseAfSRsp(base_test.BaseTest):
    SUBSYSTEM = "AF"
    TYPE = "SRSP"


class BaseStatus:
    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_fail(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()

    def test_status_memfail(self):
        self.add_byte("Status", "Memory Failure", 0x10)
        self.run_test()

    def test_status_invalid_param(self):
        self.add_byte("Status", "Invalid Parameter", 2)
        self.run_test()

    def test_status_z_not_allowed(self):
        self.add_byte("Status", "ZApsNotAllowed", 0xba)
        self.run_test()


class TestAfRegister(BaseStatus, BaseAfSRsp):
    COMMAND = 0x00
    COMMAND_NAME = "AF_REGISTER"

class TestAfDataRequest(BaseStatus, BaseAfSRsp):
    COMMAND = 0x01
    COMMAND_NAME = "AF_DATA_REQUEST"

class TestAfDataRequestExt(BaseStatus, BaseAfSRsp):
    COMMAND = 0x02
    COMMAND_NAME = "AF_DATA_REQUEST_EXT"

class TestAfDataRequestSrcRtg(BaseStatus, BaseAfSRsp):
    COMMAND = 0x03
    COMMAND_NAME = "AF_DATA_REQUEST_SRC_RTG"

class TestAfInterPanCtl(BaseStatus, BaseAfSRsp):
    COMMAND = 0x10
    COMMAND_NAME = "AF_INTER_PAN_CTL"

class TestAfDataStore(BaseStatus, BaseAfSRsp):
    COMMAND = 0x11
    COMMAND_NAME = "AF_DATA_STORE"

class TestAfApsfConfigSet(BaseStatus, BaseAfSRsp):
    COMMAND = 0x13
    COMMAND_NAME = "AF_APSF_CONFIG_SET"


class TestAfDataRetrieve(BaseAfSRsp):
    COMMAND = 0x12
    COMMAND_NAME = "AF_DATA_RETRIEVE"

    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Length", "2")
        self.add_bytes("Data", (0xfe, 0xdc))
        self.run_test()

    def test_status_failed(self):
        self.add_byte("Status", "Failed", 1)
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()


if __name__ == "__main__":
    unittest.main()

