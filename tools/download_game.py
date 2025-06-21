import serial
import time
import sys
import os
import argparse

BINARY_SIZE = 128 * 1024  # 128kB

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Download a PicoPanda game binary from the device via UART",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p /dev/ttyACM0 -b 115200
  %(prog)s -p /dev/tty.usbmodem144702 -b 115200 -o ./downloads
  %(prog)s -p /dev/ttyACM0 -b 115200 -o ./downloads -v game_slot0.bin
  %(prog)s -h

The script will:
1. Send DOWNLOAD command to Pico
2. Prompt for game slot number
3. Receive the binary data (128KB)
4. Save to specified folder and optionally verify against provided file
        """
    )
    
    parser.add_argument("-p", "--port", 
                       required=True,
                       help="Serial port (e.g., /dev/ttyACM0, /dev/tty.usbmodem144702)")
    parser.add_argument("-b", "--baud", 
                       type=int, required=True,
                       help="Baud rate (e.g., 115200)")
    parser.add_argument("-o", "--output", 
                       default=".",
                       help="Output folder for downloaded file (default: current directory)")
    parser.add_argument("-v", "--verify", 
                       help="Binary file to verify against (optional)")
    
    args = parser.parse_args()
    
    PORT = args.port
    BAUD = args.baud
    OUTPUT_DIR = args.output
    VERIFY_FILE = args.verify

    # Check if output directory exists, create if it doesn't
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            print(f"Created output directory: {OUTPUT_DIR}")
        except OSError as e:
            print(f"Error: Could not create output directory '{OUTPUT_DIR}': {e}")
            sys.exit(1)

    try:
        with serial.Serial(PORT, BAUD, timeout=2) as ser:
            time.sleep(0.5)
            ser.reset_input_buffer()

            # 1. Send DOWNLOAD command
            print("Sending DOWNLOAD command...")
            ser.write(b'DOWNLOAD\n')
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

            # 5. Receive the binary data
            print(f"Receiving {BINARY_SIZE} bytes... (this will take ~12 seconds)")
            received_data = b""
            bytes_received = 0
            
            while bytes_received < BINARY_SIZE:
                if ser.in_waiting:
                    chunk = ser.read(ser.in_waiting)
                    received_data += chunk
                    bytes_received += len(chunk)
                    # Print progress
                    if bytes_received % 1024 == 0:
                        print(f"Received: {bytes_received}/{BINARY_SIZE} bytes")
                time.sleep(0.01)
            
            print(f"Download complete! Received {len(received_data)} bytes")
            
            # 6. Save to file in specified directory
            filename = f"downloaded_slot_{slot_number}.bin"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(received_data)
            print(f"Saved to {filepath}")
            
            # 7. Verify against provided file if specified
            if VERIFY_FILE:
                if os.path.exists(VERIFY_FILE):
                    with open(VERIFY_FILE, 'rb') as f:
                        original_data = f.read()
                    if received_data == original_data:
                        print("✓ Verification successful! Files match.")
                    else:
                        print("✗ Verification failed! Files differ.")
                        # Find first difference
                        for i, (orig, recv) in enumerate(zip(original_data, received_data)):
                            if orig != recv:
                                print(f"First difference at byte {i}: original=0x{orig:02x}, received=0x{recv:02x}")
                                break
                else:
                    print(f"Error: Verification file '{VERIFY_FILE}' not found.")
                    sys.exit(1)
            else:
                print("Skipping verification (no file specified)")

    except serial.SerialException as e:
        print(f"Error: Serial connection failed - {e}")
        print(f"Please check that port '{PORT}' exists and is accessible.")
        sys.exit(1)

if __name__ == "__main__":
    main() 