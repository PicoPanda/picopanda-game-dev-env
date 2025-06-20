import serial
import time
import sys
import os

# Change this to your Pico's serial port
PORT = '/dev/tty.usbmodem144702'
BAUD = 115200
BINARY_SIZE = 128 * 1024  # 128kB

def main():
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
            
            # 6. Save to file for verification
            filename = f"downloaded_slot_{slot_number}.bin"
            with open(filename, 'wb') as f:
                f.write(received_data)
            print(f"Saved to {filename}")
            
            # 7. Optional: Compare with original if it exists
            original_file = f"game_slot{slot_number}.bin"
            if os.path.exists(original_file):
                with open(original_file, 'rb') as f:
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
                print(f"Original file {original_file} not found for comparison.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 