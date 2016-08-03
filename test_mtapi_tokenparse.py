#! /usr/bin/env python3

# test_mtapi_tokenparse.py
#
# Unit tests for token-parsing routines in the MTAPI Parser classes
#
# The tests in this file stress the field parsing functions so that
# command parsers don't need such detailed testing.
#
# Author: Rhodri James (rhodri@kynesim.co.uk)
# Date: 3 August 2016
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


import unittest
from test import support
import mtapi


class FieldTest:
    "Mixin class for testing a field"
    def field_test_ok(self, field, token, expected_result):
        buf = bytearray()
        self.assertTrue(field.parse_token(token, buf))
        self.assertEqual(buf, expected_result)


class TestParseField(FieldTest, unittest.TestCase):
    def test_basic_numeric_field(self):
        field = mtapi.ParseField("Test", 2)
        self.field_test_ok(field, "1", b'\x01\x00')
        self.field_test_ok(field, "0x1ff", b'\xff\x01')
        self.field_test_ok(field, "0o13", b'\x0b\x00')
        self.field_test_ok(field, "0b1000111", b'\x47\x00')
        self.field_test_ok(field, "0x12345", b'\x45\x23')

        buf = bytearray()
        self.assertFalse(field.parse_token("NotANumber", buf))

    def test_field_widths(self):
        field = mtapi.ParseField("Test1", 1)
        self.field_test_ok(field, "2", b'\x02')

        field = mtapi.ParseField("Test2", 2)
        self.field_test_ok(field, "0x123", b'\x23\x01')

        field = mtapi.ParseField("Test3", 3)
        self.field_test_ok(field, "0xfedcba", b'\xba\xdc\xfe')

        field = mtapi.ParseField("Test4", 4)
        self.field_test_ok(field, "0x01020304", b'\x04\x03\x02\x01')


class DictTest(FieldTest, unittest.TestCase):
    def dictionary_test(self, parser, ok_params, fail_params, width=1):
        field = mtapi.ParseField("Test", width, parser=parser)
        for token, result in ok_params.items():
            self.field_test_ok(field, token, result)

        buf = bytearray()
        for token in fail_params:
            self.assertFalse(field.parse_token(token, buf))


class TestParseDict(DictTest):
    def test_dictionary(self):
        dictionary = { 0x01: "One", 0x02: "Two" }
        default = "Bad(%d)"
        parser = mtapi.FieldParseDict(dictionary, default)
        self.dictionary_test(parser,
                             { "One": b'\x01',
                               "T": b'\x02',
                               "3": b'\x03' },
                             ["Bad(3)", "Wombat"])


class TestParseSpecificDicts(DictTest):
    def test_status(self):
        self.dictionary_test(mtapi.field_parse_status,
                             { "Success": b'\x00',
                               "Failed": b'\x01' },
                             ["Failure(0xff)"])

    def test_latency(self):
        self.dictionary_test(mtapi.field_parse_latency,
                             { "No latency": b'\x00',
                               "Fast beacons": b'\x01',
                               "Slow beacons": b'\x02' },
                             ["Invalid(0x14)"])

    def test_address_mode(self):
        self.dictionary_test(mtapi.field_parse_address_mode,
                             { "Address not present": b'\x00',
                               "Group": b'\x01',
                               "16-bit": b'\x02',
                               "64-bit": b'\x03',
                               "Broadcast": b'\xff' },
                             ["Invalid(0x04)", "NaN"])

    def test_assoc_status(self):
        self.dictionary_test(mtapi.field_parse_assoc_status,
                             { "Success": b'\x00',
                               "PAN at capacity": b'\x01',
                               "PAN access denied": b'\x02' },
                             ["Unknown(0x14)"])

    def test_disassoc(self):
        self.dictionary_test(mtapi.field_parse_disassoc_reason,
                             { "Reserved": b'\x00',
                               "Coord wishes device to leave": b'\x01',
                               "Device wishes to leave": b'\x02' },
                             ["Unknown(0x03)"])

    def test_mac_attribute(self):
        self.dictionary_test(mtapi.field_parse_mac_attr,
                             { "ZMAC_ACK_WAIT_DURATION": b'\x40',
                               "ZMAC_ASSOCIATION_PERMIT": b'\x41',
                               "ZMAC_AUTO_REQUEST": b'\x42',
                               "ZMAC_BATT_LIFE_EXT": b'\x43',
                               "ZMAC_BATT_LEFT_EXT_PERIODS": b'\x44',
                               "ZMAC_BEACON_MSDU": b'\x45',
                               "ZMAC_BEACON_MSDU_LENGTH": b'\x46',
                               "ZMAC_BEACON_ORDER": b'\x47',
                               "ZMAC_BEACON_TX_TIME": b'\x48',
                               "ZMAC_BSN": b'\x49',
                               "ZMAC_COORD_EXTENDED_ADDRESS": b'\x4a',
                               "ZMAC_COORD_SHORT_ADDRESS": b'\x4b',
                               "ZMAC_DSN": b'\x4c',
                               "ZMAC_GTS_PERMIT": b'\x4d',
                               "ZMAC_MAX_CSMA_BACKOFFS": b'\x4e',
                               "ZMAC_MIN_BE": b'\x4f',
                               "ZMAC_PANID": b'\x50',
                               "ZMAC_PROMISCUOUS_MODE": b'\x51',
                               "ZMAC_RX_ON_IDLE": b'\x52',
                               "ZMAC_SHORT_ADDRESS": b'\x53',
                               "ZMAC_SUPERFRAME_ORDER": b'\x54',
                               "ZMAC_TRANSACTION_PERSISTENCE_TIME": b'\x55',
                               "ZMAC_ASSOCIATED_PAN_COORD": b'\x56',
                               "ZMAC_MAX_BE": b'\x57',
                               "ZMAC_FRAME_TOTAL_WAIT_TIME": b'\x58',
                               "ZMAC_MAC_FRAME_RETRIES": b'\x59',
                               "ZMAC_RESPONSE_WAIT_TIME": b'\x5a',
                               "ZMAC_SYNC_SYMBOL_OFFSET": b'\x5b',
                               "ZMAC_TIMESTAMP_SUPPORTED": b'\x5c',
                               "ZMAC_SECURITY_ENABLED": b'\x5d',
                               "ZMAC_PHY_TRANSMIT_POWER": b'\xe0',
                               "ZMAC_LOGICAL_CHANNEL": b'\xe1',
                               "ZMAC_EXTENDED_ADDRESS": b'\xe2',
                               "ZMAC_ALT_BE": b'\xe3' },
                             [ "Unknown(0x00)", "Unknown(0xff)" ])

    def test_scan_type(self):
        self.dictionary_test(mtapi.field_parse_scan_type,
                             { "Energy Detect": b'\x00',
                               "Active": b'\x01',
                               "Passive": b'\x02',
                               "Orphan": b'\x03' },
                             ["Unknown(0x06)"])

    def test_reset_type(self):
        self.dictionary_test(mtapi.field_parse_reset_type,
                             { "Hardware": b'\x00',
                               "Software": b'\x01' },
                             ["Unknown(0xff)"])

    def test_reset_reason(self):
        self.dictionary_test(mtapi.field_parse_reset_reason,
                             { "Power-up": b'\x00',
                               "External": b'\x01',
                               "Watchdog": b'\x02' },
                             ["Unknown(0x30)"])

    def test_adc_channel(self):
        self.dictionary_test(mtapi.field_parse_adc_channel,
                             { "AIN0": b'\x00',
                               "AIN1": b'\x01',
                               "AIN2": b'\x02',
                               "AIN3": b'\x03',
                               "AIN4": b'\x04',
                               "AIN5": b'\x05',
                               "AIN6": b'\x06',
                               "AIN7": b'\x07',
                               "Temperature Sensor": b'\x0e',
                               "voltage reading": b'\x0f' },
                             ["Invalid(0x08)", "Lalalala"])

    def test_adc_resolution(self):
        self.dictionary_test(mtapi.field_parse_adc_resolution,
                             { "8-bit": b'\x00',
                               "10-bit": b'\x01',
                               "12-bit": b'\x02',
                               "14-bit": b'\x03' },
                             ["Invalid(0x04)"])

    def test_gpio_operation(self):
        self.dictionary_test(mtapi.field_parse_gpio_operation,
                             { "Set direction": b'\x00',
                               "Set input mode": b'\x01',
                               "Set": b'\x02',
                               "Clear": b'\x03',
                               "Toggle": b'\x04',
                               "Read": b'\x05' },
                             ["Invalid(0x15)"])

    def test_device_state(self):
        self.dictionary_test(mtapi.field_parse_device_state,
                             { "Unstarted": b'\x00',
                               "Not connected": b'\x01',
                               "Nothing to join": b'\x02',
                               "Joining": b'\x03',
                               "Rejoining": b'\x04',
                               "Unauthenticated": b'\x05',
                               "Authenticated": b'\x06',
                               "Routing": b'\x07',
                               "Starting as Coordinator": b'\x08',
                               "Started as Coordinator": b'\x09',
                               "Lost Parent Info": b'\x0a' },
                             ["Unknown(0x83)", "Not"])

    def test_subsystem_id(self):
        self.dictionary_test(mtapi.field_parse_subsystem_id,
                             { "MT_SYS":   b'\x00\x01',
                               "MT_MAC":   b'\x00\x02',
                               "MT_NWK":   b'\x00\x03',
                               "MT_AF":    b'\x00\x04',
                               "MT_ZDO":   b'\x00\x05',
                               "MT_SAPI":  b'\x00\x06',
                               "MT_UTIL":  b'\x00\x07',
                               "MT_DEBUG": b'\x00\x08',
                               "MT_APP":   b'\x00\x09',
                               "ALL_SUBSYSTEM": b'\xff\xff' },
                             ["Reserved(0x0000)"],
                             width=2)

    def test_enable(self):
        self.dictionary_test(mtapi.field_parse_enable,
                             { "Disable": b'\x00',
                               "Enable":  b'\x01' },
                             ["Unexpected(0x33)"])

    def test_shift(self):
        self.dictionary_test(mtapi.field_parse_shift,
                             { "No shift": b'\x00',
                               "Shift":    b'\x01' },
                             ["You what?"])

    def test_onoff(self):
        self.dictionary_test(mtapi.field_parse_onoff,
                             { "OFF": b'\x00',
                               "ON":  b'\x01' },
                             ["None of the above"])

    def test_relation(self):
        self.dictionary_test(mtapi.field_parse_relation,
                             { "Parent":           b'\x00',
                               "Child RFD":        b'\x01',
                               "Child RFD RxIdle": b'\x02',
                               "Child FFD":        b'\x03',
                               "Child FFD RxIdle": b'\x04',
                               "Neighbour":        b'\x05',
                               "Other":            b'\x06' },
                             ["Invalid(0x07)"])

    def test_startup_status(self):
        self.dictionary_test(mtapi.field_parse_startup_status,
                             { "Restored Network State": b'\x00',
                               "New Network State":      b'\x01',
                               "Leave and Not Started":  b'\x02' },
                             ["Unexpected(0x97)"])

    def test_routing_status(self):
        self.dictionary_test(mtapi.field_parse_routing_status,
                             { "Active":             b'\x00',
                               "Discovery Underway": b'\x01',
                               "Discovery Failed":   b'\x02',
                               "Inactive":           b'\x03' },
                             ["Invalid(0x33)", "Discovery"])

    def test_join_duration(self):
        self.dictionary_test(mtapi.field_parse_join_duration,
                             { "Disabled": b'\x00',
                               "Enabled":  b'\xff' },
                             ["Anything else"])


if __name__ == "__main__":
    unittest.main()
