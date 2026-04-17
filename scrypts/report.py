#!/usr/bin/env python3
"""
report.py
---------
Generates a final breach analysis report by querying John the Ripper's
saved results for each hash type (MD5, SHA-1, bcrypt).

Run this AFTER all john cracking commands have been executed.
Used in: Final step of the demo pipeline.
"""

import subprocess

print("\n" + "=" * 45)
print("      ACMECORP BREACH — FINAL REPORT")
print("=" * 45)

# Each tuple: (display label, john format string, hash file)
attacks = [
    ("MD5    — Dictionary Attack", "raw-md5",  "md5_hashes.txt"),
    ("SHA-1  — Dictionary Attack", "raw-sha1", "sha1_hashes.txt"),
    ("bcrypt — Wordlist Attack  ", "bcrypt",   "bcrypt_hashes.txt"),
]

total_cracked = 0

for label, fmt, hashfile in attacks:
    # Run: john --show --format=<fmt> <hashfile>
    result = subprocess.run(
        ["john", "--show", f"--format={fmt}", hashfile],
        capture_output=True, text=True
    )
    lines = [l for l in result.stdout.strip().split("\n") if l.startswith("?:")]
    count = len(lines)
    total_cracked += count

    if count > 0:
        print(f"[+] {label}: {count} password(s) cracked")
        for line in lines:
            print(f"      Password: {line.replace('?:', '')}")
    else:
        print(f"[-] {label}: 0 passwords cracked (resistant)")

print(f"\n[*] Total accounts compromised: {total_cracked} / 8")
print(f"[*] Recommendation: Migrate all password storage to bcrypt or Argon2.")
print("=" * 45 + "\n")
