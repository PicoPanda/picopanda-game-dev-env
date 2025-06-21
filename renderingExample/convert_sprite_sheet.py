#!/usr/bin/env python3
import re
import sys

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

def convert_hex_dump_to_bin(input_file, output_file):
    """Convert a hex dump file to binary."""
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    bytes_list = []
    
    for line in lines:
        # Remove comments and whitespace
        line = re.sub(r'//.*$', '', line).strip()
        if not line:
            continue
            
        # Extract hex values
        hex_values = re.findall(r'[0-9A-Fa-f]{2}', line)
        for hex_val in hex_values:
            bytes_list.append(int(hex_val, 16))
    
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_sprite_sheet.py <input_file> <output_file>")
        print("  input_file: C header file with uint8_t array or hex dump")
        print("  output_file: Binary file to create")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Try both conversion methods
    if not convert_c_array_to_bin(input_file, output_file):
        print("Trying hex dump conversion...")
        if not convert_hex_dump_to_bin(input_file, output_file):
            print("Error: Could not convert file")
            sys.exit(1) 