#! /usr/bin/env python3

# Unit tests for MT AF SREQ command parsing

import base_test
import unittest


class BaseAfSReq(base_test.BaseTest):
    SUBSYSTEM = "AF"
    TYPE = "SREQ"


class TestAfRegister(BaseAfSReq):
    COMMAND = 0x00
    COMMAND_NAME = "AF_REGISTER"

    def test_in_and_out_clusters(self):
        self.add_byte("Endpoint", "0x01")
        self.add_hword("AppProfId", "0203", 0x0203)
        self.add_hword("AppDeviceId", "0405", 0x0405)
        self.add_byte("AppDevVer", "0x11")
        self.add_byte("LatencyReq", "No latency", 0x00)
        self.add_byte("AppNumInClusters", "2")
        self.add_list("AppInClusterList",
                      "0600, 0601",
                      [0x0600, 0x0601])
        self.add_byte("AppNumOutClusters", "5")
        self.add_list("AppOutClusterList",
                      "0701, 0702, 0703, 0704, 0705",
                      [0x0701, 0x0702, 0x0703, 0x0704, 0x0705])
        self.sock.chop_max = 3
        self.run_test()

    def test_out_clusters(self):
        self.add_byte("Endpoint", "0x02")
        self.add_hword("AppProfId", "3412", 0x3412)
        self.add_hword("AppDeviceId", "7856", 0x7856)
        self.add_byte("AppDevVer", "0x22")
        self.add_byte("LatencyReq", "Fast beacons", 0x01)
        self.add_byte("AppNumInClusters", "0")
        self.add_list("AppInClusterList", "", [])
        self.add_byte("AppNumOutClusters", "3")
        self.add_list("AppOutClusterList",
                      "0001, 0002, 0003",
                      [0x0001, 0x0002, 0x0003])
        self.run_test()

    def test_in_clusters(self):
        self.add_byte("Endpoint", "0x03")
        self.add_hword("AppProfId", "9876", 0x9876)
        self.add_hword("AppDeviceId", "5432", 0x5432)
        self.add_byte("AppDevVer", "0x01")
        self.add_byte("LatencyReq", "Slow beacons", 0x02)
        self.add_byte("AppNumInClusters", "1")
        self.add_list("AppInClusterList", "0102", [0x0102])
        self.add_byte("AppNumOutClusters", "0")
        self.add_list("AppOutClusterList", "", [])
        self.run_test()

    def test_no_clusters(self):
        self.add_byte("Endpoint", "0x04")
        self.add_hword("AppProfId", "0001", 0x0001)
        self.add_hword("AppDeviceId", "0002", 0x0002)
        self.add_byte("AppDevVer", "0xff")
        self.add_byte("LatencyReq", "Invalid(0x03)", 0x03)
        self.add_byte("AppNumInClusters", "0")
        self.add_list("AppInClusterList", "", [])
        self.add_byte("AppNumOutClusters", "0")
        self.add_list("AppOutClusterList", "", [])
        self.sock.chop_max = 7
        self.run_test()

    def test_leftover_input(self):
        self.add_byte("Endpoint", "0x01")
        self.add_hword("AppProfId", "0203", 0x0203)
        self.add_hword("AppDeviceId", "0405", 0x0405)
        self.add_byte("AppDevVer", "0x06")
        self.add_byte("LatencyReq", "Invalid(0x07)", 0x07)
        self.add_byte("AppNumInClusters", "0")
        self.add_list("AppInClusterList", "", [])
        self.add_byte("AppNumOutClusters", "0")
        self.add_list("AppOutClusterList", "", [])
        # Push extra bytes onto the end of the buffer
        self.sock.bytes += bytearray((0x08,))
        self.run_test(leftovers=True)

    def test_padded_input(self):
        self.add_byte("Endpoint", "0x01")
        self.add_hword("AppProfId", "0203", 0x0203)
        self.add_hword("AppDeviceId", "0405", 0x0405)
        self.add_byte("AppDevVer", "0x06")
        self.add_byte("LatencyReq", "Invalid(0x07)", 0x07)
        self.add_byte("AppNumInClusters", "0")
        self.add_list("AppInClusterList", "", [])
        self.add_byte("AppNumOutClusters", "0")
        self.add_list("AppOutClusterList", "", [])
        self.add_padding(1, 0x09)
        self.add_parse_error("Unparsed data in AF_REGISTER")
        self.run_test()

    def test_short_input(self):
        self.add_byte("Endpoint", "0x01")
        self.add_hword("AppProfId", "0203", 0x0203)
        self.add_hword("AppDeviceId", "0405", 0x0405)
        self.add_byte("AppDevVer", "0x06")
        self.add_byte("LatencyReq", "Invalid(0x07)", 0x07)
        self.add_byte("AppNumInClusters", "0")
        self.add_list("AppInClusterList", "", [])
        # Skip the final field
        self.add_parse_error("Field AppNumOutClusters is missing")
        self.run_test()

    def test_missing_byte(self):
        # Test the parser correctly notes the lack of a byte field
        # (also everything else, but the byte is what will be noted)
        self.add_parse_error("Field Endpoint missing")
        self.run_test()

    def test_missing_hword(self):
        self.add_byte("Endpoint", "0x01")
        self.add_parse_error("Field AppProfId missing")
        self.run_test()
        self.sock.reset()
        self.add_byte("AppProfId", "0x02") # Should be an hword
        self.run_test()

    def test_missing_list(self):
        self.add_byte("Endpoint", "0x01")
        self.add_hword("AppProfId", "0203", 0x0203)
        self.add_hword("AppDeviceId", "0405", 0x0405)
        self.add_byte("AppDevVer", "0x06")
        self.add_byte("LatencyReq", "Invalid(0x07)", 0x07)
        self.add_byte("AppNumInClusters", "1")
        self.add_parse_error("Field AppInClusterList missing or short")
        self.run_test()
        self.sock.reset()
        self.add_byte("AppInClusterList", "0001", 1)
        self.run_test()


class TestAfDataRequest(BaseAfSReq):
    COMMAND = 0x01
    COMMAND_NAME = "AF_DATA_REQUEST"

    def test_af_data_request(self):
        self.add_hword("DstAddr", "abcd", 0xabcd)
        self.add_byte("DstEndpoint", "0x0e")
        self.add_byte("SrcEndpoint", "0x0f")
        self.add_hword("ClusterId", "0223", 0x0223)
        self.add_byte("TransId", "0x10")
        self.add_byte("Options",
                      "20 (Discover Route)",
                      0x20)
        self.add_byte("Radius", "0x30")
        self.add_byte("Length", "33")
        self.add_bytes("Data", (0x81, 0x82, 0x83, 0x84,
                                0x85, 0x86, 0x87, 0x88,
                                0x89, 0x8a, 0x8b, 0x8c,
                                0x8d, 0x8e, 0x8f, 0x90,
                                0x81, 0x82, 0x83, 0x84,
                                0x85, 0x86, 0x87, 0x88,
                                0x89, 0x8a, 0x8b, 0x8c,
                                0x8d, 0x8e, 0x8f, 0x90, 0x91))
        self.run_test()

    def test_af_short_data_request(self):
        self.add_hword("DstAddr", "33cc", 0x33cc)
        self.add_byte("DstEndpoint", "0x10")
        self.add_byte("SrcEndpoint", "0x11")
        self.add_hword("ClusterId", "4556", 0x4556)
        self.add_byte("TransId", "0x31")
        self.add_byte("Options",
                      "32 (Wildcard Profile Id, APS ACK, Discover Route)",
                      0x32)
        self.add_byte("Radius", "0x33")
        self.add_byte("Length", "1")
        self.add_bytes("Data", (0xff,))
        self.run_test()

    def test_af_no_data_request(self):
        self.add_hword("DstAddr", "aa55", 0xaa55)
        self.add_byte("DstEndpoint", "0xe0")
        self.add_byte("SrcEndpoint", "0xe1")
        self.add_hword("ClusterId", "7889", 0x7889)
        self.add_byte("TransId", "0x45")
        self.add_byte("Options",
                      "56 (Wildcard Profile Id, (Reserved), "
                      "APS ACK, APS Security)",
                      0x56)
        self.add_byte("Radius", "0x67")
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()

    def test_af_mismatched_data_request(self):
        self.add_hword("DstAddr", "0102", 0x0102)
        self.add_byte("DstEndpoint", "0x03")
        self.add_byte("SrcEndpoint", "0x04")
        self.add_hword("ClusterId", "0506", 0x0506)
        self.add_byte("TransId", "0x07")
        self.add_byte("Options", "00 ()", 0)
        self.add_byte("Radius", "0x08")
        self.add_byte("Length", "9")
        # The shortened Data field doesn't get parsed, so
        # can't be added the usual way via add_bytes.
        self.add_padding(3, 0x0a)
        self.add_parse_error("Field Data missing or short")
        self.run_test()


class TestAfDataRequestExt(BaseAfSReq):
    COMMAND = 0x02
    COMMAND_NAME = "AF_DATA_REQUEST_EXT"

    def test_af_data_request_ext(self):
        self.add_byte("DstAddrMode", "64-bit", 3)
        self.add_ieee("DstAddr", (0x13, 0x24, 0x35, 0x46,
                                  0xfd, 0xec, 0xdb, 0xca))
        self.add_byte("DstEndpoint", "0x57")
        self.add_hword("DstPanId", "0000")
        self.add_byte("SrcEndpoint", "0x75")
        self.add_hword("ClusterId", "8668", 0x8668)
        self.add_byte("TransId", "0x79")
        self.add_byte("Options",
                      "97 ((Reserved), Wildcard Profile Id, (Reserved), "
                      "APS ACK, Skip Routing)",
                      0x97)
        self.add_byte("Radius", "0x8a")
        self.add_hword("Len", "19")
        self.add_bytes("Data", (0x10, 0x20, 0x30, 0x40,
                                0x50, 0x60, 0x70, 0x80,
                                0x90, 0xa0, 0xb0, 0xc0,
                                0xd0, 0xe0, 0xf0, 0x01,
                                0x11, 0x21, 0x31))
        self.run_test()

    def test_af_oversize_data_request_ext(self):
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddr", "0314", 0x0314)
        self.add_padding(6)
        self.add_byte("DstEndpoint", "0x25")
        self.add_hword("DstPanId", "3647", 0x3647)
        self.add_byte("SrcEndpoint", "0x58")
        self.add_hword("ClusterId", "697a", 0x697a)
        self.add_byte("TransId", "0x8b")
        self.add_byte("Options",
                      "9c ((Reserved), (Reserved), APS ACK, Skip Routing)",
                      0x9c)
        self.add_byte("Radius", "0xad")
        self.add_hword("Len", "291")
        self.add_text("Data", "Blank")
        self.run_test()

    def test_af_no_data_request_ext(self):
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddr", "f0e1", 0xf0e1)
        self.add_padding(6)
        self.add_byte("DstEndpoint", "0xd2")
        self.add_hword("DstPanId", "c3b4", 0xc3b4)
        self.add_byte("SrcEndpoint", "0xa5")
        self.add_hword("ClusterId", "9687", 0x9687)
        self.add_byte("TransId", "0x78")
        self.add_byte("Options",
                      "69 ((Reserved), (Reserved), Discover Route, "
                      "APS Security)",
                      0x69)
        self.add_byte("Radius", "0x5a")
        self.add_hword("Len", "0")
        self.add_bytes("Data", ())
        self.run_test()

    def test_af_missing_data_request_ext(self):
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddr", "0001", 0x0001)
        self.add_padding(6)
        self.add_byte("DstEndpoint", "0x02")
        self.add_hword("DstPanId", "0304", 0x0304)
        self.add_byte("SrcEndpoint", "0x05")
        self.add_hword("ClusterId", "0607", 0x0607)
        self.add_byte("TransId", "0x08")
        self.add_byte("Options", "00 ()", 0)
        self.add_byte("Radius", "0x09")
        self.add_parse_error("Field Len is missing or short")
        self.run_test()
        self.sock.reset()
        self.add_byte("Len", "10")
        self.run_test()

    def test_af_mismatched_data_request_ext(self):
        self.add_byte("DstAddrMode", "16-bit", 2)
        self.add_hword("DstAddr", "0001", 0x0001)
        self.add_padding(6)
        self.add_byte("DstEndpoint", "0x02")
        self.add_hword("DstPanId", "0304", 0x0304)
        self.add_byte("SrcEndpoint", "0x05")
        self.add_hword("ClusterId", "0607", 0x0607)
        self.add_byte("TransId", "0x08")
        self.add_byte("Options", "00 ()", 0)
        self.add_byte("Radius", "0x09")
        self.add_hword("Len", "10")
        # The shortened Data field doesn't get parsed, so
        # can't be added the usual way via add_bytes.
        self.add_padding(3, 0x0b)
        self.add_parse_error("Field Data missing or short")
        self.run_test()


class TestAfDataRequestSrcRtg(BaseAfSReq):
    COMMAND = 0x03
    COMMAND_NAME = "AF_DATA_REQUEST_SRC_RTG"

    def test_af_data_request_src_rtg(self):
        self.add_hword("DstAddr", "0018", 0x0018)
        self.add_byte("DstEndpoint", "0x24")
        self.add_byte("SrcEndpoint", "0x3c")
        self.add_hword("ClusterId", "425a", 0x425a)
        self.add_byte("TransId", "0x66")
        self.add_byte("Options",
                      "7e (Wildcard Profile Id, (Reserved), "
                      "(Reserved), APS ACK, Discover Route, "
                      "APS Security)",
                      0x7e)
        self.add_byte("Radius", "0x81")
        self.add_byte("RelayCount", "2")
        self.add_list("RelayList", "99a5, bdc3", [0x99a5, 0xbdc3])
        self.add_byte("Length", "3")
        self.add_bytes("Data", (0xdb, 0xe7, 0xff))
        self.run_test()

    def test_no_relays(self):
        self.add_hword("DstAddr", "0000")
        self.add_byte("DstEndpoint", "0x00")
        self.add_byte("SrcEndpoint", "0x00")
        self.add_hword("ClusterId", "0000")
        self.add_byte("TransId", "0x00")
        self.add_byte("Options", "00 ()", 0x00)
        self.add_byte("Radius", "0x01")
        self.add_byte("RelayCount", "0")
        self.add_list("RelayList", "", [])
        self.add_byte("Length", "15")
        self.add_bytes("Data", (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        self.run_test()

    def test_no_clusters(self):
        self.add_hword("DstAddr", "3435", 0x3435)
        self.add_byte("DstEndpoint", "0x36")
        self.add_byte("SrcEndpoint", "0x37")
        self.add_hword("ClusterId", "3839", 0x3839)
        self.add_byte("TransId", "0x40")
        self.add_byte("Options", "41 ((Reserved), APS Security)", 0x41)
        self.add_byte("Radius", "0x42")
        self.add_byte("RelayCount", "5")
        self.add_list("RelayList",
                      "4344, 4546, 4748, 4950, 5152",
                      [0x4344, 0x4546, 0x4748, 0x4950, 0x5152])
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()

    def test_no_relays_or_clusters(self):
        self.add_hword("DstAddr", "0102", 0x0102)
        self.add_byte("DstEndpoint", "0x04")
        self.add_byte("SrcEndpoint", "0x08")
        self.add_hword("ClusterId", "1020", 0x1020)
        self.add_byte("TransId", "0x40")
        self.add_byte("Options", "80 (Skip Routing)", 0x80)
        self.add_byte("Radius", "0x03")
        self.add_byte("RelayCount", "0")
        self.add_list("RelayList", "", [])
        self.add_byte("Length", "0")
        self.add_bytes("Data", ())
        self.run_test()


class TestAfInterPanCtl(BaseAfSReq):
    COMMAND = 0x10
    COMMAND_NAME = "AF_INTER_PAN_CTL"

    def test_inter_pan_clr(self):
        self.add_byte("Command", "InterPanClr", 0)
        self.run_test()

    def test_inter_pan_set(self):
        self.add_byte("Command", "InterPanSet", 1)
        self.add_byte("Channel", "11")
        self.run_test()

    def test_inter_pan_reg(self):
        self.add_byte("Command", "InterPanReg", 2)
        self.add_byte("Endpoint", "0x0a")
        self.run_test()

    def test_inter_pan_check(self):
        self.add_byte("Command", "InterPanChk", 3)
        self.add_hword("PanId", "8e71", 0x8e71)
        self.add_byte("Endpoint", "0x69")
        self.run_test()


class TestAfDataStore(BaseAfSReq):
    COMMAND = 0x11
    COMMAND_NAME = "AF_DATA_STORE"

    def test_missing_index(self):
        self.add_parse_error("Field Index missing")
        self.run_test()

    def test_data_store(self):
        self.add_hword("Index", "1234", 0x1234)
        self.add_byte("Length", "4")
        self.add_bytes("Data", (0x55, 0x66, 0x77, 0x88))
        self.run_test()


class TestAfDataRetrieve(BaseAfSReq):
    COMMAND = 0x12
    COMMAND_NAME = "AF_DATA_RETRIEVE"

    def test_data_retrieve(self):
        self.add_word("Timestamp", "00000013", 0x13)
        self.add_hword("Index", "2435", 0x2435)
        self.add_byte("Length", "0x09")
        self.run_test()


class TestAfApsfConfigSet(BaseAfSReq):
    COMMAND = 0x13
    COMMAND_NAME = "AF_APSF_CONFIG_SET"

    def test_apsf_config(self):
        self.add_byte("Endpoint", "0x01")
        self.add_byte("FrameDelay", "0x07")
        self.add_byte("WindowSize", "0x22")
        self.run_test()


if __name__ == "__main__":
    unittest.main()
