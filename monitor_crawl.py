#!/usr/bin/env python
"""
Monitor crawl progress
"""
import time
from pathlib import Path

OUTPUT_FILE = Path("data/exports/pricerunner_full_hierarchy.csv")

print("Monitoring crawl progress...")
print("Press Ctrl+C to stop monitoring\n")

last_count = 0
start_time = time.time()

try:
    while True:
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                count = len(lines) - 1  # Minus header

            if count > last_count:
                elapsed = time.time() - start_time
                rate = count / elapsed if elapsed > 0 else 0

                print(f"[{int(elapsed)}s] Categories found: {count} ({rate:.1f}/sec)")

                # Show last few entries
                if len(lines) > 1:
                    last_line = lines[-1].strip()
                    parts = last_line.split('|')
                    if len(parts) > 6:
                        depth = parts[-4]
                        full_path = parts[-3]
                        print(f"  Latest: [Level {depth}] {full_path}")

                last_count = count
        else:
            print("Waiting for output file to be created...")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    if last_count > 0:
        print(f"\nFinal count: {last_count} categories")
