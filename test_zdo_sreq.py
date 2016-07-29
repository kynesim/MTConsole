#! /usr/bin/env python3

# test_zdo_sreq.py
#
# Unit test for MT ZDO command parsing
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


class BaseZdoSReq(base_test.BaseTest):
    SUBSYSTEM = "ZDO"
    TYPE = "SREQ"


class TestZdoNwkAddrReq(BaseZdoSReq):
    COMMAND = 0x00
    COMMAND_NAME = "ZDO_NWK_ADDR_REQ"

    def test_address_req(self):
        self.add_ieee("IEEEAddr", (0x1e, 0xee, 0x1e, 0xee,
                                   0x2f, 0xff, 0x2f, 0xff))
        self.add_byte("ReqType", "0x00")
        self.add_byte("StartIndex", "0x00")
        self.run_test()


class TestZdoIeeeAddrReq(BaseZdoSReq):
    COMMAND = 0x01
    COMMAND_NAME = "ZDO_IEEE_ADDR_REQ"

    def test_address_req(self):
        self.add_hword("ShortAddr", "5839", 0x5839)
        self.add_byte("ReqType", "0x01")
        self.add_byte("StartIndex", "0x02")
        self.run_test()


class TestZdoNodeDescReq(BaseZdoSReq):
    COMMAND = 0x02
    COMMAND_NAME = "ZDO_NODE_DESC_REQ"

    def test_node_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.run_test()


class TestZdoPowerDescReq(BaseZdoSReq):
    COMMAND = 0x03
    COMMAND_NAME = "ZDO_POWER_DESC_REQ"

    def test_power_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.run_test()


class TestZdoSimpleDescReq(BaseZdoSReq):
    COMMAND = 0x04
    COMMAND_NAME = "ZDO_SIMPLE_DESC_REQ"

    def test_simple_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.add_byte("Endpoint", "0x0a")
        self.run_test()


class TestZdoActiveEpReq(BaseZdoSReq):
    COMMAND = 0x05
    COMMAND_NAME = "ZDO_ACTIVE_EP_REQ"

    def test_ep_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.run_test()


class TestZdoMatchDescReq(BaseZdoSReq):
    COMMAND = 0x06
    COMMAND_NAME = "ZDO_MATCH_DESC_REQ"

    def test_match_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.add_hword("ProfileId", "3838", 0x3838)
        self.add_byte("NumInClusters", "0")
        self.add_list("InClusterList", "", ())
        self.add_byte("NumOutClusters", "2")
        self.add_list("OutClusterList", "0102, 0203", (0x0102, 0x0203))
        self.run_test()


class TestZdoComplexDescReq(BaseZdoSReq):
    COMMAND = 0x07
    COMMAND_NAME = "ZDO_COMPLEX_DESC_REQ"

    def test_complex_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.run_test()


class TestZdoUserDescReq(BaseZdoSReq):
    COMMAND = 0x08
    COMMAND_NAME = "ZDO_USER_DESC_REQ"

    def test_user_req(self):
        self.add_hword("DstAddr", "829e", 0x829e)
        self.add_hword("NwkAddrOfInterest", "0123", 0x0123)
        self.run_test()


class TestZdoEndDeviceAnnce(BaseZdoSReq):
    COMMAND = 0x0a
    COMMAND_NAME = "ZDO_END_DEVICE_ANNCE"

    def test_device_announcement(self):
        self.add_hword("NwkAddr", "3490", 0x3490)
        self.add_ieee("IEEEAddr", (0xad, 0x13, 0x48, 0x49,
                                   0xf8, 0xe7, 0x79, 0x11))
        self.add_byte("Capabilities",
                      "04 (End Device, Mains Powered)",
                      0x04)
        self.run_test()


class TestZdoUserDescSet(BaseZdoSReq):
    COMMAND = 0x0b
    COMMAND_NAME = "ZDO_USER_DESC_SET"

    def test_user_desc(self):
        self.add_hword("DstAddr", "2435", 0x2435)
        self.add_hword("NwkAddrOfInterest", "2990", 0x2990)
        self.add_byte("Len", "5")
        self.add_bytes("UserDescriptor", (0x01, 0x03, 0x05, 0x07, 0x09))
        self.run_test()


class TestZdoServerDiscReq(BaseZdoSReq):
    COMMAND = 0x0c
    COMMAND_NAME = "ZDO_SERVER_DISC_REQ"

    def test_server_discovery(self):
        self.add_hword("ServerMask", "0024", 0x0024)
        self.run_test()


class TestZdoEndDeviceBindReq(BaseZdoSReq):
    COMMAND = 0x20
    COMMAND_NAME = "ZDO_END_DEVICE_BIND_REQ"

    def test_end_device_bind(self):
        self.add_hword("DstAddr", "1409", 0x1409)
        self.add_hword("LocalCoordinator", "0001", 0x0001)
        self.add_byte("Endpoint", "0x01")
        self.add_hword("ProfileId", "0401", 0x0401)
        self.add_byte("NumInClusters", "2")
        self.add_list("InClusterList", "0004, 0500", (0x0004, 0x0500))
        self.add_byte("NumOutClusters", "0")
        self.add_list("OutClusterList", "", ())
        self.run_test()


class TestZdoBindReq(BaseZdoSReq):
    COMMAND = 0x21
    COMMAND_NAME = "ZDO_BIND_REQ"

    def test_bind_short(self):
        self.add_hword("DstAddr", "3781", 0x3781)
        self.add_ieee("SrcExtAddr", (0x11, 0x22, 0x33, 0x00,
                                     0xff, 0xee, 0x44, 0xdd))
        self.add_byte("SrcEndpoint", "0x0a")
        self.add_hword("ClusterId", "0400", 0x0400)
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddress", "1234", 0x1234)
        self.run_test()

    def test_bind_long(self):
        self.add_hword("DstAddr", "5829", 0x5829)
        self.add_ieee("SrcExtAddr", (0x01, 0x23, 0x45, 0x67,
                                     0x89, 0xab, 0xcd, 0xef))
        self.add_byte("SrcEndpoint", "0x01")
        self.add_hword("ClusterId", "0006", 0x0006)
        self.add_byte("DstAddrMode", "64-bit", 3)
        self.add_ieee("DstAddress", (0xfe, 0xdc, 0xba, 0x98,
                                     0x76, 0x54, 0x32, 0x10))
        self.add_byte("DstEndpoint", "02", 0x02)
        self.run_test()


class TestZdoUnbindReq(BaseZdoSReq):
    COMMAND = 0x22
    COMMAND_NAME = "ZDO_UNBIND_REQ"

    def test_unbind_short(self):
        self.add_hword("DstAddr", "3947", 0x3947)
        self.add_ieee("SrcExtAddr", (0x48, 0x59, 0x6a, 0x7b,
                                     0x8c, 0x9d, 0xae, 0xbf))
        self.add_byte("SrcEndpoint", "0x0b")
        self.add_hword("ClusterId", "0501", 0x0501)
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddress", "9876", 0x9876)
        self.run_test()

    def test_unbind_long(self):
        self.add_hword("DstAddr", "94bf", 0x94bf)
        self.add_ieee("SrcExtAddr", (0xd7, 0xe8, 0xf9, 0x0a,
                                     0x1b, 0x2c, 0x3d, 0x4e))
        self.add_byte("SrcEndpoint", "0x01")
        self.add_hword("ClusterId", "0304", 0x0304)
        self.add_byte("DstAddrMode", "64-bit", 3)
        self.add_ieee("DstAddress", (0x93, 0xa2, 0xb1, 0xc0,
                                     0xdf, 0xee, 0xfd, 0x0c))
        self.add_byte("DstEndpoint", "0a", 0x0a)
        self.run_test()


class TestZdoMgmtNwkDiscReq(BaseZdoSReq):
    COMMAND = 0x30
    COMMAND_NAME = "ZDO_MGMT_NWK_DISC_REQ"

    def test_network_discovery(self):
        self.add_hword("DstAddr", "3849", 0x3849)
        self.add_word("ScanChannels", "11,12,13,14", 0x00007800)
        self.add_byte("ScanDuration", "0x1e")
        self.add_byte("StartIndex", "0x00")
        self.run_test()


class TestZdoMgmtLqiReq(BaseZdoSReq):
    COMMAND = 0x31
    COMMAND_NAME = "ZDO_MGMT_LQI_REQ"

    def test_lqi(self):
        self.add_hword("DstAddr", "fae2", 0xfae2)
        self.add_byte("StartIndex", "0x05")
        self.run_test()


class TestZdoMgmtRtgReq(BaseZdoSReq):
    COMMAND = 0x32
    COMMAND_NAME = "ZDO_MGMT_RTG_REQ"

    def test_routing(self):
        self.add_hword("DstAddr", "2e9c", 0x2e9c)
        self.add_byte("StartIndex", "0x02")
        self.run_test()


class TestZdoMgmtBindReq(BaseZdoSReq):
    COMMAND = 0x33
    COMMAND_NAME = "ZDO_MGMT_BIND_REQ"

    def test_binding_table(self):
        self.add_hword("DstAddr", "5832", 0x5832)
        self.add_byte("StartIndex", "0x01")
        self.run_test()


class TestZdoMgmtLeaveReq(BaseZdoSReq):
    COMMAND = 0x34
    COMMAND_NAME = "ZDO_MGMT_LEAVE_REQ"

    def test_leave(self):
        self.add_hword("DstAddr", "5529", 0x5529)
        self.add_ieee("DeviceExtAddr", (0x01, 0x23, 0x45, 0x67,
                                        0xff, 0xee, 0xdc, 0xaa))
        self.add_byte("RemoveChildrenRejoin",
                      "03 (Rejoin, Remove Children)", 0x03)
        self.run_test()


class TestZdoMgmtDirectJoinReq(BaseZdoSReq):
    COMMAND = 0x35
    COMMAND_NAME = "ZDO_MGMT_DIRECT_JOIN_REQ"

    def test_join(self):
        self.add_hword("DstAddr", "1259", 0x1259)
        self.add_ieee("DeviceExtAddr", (0xfe, 0xdc, 0xba, 0x98,
                                        0x00, 0x11, 0x47, 0x66))
        self.add_byte("Capabilities",
                      "40 (End Device, Battery Powered, Security)",
                      0x40)
        self.run_test()

class TestZdoMgmtPermitJoinReq(BaseZdoSReq):
    COMMAND = 0x36
    COMMAND_NAME = "ZDO_MGMT_PERMIT_JOIN_REQ"

    def test_permit_join(self):
        self.add_byte("AddrMode", "Broadcast", 0xff)
        self.add_hword("DstAddr", "ffff", 0xffff)
        self.add_byte("Duration", "Enabled", 0xff)
        self.add_byte("TCSignificance", "0xa5")
        self.run_test()


class TestZdoMgmtNwkUpdateReq(BaseZdoSReq):
    COMMAND = 0x37
    COMMAND_NAME = "ZDO_MGMT_NWK_UPDATE_REQ"

    def test_update_req(self):
        self.add_hword("DstAddr", "0284", 0x0284)
        self.add_byte("DstAddrMode", "16-bit address", 2)
        self.add_word("ChannelMask", "All", 0x07fff800)
        self.add_byte("ScanDuration", "0x45")
        self.add_byte("ScanCount", "0x03")
        self.add_hword("NwkManagerAddr", "2285", 0x2285)
        self.run_test()


class TestZdoMsgCbRegister(BaseZdoSReq):
    COMMAND = 0x3e
    COMMAND_NAME = "ZDO_MSG_CB_REGISTER"

    def test_register_callback(self):
        self.add_hword("ClusterId", "0002", 0x0002)
        self.run_test()


class TestZdoMsgCbRemove(BaseZdoSReq):
    COMMAND = 0x3f
    COMMAND_NAME = "ZDO_MSG_CB_REMOVE"

    def test_unregister_callback(self):
        self.add_hword("ClusterId", "0301", 0x0301)
        self.run_test()


class TestZdoStartupFromApp(BaseZdoSReq):
    COMMAND = 0x40
    COMMAND_NAME = "ZDO_STARTUP_FROM_APP"

    def test_startup(self):
        self.add_hword("StartDelay", "0015", 0x0015)
        self.run_test()


class TestZdoSetLinkKey(BaseZdoSReq):
    COMMAND = 0x23
    COMMAND_NAME = "ZDO_SET_LINK_KEY"

    def test_set_link_key(self):
        self.add_hword("ShortAddr", "38dd", 0x38dd)
        self.add_ieee("IEEEAddr", (0x01, 0x02, 0x03, 0x04,
                                   0x05, 0x07, 0x08, 0x09))
        self.add_bytes("LinkKeyData", (0x41, 0x42, 0x43, 0x44,
                                       0x45, 0x46, 0x47, 0x48,
                                       0x49, 0x4a, 0x4b, 0x4c,
                                       0x4d, 0x4e, 0x4f, 0x50),
                       leading_0x=True)
        self.run_test()


class TestZdoRemoveLinkKey(BaseZdoSReq):
    COMMAND = 0x24
    COMMAND_NAME = "ZDO_REMOVE_LINK_KEY"

    def test_remove_link_key(self):
        self.add_ieee("IEEEAddr", (0xf0, 0xf1, 0xf2, 0xf3,
                                   0xf4, 0xf5, 0xf6, 0xf7))
        self.run_test()


class TestZdoGetLinkKey(BaseZdoSReq):
    COMMAND = 0x25
    COMMAND_NAME = "ZDO_GET_LINK_KEY"

    def test_get_link_key(self):
        self.add_ieee("IEEEAddr", (0x35, 0x36, 0x37, 0x38,
                                   0x39, 0x3a, 0x3b, 0x3c))
        self.run_test()


class TestZdoNwkDiscoveryReq(BaseZdoSReq):
    COMMAND = 0x26
    COMMAND_NAME = "ZDO_NWK_DISCOVERY_REQ"

    def test_network_discovery(self):
        self.add_word("ScanChannels", "10,12,14", 0x00005400)
        self.add_byte("ScanDuration", "0x3c")
        self.run_test()


class TestZdoJoinReq(BaseZdoSReq):
    COMMAND = 0x27
    COMMAND_NAME = "ZDO_JOIN_REQ"

    def test_join(self):
        self.add_byte("LogicalChannel", "0x0a")
        self.add_hword("PanId", "42fe", 0x42fe)
        self.add_ieee("ExtendedPanId", (0xff,) * 8)
        self.add_hword("ParentAddr", "9de2", 0x9de2)
        self.add_byte("Depth", "0x02")
        self.add_byte("StackProfile", "0x01")
        self.run_test()


class TestZdoSecAddLinkKey(BaseZdoSReq):
    COMMAND = 0x42
    COMMAND_NAME = "ZDO_SEC_ADD_LINK_KEY"

    def test_add_link_key(self):
        self.add_hword("ShortAddr", "3839", 0x3839)
        self.add_ieee("ExtAddr", (0x00, 0x11, 0x22, 0x33,
                                  0x44, 0x55, 0x66, 0x77))
        self.add_bytes("LinkKeyData", (0xe0, 0xe1, 0xe2, 0xe3,
                                       0xe4, 0xe5, 0xe6, 0xe7,
                                       0xe8, 0xe9, 0xea, 0xeb,
                                       0xec, 0xed, 0xee, 0xef),
                       leading_0x=True)
        self.run_test()


class TestZdoSecEntryLookupExt(BaseZdoSReq):
    COMMAND = 0x43
    COMMAND_NAME = "ZDO_SEC_ENTRY_LOOKUP_EXT"

    def test_entry_lookup(self):
        self.add_ieee("ExtAddr", (0x41, 0x52, 0x38, 0x99,
                                  0x53, 0x11, 0x28, 0x93))
        self.add_bytes("Entry", (0x11, 0x22, 0x33, 0x44))
        self.run_test()


class TestZdoSecDeviceRemove(BaseZdoSReq):
    COMMAND = 0x44
    COMMAND_NAME = "ZDO_SEC_DEVICE_REMOVE"

    def test_remove(self):
        self.add_ieee("ExtAddr", (0x1f, 0x20, 0x32, 0x58,
                                  0x1d, 0xf3, 0xe5, 0xa4))
        self.run_test()


class TestZdoExtRouteDisc(BaseZdoSReq):
    COMMAND = 0x45
    COMMAND_NAME = "ZDO_EXT_ROUTE_DISC"

    def test_route_discovery(self):
        self.add_hword("DstAddr", "0013", 0x0013)
        self.add_byte("Options", "0x44")
        self.add_byte("Radius", "0x32")
        self.run_test()


class TestZdoExtRouteCheck(BaseZdoSReq):
    COMMAND = 0x46
    COMMAND_NAME = "ZDO_EXT_ROUTE_CHECK"

    def test_route_check(self):
        self.add_hword("DstAddr", "4859", 0x4859)
        self.add_byte("RTStatus", "0x01")
        self.add_byte("Options", "0x57")
        self.run_test()


class TestZdoExtRemoveGroup(BaseZdoSReq):
    COMMAND = 0x47
    COMMAND_NAME = "ZDO_EXT_REMOVE_GROUP"

    def test_remove_group(self):
        self.add_byte("Endpoint", "0x0a")
        self.add_hword("GroupId", "0159", 0x0159)
        self.run_test()


class TestZdoExtRemoveAllGroup(BaseZdoSReq):
    COMMAND = 0x48
    COMMAND_NAME = "ZDO_EXT_REMOVE_ALL_GROUP"

    def test_remove_groups(self):
        self.add_byte("Endpoint", "0x01")
        self.run_test()


class TestZdoExtFindAllGroupsEndpoint(BaseZdoSReq):
    COMMAND = 0x49
    COMMAND_NAME = "ZDO_EXT_FIND_ALL_GROUPS_ENDPOINT"

    def test_find(self):
        self.add_byte("Endpoint", "0x02")
        self.add_hword("GroupList", "0011", 0x0011)
        self.run_test()


class TestZdoExtFindGroup(BaseZdoSReq):
    COMMAND = 0x4a
    COMMAND_NAME = "ZDO_EXT_FIND_GROUP"

    def test_find(self):
        self.add_byte("Endpoint", "0x0b")
        self.add_hword("GroupId", "0005", 0x0005)
        self.run_test()


class TestZdoExtAddGroup(BaseZdoSReq):
    COMMAND = 0x4b
    COMMAND_NAME = "ZDO_EXT_ADD_GROUP"

    def test_add_group(self):
        self.add_byte("Endpoint", "0x03")
        self.add_hword("GroupId", "5829", 0x5829)
        group_name = b'My Group'
        group_name += b'\x00' * (16 - len(group_name))
        self.add_bytes("GroupName", group_name, leading_0x=True)
        self.run_test()


class TestZdoExtCountAllGroups(BaseZdoSReq):
    COMMAND = 0x4c
    COMMAND_NAME = "ZDO_EXT_COUNT_ALL_GROUPS"

    def test_count(self):
        self.run_test()


class TestZdoExtRxIdle(BaseZdoSReq):
    COMMAND = 0x4d
    COMMAND_NAME = "ZDO_EXT_RX_IDLE"

    def test_rx_idle(self):
        self.add_byte("GetSetFlag", "0x01")
        self.add_byte("SetValue", "0x02")
        self.run_test()


class TestZdoExtUpdateNwkKey(BaseZdoSReq):
    COMMAND = 0x4e
    COMMAND_NAME = "ZDO_EXT_UPDATE_NWK_KEY"

    def test_update_key(self):
        self.add_hword("DstAddr", "5882", 0x5882)
        self.add_byte("KeySeqNum", "0x20")
        self.add_bytes("Key",
                       (0x01,) * 15 +
                       (0x25,) * 28 +
                       (0xf3,) * 19 +
                       (0xdc,) * 20 +
                       (0xa6,) * 25 +
                       (0x11,) * 21,
                       leading_0x=True)
        self.run_test()


class TestZdoExtSwitchNwkKey(BaseZdoSReq):
    COMMAND = 0x4f
    COMMAND_NAME = "ZDO_EXT_SWITCH_NWK_KEY"

    def test_switch_key(self):
        self.add_hword("DstAddr", "ace1", 0xace1)
        self.add_byte("KeySeqNum", "0x02")
        self.run_test()


class TestZdoExtNwkInfo(BaseZdoSReq):
    COMMAND = 0x50
    COMMAND_NAME = "ZDO_EXT_NWK_INFO"

    def test_get_info(self):
        self.run_test()


class TestZdoExtSecApsRemoveReq(BaseZdoSReq):
    COMMAND = 0x51
    COMMAND_NAME = "ZDO_EXT_SEC_APS_REMOVE_REQ"

    def test_remove(self):
        self.add_hword("NwkAddr", "5829", 0x5829)
        self.add_ieee("ExtAddr", (0x01, 0x02, 0x03, 0x04,
                                  0x05, 0x06, 0x07, 0x08))
        self.add_hword("ParentAddr", "20c2", 0x20c2)
        self.run_test()


class TestZdoForceConcentratorChange(BaseZdoSReq):
    COMMAND = 0x52
    COMMAND_NAME = "ZDO_FORCE_CONCENTRATOR_CHANGE"

    def test_force_change(self):
        self.run_test()


class TestZdoExtSetParams(BaseZdoSReq):
    COMMAND = 0x53
    COMMAND_NAME = "ZDO_EXT_SET_PARAMS"

    def test_set_params(self):
        self.add_byte("UseMulticast", "0x01")
        self.run_test()


if __name__ == "__main__":
    unittest.main()
