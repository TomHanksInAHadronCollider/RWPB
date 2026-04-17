# Password Breach Analysis Demo
**CIS 4378 — Security Project**

A simulated end-to-end password breach analysis pipeline. We mimic what a real attacker (or forensic analyst) would do after obtaining a stolen corporate database: parse the dump, identify hash types, and crack passwords using dictionary attacks — then compare how different hashing algorithms hold up.

---

## Project Summary

We created a fake SQL database dump from a fictional company **AcmeCorp** containing 8 employee accounts with passwords stored using three different algorithms: **MD5**, **SHA-1**, and **bcrypt**. The demo shows why algorithm choice is critical — MD5 and SHA-1 crack almost instantly while bcrypt resists attack.

### Tools Used
| Tool | Purpose | Where |
|------|---------|-------|
| Kali Linux | Demo environment | Your machine |
| Python 3 | Parser + report scripts | Pre-installed on Kali |
| John the Ripper | All cracking attacks | Pre-installed on Kali |
| RockYou wordlist | Dictionary for attacks | `/usr/share/wordlists/rockyou.txt` |

> **Note:** Hashcat was originally planned but switched to John the Ripper due to GPU/memory limitations on a VM. John works purely on CPU with no issues.

---

## File Structure

```
password-breach-demo/
├── dump.sql                  # Simulated SQL breach dump (AcmeCorp)
├── scripts/
│   ├── parse_breach.py       # Parses dump.sql → sorts hashes by type
│   └── report.py             # Final report — reads John's cracked results
├── docs/
│   └── demo_script.md        # Two-person presentation script
└── README.md
```

After running the pipeline, these files are generated:
```
├── md5_hashes.txt            # Extracted MD5 hashes
├── sha1_hashes.txt           # Extracted SHA-1 hashes
└── bcrypt_hashes.txt         # Extracted bcrypt hashes
```

---

## Setup

```bash
# 1. Clone / copy the project folder
cd ~/password_breach_demo

# 2. No pip installs needed — John the Ripper and Python 3 are pre-installed on Kali
```

---

## Full Demo Run Order

### Step 1 — View the breach dump
```bash
cat dump.sql
```
Shows the simulated leaked database with 8 AcmeCorp employee accounts.

---

### Step 2 — Parse the dump
```bash
python3 scripts/parse_breach.py
```
Reads `dump.sql` using regex, extracts all hashes, and writes them to:
- `md5_hashes.txt` (3 hashes)
- `sha1_hashes.txt` (3 hashes)
- `bcrypt_hashes.txt` (2 hashes)

---

### Step 3 — Crack MD5 (Dictionary Attack)
```bash
john --format=raw-md5 md5_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
John takes every word in RockYou (14M passwords), hashes it as MD5, and compares against our stolen hashes. MD5 runs at ~57,000 hashes/sec.

**Show results:**
```bash
john --show --format=raw-md5 md5_hashes.txt
```
Expected: `password`, `123456`, `123456789` — all 3 cracked instantly.

---

### Step 4 — Crack SHA-1 (Dictionary Attack)
```bash
john --format=raw-sha1 sha1_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
Same attack, SHA-1 format. Runs at ~13,000 hashes/sec — slower than MD5 but still very fast.

**Show results:**
```bash
john --show --format=raw-sha1 sha1_hashes.txt
```
Expected: `123456789`, `qwerty` — 2 of 3 cracked.

---

### Step 5 — Crack bcrypt (Wordlist Attack)
```bash
john --format=bcrypt bcrypt_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
Same wordlist, but bcrypt runs at only ~26 hashes/sec due to its intentional cost factor — over **2,000x slower** than MD5.

**Show results:**
```bash
john --show --format=bcrypt bcrypt_hashes.txt
```
Expected: `secret` — 1 of 2 cracked (only because it was an extremely common password).

---

### Step 6 — Final Report
```bash
python3 scripts/report.py
```
Queries John's saved results and prints a formatted summary.

Expected output:
```
=============================================
      ACMECORP BREACH — FINAL REPORT
=============================================
[+] MD5    — Dictionary Attack: 3 password(s) cracked
      Password: password
      Password: 123456
      Password: 123456789
[+] SHA-1  — Dictionary Attack: 2 password(s) cracked
      Password: 123456789
      Password: qwerty
[+] bcrypt — Wordlist Attack  : 1 password(s) cracked
      Password: secret

[*] Total accounts compromised: 6 / 8
[*] Recommendation: Migrate all password storage to bcrypt or Argon2.
=============================================
```

---

## Key Findings

| Algorithm | Accounts | Cracked | Speed | Verdict |
|-----------|----------|---------|-------|---------|
| MD5 | 3 | 3/3 (100%) | ~57,000 h/s | ❌ Completely broken |
| SHA-1 | 3 | 2/3 (67%) | ~13,000 h/s | ❌ Broken |
| bcrypt | 2 | 1/2 (50%) | ~26 h/s | ✅ Resistant |

bcrypt is **2,200x slower** than MD5. That difference means cracking a full database goes from minutes to years.

---

## Real-World Context

| Breach | Year | Algorithm Used | Outcome |
|--------|------|---------------|---------|
| RockYou | 2009 | Plaintext | 14M passwords fully exposed |
| LinkedIn | 2012 | SHA-1 (unsalted) | 100M+ passwords cracked |
| Adobe | 2013 | 3DES (misused) | 153M accounts compromised |

---

## Recommendation

Companies should use **bcrypt** or **Argon2** for password storage. Argon2 adds memory-hardness on top of time cost, making GPU-based attacks even harder. MD5 and SHA-1 should **never** be used for passwords.