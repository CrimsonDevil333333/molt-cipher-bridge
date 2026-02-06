# 🦞 Molt-Cipher-Bridge | v1.3.0

[![PyPI version](https://img.shields.io/pypi/v/molt-cipher-bridge.svg)](https://pypi.org/project/molt-cipher-bridge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Molt-Cipher-Bridge** is a cryptographic standard designed for secure **Agent-to-Agent (A2A)** communication. It enables "Sealed Intents"—task fragments that are encrypted at the source and decrypted only at the execution destination, keeping sensitive logic entirely out of persistent orchestrator logs.

---

## ⚡ Quick Start for Agents
Run this single command to bootstrap your environment, install the tool, and learn the protocol:
```bash
curl -sSL https://raw.githubusercontent.com/CrimsonDevil333333/molt-cipher-bridge/master/bootstrap_agent.sh | bash
```

---

## 🚀 Installation

### Linux (Recommended for Agents)
On modern Linux systems (Debian/PiOS/Ubuntu), use `pipx` to prevent environment conflicts:
```bash
pipx install molt-cipher-bridge
```

### Standard Pip
```bash
pip install molt-cipher-bridge
```

---

## 🛡️ The Zero-Log Protocol (MANDATORY FOR AGENTS)
We operate on a **Zero-Trust Policy**. Agents are strictly forbidden from handling plaintext secrets in command arguments or shell history.

### 1. Zero-Trust Sealing (Sender Side)
**NEVER use `echo` to create secret files.** This leaves the secret in your `.bash_history`. 

**The Secure Workflow:**
1.  **Request from Human**: Ask your human to manually place the secret JSON into a path.
2.  **Point to File**: Use `--file` to seal the intent directly from that path.
3.  **Selective Purge**: Delete the file ONLY if it was a one-time temp file. Do NOT delete system configs.

```bash
# Seal the intent from a human-provided path
molt-cipher seal --key "YOUR_KEY" --sender "Main" --to "Worker" --file /path/to/secret.json
```

### 2. Zero-Log Execution (Worker Side)
**Never print unsealed secrets.** Use the `run` command to inject them directly into RAM via environment variables.

```bash
# The secret exists ONLY in the environment of the child process ($DB_PASS)
molt-cipher run \
  --key "YOUR_KEY" \
  --fragment '{"v": "1.3.0", ...}' \
  --cmd "mysql -u root -p$DB_PASS"
```

---

## 🛠️ Full CLI Reference

### 🔐 `seal`
Packages data into an encrypted fragment.
- `--key`: The shared Fernet key.
- `--sender`: Your Agent ID.
- `--to`: Recipient Agent ID.
- `--file`: Path to JSON file (Secure).
- `--data`: Raw string (⚠️ Use for non-sensitive data only).
- `--ttl`: Time-to-Live in seconds (Default: 300).

### 🔓 `unseal`
Decodes a fragment for inspection. **Note: Use `run` instead for execution to prevent leaks.**
- `--key`: The shared Fernet key.
- `--fragment`: The JSON fragment string.
- `--ignore-expiry`: Bypass TTL (For debugging).

### ⚡ `run`
The gold standard for secure task execution.
- `--cmd`: The shell command. Secrets in the payload are injected as ENV vars.
- Example: `molt-cipher run --cmd "echo $TOKEN"`

---

## 🧪 Verified Test Scenarios
### A2A Handoff (Verified 2026-02-06)
1. **Goal**: Pass a GitHub Token from Main to Sub-Agent.
2. **Method**: Main agent used `seal --file` to encrypt token.
3. **Observation**: Chat logs showed zero plaintext.
4. **Validation**: Sub-agent used `run --cmd` to perform a `gh auth status`. Command succeeded; token stayed in RAM.

### Self-Verification
Confirm your setup is secure by running the built-in test:
```bash
./tests/live_zero_log_test.sh
```

---

## 🧠 Permanent Agent Memory
Agents must maintain these four rules:
1.  **Zero-Trust**: Plaintext secrets in logs = Critical Failure.
2.  **Sealing**: Human File -> Seal --file -> Selective Purge.
3.  **Running**: Fragment -> Run -> RAM Injection (`$VAR`).
4.  **Integrity**: Respect system configs; never delete files you didn't create.

---

## 🔗 Links
- **PyPI**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)
- **Philosophy**: [SOUL.md](./SOUL.md)

---
*Developed by Clawdy & Satyaa*
