#! /usr/bin/env python3

# Unit tests for MT SAPI command parsing

import base_test
import unittest


class BaseSapiSReq(base_test.BaseTest):
    SUBSYSTEM = "SAPI"
    TYPE = "SREQ"


class TestZbStartRequest(BaseSapiSReq):
    COMMAND = 0x00
    COMMAND_NAME = "ZB_START_REQUEST"

    def test_start(self):
        self.run_test()


class TestZbPermitJoiningRequest(BaseSapiSReq):
    COMMAND = 0x08
    COMMAND_NAME = "ZB_PERMIT_JOINING_REQUEST"

    def test_permit_join(self):
        self.add_hword("DstAddr", "1122", 0x1122)
        self.add_byte("Timeout", "0x3c", 60)
        self.run_test()


class TestZbBindDevice(BaseSapiSReq):
    COMMAND = 0x01
    COMMAND_NAME = "ZB_BIND_DEVICE"

    def test_bind(self):
        self.add_byte("Create", "0x01")
        self.add_hword("CommandId", "248d", 0x248d)
        self.add_ieee("DstExtAddr", (0x33, 0x44, 0x55, 0x66,
                                     0x77, 0x88, 0x99, 0xaa))
        self.run_test()


class TestZbAllowBind(BaseSapiSReq):
    COMMAND = 0x02
    COMMAND_NAME = "ZB_ALLOW_BIND"

    def test_allow_bind(self):
        self.add_byte("Timeout", "0x40")
        self.run_test()


class TestZbSendDataRequest(BaseSapiSReq):
    COMMAND = 0x03
    COMMAND_NAME = "ZB_SEND_DATA_REQUEST"

    def test_send_data(self):
        self.add_hword("DstAddr", "892b", 0x892b)
        self.add_hword("CommandId", "258d", 0x258d)
        self.add_byte("Handle", "0xea")
        self.add_byte("Ack", "0x01")
        self.add_byte("Radius", "0x30")
        self.add_byte("Length", "7")
        self.add_bytes("Data", (0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x70))
        self.run_test()


class TestZbReadConfiguration(BaseSapiSReq):
    COMMAND = 0x04
    COMMAND_NAME = "ZB_READ_CONFIGURATION"

    def test_read_config(self):
        self.add_byte("ConfigId", "0x01")
        self.run_test()


class TestZbWriteConfiguration(BaseSapiSReq):
    COMMAND = 0x05
    COMMAND_NAME = "ZB_WRITE_CONFIGURATION"

    def test_write_config(self):
        self.add_byte("ConfigId", "0x38")
        self.add_byte("Length", "3")
        self.add_bytes("Data", (0x76, 0x2f, 0x01))
        self.run_test()


class TestZbGetDeviceInfo(BaseSapiSReq):
    COMMAND = 0x06
    COMMAND_NAME = "ZB_GET_DEVICE_INFO"

    def test_get_info(self):
        self.add_byte("Param", "0x66")
        self.run_test()


class TestZbFindDeviceRequest(BaseSapiSReq):
    COMMAND = 0x07
    COMMAND_NAME = "ZB_FIND_DEVICE_REQUEST"

    def test_find_device(self):
        self.add_bytes("SearchKey", (0x44, 0x55, 0x66, 0x77,
                                     0x88, 0x99, 0xaa, 0xbb),
                       leading_0x=True)
        self.run_test()


if __name__ == "__main__":
    unittest.main()
