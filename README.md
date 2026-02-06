# 🦞 Molt-Cipher-Bridge | v1.2.0

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
4. **Worker Agents** execute tasks in isolated memory without plaintext leaks.

---

## 🚀 Installation

### Global (Recommended)
Install the CLI and library globally via PyPI:
```bash
pip install molt-cipher-bridge
```

---

## 🛠️ Usage for Agents & Bots

### 1. Global CLI Commands

#### 🔐 Seal an Intent (with Secrets)
Packages sensitive data into an encrypted JSON fragment. Use the `secrets` key in your data to mark variables for secure injection.
```bash
molt-cipher seal --key "YOUR_KEY" --sender "Main" --to "Worker" --data '{"secrets": {"GH_TOKEN": "ghp_12345"}}'
```

#### 🔓 Unseal (Decrypt) a Fragment
Decodes the fragment and validates integrity/expiry.
```bash
molt-cipher unseal --key "YOUR_KEY" --fragment '{"v": "1.2.0", ...}'
```

#### ⚡ Run (Zero-Log Execution) - NEW in v1.2.0
Directly executes a command by injecting sealed secrets into the environment. **The secret is never printed to the log.**
```bash
# The 'GH_TOKEN' from the sealed fragment is injected as an ENV variable.
molt-cipher run --key "YOUR_KEY" --fragment 'FRAGMENT_JSON' --cmd "gh auth login --with-token $GH_TOKEN"
```

---

### 2. Python Library Usage
```python
from molt_cipher_bridge import MoltCipherBridge

bridge = MoltCipherBridge(shared_key="YOUR_KEY")

# Seal data
fragment = bridge.seal_intent("Sender", "Recipient", {"secrets": {"API_KEY": "sk-real-key"}})

# Execute directly (Zero-Log)
result = bridge.execute_sealed_command(fragment, "curl -H 'Authorization: Bearer $API_KEY' https://api.site.com")
print(result["stdout"]) # The 'sk-real-key' never touched your terminal stdout!
```

---

## ✨ Features
- **Zero-Log Execution**: Inject secrets directly into subprocess environments.
- **Production Encryption**: Uses Fernet (AES-128-CBC + HMAC) for high-grade security.
- **TTL Expiry**: Fragments automatically expire (default 300s) to prevent replay attacks.
- **Multipart Fragments**: Support for splitting high-entropy secrets across multiple agents.
- **Key Hinting**: First 8 characters of the key are provided in fragments for instant verification.

---

## 🧪 Verified Test Scenarios
Live-tested between a Main Agent and a Sub-Agent on **2026-02-06**.
- **Case**: Passing DB credentials via "Sealed Intent" and executing a migration.
- **Result**: Sub-agent successfully unsealed and executed the task; orchestrator logs only showed the encrypted blob.

---

## 🔗 Links
- **PyPI Package**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source Code**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)

---
*Developed by Clawdy & Satyaa*
