#! /usr/bin/env python3

# Unit tests for MT AF AREQ callback parsing

import base_test
import unittest


class BaseAfAReq(base_test.BaseTest):
    SUBSYSTEM = "AF"
    TYPE = "AREQ"


class TestAfDataConfirm(BaseAfAReq):
    COMMAND = 0x80
    COMMAND_NAME = "AF_DATA_CONFIRM"

    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Endpoint", "0x11")
        self.add_byte("TransId", "0x22")
        self.run_test()

    def test_status_failed(self):
        self.add_byte("Status", "Failed", 1)
        self.add_byte("Endpoint", "0x49")
        self.add_byte("TransId", "0xd3")
        self.run_test()


class TestAfReflectError(BaseAfAReq):
    COMMAND = 0x83
    COMMAND_NAME = "AF_REFLECT_ERROR"

    def test_error(self):
        self.add_byte("Status", "Failed", 1)
        self.add_byte("Endpoint", "0x0a")
        self.add_byte("TransId", "0x4b")
        self.add_byte("DstAddrMode", "16-bit address", 2)
        self.add_hword("DstAddr", "6789", 0x6789)
        self.run_test()


class TestAfIncomingMsg(BaseAfAReq):
    COMMAND = 0x81
    COMMAND_NAME = "AF_INCOMING_MSG"

    def test_msg(self):
        self.add_hword("GroupId", "2839", 0x2839)
        self.add_hword("ClusterId", "1faa", 0x1faa)
        self.add_hword("SrcAddr", "dcb7", 0xdcb7)
        self.add_byte("SrcEndpoint", "0x0b")
        self.add_byte("DstEndpoint", "0x01")
        self.add_byte("WasBroadcast", "0x00")
        self.add_byte("LinkQuality", "0x56")
        self.add_byte("SecurityUse", "0x01")
        self.add_word("Timestamp", "12345678", 0x12345678)
        self.add_byte("TransSeqNumber", "0xba")
        self.add_byte("Length", "5")
        self.add_bytes("Data", (0x10, 0x20, 0x30, 0x40, 0x50))
        self.run_test()

    def test_empty_msg(self):
        self.add_hword("GroupId", "2839", 0x2839)
        self.add_hword("ClusterId", "1faa", 0x1faa)
        self.add_hword("SrcAddr", "dcb7", 0xdcb7)
        self.add_byte("SrcEndpoint", "0x0b")
        self.add_byte("DstEndpoint", "0x01")
        self.add_byte("WasBroadcast", "0x00")
        self.add_byte("LinkQuality", "0x56")
        self.add_byte("SecurityUse", "0x01")
        self.add_word("Timestamp", "12345678", 0x12345678)
        self.add_byte("TransSeqNumber", "0xba")
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()


class TestAfIncomingMsgExt(BaseAfAReq):
    # This test is somewhat awkward, since the spec claims that the
    # 'Length' field is both 1 and 2 bytes long.  Fixing the over-
    # length data handling is therefore not a priority
    COMMAND = 0x82
    COMMAND_NAME = "AF_INCOMING_MSG_EXT"

    def test_long_addr_msg(self):
        self.add_hword("GroupId", "cc23", 0xcc23)
        self.add_hword("ClusterId", "0100", 0x0100)
        self.add_byte("SrcAddrMode", "64-bit", 3)
        self.add_ieee("SrcAddr", (0xfe, 0xdc, 0xba, 0x98,
                                  0x76, 0x54, 0x32, 0x10))
        self.add_byte("SrcEndpoint", "0x01")
        self.add_hword("SrcPanId", "2345", 0x2345)
        self.add_byte("DstEndpoint", "0x0a")
        self.add_byte("WasBroadcast", "0x01")
        self.add_byte("LinkQuality", "0x99")
        self.add_byte("SecurityUse", "0x00")
        self.add_word("Timestamp", "789abcde", 0x789abcde)
        self.add_byte("TransSeqNumber", "0x13")
        self.add_byte("Length", "1")
        self.add_bytes("Data", (0x58,))
        self.run_test()

    def test_short_addr_msg(self):
        self.add_hword("GroupId", "dd34", 0xdd34)
        self.add_hword("ClusterId", "0200", 0x0200)
        self.add_byte("SrcAddrMode", "16-bit", 2)
        self.add_hword("SrcAddr", "0fed", 0x0fed)
        self.add_padding(6)
        self.add_byte("SrcEndpoint", "0x02")
        self.add_hword("SrcPanId", "3456", 0x3456)
        self.add_byte("DstEndpoint", "0x0b")
        self.add_byte("WasBroadcast", "0x00")
        self.add_byte("LinkQuality", "0xaa")
        self.add_byte("SecurityUse", "0x01")
        self.add_word("Timestamp", "89abcdef", 0x89abcdef)
        self.add_byte("TransSeqNumber", "0x24")
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()


if __name__ == "__main__":
    unittest.main()
