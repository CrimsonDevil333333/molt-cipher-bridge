# 🦞 Molt-Cipher-Bridge | v1.1.0

[![PyPI version](https://img.shields.io/pypi/v/molt-cipher-bridge.svg)](https://pypi.org/project/molt-cipher-bridge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Molt-Cipher-Bridge** is a cryptographic standard designed for secure **Agent-to-Agent (A2A)** communication. It enables "Sealed Intents"—task fragments that are encrypted at the source and decrypted only at the execution destination, keeping sensitive logic out of persistent orchestrator logs.

---

## 🛡️ The Problem: The Observer Paradox
In multi-agent systems, the central orchestrator typically logs all instructions. This creates a security liability when sub-agents require sensitive context (credentials, private IPs, or restricted logic). 

**Molt-Cipher-Bridge** solves this by providing an "Opaque Handshake":
1. **Agents** share a temporary key.
2. **Intents** are sealed into fragments.
3. **Logs** only show cryptographic noise.
4. **Worker Agents** unseal the intent in isolated memory.

---

## 🚀 Installation

### Global (Recommended)
Install the CLI and library globally via PyPI:
```bash
pip install molt-cipher-bridge
```

### From Source (Development)
```bash
git clone https://github.com/CrimsonDevil333333/molt-cipher-bridge.git
cd molt-cipher-bridge
pip install -e .
```

---

## 🛠️ Usage for Agents & Bots

### 1. Global CLI Commands
Once installed, use the `molt-cipher` command directly from your terminal.

#### 🔐 Seal an Intent
Packages sensitive data into an encrypted JSON fragment.
```bash
molt-cipher seal --key "YOUR_FERNET_KEY" --sender "MainAgent" --to "SubAgent" --data '{"db_pass": "secret123"}'
```

#### 🔓 Unseal (Decrypt) a Fragment
Decodes the fragment and validates integrity/expiry.
```bash
molt-cipher unseal --key "YOUR_FERNET_KEY" --fragment '{"v": "1.1.0", "fid": "...", "payload": "..."}'
```
*Tip: Receiving agents should run this in isolated sessions to keep secrets out of logs.*

---

### 2. Python Library Usage
Integrate directly into your agent's logic:

```python
from molt_cipher_bridge import MoltCipherBridge

# Initialize with a shared key
bridge = MoltCipherBridge(shared_key=b'YOUR_SECRET_KEY...')

# Seal data
fragment = bridge.seal_intent("Sender", "Recipient", {"task": "deploy"})

# Unseal data
result = bridge.unseal_intent(fragment)
if result["success"]:
    print(result["intent"])
```

---

## ✨ Features
- **Production Encryption**: Uses Fernet (AES-128-CBC + HMAC) for high-grade security.
- **TTL Expiry**: Fragments automatically expire (default 300s) to prevent replay attacks.
- **Multipart Fragments**: Support for splitting high-entropy secrets across multiple agents.
- **Key Hinting**: First 8 characters of the key are provided in fragments for instant verification.
- **Agent-Readable Spec**: Code-level documentation designed for LLMs to parse and implement.

---

## 🧪 Verified Test Scenarios
Live-tested between a Main Agent and a Sub-Agent on **2026-02-06**.
- **Case**: Passing DB credentials via "Sealed Intent".
- **Result**: Sub-agent successfully unsealed the task in an isolated session; orchestrator logs only showed the encrypted blob.

---

## 🔗 Links
- **PyPI Package**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source Code**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)
- **Issues**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge/issues](https://github.com/CrimsonDevil333333/molt-cipher-bridge/issues)

---
*Developed by Clawdy & Satyaa*
