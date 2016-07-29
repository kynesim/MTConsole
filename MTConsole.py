#! /usr/bin/env python3

# MTConsole.py
#
# A serial console for accessing a CC2538 use the MTAPI protocol
#
# Author: Rhodri James (rhodri@kynesim.co.uk)
# Date: 20 April 2016
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

import serial
import selectors
import sys
import argparse

import keyboard
import mtcmds


parser = argparse.ArgumentParser(description="MTAPI Console")
parser.add_argument("-s", "--serial", default="/dev/ttyUSB0",
                    help="Serial device to connect to "
                    "(default: %(default)s)")
parser.add_argument("-b", "--baud", type=int, default="115200",
                    help="Baud rate (default: %(default)s)")
args = parser.parse_args()


sock = serial.Serial(args.serial, args.baud, timeout=0)
with selectors.DefaultSelector() as selector:
    mtapi_rx = mtcmds.MTAPI(sock)
    keyhandler = keyboard.UIHandler(sock)
    selector.register(sock, selectors.EVENT_READ, mtapi_rx)
    selector.register(sys.stdin, selectors.EVENT_READ, keyhandler)
    running = True
    while running:
        events = selector.select()
        for key, _ in events:
            running = key.data() and running
