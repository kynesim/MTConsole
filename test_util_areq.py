#! /usr/bin/env python3

# test_util_areq.py
#
# Unit tests for MT UTIL callbacks
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


class BaseUtilAReq(base_test.BaseTest):
    SUBSYSTEM = "UTIL"
    TYPE = "AREQ"


class TestUtilSyncReq(BaseUtilAReq):
    COMMAND = 0xe0
    COMMAND_NAME = "UTIL_SYNC_REQ"

    def test_sync_req(self):
        self.run_test()


class TestUtilZclKeyEstablishInd(BaseUtilAReq):
    COMMAND = 0xe1
    COMMAND_NAME = "UTIL_ZCL_KEY_ESTABLISH_IND"

    def test_key_establish(self):
        self.add_byte("TaskId", "0x01")
        self.add_byte("Event", "0x02")
        self.add_byte("Status", "Success", 0)
        self.add_byte("WaitTime", "0x04")
        self.add_hword("Suite", "0506", 0x0506)
        self.run_test()


if __name__ == "__main__":
    unittest.main()
