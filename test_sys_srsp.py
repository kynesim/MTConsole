#! /usr/bin/env python3

# Unit tests for MT SYS SRSP command (response) parsing

import base_test
import unittest


class BaseSysSRsp(base_test.BaseTest):
    SUBSYSTEM = "SYS"
    TYPE = "SRSP"


class BaseStatus:
    def test_status_ok(self):
        self.add_byte("Status", "Success", 0)
        self.run_test()

    def test_status_fail(self):
        self.add_byte("Status", "Failed", 1)
        self.run_test()

    def test_status_created(self):
        self.add_byte("Status", "Success (no previous item)", 0x09)
        self.run_test()

    def test_status_not_done(self):
        self.add_byte("Status", "Initialisation/Deletion Failed", 0x0a)
        self.run_test()

    def test_status_bad_length(self):
        self.add_byte("Status", "Bad Length", 0x0c)
        self.run_test()


class TestSysPing(BaseSysSRsp):
    COMMAND = 0x01
    COMMAND_NAME = "SYS_PING"

    def test_pong(self):
        self.add_hword("Capabilities",
                       "000b (MT_CAP_SYS, MT_CAP_MAC, MT_CAP_AF)",
                       0x000b)
        self.run_test()


class TestSysVersion(BaseSysSRsp):
    COMMAND = 0x02
    COMMAND_NAME = "SYS_VERSION"

    def test_version(self):
        self.add_byte("TransportRev", "0x01")
        self.add_byte("ProductId", "0x02")
        self.add_byte("MajorRel", "0x03")
        self.add_byte("MinorRel", "0x04")
        self.add_byte("MaintRel", "0x05")
        self.run_test()


class TestSysSetExtAddr(BaseStatus, BaseSysSRsp):
    COMMAND = 0x03
    COMMAND_NAME = "SYS_SET_EXTADDR"


class TestSysGetExtAddr(BaseSysSRsp):
    COMMAND = 0x04
    COMMAND_NAME = "SYS_GET_EXTADDR"

    def test_get_extaddr(self):
        self.add_ieee("ExtAddr", (0x41, 0x42, 0x43, 0x44,
                                  0x45, 0x46, 0x47, 0x48))
        self.run_test()


class TestSysRamRead(BaseSysSRsp):
    COMMAND = 0x05
    COMMAND_NAME = "SYS_RAM_READ"

    def test_ram_read(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Length", "3")
        self.add_bytes("Data", (0x11, 0x12, 0x13))
        self.run_test()


class TestSysRamWrite(BaseStatus, BaseSysSRsp):
    COMMAND = 0x06
    COMMAND_NAME = "SYS_RAM_WRITE"


class TestSysOsalNvRead(BaseSysSRsp):
    COMMAND = 0x08
    COMMAND_NAME = "SYS_OSAL_NV_READ"

    def test_nv_read(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Length", "5")
        self.add_bytes("Data", (0x21, 0x22, 0x23, 0x24, 0x25))
        self.run_test()


class TestSysOsalNvWrite(BaseStatus, BaseSysSRsp):
    COMMAND = 0x09
    COMMAND_NAME = "SYS_OSAL_NV_WRITE"


class TestSysOsalNvInit(BaseStatus, BaseSysSRsp):
    COMMAND = 0x07
    COMMAND_NAME = "SYS_OSAL_NV_ITEM_INIT"


class TestSysOsalNvDelete(BaseStatus, BaseSysSRsp):
    COMMAND = 0x12
    COMMAND_NAME = "SYS_OSAL_NV_DELETE"


class TestSysOsalNvLength(BaseSysSRsp):
    COMMAND = 0x13
    COMMAND_NAME = "SYS_OSAL_NV_LENGTH"

    def test_nv_length(self):
        self.add_hword("ItemLen", "0021", 0x21)
        self.run_test()


class TestSysOsalStartTimer(BaseStatus, BaseSysSRsp):
    COMMAND = 0x0a
    COMMAND_NAME = "SYS_OSAL_START_TIMER"


class TestSysOsalStopTimer(BaseStatus, BaseSysSRsp):
    COMMAND = 0x0b
    COMMAND_NAME = "SYS_OSAL_STOP_TIMER"


class TestSysRandom(BaseSysSRsp):
    COMMAND = 0x0c
    COMMAND_NAME = "SYS_RANDOM"

    def test_random(self):
        self.add_hword("Value", "6842", 0x6842)
        self.run_test()


class TestSysAdcRead(BaseSysSRsp):
    COMMAND = 0x0d
    COMMAND_NAME = "SYS_ADC_READ"

    def test_adc_read(self):
        self.add_hword("Value", "c28a", 0xc28a)
        self.run_test()


class TestSysGpio(BaseSysSRsp):
    COMMAND = 0x0e
    COMMAND_NAME = "SYS_GPIO"

    def test_gpio(self):
        self.add_byte("Value", "0xa5")
        self.run_test()


class TestSysStackTune(BaseSysSRsp):
    COMMAND = 0x0f
    COMMAND_NAME = "SYS_STACK_TUNE"

    def test_stack_tune(self):
        self.add_byte("Value", "0x99")
        self.run_test()


class TestSysSetTime(BaseStatus, BaseSysSRsp):
    COMMAND = 0x10
    COMMAND_NAME = "SYS_SET_TIME"


class TestSysGetTime(BaseSysSRsp):
    COMMAND = 0x11
    COMMAND_NAME = "SYS_GET_TIME"

    def test_get_time(self):
        self.add_word("UTCTime", "0")
        self.add_byte("Hour", "14")
        self.add_byte("Minute", "27")
        self.add_byte("Second", "2")
        self.add_byte("Month", "12")
        self.add_byte("Day", "25")
        self.add_hword("Year", "15")
        self.run_test()


class TestSysSetTxPower(BaseSysSRsp):
    COMMAND = 0x14
    COMMAND_NAME = "SYS_SET_TX_POWER"

    def test_set_tx_power(self):
        self.add_byte("TxPower", "0x1c")
        self.run_test()


class TestSysZDiagsInitStats(BaseStatus, BaseSysSRsp):
    COMMAND = 0x17
    COMMAND_NAME = "SYS_ZDIAGS_INIT_STATS"


class TestSysZDiagsClearStats(BaseSysSRsp):
    COMMAND = 0x18
    COMMAND_NAME = "SYS_ZDIAGS_CLEAR_STATS"

    def test_clear_stats(self):
        self.add_word("SysClock", "12345678", 0x12345678)
        self.run_test()


class TestSysZDiagsGetStats(BaseSysSRsp):
    COMMAND = 0x19
    COMMAND_NAME = "SYS_ZDIAGS_GET_STATS"

    def test_get_stats(self):
        self.add_word("AttributeValue", "98765432", 0x98765432)
        self.run_test()


class TestSysZDiagsRestoreStatsNv(BaseStatus, BaseSysSRsp):
    COMMAND = 0x1a
    COMMAND_NAME = "SYS_ZDIAGS_RESTORE_STATS_NV"


class TestSysZDiagsSaveStatsToNv(BaseSysSRsp):
    COMMAND = 0x1b
    COMMAND_NAME = "SYS_ZDIAGS_SAVE_STATS_TO_NV"

    def test_clear_stats(self):
        self.add_word("SysClock", "12345678", 0x12345678)
        self.run_test()


class TestSysNvCreate(BaseStatus, BaseSysSRsp):
    COMMAND = 0x30
    COMMAND_NAME = "SYS_NV_CREATE"


class TestSysNvDelete(BaseStatus, BaseSysSRsp):
    COMMAND = 0x31
    COMMAND_NAME = "SYS_NV_DELETE"


class TestSysNvLength(BaseSysSRsp):
    COMMAND = 0x32
    COMMAND_NAME = "SYS_NV_LENGTH"

    def test_nv_length(self):
        self.add_byte("Length", "0x13")
        self.run_test()


class TestSysNvRead(BaseSysSRsp):
    COMMAND = 0x33
    COMMAND_NAME = "SYS_NV_READ"

    def test_nv_read(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Length", "8")
        self.add_bytes("Data", (0x11, 0x33, 0x55, 0x77,
                                0x99, 0xbb, 0xdd, 0xff))
        self.run_test()


class TestSysNvWrite(BaseStatus, BaseSysSRsp):
    COMMAND = 0x34
    COMMAND_NAME = "SYS_NV_WRITE"


class TestSysNvUpdate(BaseStatus, BaseSysSRsp):
    COMMAND = 0x35
    COMMAND_NAME = "SYS_NV_UPDATE"


class TestSysNvCompact(BaseStatus, BaseSysSRsp):
    COMMAND = 0x36
    COMMAND_NAME = "SYS_NV_COMPACT"


class TestSysOsalNvReadExt(BaseSysSRsp):
    COMMAND = 0x1c
    COMMAND_NAME = "SYS_OSAL_NV_READ_EXT"

    def test_nv_read_ext(self):
        self.add_byte("Status", "Success", 0)
        self.add_byte("Length", "3")
        self.add_bytes("Data", (0x78, 0x87, 0x96))
        self.run_test()


class TestSysOsalNvWriteExt(BaseStatus, BaseSysSRsp):
    COMMAND = 0x1d
    COMMAND_NAME = "SYS_OSAL_NV_WRITE_EXT"


if __name__ == "__main__":
    unittest.main()
