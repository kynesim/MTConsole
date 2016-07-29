#! /usr/bin/env python3

# test_util_srsp.py
#
# Unit tests for MT UTILS command response parsing
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


class BaseUtilSRsp(base_test.BaseTest):
    SUBSYSTEM = "UTIL"
    TYPE = "SRSP"


class BaseStatus:
    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_bad(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()


class TestUtilGetDeviceInfo(BaseUtilSRsp):
    COMMAND = 0x00
    COMMAND_NAME = "UTIL_GET_DEVICE_INFO"

    def test_get_info(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("IEEEAddr", (0xee, 0x01, 0x02, 0x34,
                                   0xff, 0x05, 0x06, 0x67))
        self.add_hword("ShortAddr", "0158", 0x0158)
        self.add_byte("DeviceType", "02 (Router)", 0x02)
        self.add_byte("DeviceState", "Joining", 0x03)
        self.add_byte("NumAssocDevices", "2")
        self.add_list("AssocDevicesList",
                      "0123, 4567",
                      (0x0123, 0x4567))
        self.run_test()


class TestUtilGetNvInfo(BaseUtilSRsp):
    COMMAND = 0x01
    COMMAND_NAME = "UTIL_GET_NV_INFO"

    def test_get_info(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("IEEEAddr", (0x12, 0x34, 0x56, 0x78,
                                   0x9a, 0xbc, 0xde, 0xf0))
        self.add_word("ScanChannels", "5,7,12", 0x000010a0)
        self.add_hword("PanId", "48ad", 0x48ad)
        self.add_byte("SecurityLevel", "0x01")
        self.add_ieee("PreCfgKey", (0x00, 0x01, 0x02, 0x03,
                                    0x04, 0x05, 0x06, 0x07,
                                    0x08, 0x09, 0x0a, 0x0b,
                                    0x0c, 0x0d, 0x0e, 0x0f))
        self.run_test()


class TestUtilTimeAlive(BaseUtilSRsp):
    COMMAND = 0x09
    COMMAND_NAME = "UTIL_TIME_ALIVE"

    def test_get_uptime(self):
        self.add_word("Seconds", "00000044", 68)
        self.run_test()


class TestUtilLoopback(BaseUtilSRsp):
    COMMAND = 0x10
    COMMAND_NAME = "UTIL_LOOPBACK"

    def test_loopback(self):
        self.add_bytes("Data", (0xfe, 0xec, 0xda, 0xc8))
        self.run_test()


class TestUtilSrcMatchCheckAllPending(BaseUtilSRsp):
    COMMAND = 0x25
    COMMAND_NAME = "UTIL_SRC_MATCH_CHECK_ALL_PENDING"

    def test_check_pending(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Value", "0x00")
        self.run_test()


class TestUtilAddrMgrExtAddrLookup(BaseUtilSRsp):
    COMMAND = 0x40
    COMMAND_NAME = "UTIL_ADDRMGR_EXT_ADDR_LOOKUP"

    def test_addr_lookup(self):
        self.add_hword("NwkAddr", "4567", 0x4567)
        self.run_test()


class TestUtilAddrMgrNwkAddrLookup(BaseUtilSRsp):
    COMMAND = 0x41
    COMMAND_NAME = "UTIL_ADDRMGR_NWK_ADDR_LOOKUP"

    def test_addr_lookup(self):
        self.add_ieee("ExtAddr", (0x2a, 0x2b, 0x2c, 0x2d,
                                  0x2e, 0x2f, 0x30, 0x31))
        self.run_test()


class TestUtilApsmeLinkKeyDataGet(BaseUtilSRsp):
    COMMAND = 0x44
    COMMAND_NAME = "UTIL_APSME_LINK_KEY_DATA_GET"

    def test_get_key_data(self):
        self.add_byte("Status", "Success", 0)
        self.add_ieee("SecKey", (0x1f, 0x20, 0x21, 0x22,
                                 0x23, 0x24, 0x25, 0x26,
                                 0x27, 0x28, 0x29, 0x30,
                                 0x31, 0x32, 0x33, 0x34))
        self.add_word("TxFrmCntr", "00000014", 0x14)
        self.add_word("RxFrmCntr", "00000032", 0x32)
        self.run_test()


class TestUtilApsmeLinkKeyNvIdGet(BaseUtilSRsp):
    COMMAND = 0x45
    COMMAND_NAME = "UTIL_APSME_LINK_KEY_NV_ID_GET"

    def test_get_key_id(self):
        self.add_byte("Status", "Success", 0)
        self.add_hword("LinkKeyNvId", "0002", 0x0002)
        self.run_test()


class TestUtilAssocCount(BaseUtilSRsp):
    COMMAND = 0x48
    COMMAND_NAME = "UTIL_ASSOC_COUNT"

    def test_assoc_count(self):
        self.add_hword("Count", "0002", 2)
        self.run_test()


class TestUtilAssocFindDevice(BaseUtilSRsp):
    COMMAND = 0x49
    COMMAND_NAME = "UTIL_ASSOC_FIND_DEVICE"

    def test_find_device(self):
        self.add_bytes("Device", (0x01, 0x02, 0x03, 0x04,
                                  0x05, 0x06, 0x07, 0x08,
                                  0x09, 0x10, 0x11, 0x12,
                                  0x13, 0x14, 0x15, 0x16,
                                  0x17, 0x18),
                       leading_0x=True)
        self.run_test()


class TestUtilAssocGetWithAddress(BaseUtilSRsp):
    COMMAND = 0x4a
    COMMAND_NAME = "UTIL_ASSOC_GET_WITH_ADDRESS"

    def test_find_device(self):
        self.add_bytes("Device", (0x71, 0x72, 0x73, 0x74,
                                  0x75, 0x76, 0x77, 0x78,
                                  0x79, 0x60, 0x61, 0x62,
                                  0x63, 0x64, 0x65, 0x66,
                                  0x67, 0x68),
                       leading_0x=True)
        self.run_test()


class TestUtilBindAddEntry(BaseUtilSRsp):
    COMMAND = 0x4d
    COMMAND_NAME = "UTIL_BIND_ADD_ENTRY"

    def test_add_bind(self):
        self.add_bytes("BindEntry", (0xa1, 0xa2, 0xa3, 0xa4,
                                     0xa5, 0xa6, 0xa7, 0xa8,
                                     0xa9, 0xaa, 0xab, 0xac,
                                     0xad, 0xae),
                       leading_0x=True)
        self.run_test()


class TestUtilZclKeyEstSign(BaseUtilSRsp):
    COMMAND = 0x81
    COMMAND_NAME = "UTIL_ZCL_KEY_EST_SIGN"

    def test_sign_key(self):
        self.add_byte("Status", "Success", 0)
        self.add_bytes("Key", (0x17,)*42, leading_0x=True)
        self.run_test()


class TestUtilSrngGen(BaseUtilSRsp):
    COMMAND = 0x4c
    COMMAND_NAME = "UTIL_SRNG_GEN"

    def test_srng(self):
        self.add_bytes("SecureRandomNumber", range(0x64), leading_0x=True)
        self.run_test()


class TestUtilSetPanId(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x02
    COMMAND_NAME = "UTIL_SET_PANID"

class TestUtilSetChannels(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x03
    COMMAND_NAME = "UTIL_SET_CHANNELS"

class TestUtilSetSecLevel(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x04
    COMMAND_NAME = "UTIL_SET_SECLEVEL"

class TestUtilSetPreCfgKey(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x05
    COMMAND_NAME = "UTIL_SET_PRECFGKEY"

class TestUtilCallbackSubCmd(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x06
    COMMAND_NAME = "UTIL_CALLBACK_SUB_CMD"

class TestUtilKeyEvent(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x07
    COMMAND_NAME = "UTIL_KEY_EVENT"

class TestLedControl(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x0a
    COMMAND_NAME = "UTIL_LED_CONTROL"

class TestUtilDataReq(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x11
    COMMAND_NAME = "UTIL_DATA_REQ"

class TestUtilSrcMatchEnable(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x20
    COMMAND_NAME = "UTIL_SRC_MATCH_ENABLE"

class TestUtilsSrcMatchAddEntry(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x21
    COMMAND_NAME = "UTIL_SRC_MATCH_ADD_ENTRY"

class TestUtilsSrcMatchDelEntry(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x22
    COMMAND_NAME = "UTIL_SRC_MATCH_DEL_ENTRY"

class TestUtilsSrcMatchCheckSrcAddr(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x23
    COMMAND_NAME = "UTIL_SRC_MATCH_CHECK_SRC_ADDR"

class TestUtilsSrcMatchAckAllPending(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x24
    COMMAND_NAME = "UTIL_SRC_MATCH_ACK_ALL_PENDING"

class TestUtilApsmeRequestKeyCmd(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x4b
    COMMAND_NAME = "UTIL_APSME_REQUEST_KEY_CMD"

class TestUtilZclKeyEstInitEst(BaseStatus, BaseUtilSRsp):
    COMMAND = 0x80
    COMMAND_NAME = "UTIL_ZCL_KEY_EST_INIT_EST"


if __name__ == "__main__":
    unittest.main()
