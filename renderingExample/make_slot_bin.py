# save as make_slot_bin.py
import sys
script_path = sys.argv[1]
out_path = sys.argv[2]
slot_size = 0x20000  # 128KB
with open(script_path, "rb") as f:
    data = f.read()
with open(out_path, "wb") as out:
    out.write(len(data).to_bytes(4, "little"))
    out.write(data)
    # Pad with 0xFF to 128KB
    out.write(b'\xFF' * (slot_size - 4 - len(data)))