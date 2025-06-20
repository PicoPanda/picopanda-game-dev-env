import serial
import time
import sys
import os

# Change this to your Pico's serial port
PORT = '/dev/tty.usbmodem144702'
BAUD = 115200
BIN_PATH = 'game_slot0.bin'
BINARY_SIZE = 128 * 1024  # 128kB

def main():
    # Read the binary file
    if not os.path.exists(BIN_PATH):
        print(f"Binary file '{BIN_PATH}' not found.")
        sys.exit(1)
    with open(BIN_PATH, 'rb') as f:
        data = f.read()
    if len(data) != BINARY_SIZE:
        print(f"Binary file size is {len(data)} bytes, expected {BINARY_SIZE} bytes.")
        sys.exit(1)

    try:
        with serial.Serial(PORT, BAUD, timeout=2) as ser:
            # Give the Pico a moment to reset if needed
            time.sleep(0.5)
            # Flush any old input
            ser.reset_input_buffer()

            # 1. Send UPLOAD command
            print("Sending UPLOAD command...")
            ser.write(b'UPLOAD\n')
            ser.flush()

            # 2. Wait for the "Enter Game Slot: " prompt
            prompt = ser.read_until(b': ')
            print("Pico:", prompt.decode(errors='replace').strip())
            if b'Enter Game Slot: ' not in prompt:
                print("Error: Did not receive game slot prompt from Pico.")
                sys.exit(1)
            
            # 3. Get slot number from the user
            slot_number = input("Enter Game Slot: ")
            if not slot_number.isdigit():
                print("Error: Please enter a valid number.")
                sys.exit(1)
            
            # 4. Send the chosen slot number
            print(f"Sending slot number {slot_number}...")
            ser.write(f"{slot_number}\n".encode())
            ser.flush()

            # 5. Wait for the "READY" response from the Pico
            response = ser.readline()
            print("Pico:", response.decode(errors='replace').strip())
            if b'READY' not in response:
                print("Error: Did not receive READY signal from Pico.")
                sys.exit(1)
            
            # 6. Send the binary data
            print(f"Sending {BINARY_SIZE} bytes... (this will take ~12 seconds)")
            ser.write(data)
            ser.flush()

            # 7. Wait for "OK" confirmation
            # We need a long timeout here because of the data transfer time.
            t0 = time.time()
            response = b""
            while time.time() - t0 < 15: # ~12s for data + buffer
                if ser.in_waiting:
                    response += ser.read(ser.in_waiting)
                    if b'OK' in response:
                        break
                time.sleep(0.01)
            
            print("Pico:", response.decode(errors='replace').strip())
            if b'OK' in response:
                print("Upload complete!")
            else:
                print("Timeout or error waiting for OK from Pico after upload.")
                sys.exit(1)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()