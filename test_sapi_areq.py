#! /usr/bin/env python3

# Unit tests for MT SAPI announcements

import base_test
import unittest


class BaseSapiAReq(base_test.BaseTest):
    SUBSYSTEM = "SAPI"
    TYPE = "AREQ"


class TestZbSystemReset(BaseSapiAReq):
    COMMAND = 0x09
    COMMAND_NAME = "ZB_SYSTEM_RESET"

    def test_reset(self):
        self.run_test()


class TestZbStartConfirm(BaseSapiAReq):
    COMMAND = 0x80
    COMMAND_NAME = "ZB_START_CONFIRM"

    def test_start(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZbBindConfirm(BaseSapiAReq):
    COMMAND = 0x81
    COMMAND_NAME = "ZB_BIND_CONFIRM"

    def test_bind(self):
        self.add_hword("CommandId", "0754", 0x0754)
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestZbAllowBindConfirm(BaseSapiAReq):
    COMMAND = 0x82
    COMMAND_NAME = "ZB_ALLOW_BIND_CONFIRM"

    def test_allow_bind(self):
        self.add_hword("SrcAddr", "7d2a", 0x7d2a)
        self.run_test()


class TestZbSendDataConfirm(BaseSapiAReq):
    COMMAND = 0x83
    COMMAND_NAME = "ZB_SEND_DATA_CONFIRM"

    def test_send_data(self):
        self.add_byte("Handle", "0x01")
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZbReceiveDataIndication(BaseSapiAReq):
    COMMAND = 0x87
    COMMAND_NAME = "ZB_RECEIVE_DATA_INDICATION"

    def test_rx_data(self):
        self.add_hword("SrcAddr", "0631", 0x0631)
        self.add_hword("CommandId", "1359", 0x1359)
        self.add_hword("Len", "3")
        self.add_bytes("Data", (0x41, 0x42, 0x43))
        self.run_test()


class TestZbFindDeviceConfirm(BaseSapiAReq):
    COMMAND = 0x85
    COMMAND_NAME = "ZB_FIND_DEVICE_CONFIRM"

    def test_find(self):
        self.add_byte("SearchType", "0x01")
        self.add_hword("SearchKey", "2345", 0x2345)
        self.add_bytes("Result", (0x67, 0x89, 0xab, 0xcd,
                                  0xef, 0x10, 0x20, 0x40),
                       leading_0x=True)
        self.run_test()


if __name__ == "__main__":
    unittest.main()
