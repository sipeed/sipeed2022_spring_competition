import serial, sys, time
from multiprocessing import Process

def send_task(ser, data, blk_size, int_ms):
  total_n = len(data)
  idx = 0
  sendcnt = 0
  while idx < total_n:
    sendcnt += ser.write(data[idx:idx+blk_size])
    idx += blk_size
    time.sleep(int_ms/1000)

  print("write %d bytes"%sendcnt)
  return

print("Usage : python3 uarttest.py port baudrate block_size block_cnt int_ms:")
print("        python3 uarttest.py /dev/ttyUSBx 2000000 1000 1000 10")

if len(sys.argv) < 6:
  exit(-1)

portx   = sys.argv[1]
bps     = int(sys.argv[2])
blk_size= int(sys.argv[3])
blk_n   = int(sys.argv[4])
int_ms  = int(sys.argv[5])
print("use port %s"%portx)
total_n = blk_n*blk_size
test_data = bytearray(total_n)
for i in range(total_n):
  test_data[i] = i%256

timex=total_n*10/bps*2 + int_ms*blk_n/1000 #超时单位s
if timex < 1:
  timex = 1
print("baudrate %d, send %d bytes, timeout %.3fs"%(bps, total_n, timex))
if bps > 3000000:  #3.2, 4, 4.8, 6, 6.4, 8, 9.6, 12
  bps = (bps/10000) + 10000  #高波特率重映射
  print("bps remap to %d"%bps)
ser=serial.Serial(portx,bps,timeout=timex)

p = Process(target=send_task, args=(ser, test_data, blk_size, int_ms))
p.start()
rcvdata = ser.read(total_n)
p.join()
ser.close()

rcv_n = len(rcvdata)
print("rcv %d bytes"%rcv_n)
if(len(rcvdata) != total_n):
  print("lost %d bytes (%.6f)"%(total_n-rcv_n, (total_n-rcv_n)/total_n))
  exit(-1)

err_n = 0
for i in range(total_n):
  if rcvdata[i] != (i%256):
    print("rcv[%d] err! %d -> %d"%(i, i%256, rcvdata[i]))
    err_n += 1
print("Total err %d bytes (%.6f)"%(err_n, err_n/total_n))

