#! /usr/bin/env python3

# Unit tests for MT ZDO announcement parsing

import base_test
import unittest


class BaseZdoAReq(base_test.BaseTest):
    SUBSYSTEM = "ZDO"
    TYPE = "AREQ"


class TestZdoAutoFindDestination(BaseZdoAReq):
    COMMAND = 0x41
    COMMAND_NAME = "ZDO_AUTO_FIND_DESTINATION"

    def test_find(self):
        self.add_byte("Endpoint", "0x01")
        self.run_test()


class TestZdoNwkAddrRsp(BaseZdoAReq):
    COMMAND = 0x80
    COMMAND_NAME = "ZDO_NWK_ADDR_RSP"

    def test_address(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("IEEEAddr", (0x14, 0x25, 0x36, 0x47,
                                   0x58, 0x69, 0x7a, 0x8b))
        self.add_hword("NwkAddr", "2885", 0x2885)
        self.add_byte("StartIndex", "0x00")
        self.add_byte("NumAssocDevices", "3")
        self.add_list("AssocDevicesList",
                      "0482, 859c, af49",
                      (0x0482, 0x859c, 0xaf49))
        self.run_test()


class TestZdoIeeeAddrRsp(BaseZdoAReq):
    COMMAND = 0x81
    COMMAND_NAME = "ZDO_IEEE_ADDR_RSP"

    def test_address(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("IEEEAddr", (0x14, 0x25, 0x36, 0x47,
                                   0x58, 0x69, 0x7a, 0x8b))
        self.add_hword("NwkAddr", "2885", 0x2885)
        self.add_byte("StartIndex", "0x00")
        self.add_byte("NumAssocDevices", "3")
        self.add_list("AssocDevicesList",
                      "0482, 859c, af49",
                      (0x0482, 0x859c, 0xaf49))
        self.run_test()


class TestZdoNodeDescRsp(BaseZdoAReq):
    COMMAND = 0x82
    COMMAND_NAME = "ZDO_NODE_DESC_RSP"

    def test_node_descriptor(self):
        self.add_hword("SrcAddr", "8593", 0x8593)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "7d2c", 0x7d2c)
        self.add_byte("TypeInfo",
                      "1a (Router, Complex Descriptor Available,"
                      " User Descriptor Available)",
                      0x1a)
        self.add_byte("APSFlags/NodeFrequencyBand", "", 0x10)
        self.add_text("  APSFlags", "00")
        self.add_text("  NodeFrequencyBand", "01")
        self.add_byte("MacCapabilitiesFlags",
                      "0c (End Device, Mains Powered, Rx On When Idle)",
                      0x0c)
        self.add_hword("ManufacturerCode", "0014", 0x0014)
        self.add_byte("MaxBufferSize", "0xfe")
        self.add_hword("MaxInTransferSize", "7fff", 0x7fff)
        self.add_hword("ServerMask", "01 (Primary Trust Centre)", 0x0001)
        self.add_hword("MaxOutTransferSize", "7ffe", 0x7ffe)
        self.add_byte("DescriptorCapabilities", "0x01")
        self.run_test()


class TestZdoPowerDescRsp(BaseZdoAReq):
    COMMAND = 0x83
    COMMAND_NAME = "ZDO_POWER_DESC_RSP"

    def test_power_descriptor(self):
        self.add_hword("SrcAddr", "face", 0xface)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "dead", 0xdead)
        self.add_byte("CurrentPowerMode/AvailablePowerSources", "", 0x56)
        self.add_text("  CurrentPowerMode", "06")
        self.add_text("  AvailablePowerSources", "05")
        self.add_byte("CurrentPowerSource/CurrentPowerSourceLevel",
                      "", 0x14)
        self.add_text("  CurrentPowerSource", "04")
        self.add_text("  CurrentPowerSourceLevel", "01")
        self.run_test()


class TestZdoSimpleDescRsp(BaseZdoAReq):
    COMMAND = 0x84
    COMMAND_NAME = "ZDO_SIMPLE_DESC_RSP"

    def test_simple_descriptor(self):
        self.add_hword("SrcAddr", "2181", 0x2181)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "7310", 0x7310)
        self.add_byte("Len", "0x10")
        self.add_byte("Endpoint", "0x01")
        self.add_hword("ProfileId", "0401", 0x0401)
        self.add_hword("DeviceId", "0118", 0x0118)
        self.add_byte("DeviceVersion", "0x00")
        self.add_byte("NumInClusters", "2")
        self.add_list("InClusterList", "0001, 0500", (0x0001, 0x0500))
        self.add_byte("NumOutClusters", "1")
        self.add_list("OutClusterList", "0003", (0x0003,))
        self.run_test()


class TestZdoActiveEpRsp(BaseZdoAReq):
    COMMAND = 0x85
    COMMAND_NAME = "ZDO_ACTIVE_EP_RSP"

    def test_active_ep(self):
        self.add_hword("SrcAddr", "38cc", 0x38cc)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "27f3", 0x27f3)
        self.add_byte("ActiveEPCount", "1")
        self.add_bytes("ActiveEPList", (0x0a,))
        self.run_test()


class TestZdoMatchDescRsp(BaseZdoAReq):
    COMMAND = 0x86
    COMMAND_NAME = "ZDO_MATCH_DESC_RSP"

    def test_match_descriptor(self):
        self.add_hword("SrcAddr", "763d", 0x763d)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "259c", 0x259c)
        self.add_byte("MatchLength", "3")
        self.add_bytes("MatchList", (0x01, 0x0a, 0x0b))
        self.run_test()


class TestZdoComplexDescRsp(BaseZdoAReq):
    COMMAND = 0x87
    COMMAND_NAME = "ZDO_COMPLEX_DESC_RSP"

    def test_complex_descriptor(self):
        self.add_hword("SrcAddr", "ff2a", 0xff2a)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "0001", 0x0001)
        self.add_byte("ComplexLength", "7")
        self.add_bytes("ComplexDescriptor", (0x01, 0x02, 0x03, 0x04,
                                             0x05, 0x06, 0xfe))
        self.run_test()


class TestZdoUserDescRsp(BaseZdoAReq):
    COMMAND = 0x88
    COMMAND_NAME = "ZDO_USER_DESC_RSP"

    def test_user_descriptor(self):
        self.add_hword("SrcAddr", "289f", 0x289f)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "1258", 0x1258)
        self.add_byte("UserLength", "15")
        self.add_bytes("UserDescriptor", range(15))
        self.run_test()


class TestZdoUserDescConf(BaseZdoAReq):
    COMMAND = 0x89
    COMMAND_NAME = "ZDO_USER_DESC_CONF"

    def test_user_descriptor(self):
        self.add_hword("SrcAddr", "5520", 0x5520)
        self.add_byte("Status", "Success", 0)
        self.add_hword("NwkAddr", "5892", 0x5892)
        self.run_test()


class TestZdoServerDiscRsp(BaseZdoAReq):
    COMMAND = 0x8a
    COMMAND_NAME = "ZDO_SERVER_DISC_RSP"

    def test_server_discovery(self):
        self.add_hword("SrcAddr", "a435", 0xa435)
        self.add_byte("Status", "Success", 0)
        self.add_hword("ServerMask", "02 (Backup Trust Centre)", 0x02)
        self.run_test()


class TestZdoEndDeviceBindRsp(BaseZdoAReq):
    COMMAND = 0xa0
    COMMAND_NAME = "ZDO_END_DEVICE_BIND_RSP"

    def test_bind(self):
        self.add_hword("SrcAddr", "5286", 0x5286)
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestZdoBindRsp(BaseZdoAReq):
    COMMAND = 0xa1
    COMMAND_NAME = "ZDO_BIND_RSP"

    def test_bind(self):
        self.add_hword("SrcAddr", "9201", 0x9201)
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZdoUnbindRsp(BaseZdoAReq):
    COMMAND = 0xa2
    COMMAND_NAME = "ZDO_UNBIND_RSP"

    def test_unbind(self):
        self.add_hword("SrcAddr", "4def", 0x4def)
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZdoMgmtNwkDiscRsp(BaseZdoAReq):
    COMMAND = 0xb0
    COMMAND_NAME = "ZDO_MGMT_NWK_DISC_RSP"

    def test_network_discovery(self):
        self.add_hword("SrcAddr", "5111", 0x5111)
        self.add_byte("Status", "Success", 0)
        self.add_byte("NetworkCount", "0x06")
        self.add_byte("StartIndex", "0x05")
        self.add_byte("NetworkListCount", "2")
        self.add_text("NetworkListRecords", "")
        self.add_hword("  PanId", "0102", 0x0102)
        self.add_byte("  LogicalChannel", "0x03")
        self.add_byte("  ZigBeeVersion/StackProfile", "", 0x45)
        self.add_text("    ZigBeeVersion", "04")
        self.add_text("    StackProfile", "05")
        self.add_byte("  SuperframeOrder/BeaconOrder", "", 0x67)
        self.add_text("    SuperframeOrder", "06")
        self.add_text("    BeaconOrder", "07")
        self.add_byte("  PermitJoining", "0x00")
        self.add_hword("  PanId", "0809", 0x0809)
        self.add_byte("  LogicalChannel", "0x0a")
        self.add_byte("  ZigBeeVersion/StackProfile", "", 0xbc)
        self.add_text("    ZigBeeVersion", "0b")
        self.add_text("    StackProfile", "0c")
        self.add_byte("  SuperframeOrder/BeaconOrder", "", 0xde)
        self.add_text("    SuperframeOrder", "0d")
        self.add_text("    BeaconOrder", "0e")
        self.add_byte("  PermitJoining", "0x01")
        self.run_test()


class TestZdoMgmtLqiRsp(BaseZdoAReq):
    COMMAND = 0xb1
    COMMAND_NAME = "ZDO_MGMT_LQI_RSP"

    def test_lqi(self):
        self.add_hword("SrcAddr", "1895", 0x1895)
        self.add_byte("Status", "Success", 0)
        self.add_byte("NeighbourTableEntries", "0x02")
        self.add_byte("StartIndex", "0x00")
        self.add_byte("NeighbourLqiListCount", "2")
        self.add_text("NeighbourLqiList","")
        self.add_ieee("  ExtendedPanId", (0x10, 0x20, 0x30, 0x40,
                                          0x50, 0x60, 0x70, 0x00))
        self.add_ieee("  ExtAddr", (0x81, 0x92, 0xa3, 0xb4,
                                    0xc5, 0xd6, 0xe7, 0xf8))
        self.add_hword("  NwkAddr", "5992", 0x5992)
        self.add_byte("  Relationship/RxOnWhenIdle/DeviceType",
                      "", 0x16)
        self.add_text("    Relationship", "01")
        self.add_text("    RxOnWhenIdle", "01")
        self.add_text("    DeviceType", "02")
        self.add_byte("  PermitJoining", "0x01")
        self.add_byte("  Depth", "0x05")
        self.add_byte("  LQI", "0x74")
        self.add_ieee("  ExtendedPanId", (0x11, 0x21, 0x31, 0x41,
                                          0x51, 0x61, 0x71, 0x01))
        self.add_ieee("  ExtAddr", (0x15, 0x16, 0x17, 0x18,
                                    0x30, 0x31, 0x42, 0x43))
        self.add_hword("  NwkAddr", "149f", 0x149f)
        self.add_byte("  Relationship/RxOnWhenIdle/DeviceType",
                      "", 0x25)
        self.add_text("    Relationship", "02")
        self.add_text("    RxOnWhenIdle", "01")
        self.add_text("    DeviceType", "01")
        self.add_byte("  PermitJoining", "0x03")
        self.add_byte("  Depth", "0x10")
        self.add_byte("  LQI", "0x14")
        self.run_test()


class TestZdoMgmtRtgRsp(BaseZdoAReq):
    COMMAND = 0xb2
    COMMAND_NAME = "ZDO_MGMT_RTG_RSP"

    def test_routing(self):
        self.add_hword("SrcAddr", "1515", 0x1515)
        self.add_byte("Status", "Success", 0)
        self.add_byte("RoutingTableEntries", "0x10")
        self.add_byte("StartIndex", "0x04")
        self.add_byte("RoutingTableListCount", "1")
        self.add_text("RoutingTableList", "")
        self.add_hword("  DstAddr", "d390", 0xd390)
        self.add_byte("  Status", "Discovery Underway", 0x01)
        self.add_hword("  NextHop", "9785", 0x9785)
        self.run_test()


class TestZdoMgmtBindRsp(BaseZdoAReq):
    COMMAND = 0xb3
    COMMAND_NAME = "ZDO_MGMT_BIND_RSP"

    def test_bind(self):
        self.add_hword("SrcAddr", "e922", 0xe922)
        self.add_byte("Status", "Success", 0)
        self.add_byte("BindingTableEntries", "0x22")
        self.add_byte("StartIndex", "0x09")
        self.add_byte("BindingTableListCount", "1")
        self.add_text("BindingTableList", "")
        self.add_ieee("  SrcExtAddr", (0x63, 0x64, 0x65, 0x66,
                                       0x29, 0x20, 0x40, 0x51))
        self.add_byte("  SrcEndpoint", "0x01")
        self.add_hword("  ClusterId", "0501", 0x0501)
        self.add_byte("  DstAddrMode", "16-bit", 2)
        self.add_hword("  DstAddr", "1958", 0x1958)
        self.add_padding(6)
        self.add_byte("  DstEndpoint", "0x0a")
        self.run_test()


class TestZdoMgmtLeaveRsp(BaseZdoAReq):
    COMMAND = 0xb4
    COMMAND_NAME = "ZDO_MGMT_LEAVE_RSP"

    def test_leave(self):
        self.add_hword("SrcAddr", "5298", 0x5298)
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZdoMgmtDirectJoinRsp(BaseZdoAReq):
    COMMAND = 0xb5
    COMMAND_NAME = "ZDO_MGMT_DIRECT_JOIN_RSP"

    def test_join(self):
        self.add_hword("SrcAddr", "1922", 0x1922)
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZdoMgmtPermitJoinRsp(BaseZdoAReq):
    COMMAND = 0xb6
    COMMAND_NAME = "ZDO_MGMT_PERMIT_JOIN_RSP"

    def test_permit_join(self):
        self.add_hword("SrcAddr", "8736", 0x8736)
        self.add_byte("Status", "Success", 0)
        self.run_test()


class TestZdoStateChangeInd(BaseZdoAReq):
    COMMAND = 0xc0
    COMMAND_NAME = "ZDO_STATE_CHANGE_IND"

    def test_state_change(self):
        self.add_byte("State", "0x01")
        self.run_test()


class TestZdoEndDeviceAnnceInd(BaseZdoAReq):
    COMMAND = 0xc1
    COMMAND_NAME = "ZDO_END_DEVICE_ANNCE_IND"

    def test_end_device_announce(self):
        self.add_hword("SrcAddr", "2587", 0x2587)
        self.add_hword("NwkAddr", "1711", 0x1711)
        self.add_ieee("IEEEAddr", (0x58, 0x59, 0x60, 0x71,
                                   0x81, 0x83, 0x73, 0x25))
        self.add_byte("Capabilities",
                      "02 (Zigbee Router, Battery Powered)",
                      0x02)
        self.run_test()


class TestZdoMatchDescRspSent(BaseZdoAReq):
    COMMAND = 0xc2
    COMMAND_NAME = "ZDO_MATCH_DESC_RSP_SENT"

    def test_match_response_sent(self):
        self.add_hword("NwkAddr", "1552", 0x1552)
        self.add_byte("NumInClusters", "2")
        self.add_list("InClusterList", "1592, 0003", (0x1592, 0x0003))
        self.add_byte("NumOutClusters", "1")
        self.add_list("OutClusterList", "0100", (0x0100,))
        self.run_test()


class TestZdoStatusErrorRsp(BaseZdoAReq):
    COMMAND = 0xc3
    COMMAND_NAME = "ZDO_STATUS_ERROR_RSP"

    def test_error_status(self):
        self.add_hword("SrcAddr", "1859", 0x1859)
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestZdoSrcRtgInd(BaseZdoAReq):
    COMMAND = 0xc4
    COMMAND_NAME = "ZDO_SRC_RTG_IND"

    def test_source_routing(self):
        self.add_hword("DstAddr", "7852", 0x7852)
        self.add_byte("RelayCount", "3")
        self.add_list("RelayList", "0014, 8749, ae28",
                      (0x0014, 0x8749, 0xae28))
        self.run_test()


class TestZdoBeaconNotifyInd(BaseZdoAReq):
    COMMAND = 0xc5
    COMMAND_NAME = "ZDO_BEACON_NOTIFY_IND"

    def test_beacon_notify(self):
        self.add_byte("BeaconCount", "1")
        self.add_text("BeaconList", "")
        self.add_hword("  SrcAddr", "1588", 0x1588)
        self.add_hword("  PanId", "feed", 0xfeed)
        self.add_byte("  LogicalChannel", "0x0a")
        self.add_byte("  PermitJoining", "0x00")
        self.add_byte("  RouterCapacity", "0x01")
        self.add_byte("  DeviceCapacity", "0x01")
        self.add_byte("  ProtocolVersion", "0x02")
        self.add_byte("  StackProfile" ,"0x02")
        self.add_byte("  LQI", "0x84")
        self.add_byte("  Depth", "0x03")
        self.add_byte("  UpdateId", "0x48")
        self.add_ieee("  ExtendedPanId", (0x04, 0x94, 0x74, 0x71,
                                          0x1d, 0x1e, 0xa3, 0x28))
        self.run_test()


class TestZdoJoinCnf(BaseZdoAReq):
    COMMAND = 0xc6
    COMMAND_NAME = "ZDO_JOIN_CNF"

    def test_join_ok(self):
        self.add_byte("Status", "Success", 0)
        self.add_hword("DeviceAddr", "8839", 0x8839)
        self.add_hword("ParentAddr", "da21", 0xda21)
        self.run_test()

    def test_join_no_ack(self):
        self.add_byte("Status", "ZMacNoAck", 0xe9)
        self.add_hword("DeviceAddr", "5920", 0x5920)
        self.add_hword("ParentAddr", "f920", 0xf920)
        self.run_test()


class TestZdoNwkDiscoveryCnf(BaseZdoAReq):
    COMMAND = 0xc7
    COMMAND_NAME = "ZDO_NWK_DISCOVERY_CNF"

    def test_discovery_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_discovery_no_beacon(self):
        self.add_byte("Status", "ZMacNoBeacon", 0xea)
        self.run_test()

    def test_discovery_bad_param(self):
        self.add_byte("Status", "ZMacInvalidParameter", 0xe8)
        self.run_test()


class TestZdoLeaveInd(BaseZdoAReq):
    COMMAND = 0xc9
    COMMAND_NAME = "ZDO_LEAVE_IND"

    def test_leave(self):
        self.add_hword("SrcAddr", "5892", 0x5892)
        self.add_ieee("ExtAddr", (0x01, 0x02, 0x03, 0x0a,
                                  0x05, 0x01, 0x05, 0x0b))
        self.add_byte("Request", "0x00")
        self.add_byte("Remove", "0x01")
        self.add_byte("Rejoin", "0x00")
        self.run_test()


class TestZdoMsgCbIncoming(BaseZdoAReq):
    COMMAND = 0xff
    COMMAND_NAME = "ZDO_MSG_CB_INCOMING"

    def test_incoming(self):
        self.add_hword("SrcAddr", "dead", 0xdead)
        self.add_byte("WasBroadcast", "0x01")
        self.add_hword("ClusterId", "0401", 0x0401)
        self.add_byte("SecurityUse", "0x00")
        self.add_byte("SeqNum", "0x1a")
        self.add_hword("MacDstAddr", "1ffa", 0x1ffa)
        self.add_bytes("Data", (0x01, 0x02, 0x03, 0x05, 0x07, 0x91))
        self.run_test()


if __name__ == "__main__":
    unittest.main()
