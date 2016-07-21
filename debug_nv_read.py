#! /usr/bin/env python3

import base_test
import mtcmds


sock = base_test.MockSock(bytes((0xfe, 0x03, 0x21, 0x08,
                                 0x75, 0x64, 0x00)))
mtapi = mtcmds.MTAPI(sock)
mtapi()
while mtapi.state != mtapi.read_sof:
    mtapi()
