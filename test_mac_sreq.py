#! /usr/bin/env python3

# Unit tests for MT MAC command parsing

import base_test
import unittest


class BaseMacSReq(base_test.BaseTest):
    SUBSYSTEM = "MAC"
    TYPE = "SREQ"


class TestMacResetReq(BaseMacSReq):
    COMMAND = 0x01
    COMMAND_NAME = "MAC_RESET_REQ"

    def test_reset_with_default(self):
        self.add_byte("SetDefault", "0x01")
        self.run_test()

    def test_reset_no_default(self):
        self.add_byte("SetDefault", "0x00")
        self.run_test()


class TestMacInit(BaseMacSReq):
    COMMAND = 0x02
    COMMAND_NAME = "MAC_INIT"

    def test_init(self):
        # There is no data to this command at all
        self.run_test()


class TestMacStartReq(BaseMacSReq):
    COMMAND = 0x03
    COMMAND_NAME = "MAC_START_REQ"

    def test_start_req(self):
        self.add_word("StartTime", "12345678", 0x12345678)
        self.add_hword("PanId", "9abc", 0x9abc)
        self.add_byte("LogicalChannel", "0xde")
        self.add_byte("ChannelPage", "0xf0")
        self.add_byte("BeaconOrder", "0x01")
        self.add_byte("SuperFrameOrder", "0x02")
        self.add_byte("PanCoordinator", "0x00")
        self.add_byte("BatteryLiftExt", "0x04")
        self.add_byte("CoordRealignment", "0x08")
        self.add_bytes("RealignKeySource", (0x10, 0x20, 0x40, 0x80,
                                            0x7f, 0xbf, 0xdf, 0xef))
        self.add_byte("RealignSecurityLevel", "No Security", 0x00)
        self.add_byte("RealignKeyIdMode", "KEY_1BYTE_INDEX", 0x01)
        self.add_byte("RealignKeyIndex", "02", 0x02)
        self.add_bytes("BeaconKeySource", (0xf7, 0xfb, 0xfd, 0xfe,
                                           0x17, 0x18, 0x19, 0x1a))
        self.add_byte("BeaconSecurityLevel", "MIC_64_AUTH", 0x02)
        self.add_byte("BeaconKeyIdMode", "KEY_8BYTE_INDEX", 0x03)
        self.add_byte("BeaconKeyIndex", "04", 0x04)
        self.run_test()


class TestMacSyncReq(BaseMacSReq):
    COMMAND = 0x04
    COMMAND_NAME = "MAC_SYNC_REQ"

    def test_sync(self):
        self.add_byte("LogicalChannel", "0x0a")
        self.add_byte("ChannelPage", "0x03")
        self.add_byte("TrackBeacon", "0x01")
        self.run_test()


class TestMacDataReq(BaseMacSReq):
    COMMAND = 0x05
    COMMAND_NAME = "MAC_DATA_REQ"

    def test_data_req(self):
        self.add_byte("DstAddrMode", "16-bit", 0x02)
        self.add_hword("DstAddr", "7fda", 0x7fda)
        self.add_padding(6)
        self.add_hword("DstPanId", "1172", 0x1172)
        self.add_byte("SrcAddressMode", "64-bit address", 0x03)
        self.add_byte("Handle", "0xdc")
        self.add_byte("TxOption", "05 (Ack, Indirect)", 0x05)
        self.add_byte("LogicalChannel", "0x0b")
        self.add_byte("Power", "0x59")
        self.add_bytes("KeySource", (0x01, 0x23, 0x45, 0x67,
                                     0x89, 0xab, 0xcd, 0xef))
        self.add_byte("SecurityLevel", "AES_ENCRYPTION", 0x04)
        self.add_byte("KeyIdMode", "Not Used", 0x00)
        self.add_byte("KeyIndex", "00", 0x00)
        self.add_byte("MSDULength", "3")
        self.add_bytes("MSDU", (0xfe, 0x38, 0xc2))
        self.run_test()


class TestMacAssociateReq(BaseMacSReq):
    COMMAND = 0x06
    COMMAND_NAME = "MAC_ASSOCIATE_REQ"

    def test_assoc_req(self):
        self.add_byte("LogicalChannel", "0x01")
        self.add_byte("ChannelPage", "0x02")
        self.add_byte("CoordAddressMode", "16-bit", 0x02)
        self.add_hword("CoordAddress", "0304", 0x0304)
        self.add_padding(6)
        self.add_hword("CoordPanId", "0506", 0x0506)
        self.add_byte("Capabilities",
                      "07 (Alternative PAN Coord,"
                      " Zigbee Router, Mains Powered)",
                      0x07)
        self.add_bytes("KeySource", (0x08, 0x09, 0x0a, 0x0b,
                                     0x0c, 0x0d, 0x0e, 0x0f))
        self.add_byte("SecurityLevel", "AES_ENCRYPTION_MIC_128", 0x07)
        self.add_byte("KeyIdMode", "Not Used", 0x00)
        self.add_byte("KeyIndex", "10", 0x10)
        self.run_test()


class TestMacAssociateRsp(BaseMacSReq):
    COMMAND = 0x50
    COMMAND_NAME = "MAC_ASSOCIATE_RSP"

    def test_assoc_rsp(self):
        self.add_ieee("ExtAddr", (0x10, 0x11, 0x12, 0x13,
                                  0x14, 0x15, 0x16, 0x17))
        self.add_hword("AssocShortAddress", "1819", 0x1819)
        self.add_byte("AssocStatus", "PAN at capacity", 1)
        self.run_test()


class TestMacDisassociateReq(BaseMacSReq):
    COMMAND = 0x07
    COMMAND_NAME = "MAC_DISASSOCIATE_REQ"

    def test_disassoc_req(self):
        self.add_byte("DeviceAddressMode", "64-bit", 0x03)
        self.add_ieee("DeviceAddress", (0x1a, 0x1b, 0x1c, 0x1d,
                                        0x1e, 0x1f, 0x20, 0x21))
        self.add_hword("DevicePanId", "2223", 0x2223)
        self.add_byte("DisassociateReason", "Device wishes to leave", 2)
        self.add_byte("TxIndirect", "0x00")
        self.add_bytes("KeySource", (0x24, 0x25, 0x26, 0x27,
                                     0x28, 0x29, 0x2a, 0x2b))
        self.add_byte("SecurityLevel", "MIC_32_AUTH", 1)
        self.add_byte("KeyIdMode", "KEY_8BYTE_INDEX", 3)
        self.add_byte("KeyIndex", "2c", 0x2c)
        self.run_test()


class TestMacGetReq(BaseMacSReq):
    COMMAND = 0x08
    COMMAND_NAME = "MAC_GET_REQ"

    def test_get_attribute(self):
        self.add_byte("Attribute", "ZMAC_ACK_WAIT_DURATION", 0x40)
        self.run_test()


class TestMacSetReq(BaseMacSReq):
    COMMAND = 0x09
    COMMAND_NAME = "MAC_SET_REQ"

    def test_set_attribute(self):
        self.add_byte("Attribute", "ZMAC_ASSOCIATION_PERMIT", 0x41)
        self.add_bytes("AttributeValue", (0x3d, 0x3e, 0x3f, 0x40,
                                0x41, 0x42, 0x43, 0x44,
                                0x45, 0x46, 0x47, 0x48,
                                0x49, 0x4a, 0x4b, 0x4c),
                       leading_0x=True)
        self.run_test()


class TestMacScanReq(BaseMacSReq):
    COMMAND = 0x0c
    COMMAND_NAME = "MAC_SCAN_REQ"

    def test_scan_request(self):
        self.add_word("ScanChannels", "16,17", 0x00030000)
        self.add_byte("ScanType", "Active", 1)
        self.add_byte("ScanDuration", "0x4d")
        self.add_byte("ChannelPage", "0x4e")
        self.add_byte("MaxResults", "0x01")
        self.add_bytes("KeySource", (0x4f, 0x50, 0x51, 0x52,
                                     0x53, 0x54, 0x55, 0x56))
        self.add_byte("SecurityLevel", "No Security", 0)
        self.add_byte("KeyIdMode", "KEY_1BYTE_INDEX", 1)
        self.add_byte("KeyIndex", "57", 0x57)
        self.run_test()


class TestMacOrphanRsp(BaseMacSReq):
    COMMAND = 0x51
    COMMAND_NAME = "MAC_ORPHAN_RSP"

    def test_orphan_response(self):
        self.add_ieee("ExtAddr", (0x58, 0x59, 0x5a, 0x5b,
                                  0x5c, 0x5d, 0x5e, 0x5f))
        self.add_hword("AssocShortAddress", "6061", 0x6061)
        self.add_byte("AssociatedMember", "0x01")
        self.run_test()


class TestMacPollReq(BaseMacSReq):
    COMMAND = 0x0d
    COMMAND_NAME = "MAC_POLL_REQ"

    def test_poll_request(self):
        self.add_byte("CoordAddressMode", "16-bit", 0x02)
        self.add_hword("CoordAddress", "6263", 0x6263)
        self.add_padding(6)
        self.add_hword("CoordPanId", "6465", 0x6465)
        self.add_bytes("KeySource", (0x66, 0x67, 0x68, 0x69,
                                     0x6a, 0x6b, 0x6c, 0x6d))
        self.add_byte("SecurityLevel", "MIC_32_AUTH", 1)
        self.add_byte("KeyIdMode", "KEY_8BYTE_INDEX", 3)
        self.add_byte("KeyIndex", "6e", 0x6e)
        self.run_test()


class TestMacPurgeReq(BaseMacSReq):
    COMMAND = 0x0e
    COMMAND_NAME = "MAC_PURGE_REQ"

    def test_purge_request(self):
        self.add_byte("MsduHandle", "0x6f")
        self.run_test()


class TestMacSetRxGainReq(BaseMacSReq):
    COMMAND = 0x0f
    COMMAND_NAME = "MAC_SET_RX_GAIN_REQ"

    def test_rx_gain_request(self):
        self.add_byte("Mode", "0x00")
        self.run_test()


if __name__ == "__main__":
    unittest.main()
