#! /usr/bin/env python3

# test_util_sreq.py
#
# Unit tests for MT UTILS command parsing
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


class BaseUtilSReq(base_test.BaseTest):
    SUBSYSTEM = "UTIL"
    TYPE = "SREQ"


class BaseNoParams:
    def test_no_params(self):
        self.run_test()


class TestUtilSetPanId(BaseUtilSReq):
    COMMAND = 0x02
    COMMAND_NAME = "UTIL_SET_PANID"

    def test_set_pan_id(self):
        self.add_hword("PanId", "6628", 0x6628)
        self.run_test()


class TestUtilSetChannels(BaseUtilSReq):
    COMMAND = 0x03
    COMMAND_NAME = "UTIL_SET_CHANNELS"

    def test_set_chanels(self):
        self.add_word("Channels", "0,1", 0x00000003)
        self.run_test()


class TestUtilSetSecLevel(BaseUtilSReq):
    COMMAND = 0x04
    COMMAND_NAME = "UTIL_SET_SECLEVEL"

    def test_set_security_level(self):
        self.add_byte("SecurityLevel", "0x01")
        self.run_test()


class TestUtilSetPreCfgKey(BaseUtilSReq):
    COMMAND = 0x05
    COMMAND_NAME = "UTIL_SET_PRECFGKEY"

    def test_set_preconfigured_key(self):
        self.add_ieee("PreCfgKey", (0x10, 0x11, 0x12, 0x13,
                                    0x14, 0x15, 0x16, 0x17,
                                    0x18, 0x19, 0x1a, 0x1b,
                                    0x1c, 0x1d, 0x1e, 0x1f))
        self.run_test()


class TestUtilCallbackSubCmd(BaseUtilSReq):
    COMMAND = 0x06
    COMMAND_NAME = "UTIL_CALLBACK_SUB_CMD"

    def test_callback_subscribe(self):
        self.add_hword("SubsystemId", "MT_DEBUG", 0x0800)
        self.add_byte("Action", "Enable", 1)
        self.run_test()

    def test_callback_unsubscribe(self):
        self.add_hword("SubsystemId", "ALL_SUBSYSTEMS", 0xffff)
        self.add_byte("Action", "Disable", 0)
        self.run_test()


class TestUtilKeyEvent(BaseUtilSReq):
    COMMAND = 0x07
    COMMAND_NAME = "UTIL_KEY_EVENT"

    def test_key_event(self):
        self.add_byte("Keys", "44 (Key 3, Key 7)", 0x44)
        self.add_byte("Shift", "No shift", 0)
        self.run_test()

    def test_no_key_event(self):
        self.add_byte("Keys", "00 ()", 0x00)
        self.add_byte("Shift", "Shift", 1)
        self.run_test()


class TestUtilLedControl(BaseUtilSReq):
    COMMAND = 0x0a
    COMMAND_NAME = "UTIL_LED_CONTROL"

    def test_led_on(self):
        self.add_byte("LedId", "0x01")
        self.add_byte("Mode", "ON", 1)
        self.run_test()

    def test_led_off(self):
        self.add_byte("LedId", "0x02")
        self.add_byte("Mode", "OFF", 0)
        self.run_test()


class TestUtilLoopback(BaseUtilSReq):
    COMMAND = 0x10
    COMMAND_NAME = "UTIL_LOOPBACK"

    def test_loopback(self):
        self.add_bytes("Data", (0xfe, 0xec, 0xda, 0xc8))
        self.run_test()


class TestUtilDataReq(BaseUtilSReq):
    COMMAND = 0x11
    COMMAND_NAME = "UTIL_DATA_REQ"

    def test_data_req(self):
        self.add_byte("SecurityUse", "0x00")
        self.run_test()

class TestUtilSrcMatchAddEntry(BaseUtilSReq):
    COMMAND = 0x21
    COMMAND_NAME = "UTIL_SRC_MATCH_ADD_ENTRY"

    def test_add_match_entry(self):
        self.add_byte("AddressMode", "16-bit", 2)
        self.add_hword("Address", "0622", 0x0622)
        self.add_padding(6)
        self.add_hword("PanId", "af17", 0xaf17)
        self.run_test()


class TestUtilSrcMatchDelEntry(BaseUtilSReq):
    COMMAND = 0x22
    COMMAND_NAME = "UTIL_SRC_MATCH_DEL_ENTRY"

    def test_delete_match_entry(self):
        self.add_byte("AddressMode", "64-bit", 3)
        self.add_ieee("Address", (0x20, 0x21, 0x22, 0x23,
                                  0x24, 0x25, 0x26, 0x27))
        self.add_hword("PanId", "0000", 0)
        self.run_test()


class TestUtilSrcMatchCheckSrcAddr(BaseUtilSReq):
    COMMAND = 0x23
    COMMAND_NAME = "UTIL_SRC_MATCH_CHECK_SRC_ADDR"

    def test_check_addr(self):
        self.add_byte("AddressMode", "16-bit", 2)
        self.add_hword("Address", "8331", 0x8331)
        self.add_padding(6)
        self.add_hword("PanId", "f291", 0xf291)
        self.run_test()


class TestUtilSrcMatchAckAllPending(BaseUtilSReq):
    COMMAND = 0x24
    COMMAND_NAME = "UTIL_SRC_MATCH_ACK_ALL_PENDING"

    def test_ack_pending(self):
        self.add_byte("Option", "0x01")
        self.run_test()


class TestUtilAddrMgrExtAddrLookup(BaseUtilSReq):
    COMMAND = 0x40
    COMMAND_NAME = "UTIL_ADDRMGR_EXT_ADDR_LOOKUP"

    def test_addr_lookup(self):
        self.add_ieee("ExtAddr", (0x31, 0x32, 0x33, 0x34,
                                  0x35, 0x36, 0x37, 0x38))
        self.run_test()


class TestUtilAddrMgrNwkAddrLookup(BaseUtilSReq):
    COMMAND = 0x41
    COMMAND_NAME = "UTIL_ADDRMGR_NWK_ADDR_LOOKUP"

    def test_addr_lookup(self):
        self.add_hword("NwkAddr", "478a", 0x478a)
        self.run_test()


class TestUtilApsmeLinkKeyDataGet(BaseUtilSReq):
    COMMAND = 0x44
    COMMAND_NAME = "UTIL_APSME_LINK_KEY_DATA_GET"

    def test_get_key_data(self):
        self.add_ieee("ExtAddr", (0x15, 0x16, 0x17, 0x18,
                                  0x19, 0x1a, 0x1b, 0x1c))
        self.run_test()


class TestUtilApsmeLinkKeyNvIdGet(BaseUtilSReq):
    COMMAND = 0x45
    COMMAND_NAME = "UTIL_APSME_LINK_KEY_NV_ID_GET"

    def test_get_key_id(self):
        self.add_ieee("ExtAddr", (0x16, 0x17, 0x18, 0x19,
                                  0x10, 0x11, 0x12, 0x13))
        self.run_test()


class TestUtilApsmeRequestKeyCmd(BaseUtilSReq):
    COMMAND = 0x4b
    COMMAND_NAME = "UTIL_APSME_REQUEST_KEY_CMD"

    def test_request_key(self):
        self.add_hword("PartnerAddr", "8491", 0x8491)
        self.run_test()


class TestUtilAssocCount(BaseUtilSReq):
    COMMAND = 0x48
    COMMAND_NAME = "UTIL_ASSOC_COUNT"

    def test_assoc_count(self):
        self.add_byte("StartRelation", "Parent", 0)
        self.add_byte("EndRelation", "Neighbour", 5)
        self.run_test()


class TestUtilAssocFindDevice(BaseUtilSReq):
    COMMAND = 0x49
    COMMAND_NAME = "UTIL_ASSOC_FIND_DEVICE"

    def test_find_device(self):
        self.add_byte("Number", "0x02")
        self.run_test()


class TestUtilAssocGetWithAddress(BaseUtilSReq):
    COMMAND = 0x4a
    COMMAND_NAME = "UTIL_ASSOC_GET_WITH_ADDRESS"

    def test_find_device(self):
        self.add_ieee("ExtAddr", (0x00, 0x00, 0x00, 0x00,
                                  0x00, 0x00, 0x00, 0x00))
        self.add_hword("NwkAddr", "4829", 0x4829)
        self.run_test()


class TestUtilBindAddEntry(BaseUtilSReq):
    COMMAND = 0x4d
    COMMAND_NAME = "UTIL_BIND_ADD_ENTRY"

    def test_add_bind(self):
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddr", "3478", 0x3478)
        self.add_padding(6)
        self.add_byte("DstEndpoint", "0x01")
        self.add_byte("NumClusterIds", "3")
        self.add_list("ClusterIds",
                      "4839, 7650, a8d0",
                      (0x4839, 0x7650, 0xa8d0))
        self.run_test()


class TestUtilZclKeyEstInitEst(BaseUtilSReq):
    COMMAND = 0x80
    COMMAND_NAME = "UTIL_ZCL_KEY_EST_INIT_EST"

    def test_init_key(self):
        self.add_byte("TaskId", "0x33")
        self.add_byte("SeqNum", "0x13")
        self.add_byte("Endpoint", "0x0a")
        self.add_byte("AddressMode", "16-bit", 2)
        self.add_hword("Address", "88f3", 0x88f3)
        self.add_padding(6)
        self.run_test()


class TestUtilZclKeyEstSign(BaseUtilSReq):
    COMMAND = 0x81
    COMMAND_NAME = "UTIL_ZCL_KEY_EST_SIGN"

    def test_sign_key(self):
        self.add_byte("InputLen", "5")
        self.add_bytes("Input", (0x01, 0x02, 0x03, 0x04, 0x05))
        self.run_test()


class TestUtilGetDeviceInfo(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x00
    COMMAND_NAME = "UTIL_GET_DEVICE_INFO"

class TestUtilGetNvInfo(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x01
    COMMAND_NAME = "UTIL_GET_NV_INFO"

class TestUtilTimeAlive(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x09
    COMMAND_NAME = "UTIL_TIME_ALIVE"

class TestUtilSrcMatchEnable(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x20
    COMMAND_NAME = "UTIL_SRC_MATCH_ENABLE"

class TestUtilsSrcMatchCheckAllPending(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x25
    COMMAND_NAME = "UTIL_SRC_MATCH_CHECK_ALL_PENDING"

class TestUtilSrngGen(BaseNoParams, BaseUtilSReq):
    COMMAND = 0x4c
    COMMAND_NAME = "UTIL_SRNG_GEN"


if __name__ == "__main__":
    unittest.main()
