#! /usr/bin/env python3

# Unit tests for MT SYS command parsing

import base_test
import unittest


class BaseSysSReq(base_test.BaseTest):
    SUBSYSTEM = "SYS"
    TYPE = "SREQ"


class BaseNoParams:
    def test_no_params(self):
        self.run_test()


class TestSysPing(BaseNoParams, BaseSysSReq):
    COMMAND = 0x01
    COMMAND_NAME = "SYS_PING"


class TestSysVersion(BaseNoParams, BaseSysSReq):
    COMMAND = 0x02
    COMMAND_NAME = "SYS_VERSION"


class TestSysSetExtAddr(BaseSysSReq):
    COMMAND = 0x03
    COMMAND_NAME = "SYS_SET_EXTADDR"

    def test_set_extaddr(self):
        self.add_ieee("ExtAddr", (0x41, 0x42, 0x43, 0x44,
                                  0x45, 0x46, 0x47, 0x48))
        self.run_test()


class TestSysGetExtAddr(BaseNoParams, BaseSysSReq):
    COMMAND = 0x04
    COMMAND_NAME = "SYS_GET_EXTADDR"


class TestSysRamRead(BaseSysSReq):
    COMMAND = 0x05
    COMMAND_NAME = "SYS_RAM_READ"

    def test_ram_read(self):
        self.add_hword("Address", "7654", 0x7654)
        self.add_byte("Len", "0x06")
        self.run_test()


class TestSysRamWrite(BaseSysSReq):
    COMMAND = 0x06
    COMMAND_NAME = "SYS_RAM_WRITE"

    def test_ram_write(self):
        self.add_hword("Address", "1234", 0x1234)
        self.add_byte("Length", "2")
        self.add_bytes("Data", (0x23, 0xfa))
        self.run_test()


class TestSysOsalNvRead(BaseSysSReq):
    COMMAND = 0x08
    COMMAND_NAME = "SYS_OSAL_NV_READ"

    def test_nv_read(self):
        self.add_hword("Id", "6475", 0x6475)
        self.add_byte("Offset", "0x00")
        self.run_test()


class TestSysOsalNvWrite(BaseSysSReq):
    COMMAND = 0x09
    COMMAND_NAME = "SYS_OSAL_NV_WRITE"

    def test_nv_write(self):
        self.add_hword("Id", "0001", 1)
        self.add_byte("Offset", "0x00")
        self.add_byte("Length", "8")
        self.add_bytes("Data", (0x18, 0x19, 0x1a, 0x1b,
                                0x1c, 0x1d, 0x1e, 0x1f))
        self.run_test()


class TestSysOsalNvInit(BaseSysSReq):
    COMMAND = 0x07
    COMMAND_NAME = "SYS_OSAL_NV_ITEM_INIT"

    def test_nv_init(self):
        self.add_hword("Id", "0002", 2)
        self.add_hword("ItemLen", "0010", 0x10)
        self.add_byte("InitLen", "3")
        self.add_bytes("InitData", (0x00, 0x01, 0x02))
        self.run_test()


class TestSysOsalNvDelete(BaseSysSReq):
    COMMAND = 0x12
    COMMAND_NAME = "SYS_OSAL_NV_DELETE"

    def test_nv_delete(self):
        self.add_hword("Id", "0003", 3)
        self.add_hword("ItemLen", "0011", 0x11)
        self.run_test()


class TestSysOsalNvLength(BaseSysSReq):
    COMMAND = 0x13
    COMMAND_NAME = "SYS_OSAL_NV_LENGTH"

    def test_nv_length(self):
        self.add_hword("Id", "0004", 4)
        self.run_test()


class TestSysOsalStartTimer(BaseSysSReq):
    COMMAND = 0x0a
    COMMAND_NAME = "SYS_OSAL_START_TIMER"

    def test_start_timer(self):
        self.add_byte("Id", "0x00")
        self.add_hword("Timeout", "0112", 0x0112)
        self.run_test()


class TestSysOsalStopTimer(BaseSysSReq):
    COMMAND = 0x0b
    COMMAND_NAME = "SYS_OSAL_STOP_TIMER"

    def test_stop_timer(self):
        self.add_byte("Id", "0x01")
        self.run_test()


class TestSysRandom(BaseNoParams, BaseSysSReq):
    COMMAND = 0x0c
    COMMAND_NAME = "SYS_RANDOM"


class TestSysAdcRead(BaseSysSReq):
    COMMAND = 0x0d
    COMMAND_NAME = "SYS_ADC_READ"

    def test_adc_read(self):
        self.add_byte("Channel", "AIN2", 2)
        self.add_byte("Resolution", "10-bit", 1)
        self.run_test()


class TestSysGpio(BaseSysSReq):
    COMMAND = 0x0e
    COMMAND_NAME = "SYS_GPIO"

    def test_gpio(self):
        self.add_byte("Operation", "Set", 2)
        self.add_byte("Value", "0x5a")
        self.run_test()


class TestSysStackTune(BaseSysSReq):
    COMMAND = 0x0f
    COMMAND_NAME = "SYS_STACK_TUNE"

    def test_stack_tune(self):
        self.add_byte("Operation", "0x01")
        self.add_byte("Value", "0x66")
        self.run_test()


class TestSysSetTime(BaseSysSReq):
    COMMAND = 0x10
    COMMAND_NAME = "SYS_SET_TIME"

    def test_set_time(self):
        self.add_word("UTCTime", "0")
        self.add_byte("Hour", "7")
        self.add_byte("Minute", "31")
        self.add_byte("Second", "0")
        self.add_byte("Month", "2")
        self.add_byte("Day", "9")
        self.add_hword("Year", "14")
        self.run_test()


class TestSysGetTime(BaseNoParams, BaseSysSReq):
    COMMAND = 0x11
    COMMAND_NAME = "SYS_GET_TIME"


class TestSysSetTxPower(BaseSysSReq):
    COMMAND = 0x14
    COMMAND_NAME = "SYS_SET_TX_POWER"

    def test_set_tx_power(self):
        self.add_byte("TxPower", "0x1c")
        self.run_test()


class TestSysZDiagsInitStats(BaseNoParams, BaseSysSReq):
    COMMAND = 0x17
    COMMAND_NAME = "SYS_ZDIAGS_INIT_STATS"


class TestSysZDiagsClearStats(BaseSysSReq):
    COMMAND = 0x18
    COMMAND_NAME = "SYS_ZDIAGS_CLEAR_STATS"

    def test_clear_stats(self):
        self.add_byte("ClearNV", "0x01")
        self.run_test()


class TestSysZDiagsGetStats(BaseSysSReq):
    COMMAND = 0x19
    COMMAND_NAME = "SYS_ZDIAGS_GET_STATS"

    def test_get_stats(self):
        self.add_hword("AttributeId", "8642", 0x8642)
        self.run_test()


class TestSysZDiagsRestoreStatsNv(BaseNoParams, BaseSysSReq):
    COMMAND = 0x1a
    COMMAND_NAME = "SYS_ZDIAGS_RESTORE_STATS_NV"


class TestSysZDiagsSaveStatsToNv(BaseNoParams, BaseSysSReq):
    COMMAND = 0x1b
    COMMAND_NAME = "SYS_ZDIAGS_SAVE_STATS_TO_NV"


class TestSysNvCreate(BaseSysSReq):
    COMMAND = 0x30
    COMMAND_NAME = "SYS_NV_CREATE"

    def test_nv_create(self):
        self.add_byte("SysId", "0x01")
        self.add_hword("ItemId", "0002", 0x0002)
        self.add_hword("SubId", "0003", 0x0003)
        self.add_word("Length", "00000010", 0x0010)
        self.run_test()


class TestSysNvDelete(BaseSysSReq):
    COMMAND = 0x31
    COMMAND_NAME = "SYS_NV_DELETE"

    def test_nv_delete(self):
        self.add_byte("SysId", "0x02")
        self.add_hword("ItemId", "0003", 0x0003)
        self.add_hword("SubId", "0004", 0x0004)
        self.run_test()


class TestSysNvLength(BaseSysSReq):
    COMMAND = 0x32
    COMMAND_NAME = "SYS_NV_LENGTH"

    def test_nv_length(self):
        self.add_byte("SysId", "0x03")
        self.add_hword("ItemId", "0004", 0x0004)
        self.add_hword("SubId", "0005", 0x0005)
        self.run_test()


class TestSysNvRead(BaseSysSReq):
    COMMAND = 0x33
    COMMAND_NAME = "SYS_NV_READ"

    def test_nv_read(self):
        self.add_byte("SysId", "0x04")
        self.add_hword("ItemId", "0005", 0x0005)
        self.add_hword("SubId", "0006", 0x0006)
        self.add_hword("Offset", "0007", 0x0007)
        self.add_byte("Length", "0x08")
        self.run_test()


class TestSysNvWrite(BaseSysSReq):
    COMMAND = 0x34
    COMMAND_NAME = "SYS_NV_WRITE"

    def test_nv_write(self):
        self.add_byte("SysId", "0x05")
        self.add_hword("ItemId", "0006", 0x0006)
        self.add_hword("SubId", "0007", 0x0007)
        self.add_hword("Offset", "0008", 0x0008)
        self.add_byte("Length", "4")
        self.add_bytes("Data", (0x22, 0x44, 0x66, 0x88))
        self.run_test()


class TestSysNvUpdate(BaseSysSReq):
    COMMAND = 0x35
    COMMAND_NAME = "SYS_NV_UPDATE"

    def test_nv_update(self):
        self.add_byte("SysId", "0x06")
        self.add_hword("ItemId", "0006", 0x0006)
        self.add_hword("SubId", "0008", 0x0008)
        self.add_byte("Length", "3")
        self.add_bytes("Data", (0x1f, 0x2e, 0x3d))
        self.run_test()


class TestSysNvCompact(BaseSysSReq):
    COMMAND = 0x36
    COMMAND_NAME = "SYS_NV_COMPACT"

    def test_nv_compact(self):
        self.add_hword("Threshold", "0006", 6)
        self.run_test()


class TestSysOsalNvReadExt(BaseSysSReq):
    COMMAND = 0x1c
    COMMAND_NAME = "SYS_OSAL_NV_READ_EXT"

    def test_nv_read_ext(self):
        self.add_hword("Id", "0009", 0x0009)
        self.add_hword("Offset", "000a", 0x000a)
        self.run_test()


class TestSysOsalNvWriteExt(BaseSysSReq):
    COMMAND = 0x1d
    COMMAND_NAME = "SYS_OSAL_NV_WRITE_EXT"

    def test_nv_write_ext(self):
        self.add_hword("Id", "000a", 0x000a)
        self.add_hword("Offset", "000b", 0x000b)
        self.add_byte("Length", "7")
        self.add_bytes("Data", (0x01, 0x02, 0x03, 0x04,
                                0x05, 0x06, 0x07))
        self.run_test()


if __name__ == "__main__":
    unittest.main()
