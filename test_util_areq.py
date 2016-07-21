#! /usr/bin/env python3

# Unit tests for MT UTIL callbacks

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
