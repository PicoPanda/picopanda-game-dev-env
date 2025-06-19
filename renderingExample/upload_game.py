import serial
import sys

port = '/dev/tty.usbmodem144401'  # Change to your Pico's port
baud = 115200
slot_offset = 0x10100000
bin_path = 'game_slot0.bin'

with open(bin_path, 'rb') as f:
    data = f.read()

ser = serial.Serial(port, baud, timeout=2)
ser.write(f'UPLOAD {slot_offset:x} {len(data)}\n'.encode())
resp = ser.readline()
print('Pico:', resp.decode().strip())
if b'READY' not in resp:
    print('Did not get READY')
    sys.exit(1)

ser.write(data)
resp = ser.readline()
print('Pico:', resp.decode().strip())
ser.close()