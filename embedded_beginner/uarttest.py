# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 09:59:37 2022

@author: LAKKA

ONLY FOR LINUX

WILL NOT WORK ON WINDOWS
"""


import sys
import time

import numpy as np

from math import ceil
from serial import Serial as Ser
from multiprocessing import Process, Value, Manager


def send_task(ser, data, blkcnt, index, timeout):
    for i in range(blkcnt):
        btime = time.time()
        while(index.value != i):
            if(time.time() - btime > timeout):
                return
            pass
        ser.write(data[i])
    return


def recv_task(ser, recvlen, blkcnt, index, q):
    buf = [0 for i in range(blkcnt)]
    for i in range(blkcnt):
        buf[i] = ser.read(recvlen)
        index.value += 1
    q.put(buf)
    return


def test_work(bps, trytimes, blkcnt, blksize, sername0, sername1=None):
    # 生成随机测试值
    # 通过给定seed，固定测试值
    np.random.seed(0)
    test_pattern = [
        np.random.randint(low=256, size=blksize, dtype='uint8').tobytes()
        for i in range(blkcnt)]

    manager = Manager()

    maxrate = 0
    maxpassrate = 0

    for i in range(trytimes):
        timeoutv = (blksize*10 / bps + 500)/1000.0

        index0 = Value('i', 0)
        index1 = 0
        q0 = manager.JoinableQueue()
        q1 = 0
        ser0 = Ser(
            port=sername0, baudrate=remap(bps),
            timeout=timeoutv, exclusive=False)
        ser1 = 0
        if(sername1 is not None):
            index1 = Value('i', 0)
            q1 = manager.JoinableQueue()
            ser1 = Ser(
                port=sername1, baudrate=remap(bps),
                timeout=timeoutv, exclusive=False)

        starttime = 0
        endtime = 0

        if(sername1 is None):
            psend0 = Process(target=send_task, args=(
                ser0, test_pattern, blkcnt, index0, timeoutv))
            precv0 = Process(target=recv_task, args=(
               ser0, blksize, blkcnt, index0, q0))

            starttime = time.time()
            psend0.start()
            precv0.start()
            psend0.join()
            precv0.join()
            endtime = time.time()

            ser0.close()
        else:
            psend0 = Process(target=send_task, args=(
                ser0, test_pattern, blkcnt, index0, timeoutv))
            precv0 = Process(target=recv_task, args=(
               ser0, blksize, blkcnt, index0, q0))
            psend1 = Process(target=send_task, args=(
                ser1, test_pattern, blkcnt, index1, timeoutv))
            precv1 = Process(target=recv_task, args=(
               ser1, blksize, blkcnt, index1, q1))

            starttime = time.time()
            psend0.start()
            precv0.start()
            psend1.start()
            precv1.start()
            psend0.join()
            precv0.join()
            psend1.join()
            precv1.join()
            endtime = time.time()

            ser0.close()
            ser1.close()

        buf0 = q0.get()
        passcnt = 0
        targetcnt = blkcnt
        for j, d in enumerate(buf0):
            if(d == test_pattern[j]):
                passcnt += 1
        if(sername1 is not None):
            buf1 = q1.get()
            targetcnt += blkcnt
            for j, d in enumerate(buf1):
                if(d == test_pattern[j]):
                    passcnt += 1
        passrate = passcnt/targetcnt
        datarate = blksize*targetcnt/1000/(endtime-starttime)
        if(passrate > maxpassrate):
            maxpassrate = passrate
        if(passrate == 1):
            print("Cycle:{0}, Timecost:{1:.4f}".format(i, endtime-starttime))
            print("Daterate:{0:.2f}kBps".format(datarate))
            if(datarate > maxrate):
                maxrate = datarate
        else:
            print("Cycle:{0}, Transmission error".format(i))
            print("Passrate:{0:.2f}".format(passrate))
    return (maxpassrate, maxrate)


def genbps(n):
    # 最小速率 = 96M / 96
    # 最大速率 = 96M / 8
    # n = 8~96
    return ceil(96_000_000 / n)


def remap(bps):
    if(bps <= 3000000):
        return bps
    return (bps/10000)+10000


trytimes = 4
blkcnt = 10
blksize = 10000
sername0 = "/dev/ttyUSB0"
sername1 = None

if sys.platform != "linux":
    print("ONLY FOR LINUX")
    exit(-1)

print("Usage : python3 uarttest.py port0 [port1 cycles block_size block_cnt]")
print("        python3 uarttest.py /dev/ttyUSB0")
print("        python3 uarttest.py /dev/ttyUSB0 /dev/ttyUSB1")
print("        python3 uarttest.py /dev/ttyUSB0 /dev/ttyUSB1 4 10000 10")

if len(sys.argv) < 2:
    exit(-1)

sername0 = sys.argv[1]

if(len(sys.argv) > 2):
    sername1 = sys.argv[2]
if(len(sys.argv) > 3):
    trytimes = int(sys.argv[3])
if(len(sys.argv) > 4):
    blksize = int(sys.argv[4])
if(len(sys.argv) > 5):
    blkcnt = int(sys.argv[5])


for n in range(96, 7, -1):
    bps = genbps(n)
    print("Test with bps:{0}".format(bps))
    result = test_work(bps, trytimes, blkcnt, blksize, sername0, sername1)
    print()
    if(result[0] != 1):
        print("bps:{0}, not passed, passrate:{1:.2f}".format(bps, result[0]))
        print("try again with more chances")
        result = test_work(bps, trytimes*4,
                           blkcnt, blksize, sername0, sername1)
        if(result[0] != 1):
            print("bps:{0}, not passed, passrate:{1:.2f}".
                  format(bps, result[0]))
            print("Failed")
            break
        else:
            print("bps:{0}, Daterate:{1:.2f}kBps".format(bps, result[1]))
    else:
        print("bps:{0}, Daterate:{1:.2f}kBps".format(bps, result[1]))
    print()
