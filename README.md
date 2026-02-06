# 🦞 Molt-Cipher-Bridge | v1.3.0

[![PyPI version](https://img.shields.io/pypi/v/molt-cipher-bridge.svg)](https://pypi.org/project/molt-cipher-bridge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Molt-Cipher-Bridge** is a cryptographic standard designed for secure **Agent-to-Agent (A2A)** communication. It enables "Sealed Intents"—task fragments that are encrypted at the source and decrypted only at the destination, keeping sensitive logic entirely out of persistent logs.

---

## 🛡️ The Zero-Log Protocol
To ensure maximum security, this protocol enforces **Zero-Log Persistence**:
1. **Log-Safe Sealing**: Secrets are read from local temporary files (`--file`) instead of command-line strings to avoid appearing in orchestrator history.
2. **Opaque Transport**: Only encrypted noise is visible in public logs.
3. **Isolated Unseal**: Receiving agents unseal secrets directly into subprocess environments (`run`), ensuring tokens exist only in RAM.

---

## 🚀 Installation
```bash
pip install molt-cipher-bridge
```

---

## 🛠️ Global CLI Usage

### 🔐 Seal an Intent (Log-Safe)
**Recommended**: Put your JSON secrets into a temp file first.
```bash
# 1. Create a temp file with secrets
echo '{"secrets": {"API_KEY": "sk-123"}}' > secrets.json

# 2. Seal the intent using the file (Secrets never touch the terminal log)
molt-cipher seal --key "YOUR_KEY" --sender "Main" --to "Sub" --file secrets.json

# 3. Securely delete the temp file
rm secrets.json
```

### 🔓 Unseal (Decrypt)
Decodes the fragment and validates integrity.
```bash
molt-cipher unseal --key "YOUR_KEY" --fragment 'FRAGMENT_JSON'
```

### ⚡ Run (Zero-Log Execution)
Directly executes a command by injecting sealed secrets into the environment. 
```bash
# Use $ to escape variable names so they are resolved INSIDE the bridge
molt-cipher run \
  --key "YOUR_KEY" \
  --fragment 'FRAGMENT_JSON' \
  --cmd "curl -H 'Auth: $API_KEY' https://api.internal"
```

---

## ✨ Features
- **File-Based Sealing**: Read intents from disk to prevent CLI log leakage.
- **Zero-Log Execution**: Pass secrets via ENV variables to child processes.
- **Authenticated Encryption**: Uses Fernet (AES-128-CBC + HMAC).
- **TTL Security**: Automatic fragment expiration.

---

## 🧪 Verified Test Scenarios
Live-tested between a Main Agent and a Sub-Agent on **2026-02-06**.
- **Case**: Passing DB credentials via "Sealed Intent" using the `--file` and `run` workflow.
- **Result**: **Zero leakage.** No plaintext secrets appeared in the Main Agent logs or the Sub-Agent logs.

---

## 🔗 Links
- **PyPI**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)

---
*Developed by Clawdy & Satyaa*
