#!/usr/bin/env python3
import re
import sys
import argparse

def convert_c_array_to_bin(input_file, output_file):
    """Convert a C uint8_t array to a binary file."""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Find the array declaration
    # This regex looks for uint8_t array_name[size] = { ... };
    pattern = r'uint8_t\s+\w+\s*\[\s*\d+\s*\]\s*=\s*\{([^}]+)\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Error: Could not find uint8_t array declaration")
        print("Make sure the .h file contains a uint8_t array with hex values")
        return False
    
    # Extract the hex values
    hex_values = match.group(1)
    
    # Parse hex values (0x00, 0x01, etc.)
    hex_pattern = r'0x([0-9A-Fa-f]{2})'
    bytes_list = []
    
    for hex_match in re.findall(hex_pattern, hex_values):
        bytes_list.append(int(hex_match, 16))
    
    if len(bytes_list) != 8192:
        print(f"Warning: Expected 8192 bytes, found {len(bytes_list)}")
        if len(bytes_list) < 8192:
            bytes_list.extend([0] * (8192 - len(bytes_list)))
        else:
            bytes_list = bytes_list[:8192]
    
    # Write to binary file
    with open(output_file, 'wb') as f:
        f.write(bytes(bytes_list))
    
    print(f"Successfully converted {len(bytes_list)} bytes to {output_file}")
    return True

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert C header sprite sheet to PicoPanda binary format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sprite_sheet.h sprite_sheet.bin
  %(prog)s -h

The script converts a C header file containing a uint8_t array declaration
to a 8192-byte binary file (128x128 pixels, 4-bit greyscale).

Expected format in .h file:
  uint8_t sprite_sheet[8192] = { 0x00, 0x01, 0x02, ... };
        """
    )
    
    parser.add_argument("input_file", 
                       help="Input C header file (.h) with uint8_t array declaration")
    parser.add_argument("output_file", 
                       help="Output binary file")
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    
    # Check if input file has .h extension
    if not input_file.lower().endswith('.h'):
        print("Error: Input file must be a C header file (.h)")
        sys.exit(1)
    
    # Convert C array to binary
    if not convert_c_array_to_bin(input_file, output_file):
        print("Error: Could not convert file")
        print("Make sure the .h file contains a uint8_t array declaration with hex values")
        sys.exit(1)

if __name__ == "__main__":
    main() 