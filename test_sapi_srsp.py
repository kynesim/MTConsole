#! /usr/bin/env python3

# Unit tests for MT SAPI command response parsing

import base_test
import unittest


class BaseSapiSRsp(base_test.BaseTest):
    SUBSYSTEM = "SAPI"
    TYPE = "SRSP"


class TestZbStartRequest(BaseSapiSRsp):
    COMMAND = 0x00
    COMMAND_NAME = "ZB_START_REQUEST"

    def test_start(self):
        self.run_test()


class TestZbPermitJoiningRequest(BaseSapiSRsp):
    COMMAND = 0x08
    COMMAND_NAME = "ZB_PERMIT_JOINING_REQUEST"

    def test_permit_join(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZbBindDevice(BaseSapiSRsp):
    COMMAND = 0x01
    COMMAND_NAME = "ZB_BIND_DEVICE"

    def test_bind(self):
        self.run_test()


class TestZbAllowBind(BaseSapiSRsp):
    COMMAND = 0x02
    COMMAND_NAME = "ZB_ALLOW_BIND"

    def test_allow_bind(self):
        self.run_test()


class TestZbSendDataRequest(BaseSapiSRsp):
    COMMAND = 0x03
    COMMAND_NAME = "ZB_SEND_DATA_REQUEST"

    def test_send_data(self):
        self.run_test()


class TestZbReadConfiguration(BaseSapiSRsp):
    COMMAND = 0x04
    COMMAND_NAME = "ZB_READ_CONFIGURATION"

    def test_read_config(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("ConfigId", "0x02")
        self.add_byte("Length", "4")
        self.add_bytes("Data", (0x05, 0x06, 0x07, 0x99))
        self.run_test()


class TestZbWriteConfiguration(BaseSapiSRsp):
    COMMAND = 0x05
    COMMAND_NAME = "ZB_WRITE_CONFIGURATION"

    def test_write_config(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestZbGetDeviceInfo(BaseSapiSRsp):
    COMMAND = 0x06
    COMMAND_NAME = "ZB_GET_DEVICE_INFO"

    def test_get_info(self):
        self.add_byte("Param", "0x42")
        self.add_bytes("Value", (0x01, 0x02, 0x03, 0x04,
                                 0x05, 0x06, 0x07, 0x08),
                       leading_0x=True)
        self.run_test()


class TestZbFindDeviceRequest(BaseSapiSRsp):
    COMMAND = 0x07
    COMMAND_NAME = "ZB_FIND_DEVICE_REQUEST"

    def test_find_device(self):
        self.run_test()


if __name__ == "__main__":
    unittest.main()
