import serial
import time
import sys
import os
import argparse

BINARY_SIZE = 128 * 1024  # 128kB

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Upload a PicoPanda game binary to the device via UART",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p /dev/ttyACM0 -f game_slot0.bin
  %(prog)s -p /dev/tty.usbmodem144702 -f game_slot1.bin -b 115200
  %(prog)s -h

The script will:
1. Send UPLOAD command to Pico
2. Prompt for game slot number
3. Send the binary data (128KB)
4. Wait for confirmation
        """
    )
    
    parser.add_argument("-p", "--port", 
                       required=True,
                       help="Serial port (e.g., /dev/ttyACM0, /dev/tty.usbmodem144702)")
    parser.add_argument("-b", "--baud", 
                       type=int, required=True,
                       help="Baud rate (e.g., 115200)")
    parser.add_argument("-f", "--file", 
                       required=True,
                       help="Binary file to upload")
    
    args = parser.parse_args()
    
    PORT = args.port
    BAUD = args.baud
    BIN_PATH = args.file

    # Read the binary file
    if not os.path.exists(BIN_PATH):
        print(f"Error: Binary file '{BIN_PATH}' not found.")
        sys.exit(1)
    with open(BIN_PATH, 'rb') as f:
        data = f.read()
    if len(data) != BINARY_SIZE:
        print(f"Error: Binary file size is {len(data)} bytes, expected {BINARY_SIZE} bytes.")
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
            
            if b'OK' in response:
                print("Upload complete!")
            else:
                print("Timeout or error waiting for OK from Pico after upload.")
                sys.exit(1)

    except serial.SerialException as e:
        print(f"Error: Serial connection failed - {e}")
        print(f"Please check that port '{PORT}' exists and is accessible.")
        sys.exit(1)

if __name__ == "__main__":
    main()