#! /usr/bin/env python3

# Unit tests for MT MAC command response parsing

import base_test
import unittest


class BaseMacSRsp(base_test.BaseTest):
    SUBSYSTEM = "MAC"
    TYPE = "SRSP"


class BaseStatus:
    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_fail(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestMacResetReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x01
    COMMAND_NAME = "MAC_RESET_REQ"

class TestMacInit(BaseStatus, BaseMacSRsp):
    COMMAND = 0x02
    COMMAND_NAME = "MAC_INIT"

class TestMacStartReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x03
    COMMAND_NAME = "MAC_START_REQ"

class TestMacSyncReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x04
    COMMAND_NAME = "MAC_SYNC_REQ"

class TestMacDataReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x05
    COMMAND_NAME = "MAC_DATA_REQ"

class TestMacAssociateReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x06
    COMMAND_NAME = "MAC_ASSOCIATE_REQ"

class TestMacAssociateRsp(BaseStatus, BaseMacSRsp):
    COMMAND = 0x50
    COMMAND_NAME = "MAC_ASSOCIATE_RSP"

class TestMacDisassociateRsp(BaseStatus, BaseMacSRsp):
    COMMAND = 0x07
    COMMAND_NAME = "MAC_DISASSOCIATE_REQ"

class TestMacSetReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x09
    COMMAND_NAME = "MAC_SET_REQ"

class TestMacScanReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x0c
    COMMAND_NAME = "MAC_SCAN_REQ"

class TestMacOrphanRsp(BaseStatus, BaseMacSRsp):
    COMMAND = 0x51
    COMMAND_NAME = "MAC_ORPHAN_RSP"

class TestMacPollReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x0d
    COMMAND_NAME = "MAC_POLL_REQ"

class TestMacPurgeReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x0e
    COMMAND_NAME = "MAC_PURGE_REQ"

class TestMacSetRxGainReq(BaseStatus, BaseMacSRsp):
    COMMAND = 0x0f
    COMMAND_NAME = "MAC_SET_RX_GAIN_REQ"


class TestMacGetReq(BaseMacSRsp):
    COMMAND = 0x08
    COMMAND_NAME = "MAC_GET_REQ"

    def test_get_attribute_ok(self):
        self.add_byte("Status", "Success", 0)
        self.add_bytes("Data", (0x2d, 0x2e, 0x2f, 0x30,
                                0x31, 0x32, 0x33, 0x34,
                                0x35, 0x36, 0x37, 0x38,
                                0x39, 0x3a, 0x3b, 0x3c),
                       leading_0x=True)
        self.run_test()

    def test_get_attribute_bad(self):
        self.add_byte("Status", "Failed", 1)
        self.add_bytes("Data", (0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00),
                       leading_0x=True)
        self.run_test()


if __name__ == "__main__":
    unittest.main()
