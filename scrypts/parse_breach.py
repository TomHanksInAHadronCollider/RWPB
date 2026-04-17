#!/usr/bin/env python3
"""
parse_breach.py
---------------
Reads the simulated SQL breach dump (dump.sql) and extracts
password hashes, sorting them by algorithm type into separate files:
  - md5_hashes.txt
  - sha1_hashes.txt
  - bcrypt_hashes.txt

Used in: Step 1 of the demo pipeline.
"""

import re

print("=" * 45)
print("   ACMECORP BREACH — HASH EXTRACTION TOOL")
print("=" * 45)

with open("dump.sql", "r") as f:
    content = f.read()

# Regex matches each INSERT row: (id, 'username', 'email', 'hash', 'type')
pattern = r"\((\d+), '(\w+)', '[\w@.]+', '([^']+)', '(\w+)'\)"
matches = re.findall(pattern, content)

md5_file    = open("md5_hashes.txt", "w")
sha1_file   = open("sha1_hashes.txt", "w")
bcrypt_file = open("bcrypt_hashes.txt", "w")

md5_count = sha1_count = bcrypt_count = 0

for uid, username, hash_val, hash_type in matches:
    print(f"[+] Extracted | User: {username:<12} | Type: {hash_type:<6} | Hash: {hash_val[:20]}...")
    if hash_type == "md5":
        md5_file.write(hash_val + "\n")
        md5_count += 1
    elif hash_type == "sha1":
        sha1_file.write(hash_val + "\n")
        sha1_count += 1
    elif hash_type == "bcrypt":
        bcrypt_file.write(hash_val + "\n")
        bcrypt_count += 1

md5_file.close()
sha1_file.close()
bcrypt_file.close()

print(f"\n[*] Extraction complete.")
print(f"    MD5 hashes:    {md5_count}")
print(f"    SHA-1 hashes:  {sha1_count}")
print(f"    bcrypt hashes: {bcrypt_count}")
print(f"[*] Files saved: md5_hashes.txt, sha1_hashes.txt, bcrypt_hashes.txt\n")
