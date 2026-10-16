#!/usr/bin/env python3
"""
tools/scribble_sync.py — USB-C companion sync tool for The Scribble.
Connects to The Scribble over USB serial to list and download Markdown (.md) notes.
"""

import os
import sys
import time
import argparse

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    serial = None

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Documents/TheScribbleNotes")

def find_scribble_port():
    if not serial:
        print("pyserial is not installed. Run: pip install pyserial")
        return None
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # Match Espressif USB JTAG / serial or CP210x / CH340 / USB serial
        desc = (p.description or "").lower()
        mfg = (p.manufacturer or "").lower()
        if "espressif" in desc or "espressif" in mfg or "usb jtag" in desc or "cp210" in desc or "ch340" in desc:
            return p.device
    if ports:
        print(f"Available serial ports: {[p.device for p in ports]}")
    return None

def sync_notes(port=None, output_dir=DEFAULT_OUTPUT_DIR, baud=115200):
    os.makedirs(output_dir, exist_ok=True)
    target_port = port or find_scribble_port()
    if not target_port:
        print("ERROR: The Scribble device was not detected on USB. Check cable connection.")
        return False
    print(f"Connecting to The Scribble on {target_port} at {baud} baud...")
    try:
        with serial.Serial(target_port, baud, timeout=2) as ser:
            time.sleep(0.5)
            # Send sync command
            ser.write(b"SYNC_NOTES\n")
            print(f"Syncing notes to {output_dir}...")
            # Protocol loop to read and save incoming notes
            # Files are streamed as: BEGIN_FILE <filename>\n<content>\nEND_FILE\n
            synced_count = 0
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line:
                    break
                if line.startswith("BEGIN_FILE "):
                    fname = line.split(" ", 1)[1]
                    dst_path = os.path.join(output_dir, fname)
                    content = []
                    while True:
                        sub = ser.readline().decode("utf-8", errors="ignore")
                        if sub.strip() == "END_FILE":
                            break
                        content.append(sub)
                    with open(dst_path, "w", encoding="utf-8") as f:
                        f.writelines(content)
                    print(f"  [SYNCED] {fname} ({len(content)} lines)")
                    synced_count += 1
                elif line == "SYNC_COMPLETE":
                    break
            print(f"Sync complete. {synced_count} note(s) downloaded.")
            return True
    except Exception as e:
        print(f"Serial communication error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="The Scribble USB-C Companion Note Sync")
    parser.add_argument("--port", help="Serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Destination directory for .md notes")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    args = parser.parse_args()
    sync_notes(port=args.port, output_dir=args.out, baud=args.baud)

if __name__ == "__main__":
    main()
