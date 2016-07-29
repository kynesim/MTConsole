#! /usr/bin/env python3

# test_zdo_srsp.py
#
# Unit test for MT ZDO command response parsing
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
from collections import namedtuple


class BaseZdoSRsp(base_test.BaseTest):
    SUBSYSTEM = "ZDO"
    TYPE = "SRSP"

Status = namedtuple("Status", "text, number")

Command = namedtuple("Command", "code, name")


class TestStatus(BaseZdoSRsp):
    STATUS_LIST = (Status("Success", 0),
                   Status("Failed", 1),
                   Status("Invalid Parameter", 2),
                   Status("Out of resources", 0x1a),
                   Status("ZNwkInvalidRequest", 0xc2),
                   Status("ZNwkNotPermitted", 0xc3),
                   Status("Unknown device", 0xc8),
                   Status("Scan in progress", 0xfc))

    COMMANDS = (Command(0x00, "ZDO_NWK_ADDR_REQ"),
                Command(0x01, "ZDO_IEEE_ADDR_REQ"),
                Command(0x02, "ZDO_NODE_DESC_REQ"),
                Command(0x03, "ZDO_POWER_DESC_REQ"),
                Command(0x04, "ZDO_SIMPLE_DESC_REQ"),
                Command(0x05, "ZDO_ACTIVE_EP_REQ"),
                Command(0x06, "ZDO_MATCH_DESC_REQ"),
                Command(0x07, "ZDO_COMPLEX_DESC_REQ"),
                Command(0x08, "ZDO_USER_DESC_REQ"),
                Command(0x0a, "ZDO_END_DEVICE_ANNCE"),
                Command(0x0b, "ZDO_USER_DESC_SET"),
                Command(0x0c, "ZDO_SERVER_DISC_REQ"),
                Command(0x20, "ZDO_END_DEVICE_BIND_REQ"),
                Command(0x21, "ZDO_BIND_REQ"),
                Command(0x22, "ZDO_UNBIND_REQ"),
                Command(0x30, "ZDO_MGMT_NWK_DISC_REQ"),
                Command(0x31, "ZDO_MGMT_LQI_REQ"),
                Command(0x32, "ZDO_MGMT_RTG_REQ"),
                Command(0x33, "ZDO_MGMT_BIND_REQ"),
                Command(0x34, "ZDO_MGMT_LEAVE_REQ"),
                Command(0x35, "ZDO_MGMT_DIRECT_JOIN_REQ"),
                Command(0x36, "ZDO_MGMT_PERMIT_JOIN_REQ"),
                Command(0x37, "ZDO_MGMT_NWK_UPDATE_REQ"),
                Command(0x3e, "ZDO_MSG_CB_REGISTER"),
                Command(0x3f, "ZDO_MSG_CB_REMOVE"),
                Command(0x23, "ZDO_SET_LINK_KEY"),
                Command(0x24, "ZDO_REMOVE_LINK_KEY"),
                Command(0x26, "ZDO_NWK_DISCOVERY_REQ"),
                Command(0x27, "ZDO_JOIN_REQ"),
                Command(0x42, "ZDO_SEC_ADD_LINK_KEY"),
                Command(0x44, "ZDO_SEC_DEVICE_REMOVE"),
                Command(0x45, "ZDO_EXT_ROUTE_DISC"),
                Command(0x46, "ZDO_EXT_ROUTE_CHECK"),
                Command(0x47, "ZDO_EXT_REMOVE_GROUP"),
                Command(0x48, "ZDO_EXT_REMOVE_ALL_GROUP"),
                Command(0x4b, "ZDO_EXT_ADD_GROUP"),
                Command(0x4d, "ZDO_EXT_RX_IDLE"),
                Command(0x4e, "ZDO_EXT_UPDATE_NWK_KEY"),
                Command(0x4f, "ZDO_EXT_SWITCH_NWK_KEY"),
                Command(0x51, "ZDO_EXT_SEC_APS_REMOVE_REQ"),
                Command(0x53, "ZDO_EXT_SET_PARAMS"))

    def setUp(self):
        pass

    def test_status(self):
        for command in TestStatus.COMMANDS:
            # Normally self.COMMAND and self.COMMAND_NAME are
            # constants, hence the capitals.  However I've got bored
            # of the typing, so for these status tests they are
            # variables.  Sorry for the impurity.
            self.COMMAND = command.code
            self.COMMAND_NAME = command.name
            for status in TestStatus.STATUS_LIST:
                BaseZdoSRsp.setUp(self)
                self.add_byte("Status", status.text, status.number)
                self.run_test()


class TestZdoStartupFromApp(BaseZdoSRsp):
    COMMAND = 0x40
    COMMAND_NAME = "ZDO_STARTUP_FROM_APP"

    def test_startup(self):
        self.add_byte("Status", "New network state", 1)
        self.run_test()


class TestZdoGetLinkKey(BaseZdoSRsp):
    COMMAND = 0x25
    COMMAND_NAME = "ZDO_GET_LINK_KEY"

    def test_get_link_key(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("IEEEAddr", (0x35, 0x36, 0x37, 0x38,
                                   0x39, 0x3a, 0x3b, 0x3c))
        self.add_bytes("LinkKeyData", (0x11, 0x21, 0x31, 0x41,
                                       0x51, 0x61, 0x71, 0x81,
                                       0x91, 0xa1, 0xb1, 0xc1,
                                       0xd1, 0xe1, 0xf1, 0x01),
                       leading_0x=True)
        self.run_test()


class TestZdoSecEntryLookupExt(BaseZdoSRsp):
    COMMAND = 0x43
    COMMAND_NAME = "ZDO_SEC_ENTRY_LOOKUP_EXT"

    def test_lookup(self):
        self.add_hword("AMI", "0002", 2)
        self.add_hword("KeyNVID", "0003", 3)
        self.add_byte("AuthenticationOption", "0x04")
        self.run_test()


class TestZdoExtFindAllGroupsEndpoint(BaseZdoSRsp):
    COMMAND = 0x49
    COMMAND_NAME = "ZDO_EXT_FIND_ALL_GROUPS_ENDPOINT"

    def test_find(self):
        self.add_byte("NumGroups", "4")
        self.add_list("Groups", "0001, 0002, 0004, 0008",
                      (0x0001, 0x0002, 0x0004, 0x0008))
        self.run_test()


class TestZdoExtFindGroup(BaseZdoSRsp):
    COMMAND = 0x4a
    COMMAND_NAME = "ZDO_EXT_FIND_GROUP"

    def test_find(self):
        self.add_bytes("Group", (0x34, 0x12, 0x78))
        self.run_test()


class TestZdoExtCountAllGroups(BaseZdoSRsp):
    COMMAND = 0x4c
    COMMAND_NAME = "ZDO_EXT_COUNT_ALL_GROUPS"

    def test_count(self):
        self.add_byte("NumGroups", "0x15")
        self.run_test()


class TestZdoExtNwkInfo(BaseZdoSRsp):
    COMMAND = 0x50
    COMMAND_NAME = "ZDO_EXT_NWK_INFO"

    def test_info(self):
        self.add_hword("ShortAddr", "58d2", 0x58d2)
        self.add_hword("PanId", "7729", 0x7729)
        self.add_hword("ParentAddr", "8ca3", 0x8ca3)
        self.add_ieee("ExtendedPanId",
                      (0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48))
        self.add_ieee("ExtendedParentAddress",
                      (0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58))
        self.add_hword("Channel", "0010", 0x0010)
        self.run_test()


class TestZdoForceConcentratorChange(BaseZdoSRsp):
    COMMAND = 0x52
    COMMAND_NAME = "ZDO_FORCE_CONCENTRATOR_CHANGE"

    def test_force_change(self):
        self.run_test()


if __name__ == "__main__":
    unittest.main()
