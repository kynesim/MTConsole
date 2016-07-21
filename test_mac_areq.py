#! /usr/bin/env python3

# Unit tests for MT MAC announcements

import base_test
import unittest


class BaseMacAReq(base_test.BaseTest):
    SUBSYSTEM = "MAC"
    TYPE = "AREQ"


class TestMacSyncLossInd(BaseMacAReq):
    COMMAND = 0x80
    COMMAND_NAME = "MAC_SYNC_LOSS_IND"

    def test_sync_loss_ind(self):
        self.add_byte("Status", "Success", 0)
        self.add_hword("PanId", "7071", 0x7071)
        self.add_byte("LogicalChannel", "0x0c")
        self.add_byte("ChannelPage", "0x72")
        self.add_bytes("KeySource", (0x73, 0x74, 0x75, 0x76,
                                     0x77, 0x78, 0x79, 0x7a))
        self.add_byte("SecurityLevel", "AES_ENCRYPTION_MIC_32", 5)
        self.add_byte("KeyIdMode", "Not Used", 0)
        self.add_byte("KeyIndex", "7b", 0x7b)
        self.run_test()


class TestMacAssociateInd(BaseMacAReq):
    COMMAND = 0x81
    COMMAND_NAME = "MAC_ASSOCIATE_IND"

    def test_associate_ind(self):
        self.add_ieee("DeviceExtAddr", (0x7c, 0x7d, 0x7e, 0x7f,
                                        0x80, 0x81, 0x82, 0x83))
        self.add_byte("Capabilities",
                      "00 (End Device, Battery Powered)",
                      0x00)
        self.add_bytes("KeySource", (0x84, 0x85, 0x86, 0x87,
                                     0x88, 0x89, 0x8a, 0x8b))
        self.add_byte("SecurityLevel", "MIC_128_AUTH", 0x03)
        self.add_byte("KeyIdMode", "KEY_1BYTE_INDEX", 1)
        self.add_byte("KeyIndex", "8c", 0x8c)
        self.run_test()


class TestMacAssociateCnf(BaseMacAReq):
    COMMAND = 0x82
    COMMAND_NAME = "MAC_ASSOCIATE_CNF"

    def test_associate_confirm(self):
        self.add_byte("Status", "Failed", 1)
        self.add_hword("DeviceAddr", "8d8e", 0x8d8e)
        self.add_bytes("KeySource", (0x8f, 0x90, 0x91, 0x92,
                                     0x93, 0x94, 0x95, 0x96))
        self.add_byte("SecurityLevel", "MIC_64_AUTH", 0x02)
        self.add_byte("KeyIdMode", "KEY_4BYTE_INDEX", 2)
        self.add_byte("KeyIndex", "97", 0x97)
        self.run_test()


class TestMacBeaconNotifyInd(BaseMacAReq):
    COMMAND = 0x83
    COMMAND_NAME = "MAC_BEACON_NOTIFY_IND"

    def test_beacon_notify(self):
        self.add_byte("BSN", "0x98")
        self.add_word("Timestamp", "999a9b9c", 0x999a9b9c)
        self.add_byte("CoordAddressMode", "64-bit", 3)
        self.add_ieee("CoordAddress",
                      (0x9d, 0x9e, 0x9f, 0xa0, 0xa1, 0xa2, 0xa3, 0xa4))
        self.add_hword("PanId", "a5a6", 0xa5a6)
        self.add_hword("SuperframeSpec", "a7a8", 0xa7a8)
        self.add_byte("LogicalChannel", "0xa9")
        self.add_byte("GTSPermit", "0x00")
        self.add_byte("LinkQuality", "0xaa")
        self.add_byte("SecurityFailure", "0x00")
        self.add_bytes("KeySource", (0xab, 0xac, 0xad, 0xae,
                                     0xaf, 0xb0, 0xb1, 0xb2))
        self.add_byte("SecurityLevel", "AES_ENCRYPTION", 4)
        self.add_byte("KeyIdMode", "KEY_8BYTE_INDEX", 3)
        self.add_byte("KeyIndex", "01", 0x01)
        self.add_byte("PendingAddrSpec", "0xb3")
        self.add_byte("AddressList", "0xb4")
        self.add_byte("SDULength", "5")
        self.add_bytes("NSDU", (0xb5, 0xb6, 0xb7, 0xb8, 0xb9))
        self.run_test()


class TestMacDataCnf(BaseMacAReq):
    COMMAND = 0x84
    COMMAND_NAME = "MAC_DATA_CNF"

    def test_data_confirm(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Handle", "0xba")
        self.add_word("Timestamp", "bbbcbdbe", 0xbbbcbdbe)
        self.add_hword("Timestamp2", "bfc0", 0xbfc0)
        self.run_test()


class TestMacDataInd(BaseMacAReq):
    COMMAND = 0x85
    COMMAND_NAME = "MAC_DATA_IND"

    def test_data_indication(self):
        self.add_byte("SrcAddrMode", "16-bit", 2)
        self.add_hword("SrcAddr", "c1c2", 0xc1c2)
        self.add_padding(6)
        self.add_byte("DstAddrMode", "Group address", 1)
        self.add_hword("DstAddr", "c3c4", 0xc3c4)
        self.add_padding(6)
        self.add_word("Timestamp", "c5c6c7c8", 0xc5c6c7c8)
        self.add_hword("Timestamp2", "c9ca", 0xc9ca)
        self.add_hword("SrcPanId", "cbcc", 0xcbcc)
        self.add_hword("DstPanId", "cdce", 0xcdce)
        self.add_byte("LinkQuality", "0xcf")
        self.add_byte("Correlation", "0xd0")
        self.add_byte("RSSI", "0xd1")
        self.add_byte("DSN", "0xd2")
        self.add_bytes("KeySource", (0xd3, 0xd4, 0xd5, 0xd6,
                                     0xd7, 0xd8, 0xd9, 0xda))
        self.add_byte("SecurityLevel", "AES_ENCRYPTION_MIC_64", 6)
        self.add_byte("KeyIdMode", "Not Used", 0)
        self.add_byte("KeyIndex", "db", 0xdb)
        self.add_byte("Length", "4")
        self.add_bytes("Data", (0xdc, 0xdd, 0xde, 0xdf))
        self.run_test()


class TestMacDisassociateInd(BaseMacAReq):
    COMMAND = 0x86
    COMMAND_NAME = "MAC_DISASSOCIATE_IND"

    def test_disassociate(self):
        self.add_ieee("ExtAddr", (0xe0, 0xe1, 0xe2, 0xe3,
                                  0xe4, 0xe5, 0xe6, 0xe7))
        self.add_byte("DisassociateReason",
                      "Coord wishes device to leave", 1)
        self.add_bytes("KeySource", (0xe8, 0xe9, 0xea, 0xeb,
                                     0xec, 0xed, 0xee, 0xef))
        self.add_byte("SecurityLevel", "No Security", 0)
        self.add_byte("KeyIdMode", "Not Used", 0)
        self.add_byte("KeyIndex", "f0", 0xf0)
        self.run_test()


class TestMacDisassociateCnf(BaseMacAReq):
    COMMAND = 0x87
    COMMAND_NAME = "MAC_DISASSOCIATE_CNF"

    def test_disassociate(self):
        self.add_byte("Status", "Failed", 1)
        self.add_byte("DeviceAddressMode", "16-bit", 0x02)
        self.add_hword("DeviceAddress", "f1f2", 0xf1f2)
        self.add_padding(6)
        self.add_hword("DevicePanId", "f3f4", 0xf3f4)
        self.run_test()


class TestMacOrphanInd(BaseMacAReq):
    COMMAND = 0x8a
    COMMAND_NAME = "MAC_ORPHAN_IND"

    def test_orphan_indication(self):
        self.add_ieee("ExtAddr", (0xf5, 0xf6, 0xf7, 0xf8,
                                  0xf9, 0xfa, 0xfb, 0xfc))
        self.add_bytes("KeySource", (0xfd, 0xfe, 0xff, 0x00,
                                     0x01, 0x02, 0x03, 0x04))
        self.add_byte("SecurityLevel", "No Security", 0)
        self.add_byte("KeyIdMode", "Not Used", 0)
        self.add_byte("KeyIndex", "05", 0x05)
        self.run_test()


class TestMacPollCnf(BaseMacAReq):
    COMMAND = 0x8b
    COMMAND_NAME = "MAC_POLL_CNF"

    def test_poll(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestMacScanCnf(BaseMacAReq):
    COMMAND = 0x8c
    COMMAND_NAME = "MAC_SCAN_CNF"

    def test_scan(self):
        self.add_byte("Status", "Failed", 1)
        self.add_byte("ED", "0x06")
        self.add_byte("ScanType", "Passive", 2)
        self.add_byte("ChannelPage", "0x07")
        self.add_word("UnscannedChannelList", "8,9,10", 0x00000700)
        self.add_byte("ResultListCount", "0x01")
        self.add_byte("ResultListMaxLength", "5")
        self.add_bytes("ResultList", (0x08, 0x09, 0x0a, 0x0b, 0x0c))
        self.run_test()


class TestMacCommStatusInd(BaseMacAReq):
    COMMAND = 0x8d
    COMMAND_NAME = "MAC_COMM_STATUS_IND"

    def test_comm_status_indication(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("SrcExtAddr", (0x0d, 0x0e, 0x0f, 0x10,
                                     0x11, 0x12, 0x13, 0x14))
        self.add_byte("DstAddrMode", "64-bit", 3)
        self.add_ieee("DstAddr", (0x15, 0x16, 0x17, 0x18,
                                  0x19, 0x1a, 0x1b, 0x1c))
        self.add_word("Timestamp", "1d1e1f20", 0x1d1e1f20)
        self.add_hword("DevicePanId", "2122", 0x2122)
        self.add_byte("Reason", "0x23")
        self.add_bytes("KeySource", (0x24, 0x25, 0x26, 0x27,
                                     0x28, 0x29, 0x2a, 0x2b))
        self.add_byte("SecurityLevel", "No Security", 0)
        self.add_byte("KeyIdMode", "Not Used", 0)
        self.add_byte("KeyIndex", "2c", 0x2c)
        self.run_test()


class TestMacStartCnf(BaseMacAReq):
    COMMAND = 0x8e
    COMMAND_NAME = "MAC_START_CNF"

    def test_start_confirm(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestMacRxEnableCnf(BaseMacAReq):
    COMMAND = 0x8f
    COMMAND_NAME = "MAC_RX_ENABLE_CNF"

    def test_rx_enable(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestMacPurgeCnf(BaseMacAReq):
    COMMAND = 0x9a
    COMMAND_NAME = "MAC_PURGE_CNF"

    def test_purge_confirm(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Handle", "0x2d")
        self.run_test()


if __name__ == "__main__":
    unittest.main()
