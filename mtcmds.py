#! /usr/bin/env python3

# mtcmds.py
#
# The command tables for the MTAPI protocol
#
# Author: Rhodri James (rhodri@kynesim.co.uk)
# Date: 20 July 2016
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


from mtapi import *


# Some common field parsers to reduce the proliferation of objects
PARSE_ENDPOINT = ParseField("Endpoint", 1)
PARSE_DST_EP = ParseField("DstEndpoint", 1)
PARSE_SRC_EP = ParseField("SrcEndpoint", 1)

PARSE_DST_ADDR = ParseField("DstAddr", 2, field_parse_hword)
PARSE_SRC_ADDR = ParseField("SrcAddr", 2, field_parse_hword)
PARSE_ASSOC_ADDR = ParseField("AssocShortAddress", 2,
                              field_parse_hword)
PARSE_DEV_ADDR = ParseField("DeviceAddr", 2, field_parse_hword)
PARSE_NWK_ADDR = ParseField("NwkAddr", 2, field_parse_hword)
PARSE_SHORT_ADDR = ParseField("ShortAddr", 2, field_parse_hword)
PARSE_INTEREST_ADDR = ParseField("NwkAddrOfInterest", 2,
                                 field_parse_hword)
PARSE_PARENT_ADDR = ParseField("ParentAddr", 2, field_parse_hword)

PARSE_ADDR_MODE = ParseField("AddrMode", 1, field_parse_address_mode)
PARSE_DST_MODE = ParseField("DstAddrMode", 1,
                            field_parse_address_mode)
PARSE_SRC_MODE = ParseField("SrcAddressMode", 1,
                            field_parse_address_mode)

PARSE_MODED_ADDR = ParseAddress("AddressMode", "Address")
PARSE_MODED_DST_ADDR = ParseAddress("DstAddrMode", "DstAddr")
PARSE_MODED_SRC_ADDR = ParseAddress("SrcAddrMode", "SrcAddr")
PARSE_MODED_COORD_ADDR = ParseAddress("CoordAddressMode",
                                      "CoordAddress")
PARSE_MODED_DEV_ADDR = ParseAddress("DeviceAddressMode",
                                    "DeviceAddress")

PARSE_EXT_ADDR = ParseField("ExtAddr", 8, field_parse_colon_sep)
PARSE_DEV_EXT_ADDR = ParseField("DeviceExtAddr", 8,
                                field_parse_colon_sep)
PARSE_SRC_EXT_ADDR = ParseField("SrcExtAddr", 8,
                                field_parse_colon_sep)
PARSE_DST_EXT_ADDR = ParseField("DstExtAddr", 8,
                                field_parse_colon_sep)
PARSE_IEEE_ADDR = ParseField("IEEEAddr", 8, field_parse_colon_sep)

PARSE_PAN_ID = ParseField("PanId", 2, field_parse_hword)
PARSE_DST_PAN_ID = ParseField("DstPanId", 2, field_parse_hword)
PARSE_SRC_PAN_ID = ParseField("SrcPanId", 2, field_parse_hword)
PARSE_COORD_PAN_ID = ParseField("CoordPanId", 2, field_parse_hword)
PARSE_DEV_PAN_ID = ParseField("DevicePanId", 2, field_parse_hword)
PARSE_EXT_PAN_ID = ParseField("ExtendedPanId", 8,
                              field_parse_colon_sep)

PARSE_STATUS = ParseField("Status", 1, field_parse_status)
PARSE_TRANS_ID = ParseField("TransId", 1)
PARSE_OPTIONS = ParseField("Options", 1, field_parse_options)
PARSE_RADIUS = ParseField("Radius", 1)
PARSE_WAS_BROADCAST = ParseField("WasBroadcast", 1)
PARSE_LINK_QUALITY = ParseField("LinkQuality", 1)
PARSE_SECURITY_USE = ParseField("SecurityUse", 1)
PARSE_LOGICAL_CHANNEL = ParseField("LogicalChannel", 1)
PARSE_CHANNEL_PAGE = ParseField("ChannelPage", 1)
PARSE_CAPABILITIES = ParseField("Capabilities", 1,
                                field_parse_capabilities)
PARSE_DISASSOC_REASON = ParseField("DisassociateReason", 1,
                                   field_parse_disassoc_reason)
PARSE_MAC_ATTRIBUTE = ParseField("Attribute", 1, field_parse_mac_attr)
PARSE_SCAN_TYPE = ParseField("ScanType", 1, field_parse_scan_type)
PARSE_SCAN_DURATION = ParseField("ScanDuration", 1)
PARSE_HANDLE = ParseField("Handle", 1)
PARSE_CONFIG_ID = ParseField("ConfigId", 1)
PARSE_PARAM = ParseField("Param", 1)
PARSE_NV_OFFSET = ParseField("Offset", 1)
PARSE_TIMER_ID = ParseField("Id", 1)
PARSE_TX_POWER = ParseField("TxPower", 1)
PARSE_VALUE_BYTE = ParseField("Value", 1)
PARSE_SECURITY_LEVEL = ParseField("SecurityLevel", 1)
PARSE_TASK_ID = ParseField("TaskId", 1)
PARSE_REQ_TYPE = ParseField("ReqType", 1)
PARSE_START_INDEX = ParseField("StartIndex", 1)
PARSE_SEQ_NUM = ParseField("SeqNum", 1)
PARSE_DEPTH = ParseField("Depth", 1)
PARSE_STACK_PROFILE = ParseField("StackProfile", 1)
PARSE_KEY_SEQ_NUM = ParseField("KeySeqNum", 1)
PARSE_LQI = ParseField("LQI", 1)

PARSE_CLUSTER_ID = ParseField("ClusterId", 2, field_parse_hword)
PARSE_GROUP_ID = ParseField("GroupId", 2, field_parse_hword)
PARSE_INDEX = ParseField("Index", 2, field_parse_hword)
PARSE_TIMESTAMP2 = ParseField("Timestamp2", 2, field_parse_hword)
PARSE_COMMAND_ID = ParseField("CommandId", 2, field_parse_hword)
PARSE_NV_ID = ParseField("Id", 2, field_parse_hword)
PARSE_NV_ITEM_LEN = ParseField("ItemLen", 2, field_parse_hword)
PARSE_RAM_ADDR = ParseField("Address", 2, field_parse_hword)
PARSE_VALUE_HWORD = ParseField("Value", 2, field_parse_hword)
PARSE_PROFILE_ID = ParseField("ProfileId", 2, field_parse_hword)
PARSE_DEVICE_ID = ParseField("DeviceId", 2, field_parse_hword)
PARSE_SERVER_MASK = ParseField("ServerMask", 2,
                               field_parse_server_mask)

PARSE_TIMESTAMP = ParseField("Timestamp", 4, field_parse_word)
PARSE_SCAN_CHANNELS = ParseField("ScanChannels", 4,
                                 field_parse_scan_channels)
PARSE_SYS_CLOCK = ParseField("SysClock", 4, field_parse_word)

PARSE_DATA = ParseVariable("Length", "Data")
PARSE_RELAY_LIST = ParseClusterList("RelayCount", "RelayList")
PARSE_KEY = ParseKey("KeySource", "SecurityLevel",
                     "KeyIdMode", "KeyIndex")
PARSE_TIME = ParseTime()
PARSE_ASSOCIATION_LIST = ParseClusterList("NumAssocDevices",
                                          "AssocDevicesList")
PARSE_PRECONFIGURED_KEY = ParseField("PreCfgKey", 16,
                                     field_parse_colon_sep)
PARSE_DEVICE_INFO = ParseField("Device", 18)
PARSE_IN_CLUSTERS = ParseClusterList("NumInClusters", "InClusterList")
PARSE_OUT_CLUSTERS = ParseClusterList("NumOutClusters",
                                      "OutClusterList")
PARSE_BIND_ADDR = ParseBindAddress("DstAddrMode",
                                   "DstAddress",
                                   "DstEndpoint")
PARSE_LINK_KEY = ParseField("LinkKeyData", 16)

PARSE_SYS_ID = ParseField("SysId", 1)
PARSE_ITEM_ID = ParseField("ItemId", 2, field_parse_hword)
PARSE_SUB_ID = ParseField("SubId", 2, field_parse_hword)
PARSE_OFFSET = ParseField("Offset", 2, field_parse_hword)

PARSE_TRANSPORT_REVISION = ParseField("TransportRev", 1)
PARSE_PRODUCT_ID = ParseField("ProductId", 1)
PARSE_MAJOR_RELEASE = ParseField("MajorRel", 1)
PARSE_MINOR_RELEASE = ParseField("MinorRel", 1)

MT_AF_SREQ_CMDS = {
    0x00: MTAPICmd("AF_REGISTER",
                   [ PARSE_ENDPOINT,
                     ParseField("AppProfId", 2, field_parse_hword),
                     ParseField("AppDeviceId", 2, field_parse_hword),
                     ParseField("AppDevVer", 1),
                     ParseField("LatencyReq", 1, field_parse_latency),
                     ParseClusterList("AppNumInClusters",
                                      "AppInClusterList"),
                     ParseClusterList("AppNumOutClusters",
                                      "AppOutClusterList")]),
    0x01: MTAPICmd("AF_DATA_REQUEST",
                   [ PARSE_DST_ADDR,
                     PARSE_DST_EP,
                     PARSE_SRC_EP,
                     PARSE_CLUSTER_ID,
                     PARSE_TRANS_ID,
                     PARSE_OPTIONS,
                     PARSE_RADIUS,
                     ParseVariable("Length", "Data", limit=128)]),
    0x02: MTAPICmd("AF_DATA_REQUEST_EXT",
                   [ PARSE_MODED_DST_ADDR,
                     PARSE_DST_EP,
                     PARSE_DST_PAN_ID,
                     PARSE_SRC_EP,
                     PARSE_CLUSTER_ID,
                     PARSE_TRANS_ID,
                     PARSE_OPTIONS,
                     PARSE_RADIUS,
                     ParseExtData("Len", "Data", 230)]),
    0x03: MTAPICmd("AF_DATA_REQUEST_SRC_RTG",
                   [ PARSE_DST_ADDR,
                     PARSE_DST_EP,
                     PARSE_SRC_EP,
                     PARSE_CLUSTER_ID,
                     PARSE_TRANS_ID,
                     PARSE_OPTIONS,
                     PARSE_RADIUS,
                     PARSE_RELAY_LIST,
                     PARSE_DATA]),
    0x10: MTAPICmd("AF_INTER_PAN_CTL", [ ParseInterPan() ]),
    0x11: MTAPICmd("AF_DATA_STORE", [ PARSE_INDEX, PARSE_DATA]),
    0x12: MTAPICmd("AF_DATA_RETRIEVE",
                   [ PARSE_TIMESTAMP,
                     PARSE_INDEX,
                     ParseField("Length", 1)]),
    0x13: MTAPICmd("AF_APSF_CONFIG_SET",
                   [ PARSE_ENDPOINT,
                     ParseField("FrameDelay", 1),
                     ParseField("WindowSize", 1)])
}

MT_AF_SRSP_CMDS = {
    0x00: MTAPICmd("AF_REGISTER", [ PARSE_STATUS ]),
    0x01: MTAPICmd("AF_DATA_REQUEST", [ PARSE_STATUS ]),
    0x02: MTAPICmd("AF_DATA_REQUEST_EXT", [ PARSE_STATUS ]),
    0x03: MTAPICmd("AF_DATA_REQUEST_SRC_RTG", [ PARSE_STATUS ]),
    0x10: MTAPICmd("AF_INTER_PAN_CTL", [ PARSE_STATUS ]),
    0x11: MTAPICmd("AF_DATA_STORE", [ PARSE_STATUS ]),
    0x12: MTAPICmd("AF_DATA_RETRIEVE", [ PARSE_STATUS, PARSE_DATA]),
    0x13: MTAPICmd("AF_APSF_CONFIG_SET", [ PARSE_STATUS ])
}

MT_AF_AREQ_CMDS = {
    0x80: MTAPICmd("AF_DATA_CONFIRM",
                   [ PARSE_STATUS, PARSE_ENDPOINT, PARSE_TRANS_ID]),
    0x83: MTAPICmd("AF_REFLECT_ERROR",
                   [ PARSE_STATUS,
                     PARSE_ENDPOINT,
                     PARSE_TRANS_ID,
                     PARSE_DST_MODE,
                     PARSE_DST_ADDR]),
    0x81: MTAPICmd("AF_INCOMING_MSG",
                   [ PARSE_GROUP_ID,
                     PARSE_CLUSTER_ID,
                     PARSE_SRC_ADDR,
                     PARSE_SRC_EP,
                     PARSE_DST_EP,
                     PARSE_WAS_BROADCAST,
                     PARSE_LINK_QUALITY,
                     PARSE_SECURITY_USE,
                     PARSE_TIMESTAMP,
                     ParseField("TransSeqNumber", 1),
                     PARSE_DATA]),
    0x82: MTAPICmd("AF_INCOMING_MSG_EXT",
                   [ PARSE_GROUP_ID,
                     PARSE_CLUSTER_ID,
                     PARSE_MODED_SRC_ADDR,
                     PARSE_SRC_EP,
                     PARSE_SRC_PAN_ID,
                     PARSE_DST_EP,
                     PARSE_WAS_BROADCAST,
                     PARSE_LINK_QUALITY,
                     PARSE_SECURITY_USE,
                     PARSE_TIMESTAMP,
                     ParseField("TransSeqNumber", 1),
                     PARSE_DATA])
}

MT_APP_SREQ_CMDS = {
    0x00: MTAPICmd("APP_MSG",
                   [ ParseField("AppEndpoint", 1),
                     PARSE_DST_ADDR,
                     PARSE_DST_EP,
                     PARSE_CLUSTER_ID,
                     ParseVariable("MsgLen", "Message")]),
    0x01: MTAPICmd("APP_USER_TEST",
                   [ PARSE_SRC_EP,
                     ParseField("CommandId", 2, field_parse_hword),
                     ParseField("Parameter1", 2, field_parse_hword),
                     ParseField("Parameter2", 2, field_parse_hword)])
}

MT_APP_SRSP_CMDS = {
    0x00: MTAPICmd("APP_MSG", [ PARSE_STATUS ]),
    0x01: MTAPICmd("APP_USER_TEST", [ PARSE_STATUS ])
}

MT_DEBUG_SREQ_CMDS = {
    0x00: MTAPICmd("DEBUG_SET_THRESHOLD",
                   [ ParseField("ComponentId", 1),
                     ParseField("Threshold", 1)])
}

MT_DEBUG_SRSP_CMDS = {
    0x00: MTAPICmd("DEBUG_SET_THRESHOLD", [ PARSE_STATUS ])
}

MT_DEBUG_AREQ_CMDS = {
    0x00: MTAPICmd("DEBUG_MSG", [ ParseVariable("Length", "String") ])
}

MT_MAC_SREQ_CMDS = {
    0x01: MTAPICmd("MAC_RESET_REQ",
                   [ ParseField("SetDefault", 1) ]),
    0x02: MTAPICmd("MAC_INIT", []),
    0x03: MTAPICmd("MAC_START_REQ",
                   [ ParseField("StartTime", 4, field_parse_word),
                     PARSE_PAN_ID,
                     PARSE_LOGICAL_CHANNEL,
                     PARSE_CHANNEL_PAGE,
                     ParseField("BeaconOrder", 1),
                     ParseField("SuperFrameOrder", 1),
                     ParseField("PanCoordinator", 1),
                     ParseField("BatteryLiftExt", 1),
                     ParseField("CoordRealignment", 1),
                     ParseKey("RealignKeySource",
                              "RealignSecurityLevel",
                              "RealignKeyIdMode",
                              "RealignKeyIndex"),
                     ParseKey("BeaconKeySource",
                              "BeaconSecurityLevel",
                              "BeaconKeyIdMode",
                              "BeaconKeyIndex")]),
    0x04: MTAPICmd("MAC_SYNC_REQ",
                   [ PARSE_LOGICAL_CHANNEL,
                     PARSE_CHANNEL_PAGE,
                     ParseField("TrackBeacon", 1)]),
    0x05: MTAPICmd("MAC_DATA_REQ",
                   [ PARSE_MODED_DST_ADDR,
                     PARSE_DST_PAN_ID,
                     PARSE_SRC_MODE,
                     PARSE_HANDLE,
                     ParseField("TxOption", 1,
                                field_parse_tx_option),
                     PARSE_LOGICAL_CHANNEL,
                     ParseField("Power", 1),
                     PARSE_KEY,
                     ParseVariable("MSDULength", "MSDU")]),
    0x06: MTAPICmd("MAC_ASSOCIATE_REQ",
                   [ PARSE_LOGICAL_CHANNEL,
                     PARSE_CHANNEL_PAGE,
                     PARSE_MODED_COORD_ADDR,
                     PARSE_COORD_PAN_ID,
                     PARSE_CAPABILITIES,
                     PARSE_KEY]),
    0x50: MTAPICmd("MAC_ASSOCIATE_RSP",
                   [ PARSE_EXT_ADDR,
                     PARSE_ASSOC_ADDR,
                     ParseField("AssocStatus", 1,
                                field_parse_assoc_status)]),
    0x07: MTAPICmd("MAC_DISASSOCIATE_REQ",
                   [ PARSE_MODED_DEV_ADDR,
                     PARSE_DEV_PAN_ID,
                     PARSE_DISASSOC_REASON,
                     ParseField("TxIndirect", 1),
                     PARSE_KEY]),
    0x08: MTAPICmd("MAC_GET_REQ", [ PARSE_MAC_ATTRIBUTE ]),
    0x09: MTAPICmd("MAC_SET_REQ",
                   [ PARSE_MAC_ATTRIBUTE,
                     ParseField("AttributeValue", 16)]),
    0x0c: MTAPICmd("MAC_SCAN_REQ",
                   [ PARSE_SCAN_CHANNELS,
                     PARSE_SCAN_TYPE,
                     PARSE_SCAN_DURATION,
                     PARSE_CHANNEL_PAGE,
                     ParseField("MaxResults", 1),
                     PARSE_KEY]),
    0x51: MTAPICmd("MAC_ORPHAN_RSP",
                   [ PARSE_EXT_ADDR,
                     PARSE_ASSOC_ADDR,
                     ParseField("AssociatedMember", 1)]),
    0x0d: MTAPICmd("MAC_POLL_REQ",
                   [ PARSE_MODED_COORD_ADDR,
                     PARSE_COORD_PAN_ID,
                     PARSE_KEY]),
    0x0e: MTAPICmd("MAC_PURGE_REQ",
                   [ ParseField("MsduHandle", 1) ]),
    0x0f: MTAPICmd("MAC_SET_RX_GAIN_REQ", [ ParseField("Mode", 1) ])
}

MT_MAC_SRSP_CMDS = {
    0x01: MTAPICmd("MAC_RESET_REQ", [ PARSE_STATUS ]),
    0x02: MTAPICmd("MAC_INIT", [ PARSE_STATUS ]),
    0x03: MTAPICmd("MAC_START_REQ", [ PARSE_STATUS ]),
    0x04: MTAPICmd("MAC_SYNC_REQ", [ PARSE_STATUS ]),
    0x05: MTAPICmd("MAC_DATA_REQ", [ PARSE_STATUS ]),
    0x06: MTAPICmd("MAC_ASSOCIATE_REQ", [ PARSE_STATUS ]),
    0x50: MTAPICmd("MAC_ASSOCIATE_RSP", [ PARSE_STATUS ]),
    0x07: MTAPICmd("MAC_DISASSOCIATE_REQ", [ PARSE_STATUS ]),
    0x08: MTAPICmd("MAC_GET_REQ",
                   [ PARSE_STATUS, ParseField("Data", 16)]),
    0x09: MTAPICmd("MAC_SET_REQ", [ PARSE_STATUS ]),
    0x0c: MTAPICmd("MAC_SCAN_REQ", [ PARSE_STATUS ]),
    0x51: MTAPICmd("MAC_ORPHAN_RSP", [ PARSE_STATUS ]),
    0x0d: MTAPICmd("MAC_POLL_REQ", [ PARSE_STATUS ]),
    0x0e: MTAPICmd("MAC_PURGE_REQ", [ PARSE_STATUS ]),
    0x0f: MTAPICmd("MAC_SET_RX_GAIN_REQ", [ PARSE_STATUS ])
}

MT_MAC_AREQ_CMDS = {
    0x80: MTAPICmd("MAC_SYNC_LOSS_IND",
                   [ PARSE_STATUS,
                     PARSE_PAN_ID,
                     PARSE_LOGICAL_CHANNEL,
                     PARSE_CHANNEL_PAGE,
                     PARSE_KEY]),
    0x81: MTAPICmd("MAC_ASSOCIATE_IND",
                   [ PARSE_DEV_EXT_ADDR,
                     PARSE_CAPABILITIES,
                     PARSE_KEY]),
    0x82: MTAPICmd("MAC_ASSOCIATE_CNF",
                   [ PARSE_STATUS,
                     PARSE_DEV_ADDR,
                     PARSE_KEY]),
    0x83: MTAPICmd("MAC_BEACON_NOTIFY_IND",
                   [ ParseField("BSN", 1),
                     PARSE_TIMESTAMP,
                     PARSE_MODED_COORD_ADDR,
                     PARSE_PAN_ID,
                     ParseField("SuperframeSpec", 2, field_parse_hword),
                     PARSE_LOGICAL_CHANNEL,
                     ParseField("GTSPermit", 1),
                     PARSE_LINK_QUALITY,
                     ParseField("SecurityFailure", 1),
                     PARSE_KEY,
                     ParseField("PendingAddrSpec", 1),
                     ParseField("AddressList", 1),
                     ParseVariable("SDULength", "NSDU")]),
    0x84: MTAPICmd("MAC_DATA_CNF",
                   [ PARSE_STATUS,
                     PARSE_HANDLE,
                     PARSE_TIMESTAMP,
                     PARSE_TIMESTAMP2 ]),
    0x85: MTAPICmd("MAC_DATA_IND",
                   [ PARSE_MODED_SRC_ADDR,
                     PARSE_MODED_DST_ADDR,
                     PARSE_TIMESTAMP,
                     PARSE_TIMESTAMP2,
                     PARSE_SRC_PAN_ID,
                     PARSE_DST_PAN_ID,
                     PARSE_LINK_QUALITY,
                     ParseField("Correlation", 1),
                     ParseField("RSSI", 1),
                     ParseField("DSN", 1),
                     PARSE_KEY,
                     PARSE_DATA]),
    0x86: MTAPICmd("MAC_DISASSOCIATE_IND",
                   [ PARSE_EXT_ADDR,
                     PARSE_DISASSOC_REASON,
                     PARSE_KEY]),
    0x87: MTAPICmd("MAC_DISASSOCIATE_CNF",
                   [ PARSE_STATUS,
                     PARSE_MODED_DEV_ADDR,
                     PARSE_DEV_PAN_ID]),
    0x8a: MTAPICmd("MAC_ORPHAN_IND", [ PARSE_EXT_ADDR, PARSE_KEY]),
    0x8b: MTAPICmd("MAC_POLL_CNF", [ PARSE_STATUS ]),
    0x8c: MTAPICmd("MAC_SCAN_CNF",
                   [ PARSE_STATUS,
                     ParseField("ED", 1),
                     PARSE_SCAN_TYPE,
                     PARSE_CHANNEL_PAGE,
                     ParseField("UnscannedChannelList", 4,
                                field_parse_scan_channels),
                     ParseField("ResultListCount", 1),
                     ParseVariable("ResultListMaxLength",
                                   "ResultList")]),
    0x8d: MTAPICmd("MAC_COMM_STATUS_IND",
                   [ PARSE_STATUS,
                     PARSE_SRC_EXT_ADDR,
                     PARSE_MODED_DST_ADDR,
                     PARSE_TIMESTAMP,
                     PARSE_DEV_PAN_ID,
                     ParseField("Reason", 1),
                     PARSE_KEY]),
    0x8e: MTAPICmd("MAC_START_CNF", [ PARSE_STATUS ]),
    0x8f: MTAPICmd("MAC_RX_ENABLE_CNF", [ PARSE_STATUS ]),
    0x9a: MTAPICmd("MAC_PURGE_CNF", [ PARSE_STATUS, PARSE_HANDLE ])
}

MT_SAPI_SREQ_CMDS = {
    0x00: MTAPICmd("ZB_START_REQUEST", []),
    0x08: MTAPICmd("ZB_PERMIT_JOINING_REQUEST",
                   [ PARSE_DST_ADDR,
                     ParseField("Timeout", 1)]),
    0x01: MTAPICmd("ZB_BIND_DEVICE",
                   [ ParseField("Create", 1),
                     PARSE_COMMAND_ID,
                     PARSE_DST_EXT_ADDR]),
    0x02: MTAPICmd("ZB_ALLOW_BIND",
                   [ ParseField("Timeout", 1) ]),
    0x03: MTAPICmd("ZB_SEND_DATA_REQUEST",
                   [ PARSE_DST_ADDR,
                     PARSE_COMMAND_ID,
                     PARSE_HANDLE,
                     ParseField("Ack", 1),
                     PARSE_RADIUS,
                     PARSE_DATA]),
    0x04: MTAPICmd("ZB_READ_CONFIGURATION", [ PARSE_CONFIG_ID ]),
    0x05: MTAPICmd("ZB_WRITE_CONFIGURATION",
                   [ PARSE_CONFIG_ID, PARSE_DATA ]),
    0x06: MTAPICmd("ZB_GET_DEVICE_INFO", [ PARSE_PARAM ]),
    0x07: MTAPICmd("ZB_FIND_DEVICE_REQUEST",
                   [ ParseField("SearchKey", 8) ])
}

MT_SAPI_SRSP_CMDS = {
    0x00: MTAPICmd("ZB_START_REQUEST", []),
    0x08: MTAPICmd("ZB_PERMIT_JOINING_REQUEST", [ PARSE_STATUS ]),
    0x01: MTAPICmd("ZB_BIND_DEVICE", []),
    0x02: MTAPICmd("ZB_ALLOW_BIND", []),
    0x03: MTAPICmd("ZB_SEND_DATA_REQUEST", []),
    0x04: MTAPICmd("ZB_READ_CONFIGURATION",
                   [ PARSE_STATUS, PARSE_CONFIG_ID, PARSE_DATA ]),
    0x05: MTAPICmd("ZB_WRITE_CONFIGURATION", [ PARSE_STATUS ]),
    0x06: MTAPICmd("ZB_GET_DEVICE_INFO",
                   [ PARSE_PARAM, ParseField("Value", 8)]),
    0x07: MTAPICmd("ZB_FIND_DEVICE_REQUEST", [])
}

MT_SAPI_AREQ_CMDS = {
    0x09: MTAPICmd("ZB_SYSTEM_RESET", []),
    0x80: MTAPICmd("ZB_START_CONFIRM", [ PARSE_STATUS ]),
    0x81: MTAPICmd("ZB_BIND_CONFIRM",
                   [ PARSE_COMMAND_ID, PARSE_STATUS ]),
    0x82: MTAPICmd("ZB_ALLOW_BIND_CONFIRM", [ PARSE_SRC_ADDR ]),
    0x83: MTAPICmd("ZB_SEND_DATA_CONFIRM",
                   [ PARSE_HANDLE, PARSE_STATUS ]),
    0x87: MTAPICmd("ZB_RECEIVE_DATA_INDICATION",
                   [ PARSE_SRC_ADDR,
                     PARSE_COMMAND_ID,
                     ParseVariable("Len", "Data", len_bytes=2)]),
    0x85: MTAPICmd("ZB_FIND_DEVICE_CONFIRM",
                   [ ParseField("SearchType", 1),
                     ParseField("SearchKey", 2, field_parse_hword),
                     ParseField("Result", 8)])
}

MT_SYS_SREQ_CMDS = {
    0x01: MTAPICmd("SYS_PING", []),
    0x02: MTAPICmd("SYS_VERSION", []),
    0x03: MTAPICmd("SYS_SET_EXTADDR", [ PARSE_EXT_ADDR ]),
    0x04: MTAPICmd("SYS_GET_EXTADDR", []),
    0x05: MTAPICmd("SYS_RAM_READ",
                   [ PARSE_RAM_ADDR, ParseField("Len", 1)]),
    0x06: MTAPICmd("SYS_RAM_WRITE",
                   [ PARSE_RAM_ADDR, PARSE_DATA]),
    0x08: MTAPICmd("SYS_OSAL_NV_READ",
                   [ PARSE_NV_ID, PARSE_NV_OFFSET ]),
    0x09: MTAPICmd("SYS_OSAL_NV_WRITE",
                   [ PARSE_NV_ID, PARSE_NV_OFFSET, PARSE_DATA ]),
    0x07: MTAPICmd("SYS_OSAL_NV_ITEM_INIT",
                   [ PARSE_NV_ID,
                     PARSE_NV_ITEM_LEN,
                     ParseVariable("InitLen", "InitData")]),
    0x12: MTAPICmd("SYS_OSAL_NV_DELETE",
                   [ PARSE_NV_ID, PARSE_NV_ITEM_LEN ]),
    0x13: MTAPICmd("SYS_OSAL_NV_LENGTH", [ PARSE_NV_ID ]),
    0x0a: MTAPICmd("SYS_OSAL_START_TIMER",
                   [ PARSE_TIMER_ID,
                     ParseField("Timeout", 2, field_parse_hword)]),
    0x0b: MTAPICmd("SYS_OSAL_STOP_TIMER", [ PARSE_TIMER_ID ]),
    0x0c: MTAPICmd("SYS_RANDOM", []),
    0x0d: MTAPICmd("SYS_ADC_READ",
                   [ ParseField("Channel", 1,
                                field_parse_adc_channel),
                     ParseField("Resolution", 1,
                                field_parse_adc_resolution)]),
    0x0e: MTAPICmd("SYS_GPIO",
                   [ ParseField("Operation", 1,
                                field_parse_gpio_operation),
                     PARSE_VALUE_BYTE ]),
    0x0f: MTAPICmd("SYS_STACK_TUNE",
                   [ ParseField("Operation", 1),
                     PARSE_VALUE_BYTE ]),
    0x10: MTAPICmd("SYS_SET_TIME", [ PARSE_TIME ]),
    0x11: MTAPICmd("SYS_GET_TIME", []),
    0x14: MTAPICmd("SYS_SET_TX_POWER", [ PARSE_TX_POWER ]),
    0x17: MTAPICmd("SYS_ZDIAGS_INIT_STATS", []),
    0x18: MTAPICmd("SYS_ZDIAGS_CLEAR_STATS",
                   [ ParseField("ClearNV", 1) ]),
    0x19: MTAPICmd("SYS_ZDIAGS_GET_STATS",
                   [ ParseField("AttributeId", 2,
                                field_parse_hword) ]),
    0x1a: MTAPICmd("SYS_ZDIAGS_RESTORE_STATS_NV", []),
    0x1b: MTAPICmd("SYS_ZDIAGS_SAVE_STATS_TO_NV", []),
    0x30: MTAPICmd("SYS_NV_CREATE",
                   [ PARSE_SYS_ID,
                     PARSE_ITEM_ID,
                     PARSE_SUB_ID,
                     ParseField("Length", 4, field_parse_word)]),
    0x31: MTAPICmd("SYS_NV_DELETE",
                   [ PARSE_SYS_ID, PARSE_ITEM_ID, PARSE_SUB_ID ]),
    0x32: MTAPICmd("SYS_NV_LENGTH",
                   [ PARSE_SYS_ID, PARSE_ITEM_ID, PARSE_SUB_ID ]),
    0x33: MTAPICmd("SYS_NV_READ",
                   [ PARSE_SYS_ID,
                     PARSE_ITEM_ID,
                     PARSE_SUB_ID,
                     PARSE_OFFSET,
                     ParseField("Length", 1)]),
    0x34: MTAPICmd("SYS_NV_WRITE",
                   [ PARSE_SYS_ID,
                     PARSE_ITEM_ID,
                     PARSE_SUB_ID,
                     PARSE_OFFSET,
                     PARSE_DATA ]),
    0x35: MTAPICmd("SYS_NV_UPDATE",
                   [ PARSE_SYS_ID,
                     PARSE_ITEM_ID,
                     PARSE_SUB_ID,
                     PARSE_DATA ]),
    0x36: MTAPICmd("SYS_NV_COMPACT",
                   [ ParseField("Threshold", 2, field_parse_hword) ]),
    0x1c: MTAPICmd("SYS_OSAL_NV_READ_EXT",
                   [ PARSE_NV_ID, PARSE_OFFSET ]),
    0x1d: MTAPICmd("SYS_OSAL_NV_WRITE_EXT",
                   [ PARSE_NV_ID, PARSE_OFFSET, PARSE_DATA ])
}

MT_SYS_SRSP_CMDS = {
    0x01: MTAPICmd("SYS_PING",
                   [ ParseField("Capabilities", 2,
                                field_parse_sys_capabilities)]),
    0x02: MTAPICmd("SYS_VERSION",
                   [ PARSE_TRANSPORT_REVISION,
                     PARSE_PRODUCT_ID,
                     PARSE_MAJOR_RELEASE,
                     PARSE_MINOR_RELEASE,
                     ParseField("MaintRel", 1)]),
    0x03: MTAPICmd("SYS_SET_EXTADDR", [ PARSE_STATUS ]),
    0x04: MTAPICmd("SYS_GET_EXTADDR", [ PARSE_EXT_ADDR ]),
    0x05: MTAPICmd("SYS_RAM_READ", [ PARSE_STATUS, PARSE_DATA ]),
    0x06: MTAPICmd("SYS_RAM_WRITE", [ PARSE_STATUS ]),
    0x08: MTAPICmd("SYS_OSAL_NV_READ", [ PARSE_STATUS, PARSE_DATA ]),
    0x09: MTAPICmd("SYS_OSAL_NV_WRITE", [ PARSE_STATUS ]),
    0x07: MTAPICmd("SYS_OSAL_NV_ITEM_INIT", [ PARSE_STATUS ]),
    0x12: MTAPICmd("SYS_OSAL_NV_DELETE", [ PARSE_STATUS ]),
    0x13: MTAPICmd("SYS_OSAL_NV_LENGTH", [ PARSE_NV_ITEM_LEN ]),
    0x0a: MTAPICmd("SYS_OSAL_START_TIMER", [ PARSE_STATUS ]),
    0x0b: MTAPICmd("SYS_OSAL_STOP_TIMER", [ PARSE_STATUS ]),
    0x0c: MTAPICmd("SYS_RANDOM", [ PARSE_VALUE_HWORD ]),
    0x0d: MTAPICmd("SYS_ADC_READ", [ PARSE_VALUE_HWORD ]),
    0x0e: MTAPICmd("SYS_GPIO", [ PARSE_VALUE_BYTE ]),
    0x0f: MTAPICmd("SYS_STACK_TUNE", [ PARSE_VALUE_BYTE ]),
    0x10: MTAPICmd("SYS_SET_TIME", [ PARSE_STATUS ]),
    0x11: MTAPICmd("SYS_GET_TIME", [ PARSE_TIME ]),
    0x14: MTAPICmd("SYS_SET_TX_POWER", [ PARSE_TX_POWER ]),
    0x17: MTAPICmd("SYS_ZDIAGS_INIT_STATS", [ PARSE_STATUS ]),
    0x18: MTAPICmd("SYS_ZDIAGS_CLEAR_STATS", [ PARSE_SYS_CLOCK ]),
    0x19: MTAPICmd("SYS_ZDIAGS_GET_STATS",
                   [ ParseField("AttributeValue", 4,
                                field_parse_word) ]),
    0x1a: MTAPICmd("SYS_ZDIAGS_RESTORE_STATS_NV", [ PARSE_STATUS ]),
    0x1b: MTAPICmd("SYS_ZDIAGS_SAVE_STATS_TO_NV", [ PARSE_SYS_CLOCK ]),
    0x30: MTAPICmd("SYS_NV_CREATE", [ PARSE_STATUS ]),
    0x31: MTAPICmd("SYS_NV_DELETE", [ PARSE_STATUS ]),
    0x32: MTAPICmd("SYS_NV_LENGTH", [ ParseField("Length", 1) ]),
    0x33: MTAPICmd("SYS_NV_READ", [ PARSE_STATUS, PARSE_DATA ]),
    0x34: MTAPICmd("SYS_NV_WRITE", [ PARSE_STATUS ]),
    0x35: MTAPICmd("SYS_NV_UPDATE", [ PARSE_STATUS ]),
    0x36: MTAPICmd("SYS_NV_COMPACT", [ PARSE_STATUS ]),
    0x1c: MTAPICmd("SYS_OSAL_NV_READ_EXT", [ PARSE_STATUS, PARSE_DATA ]),
    0x1d: MTAPICmd("SYS_OSAL_NV_WRITE_EXT", [ PARSE_STATUS ])
}

MT_SYS_AREQ_CMDS = {
    0x00: MTAPICmd("SYS_RESET_REQ",
                   [ ParseField("Type", 1, field_parse_reset_type) ]),
    0x80: MTAPICmd("SYS_RESET_IND",
                   [ ParseField("Reason", 1,
                                field_parse_reset_reason),
                     PARSE_TRANSPORT_REVISION,
                     PARSE_PRODUCT_ID,
                     PARSE_MAJOR_RELEASE,
                     PARSE_MINOR_RELEASE,
                     ParseField("HwRev", 1) ]),
    0x81: MTAPICmd("SYS_OSAL_TIMER_EXPIRED", [ PARSE_TIMER_ID ])
}

MT_UTIL_SREQ_CMDS = {
    0x00: MTAPICmd("UTIL_GET_DEVICE_INFO", []),
    0x01: MTAPICmd("UTIL_GET_NV_INFO", []),
    0x02: MTAPICmd("UTIL_SET_PANID", [ PARSE_PAN_ID ]),
    0x03: MTAPICmd("UTIL_SET_CHANNELS",
                   [ ParseField("Channels", 4,
                                field_parse_scan_channels) ]),
    0x04: MTAPICmd("UTIL_SET_SECLEVEL", [ PARSE_SECURITY_LEVEL ]),
    0x05: MTAPICmd("UTIL_SET_PRECFGKEY", [ PARSE_PRECONFIGURED_KEY ]),
    0x06: MTAPICmd("UTIL_CALLBACK_SUB_CMD",
                   [ ParseField("SubsystemId", 2,
                                field_parse_subsystem_id),
                     ParseField("Action", 1,
                                field_parse_enable)]),
    0x07: MTAPICmd("UTIL_KEY_EVENT",
                   [ ParseField("Keys", 1, field_parse_keys),
                     ParseField("Shift", 1, field_parse_shift)]),
    0x09: MTAPICmd("UTIL_TIME_ALIVE", []),
    0x0a: MTAPICmd("UTIL_LED_CONTROL",
                   [ ParseField("LedId", 1),
                     ParseField("Mode", 1, field_parse_onoff)]),
    0x10: MTAPICmd("UTIL_LOOPBACK", [ ParseRemaining("Data") ]),
    0x11: MTAPICmd("UTIL_DATA_REQ", [ PARSE_SECURITY_USE ]),
    0x20: MTAPICmd("UTIL_SRC_MATCH_ENABLE", []),
    0x21: MTAPICmd("UTIL_SRC_MATCH_ADD_ENTRY",
                   [ PARSE_MODED_ADDR, PARSE_PAN_ID ]),
    0x22: MTAPICmd("UTIL_SRC_MATCH_DEL_ENTRY",
                   [ PARSE_MODED_ADDR, PARSE_PAN_ID ]),
    0x23: MTAPICmd("UTIL_SRC_MATCH_CHECK_SRC_ADDR",
                   [ PARSE_MODED_ADDR, PARSE_PAN_ID ]),
    0x24: MTAPICmd("UTIL_SRC_MATCH_ACK_ALL_PENDING",
                   [ ParseField("Option", 1) ]),
    0x25: MTAPICmd("UTIL_SRC_MATCH_CHECK_ALL_PENDING", []),
    0x40: MTAPICmd("UTIL_ADDRMGR_EXT_ADDR_LOOKUP", [ PARSE_EXT_ADDR ]),
    0x41: MTAPICmd("UTIL_ADDRMGR_NWK_ADDR_LOOKUP", [ PARSE_NWK_ADDR ]),
    0x44: MTAPICmd("UTIL_APSME_LINK_KEY_DATA_GET", [ PARSE_EXT_ADDR ]),
    0x45: MTAPICmd("UTIL_APSME_LINK_KEY_NV_ID_GET", [ PARSE_EXT_ADDR ]),
    0x4b: MTAPICmd("UTIL_APSME_REQUEST_KEY_CMD",
                   [ ParseField("PartnerAddr", 2,
                                field_parse_hword) ]),
    0x48: MTAPICmd("UTIL_ASSOC_COUNT",
                   [ ParseField("StartRelation", 1,
                                field_parse_relation),
                     ParseField("EndRelation", 1,
                                field_parse_relation)]),
    0x49: MTAPICmd("UTIL_ASSOC_FIND_DEVICE",
                   [ ParseField("Number", 1) ]),
    0x4a: MTAPICmd("UTIL_ASSOC_GET_WITH_ADDRESS",
                   [ PARSE_EXT_ADDR, PARSE_NWK_ADDR ]),
    0x4d: MTAPICmd("UTIL_BIND_ADD_ENTRY",
                   [ PARSE_MODED_DST_ADDR,
                     PARSE_DST_EP,
                     ParseClusterList("NumClusterIds",
                                      "ClusterIds")]),
    0x80: MTAPICmd("UTIL_ZCL_KEY_EST_INIT_EST",
                   [ PARSE_TASK_ID,
                     PARSE_SEQ_NUM,
                     PARSE_ENDPOINT,
                     PARSE_MODED_ADDR ]),
    0x81: MTAPICmd("UTIL_ZCL_KEY_EST_SIGN",
                   [ ParseVariable("InputLen", "Input") ]),
    0x4c: MTAPICmd("UTIL_SRNG_GEN", [])
}

MT_UTIL_SRSP_CMDS = {
    0x00: MTAPICmd("UTIL_GET_DEVICE_INFO",
                   [ PARSE_STATUS,
                     PARSE_IEEE_ADDR,
                     PARSE_SHORT_ADDR,
                     ParseField("DeviceType", 1,
                                field_parse_device_type),
                     ParseField("DeviceState", 1,
                                field_parse_device_state),
                     PARSE_ASSOCIATION_LIST ]),
    0x01: MTAPICmd("UTIL_GET_NV_INFO",
                   [ PARSE_STATUS,
                     PARSE_IEEE_ADDR,
                     PARSE_SCAN_CHANNELS,
                     PARSE_PAN_ID,
                     PARSE_SECURITY_LEVEL,
                     PARSE_PRECONFIGURED_KEY ]),
    0x02: MTAPICmd("UTIL_SET_PANID", [ PARSE_STATUS ]),
    0x03: MTAPICmd("UTIL_SET_CHANNELS", [ PARSE_STATUS ]),
    0x04: MTAPICmd("UTIL_SET_SECLEVEL", [ PARSE_STATUS ]),
    0x05: MTAPICmd("UTIL_SET_PRECFGKEY", [ PARSE_STATUS ]),
    0x06: MTAPICmd("UTIL_CALLBACK_SUB_CMD", [ PARSE_STATUS ]),
    0x07: MTAPICmd("UTIL_KEY_EVENT", [ PARSE_STATUS ]),
    0x09: MTAPICmd("UTIL_TIME_ALIVE",
                   [ ParseField("Seconds", 4, field_parse_word) ]),
    0x0a: MTAPICmd("UTIL_LED_CONTROL", [ PARSE_STATUS ]),
    0x10: MTAPICmd("UTIL_LOOPBACK", [ ParseRemaining("Data") ]),
    0x11: MTAPICmd("UTIL_DATA_REQ", [ PARSE_STATUS ]),
    0x20: MTAPICmd("UTIL_SRC_MATCH_ENABLE", [ PARSE_STATUS ]),
    0x21: MTAPICmd("UTIL_SRC_MATCH_ADD_ENTRY", [ PARSE_STATUS ]),
    0x22: MTAPICmd("UTIL_SRC_MATCH_DEL_ENTRY", [ PARSE_STATUS ]),
    0x23: MTAPICmd("UTIL_SRC_MATCH_CHECK_SRC_ADDR", [ PARSE_STATUS ]),
    0x24: MTAPICmd("UTIL_SRC_MATCH_ACK_ALL_PENDING", [ PARSE_STATUS ]),
    0x25: MTAPICmd("UTIL_SRC_MATCH_CHECK_ALL_PENDING",
                   [ PARSE_STATUS, PARSE_VALUE_BYTE ]),
    0x40: MTAPICmd("UTIL_ADDRMGR_EXT_ADDR_LOOKUP", [ PARSE_NWK_ADDR ]),
    0x41: MTAPICmd("UTIL_ADDRMGR_NWK_ADDR_LOOKUP", [ PARSE_EXT_ADDR ]),
    0x44: MTAPICmd("UTIL_APSME_LINK_KEY_DATA_GET",
                   [ PARSE_STATUS,
                     ParseField("SecKey", 16, field_parse_colon_sep),
                     ParseField("TxFrmCntr", 4, field_parse_word),
                     ParseField("RxFrmCntr", 4, field_parse_word) ]),
    0x45: MTAPICmd("UTIL_APSME_LINK_KEY_NV_ID_GET",
                   [ PARSE_STATUS,
                     ParseField("LinkKeyNvId", 2,
                                field_parse_hword) ]),
    0x4b: MTAPICmd("UTIL_APSME_REQUEST_KEY_CMD", [ PARSE_STATUS ]),
    0x48: MTAPICmd("UTIL_ASSOC_COUNT",
                   [ ParseField("Count", 2, field_parse_hword) ]),
    0x49: MTAPICmd("UTIL_ASSOC_FIND_DEVICE", [ PARSE_DEVICE_INFO ]),
    0x4a: MTAPICmd("UTIL_ASSOC_GET_WITH_ADDRESS", [ PARSE_DEVICE_INFO ]),
    0x4d: MTAPICmd("UTIL_BIND_ADD_ENTRY",
                   [ ParseField("BindEntry", 14) ]),
    0x80: MTAPICmd("UTIL_ZCL_KEY_EST_INIT_EST", [ PARSE_STATUS ]),
    0x81: MTAPICmd("UTIL_ZCL_KEY_EST_SIGN",
                   [ PARSE_STATUS,
                     ParseField("Key", 42)]),
    0x4c: MTAPICmd("UTIL_SRNG_GEN",
                   [ ParseField("SecureRandomNumber", 0x64) ])
}

MT_UTIL_AREQ_CMDS = {
    0xe0: MTAPICmd("UTIL_SYNC_REQ", []),
    0xe1: MTAPICmd("UTIL_ZCL_KEY_ESTABLISH_IND",
                   [ PARSE_TASK_ID,
                     ParseField("Event", 1),
                     PARSE_STATUS,
                     ParseField("WaitTime", 1),
                     ParseField("Suite", 2, field_parse_hword)])
}

MT_ZDO_SREQ_CMDS = {
    0x00: MTAPICmd("ZDO_NWK_ADDR_REQ",
                   [ PARSE_IEEE_ADDR,
                     PARSE_REQ_TYPE,
                     PARSE_START_INDEX ]),
    0x01: MTAPICmd("ZDO_IEEE_ADDR_REQ",
                   [ PARSE_SHORT_ADDR,
                     PARSE_REQ_TYPE,
                     PARSE_START_INDEX ]),
    0x02: MTAPICmd("ZDO_NODE_DESC_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR ]),
    0x03: MTAPICmd("ZDO_POWER_DESC_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR ]),
    0x04: MTAPICmd("ZDO_SIMPLE_DESC_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR,
                     PARSE_ENDPOINT]),
    0x05: MTAPICmd("ZDO_ACTIVE_EP_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR ]),
    0x06: MTAPICmd("ZDO_MATCH_DESC_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR,
                     PARSE_PROFILE_ID,
                     PARSE_IN_CLUSTERS,
                     PARSE_OUT_CLUSTERS ]),
    0x07: MTAPICmd("ZDO_COMPLEX_DESC_REQ",
                   [ PARSE_DST_ADDR, PARSE_INTEREST_ADDR ]),
    0x08: MTAPICmd("ZDO_USER_DESC_REQ",
                   [ PARSE_DST_ADDR, PARSE_INTEREST_ADDR ]),
    0x0a: MTAPICmd("ZDO_END_DEVICE_ANNCE",
                   [ PARSE_NWK_ADDR,
                     PARSE_IEEE_ADDR,
                     PARSE_CAPABILITIES]),
    0x0b: MTAPICmd("ZDO_USER_DESC_SET",
                   [ PARSE_DST_ADDR,
                     PARSE_INTEREST_ADDR,
                     ParseVariable("Len", "UserDescriptor")]),
    0x0c: MTAPICmd("ZDO_SERVER_DISC_REQ",
                   [ ParseField("ServerMask", 2,
                                field_parse_hword)]),
    0x20: MTAPICmd("ZDO_END_DEVICE_BIND_REQ",
                   [ PARSE_DST_ADDR,
                     ParseField("LocalCoordinator", 2,
                                field_parse_hword),
                     PARSE_ENDPOINT,
                     PARSE_PROFILE_ID,
                     PARSE_IN_CLUSTERS,
                     PARSE_OUT_CLUSTERS ]),
    0x21: MTAPICmd("ZDO_BIND_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_SRC_EXT_ADDR,
                     PARSE_SRC_EP,
                     PARSE_CLUSTER_ID,
                     PARSE_BIND_ADDR ]),
    0x22: MTAPICmd("ZDO_UNBIND_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_SRC_EXT_ADDR,
                     PARSE_SRC_EP,
                     PARSE_CLUSTER_ID,
                     PARSE_BIND_ADDR ]),
    0x30: MTAPICmd("ZDO_MGMT_NWK_DISC_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_SCAN_CHANNELS,
                     PARSE_SCAN_DURATION,
                     PARSE_START_INDEX ]),
    0x31: MTAPICmd("ZDO_MGMT_LQI_REQ",
                   [ PARSE_DST_ADDR, PARSE_START_INDEX ]),
    0x32: MTAPICmd("ZDO_MGMT_RTG_REQ",
                   [ PARSE_DST_ADDR, PARSE_START_INDEX ]),
    0x33: MTAPICmd("ZDO_MGMT_BIND_REQ",
                   [ PARSE_DST_ADDR, PARSE_START_INDEX ]),
    0x34: MTAPICmd("ZDO_MGMT_LEAVE_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_DEV_EXT_ADDR,
                     ParseField("RemoveChildrenRejoin", 1,
                                field_parse_leave_action)]),
    0x35: MTAPICmd("ZDO_MGMT_DIRECT_JOIN_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_DEV_EXT_ADDR,
                     PARSE_CAPABILITIES]),
    0x36: MTAPICmd("ZDO_MGMT_PERMIT_JOIN_REQ",
                   [ PARSE_ADDR_MODE,
                     PARSE_DST_ADDR,
                     ParseField("Duration", 1,
                                field_parse_join_duration),
                     ParseField("TCSignificance", 1)]),
    0x37: MTAPICmd("ZDO_MGMT_NWK_UPDATE_REQ",
                   [ PARSE_DST_ADDR,
                     PARSE_DST_MODE,
                     ParseField("ChannelMask", 4,
                                field_parse_scan_channels),
                     PARSE_SCAN_DURATION,
                     ParseField("ScanCount", 1),
                     ParseField("NwkManagerAddr", 2,
                                field_parse_hword)]),
    0x3e: MTAPICmd("ZDO_MSG_CB_REGISTER", [ PARSE_CLUSTER_ID ]),
    0x3f: MTAPICmd("ZDO_MSG_CB_REMOVE", [ PARSE_CLUSTER_ID ]),
    0x40: MTAPICmd("ZDO_STARTUP_FROM_APP",
                   [ ParseField("StartDelay", 2,
                                field_parse_hword) ]),
    0x23: MTAPICmd("ZDO_SET_LINK_KEY",
                   [ PARSE_SHORT_ADDR,
                     PARSE_IEEE_ADDR,
                     PARSE_LINK_KEY ]),
    0x24: MTAPICmd("ZDO_REMOVE_LINK_KEY", [ PARSE_IEEE_ADDR ]),
    0x25: MTAPICmd("ZDO_GET_LINK_KEY", [ PARSE_IEEE_ADDR ]),
    0x26: MTAPICmd("ZDO_NWK_DISCOVERY_REQ",
                   [ PARSE_SCAN_CHANNELS, PARSE_SCAN_DURATION ]),
    0x27: MTAPICmd("ZDO_JOIN_REQ",
                   [ PARSE_LOGICAL_CHANNEL,
                     PARSE_PAN_ID,
                     PARSE_EXT_PAN_ID,
                     PARSE_PARENT_ADDR,
                     PARSE_DEPTH,
                     PARSE_STACK_PROFILE ]),
    0x42: MTAPICmd("ZDO_SEC_ADD_LINK_KEY",
                   [ PARSE_SHORT_ADDR,
                     PARSE_EXT_ADDR,
                     PARSE_LINK_KEY ]),
    0x43: MTAPICmd("ZDO_SEC_ENTRY_LOOKUP_EXT",
                   [ PARSE_EXT_ADDR, ParseRemaining("Entry")]),
    0x44: MTAPICmd("ZDO_SEC_DEVICE_REMOVE", [ PARSE_EXT_ADDR ]),
    0x45: MTAPICmd("ZDO_EXT_ROUTE_DISC",
                   [ PARSE_DST_ADDR,
                     ParseField("Options", 1),
                     PARSE_RADIUS ]),
    0x46: MTAPICmd("ZDO_EXT_ROUTE_CHECK",
                   [ PARSE_DST_ADDR,
                     ParseField("RTStatus", 1),
                     ParseField("Options", 1) ]),
    0x47: MTAPICmd("ZDO_EXT_REMOVE_GROUP",
                   [ PARSE_ENDPOINT, PARSE_GROUP_ID ]),
    0x48: MTAPICmd("ZDO_EXT_REMOVE_ALL_GROUP", [ PARSE_ENDPOINT ]),
    0x49: MTAPICmd("ZDO_EXT_FIND_ALL_GROUPS_ENDPOINT",
                   [ PARSE_ENDPOINT,
                     ParseField("GroupList", 2, field_parse_hword) ]),
    0x4a: MTAPICmd("ZDO_EXT_FIND_GROUP",
                   [ PARSE_ENDPOINT, PARSE_GROUP_ID ]),
    0x4b: MTAPICmd("ZDO_EXT_ADD_GROUP",
                   [ PARSE_ENDPOINT,
                     PARSE_GROUP_ID,
                     ParseField("GroupName", 16)]),
    0x4c: MTAPICmd("ZDO_EXT_COUNT_ALL_GROUPS", []),
    0x4d: MTAPICmd("ZDO_EXT_RX_IDLE",
                   [ ParseField("GetSetFlag", 1),
                     ParseField("SetValue", 1)]),
    0x4e: MTAPICmd("ZDO_EXT_UPDATE_NWK_KEY",
                   [ PARSE_DST_ADDR,
                     PARSE_KEY_SEQ_NUM,
                     ParseField("Key", 128)]),
    0x4f: MTAPICmd("ZDO_EXT_SWITCH_NWK_KEY",
                   [ PARSE_DST_ADDR, PARSE_KEY_SEQ_NUM ]),
    0x50: MTAPICmd("ZDO_EXT_NWK_INFO", []),
    0x51: MTAPICmd("ZDO_EXT_SEC_APS_REMOVE_REQ",
                   [ PARSE_NWK_ADDR,
                     PARSE_EXT_ADDR,
                     PARSE_PARENT_ADDR ]),
    0x52: MTAPICmd("ZDO_FORCE_CONCENTRATOR_CHANGE", []),
    0x53: MTAPICmd("ZDO_EXT_SET_PARAMS",
                   [ ParseField("UseMulticast", 1) ]),
}

MT_ZDO_SRSP_CMDS = {
    0x00: MTAPICmd("ZDO_NWK_ADDR_REQ", [ PARSE_STATUS ]),
    0x01: MTAPICmd("ZDO_IEEE_ADDR_REQ", [ PARSE_STATUS ]),
    0x02: MTAPICmd("ZDO_NODE_DESC_REQ", [ PARSE_STATUS ]),
    0x03: MTAPICmd("ZDO_POWER_DESC_REQ", [ PARSE_STATUS ]),
    0x04: MTAPICmd("ZDO_SIMPLE_DESC_REQ", [ PARSE_STATUS ]),
    0x05: MTAPICmd("ZDO_ACTIVE_EP_REQ", [ PARSE_STATUS ]),
    0x06: MTAPICmd("ZDO_MATCH_DESC_REQ", [ PARSE_STATUS ]),
    0x07: MTAPICmd("ZDO_COMPLEX_DESC_REQ", [ PARSE_STATUS ]),
    0x08: MTAPICmd("ZDO_USER_DESC_REQ", [ PARSE_STATUS ]),
    0x0a: MTAPICmd("ZDO_END_DEVICE_ANNCE", [ PARSE_STATUS ]),
    0x0b: MTAPICmd("ZDO_USER_DESC_SET", [ PARSE_STATUS ]),
    0x0c: MTAPICmd("ZDO_SERVER_DISC_REQ", [ PARSE_STATUS ]),
    0x20: MTAPICmd("ZDO_END_DEVICE_BIND_REQ", [ PARSE_STATUS ]),
    0x21: MTAPICmd("ZDO_BIND_REQ", [ PARSE_STATUS ]),
    0x22: MTAPICmd("ZDO_UNBIND_REQ", [ PARSE_STATUS ]),
    0x30: MTAPICmd("ZDO_MGMT_NWK_DISC_REQ", [ PARSE_STATUS ]),
    0x31: MTAPICmd("ZDO_MGMT_LQI_REQ", [ PARSE_STATUS ]),
    0x32: MTAPICmd("ZDO_MGMT_RTG_REQ", [ PARSE_STATUS ]),
    0x33: MTAPICmd("ZDO_MGMT_BIND_REQ", [ PARSE_STATUS ]),
    0x34: MTAPICmd("ZDO_MGMT_LEAVE_REQ", [ PARSE_STATUS ]),
    0x35: MTAPICmd("ZDO_MGMT_DIRECT_JOIN_REQ", [ PARSE_STATUS ]),
    0x36: MTAPICmd("ZDO_MGMT_PERMIT_JOIN_REQ", [ PARSE_STATUS ]),
    0x37: MTAPICmd("ZDO_MGMT_NWK_UPDATE_REQ", [ PARSE_STATUS ]),
    0x3e: MTAPICmd("ZDO_MSG_CB_REGISTER", [ PARSE_STATUS ]),
    0x3f: MTAPICmd("ZDO_MSG_CB_REMOVE", [ PARSE_STATUS ]),
    0x40: MTAPICmd("ZDO_STARTUP_FROM_APP",
                   [ ParseField("Status", 1,
                                field_parse_startup_status) ]),
    0x23: MTAPICmd("ZDO_SET_LINK_KEY", [ PARSE_STATUS ]),
    0x24: MTAPICmd("ZDO_REMOVE_LINK_KEY", [ PARSE_STATUS ]),
    0x25: MTAPICmd("ZDO_GET_LINK_KEY",
                   [ PARSE_STATUS,
                     PARSE_IEEE_ADDR,
                     PARSE_LINK_KEY ]),
    0x26: MTAPICmd("ZDO_NWK_DISCOVERY_REQ", [ PARSE_STATUS ]),
    0x27: MTAPICmd("ZDO_JOIN_REQ", [ PARSE_STATUS ]),
    0x42: MTAPICmd("ZDO_SEC_ADD_LINK_KEY", [ PARSE_STATUS ]),
    0x43: MTAPICmd("ZDO_SEC_ENTRY_LOOKUP_EXT",
                   [ ParseField("AMI", 2 ,field_parse_hword),
                     ParseField("KeyNVID", 2, field_parse_hword),
                     ParseField("AuthenticationOption", 1)]),
    0x44: MTAPICmd("ZDO_SEC_DEVICE_REMOVE", [ PARSE_STATUS ]),
    0x45: MTAPICmd("ZDO_EXT_ROUTE_DISC", [ PARSE_STATUS ]),
    0x46: MTAPICmd("ZDO_EXT_ROUTE_CHECK", [ PARSE_STATUS ]),
    0x47: MTAPICmd("ZDO_EXT_REMOVE_GROUP", [ PARSE_STATUS ]),
    0x48: MTAPICmd("ZDO_EXT_REMOVE_ALL_GROUP", [ PARSE_STATUS ]),
    0x49: MTAPICmd("ZDO_EXT_FIND_ALL_GROUPS_ENDPOINT",
                   [ ParseClusterList("NumGroups", "Groups") ]),
    0x4a: MTAPICmd("ZDO_EXT_FIND_GROUP",
                   [ ParseRemaining("Group") ]),
    0x4b: MTAPICmd("ZDO_EXT_ADD_GROUP", [ PARSE_STATUS ]),
    0x4c: MTAPICmd("ZDO_EXT_COUNT_ALL_GROUPS",
                   [ ParseField("NumGroups", 1) ]),
    0x4d: MTAPICmd("ZDO_EXT_RX_IDLE", [ PARSE_STATUS ]),
    0x4e: MTAPICmd("ZDO_EXT_UPDATE_NWK_KEY", [ PARSE_STATUS ]),
    0x4f: MTAPICmd("ZDO_EXT_SWITCH_NWK_KEY", [ PARSE_STATUS ]),
    0x50: MTAPICmd("ZDO_EXT_NWK_INFO",
                   [ PARSE_SHORT_ADDR,
                     PARSE_PAN_ID,
                     PARSE_PARENT_ADDR,
                     PARSE_EXT_PAN_ID,
                     ParseField("ExtendedParentAddress", 8,
                                field_parse_colon_sep),
                     ParseField("Channel", 2, field_parse_hword)]),
    0x51: MTAPICmd("ZDO_EXT_SEC_APS_REMOVE_REQ", [ PARSE_STATUS ]),
    0x52: MTAPICmd("ZDO_FORCE_CONCENTRATOR_CHANGE", []),
    0x53: MTAPICmd("ZDO_EXT_SET_PARAMS", [ PARSE_STATUS ]),
}

MT_ZDO_AREQ_CMDS = {
    0x41: MTAPICmd("ZDO_AUTO_FIND_DESTINATION", [ PARSE_ENDPOINT ]),
    0x80: MTAPICmd("ZDO_NWK_ADDR_RSP",
                   [ PARSE_STATUS,
                     PARSE_IEEE_ADDR,
                     PARSE_NWK_ADDR,
                     PARSE_START_INDEX,
                     PARSE_ASSOCIATION_LIST ]),
    0x81: MTAPICmd("ZDO_IEEE_ADDR_RSP",
                   [ PARSE_STATUS,
                     PARSE_IEEE_ADDR,
                     PARSE_NWK_ADDR,
                     PARSE_START_INDEX,
                     PARSE_ASSOCIATION_LIST ]),
    0x82: MTAPICmd("ZDO_NODE_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseField("TypeInfo", 1,
                                field_parse_type_and_info),
                     ParseBitFields((("APSFlags", 0x0f),
                                     ("NodeFrequencyBand", 0xf0))),
                     ParseField("MacCapabilitiesFlags", 1,
                                field_parse_capabilities),
                     ParseField("ManufacturerCode", 2,
                                field_parse_hword),
                     ParseField("MaxBufferSize", 1),
                     ParseField("MaxInTransferSize", 2,
                                field_parse_hword),
                     PARSE_SERVER_MASK,
                     ParseField("MaxOutTransferSize", 2,
                                field_parse_hword),
                     ParseField("DescriptorCapabilities", 1)]),
    0x83: MTAPICmd("ZDO_POWER_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseBitFields((("CurrentPowerMode", 0x0f),
                                     ("AvailablePowerSources", 0xf0))),
                     ParseBitFields((("CurrentPowerSource", 0x0f),
                                     ("CurrentPowerSourceLevel",
                                      0xf0)))]),
    0x84: MTAPICmd("ZDO_SIMPLE_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseField("Len", 1),
                     PARSE_ENDPOINT,
                     PARSE_PROFILE_ID,
                     PARSE_DEVICE_ID,
                     ParseField("DeviceVersion", 1),
                     PARSE_IN_CLUSTERS,
                     PARSE_OUT_CLUSTERS ]),
    0x85: MTAPICmd("ZDO_ACTIVE_EP_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseVariable("ActiveEPCount", "ActiveEPList")]),
    0x86: MTAPICmd("ZDO_MATCH_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseVariable("MatchLength", "MatchList")]),
    0x87: MTAPICmd("ZDO_COMPLEX_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseVariable("ComplexLength",
                                   "ComplexDescriptor")]),
    0x88: MTAPICmd("ZDO_USER_DESC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_NWK_ADDR,
                     ParseVariable("UserLength",
                                   "UserDescriptor")]),
    0x89: MTAPICmd("ZDO_USER_DESC_CONF",
                   [ PARSE_SRC_ADDR, PARSE_STATUS, PARSE_NWK_ADDR ]),
    0x8a: MTAPICmd("ZDO_SERVER_DISC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     PARSE_SERVER_MASK ]),
    0xa0: MTAPICmd("ZDO_END_DEVICE_BIND_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS]),
    0xa1: MTAPICmd("ZDO_BIND_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS]),
    0xa2: MTAPICmd("ZDO_UNBIND_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS]),
    0xb0: MTAPICmd("ZDO_MGMT_NWK_DISC_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     ParseField("NetworkCount", 1),
                     PARSE_START_INDEX,
                     ParseRepeated(
                         "NetworkListCount",
                         "NetworkListRecords",
                         [ PARSE_PAN_ID,
                           PARSE_LOGICAL_CHANNEL,
                           ParseBitFields((("ZigBeeVersion", 0xf0),
                                           ("StackProfile", 0x0f))),
                           ParseBitFields((("SuperframeOrder", 0xf0),
                                           ("BeaconOrder", 0x0f))),
                           ParseField("PermitJoining", 1)])]),
    0xb1: MTAPICmd("ZDO_MGMT_LQI_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     ParseField("NeighbourTableEntries", 1),
                     PARSE_START_INDEX,
                     ParseRepeated(
                         "NeighbourLqiListCount",
                         "NeighbourLqiList",
                         [ PARSE_EXT_PAN_ID,
                           PARSE_EXT_ADDR,
                           PARSE_NWK_ADDR,
                           ParseBitFields((("Relationship", 0x70),
                                           ("RxOnWhenIdle", 0x0c),
                                           ("DeviceType", 0x03))),
                           ParseField("PermitJoining", 1),
                           PARSE_DEPTH,
                           PARSE_LQI ])]),
    0xb2: MTAPICmd("ZDO_MGMT_RTG_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     ParseField("RoutingTableEntries", 1),
                     PARSE_START_INDEX,
                     ParseRepeated(
                         "RoutingTableListCount",
                         "RoutingTableList",
                         [ PARSE_DST_ADDR,
                           ParseField("Status", 1,
                                      field_parse_routing_status),
                           ParseField("NextHop", 2,
                                      field_parse_hword)])]),
    0xb3: MTAPICmd("ZDO_MGMT_BIND_RSP",
                   [ PARSE_SRC_ADDR,
                     PARSE_STATUS,
                     ParseField("BindingTableEntries", 1),
                     PARSE_START_INDEX,
                     ParseRepeated(
                         "BindingTableListCount",
                         "BindingTableList",
                         [ PARSE_SRC_EXT_ADDR,
                           PARSE_SRC_EP,
                           PARSE_CLUSTER_ID,
                           PARSE_MODED_DST_ADDR,
                           PARSE_DST_EP])]),
    0xb4: MTAPICmd("ZDO_MGMT_LEAVE_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS ]),
    0xb5: MTAPICmd("ZDO_MGMT_DIRECT_JOIN_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS ]),
    0xb6: MTAPICmd("ZDO_MGMT_PERMIT_JOIN_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS ]),
    0xc0: MTAPICmd("ZDO_STATE_CHANGE_IND",
                   [ ParseField("State", 1) ]),
    0xc1: MTAPICmd("ZDO_END_DEVICE_ANNCE_IND",
                   [ PARSE_SRC_ADDR,
                     PARSE_NWK_ADDR,
                     PARSE_IEEE_ADDR,
                     PARSE_CAPABILITIES]),
    0xc2: MTAPICmd("ZDO_MATCH_DESC_RSP_SENT",
                   [ PARSE_NWK_ADDR,
                     PARSE_IN_CLUSTERS,
                     PARSE_OUT_CLUSTERS ]),
    0xc3: MTAPICmd("ZDO_STATUS_ERROR_RSP",
                   [ PARSE_SRC_ADDR, PARSE_STATUS ]),
    0xc4: MTAPICmd("ZDO_SRC_RTG_IND",
                   [ PARSE_DST_ADDR, PARSE_RELAY_LIST ]),
    0xc5: MTAPICmd("ZDO_BEACON_NOTIFY_IND",
                   [ ParseRepeated(
                       "BeaconCount",
                       "BeaconList",
                       [ PARSE_SRC_ADDR,
                         PARSE_PAN_ID,
                         PARSE_LOGICAL_CHANNEL,
                         ParseField("PermitJoining", 1),
                         ParseField("RouterCapacity", 1),
                         ParseField("DeviceCapacity", 1),
                         ParseField("ProtocolVersion", 1),
                         PARSE_STACK_PROFILE,
                         PARSE_LQI,
                         PARSE_DEPTH,
                         ParseField("UpdateId", 1),
                         PARSE_EXT_PAN_ID ])]),
    0xc6: MTAPICmd("ZDO_JOIN_CNF",
                   [ PARSE_STATUS,
                     PARSE_DEV_ADDR,
                     PARSE_PARENT_ADDR ]),
    0xc7: MTAPICmd("ZDO_NWK_DISCOVERY_CNF", [ PARSE_STATUS ]),
    0xc9: MTAPICmd("ZDO_LEAVE_IND",
                   [ PARSE_SRC_ADDR,
                     PARSE_EXT_ADDR,
                     ParseField("Request", 1),
                     ParseField("Remove", 1),
                     ParseField("Rejoin", 1) ]),
    0xff: MTAPICmd("ZDO_MSG_CB_INCOMING",
                   [ PARSE_SRC_ADDR,
                     PARSE_WAS_BROADCAST,
                     PARSE_CLUSTER_ID,
                     PARSE_SECURITY_USE,
                     PARSE_SEQ_NUM,
                     ParseField("MacDstAddr", 2, field_parse_hword),
                     ParseRemaining("Data")])
}


MT_COMMANDS = { ("SREQ", "AF"):    MT_AF_SREQ_CMDS,
                ("SRSP", "AF"):    MT_AF_SRSP_CMDS,
                ("AREQ", "AF"):    MT_AF_AREQ_CMDS,
                ("SREQ", "APP"):   MT_APP_SREQ_CMDS,
                ("SRSP", "APP"):   MT_APP_SRSP_CMDS,
                ("SREQ", "DEBUG"): MT_DEBUG_SREQ_CMDS,
                ("SRSP", "DEBUG"): MT_DEBUG_SRSP_CMDS,
                ("AREQ", "DEBUG"): MT_DEBUG_AREQ_CMDS,
                ("SREQ", "MAC"):   MT_MAC_SREQ_CMDS,
                ("SRSP", "MAC"):   MT_MAC_SRSP_CMDS,
                ("AREQ", "MAC"):   MT_MAC_AREQ_CMDS,
                ("SREQ", "SAPI"):  MT_SAPI_SREQ_CMDS,
                ("SRSP", "SAPI"):  MT_SAPI_SRSP_CMDS,
                ("AREQ", "SAPI"):  MT_SAPI_AREQ_CMDS,
                ("SREQ", "SYS"):   MT_SYS_SREQ_CMDS,
                ("SRSP", "SYS"):   MT_SYS_SRSP_CMDS,
                ("AREQ", "SYS"):   MT_SYS_AREQ_CMDS,
                ("SREQ", "UTIL"):  MT_UTIL_SREQ_CMDS,
                ("SRSP", "UTIL"):  MT_UTIL_SRSP_CMDS,
                ("AREQ", "UTIL"):  MT_UTIL_AREQ_CMDS,
                ("SREQ", "ZDO"):   MT_ZDO_SREQ_CMDS,
                ("SRSP", "ZDO"):   MT_ZDO_SRSP_CMDS,
                ("AREQ", "ZDO"):   MT_ZDO_AREQ_CMDS
}


class MTAPI:
    """State machine for managing serial comms reception from a device
    talking the MTAPI protocols."""
    def __init__(self, sock):
        """Create an MTAPI reception state machine and initialise it
        to expect a Start Of Frame byte."""
        self.sock = sock
        self.state = self.read_sof

    def read_sof(self):
        """State in which the protocol is expecting a start of frame
        (0xfe) byte."""
        byte = self.sock.read(1)
        if len(byte) == 1 and byte[0] == 0xfe:
            self.state = self.read_len

    def read_len(self):
        """State in which the protocol is expecting the first byte of
        an MTAPI header, the body length.  Will read the rest of the
        header if it is available."""
        byte = self.sock.read(3)
        if len(byte) == 0:
            return
        self.len = byte[0]
        self.state = self.read_cmd0
        if len(byte) > 1:
            self.read_cmd0(byte[1:])

    def read_cmd0(self, byte=None):
        """State in which the protocol is expecting the second byte of
        an MTAPI header, "CMD0", the type and subsystem byte.  Will
        read the rest of the header if it is available."""
        if byte is None:
            byte = self.sock.read(2)
        if len(byte) == 0:
            return
        self.type = MTAPIType(byte[0])
        self.subsystem = MTAPISubsystem(byte[0])
        self.state = self.read_cmd1
        if len(byte) > 1:
            self.read_cmd1(byte[1:])

    def read_cmd1(self, byte=None):
        """State in which the protocol is expecting the final byte of
        an MTAPI header, "CMD1", the subsystem command.  Does not
        attempt to read the body of the MTAPI packet, if there is one."""
        if byte is None:
            byte = self.sock.read(1)
        if len(byte) == 0:
            return
        self.cmd = byte[0]
        self.data = bytes(0)
        if self.len > 0:
            self.bytes_to_read = self.len
            self.state = self.read_data
        else:
            self.state = self.read_sof
            self.execute()

    def read_data(self):
        """State in which the protocol is reading bytes from the body
        of an MTAPI packet.   Once all bytes are read, the packet will
        be parsed and the state machine return to waiting for a start
        of frame."""
        bytestream = self.sock.read(self.bytes_to_read)
        if len(bytestream) == 0:
            return
        self.bytes_to_read -= len(bytestream)
        self.data = self.data + bytestream
        if self.bytes_to_read == 0:
            self.state = self.read_sof
            self.execute()

    def execute(self):
        """Parse the MTAPI packet read in, using the packet
        descriptions held in the MT_COMMANDS global variable.  The
        results are written to stdout."""
        print(self.type, self.subsystem, "Cmd = %02x" % self.cmd)
        key = (str(self.type), str(self.subsystem))
        if key in MT_COMMANDS:
            command_table = MT_COMMANDS[key]
            if self.cmd in command_table:
                command = command_table[self.cmd]
                print(" ", command.name)
                offset = command(self.data)
                if offset != len(self.data):
                    raise ParseError("Unparsed data in " + command.name)
        self.data = None

    def __call__(self):
        "Work the state machine."
        self.state()
        # Return value is True to continue execution, False to quit
        return True


class MTBuffer:
    """Class for constructing an MTAPI packet to transmit on the
    serial comms.  MTBuffers are specific to MTAPI commands, so are
    created on the fly."""
    def __init__(self, subsystem_name, mtype_name, command_name):
        """Create a transmission buffer for the MTAPI command defined
        by the subsystem, type and command names passed as
        parameters.  The command is looked up in the global variable
        MT_COMMANDS.  An mtapi.ParseError is raised if the command is
        not found."""
        dictionary = MT_COMMANDS[(mtype_name, subsystem_name)]
        for cmd_code, command in dictionary.items():
            if command.name == command_name:
                break
        else:
            raise ParseError("Unable to find command " + command_name)

        self.cmd = command
        self.buffer = bytearray(4)
        self.buffer[0] = 0xfe # SOF
        self.buffer[1] = 0
        self.buffer[2] = (MTAPIType.to_number(mtype_name) |
                          MTAPISubsystem.to_number(subsystem_name))
        self.buffer[3] = cmd_code

    def append(self, byte):
        """Adds a single byte to the transmission buffer.  Raises an
        mtapi.ParseError if this causes the buffer to overflow."""
        if self.buffer[1] == 0xff:
            raise ParseError("MT Buffer body overflow")
        self.buffer[1] += 1
        self.buffer.append(byte)

    def extend(self, iterable):
        """Adds a number of bytes to the transmission buffer.  Raises
        an mtapi.ParseError if this cases the buffer to overflow."""
        if self.buffer[1] + len(iterable) < self.buffer[1]:
            raise ParseError("MT Buffer body overflow")
        self.buffer[1] += len(iterable)
        self.buffer.extend(iterable)

    def send(self, socket):
        "Sends the assembled transmit buffer to the serial socket."
        socket.write(self.buffer)
