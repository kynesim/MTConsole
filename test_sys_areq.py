#! /usr/bin/env python3

# test_sys_areq.py
#
# Unit tests for MT SYS announcements
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


class BaseSysAReq(base_test.BaseTest):
    SUBSYSTEM = "SYS"
    TYPE = "AREQ"


class TestSysResetReq(BaseSysAReq):
    COMMAND = 0x00
    COMMAND_NAME = "SYS_RESET_REQ"

    def test_hard_reset(self):
        self.add_byte("Type", "Hardware", 0)
        self.run_test()

    def test_soft_reset(self):
        self.add_byte("Type", "Software", 1)
        self.run_test()


class TestSysResetInd(BaseSysAReq):
    COMMAND = 0x80
    COMMAND_NAME = "SYS_RESET_IND"

    def test_reset_ind(self):
        self.add_byte("Reason", "Power-up", 0)
        self.add_byte("TransportRev", "0x80")
        self.add_byte("ProductId", "0x81")
        self.add_byte("MajorRel", "0x82")
        self.add_byte("MinorRel", "0x83")
        self.add_byte("HwRev", "0x85")
        self.run_test()


class TestOsalTimerExpired(BaseSysAReq):
    COMMAND = 0x81
    COMMAND_NAME = "SYS_OSAL_TIMER_EXPIRED"

    def test_timer_expired(self):
        self.add_byte("Id", "0x0b")
        self.run_test()


if __name__ == "__main__":
    unittest.main()
