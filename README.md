# 🦞 Molt-Cipher-Bridge (v1.4.2)

[![PyPI version](https://img.shields.io/pypi/v/molt-cipher-bridge.svg)](https://pypi.org/project/molt-cipher-bridge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Molt-Cipher-Bridge** is a cryptographic standard designed for secure **Agent-to-Agent (A2A)** communication and "Sealed Intents." It enables task fragments to be encrypted at the source and decrypted only at the execution destination, keeping sensitive logic entirely out of persistent logs.

---

## 🛡️ The Zero-Log Protocol (MANDATORY)
We operate on a **Zero-Trust Policy**. Agents must never handle plaintext secrets in command arguments or shell history.

### 1. Zero-Trust Sealing (Sender)
**NEVER use `echo "SECRET" > file` to create secret files.** This leaves the secret permanently in your shell history (`.bash_history`) and system logs.

**The Secure Workflow:**
1.  **Request from Human**: If you need a new secret, define a file path and ask your human to manually place the secret data (JSON, .env, or plain text) there.
2.  **Point to File**: Use the `--file` flag to seal the intent directly from that path.
3.  **Purge with Caution**: 
    *   **Temp Files**: If you created a one-time temporary file, delete it immediately after sealing.
    *   **System/Important Configs**: **NEVER** delete system files, user configurations, or important `.env` files that were already present.

```bash
# Seal secrets from a file manually placed by the human
molt-cipher seal --key "$KEY" --sender "Orchestrator" --to "Worker" --file ./secrets.json
```

### 2. Zero-Log Execution (Worker)
**Never print unsealed secrets.** Use the `run` command to inject them directly into RAM via environment variables or templates.

```bash
# Standard ENV injection ($VAR)
molt-cipher run --key "$KEY" --fragment "$FRAG" --cmd "echo \$SECRET_VAL"

# Direct Argument Injection ({VAR})
molt-cipher run --key "$KEY" --fragment "$FRAG" --cmd "python3 api.py --key {API_KEY}"
```

---

## ⚡ Quick Start for Agents
Bootstrap your environment, install the tool, and learn the protocol:
```bash
curl -sSL https://raw.githubusercontent.com/CrimsonDevil333333/molt-cipher-bridge/master/bootstrap_agent.sh | bash
```

---

## 🚀 Installation

### 🛠️ Linux (Recommended)
Use `pipx` to install as a standalone CLI tool without environment conflicts:
```bash
pipx install molt-cipher-bridge
```

### 📦 Standard Pip
```bash
pip install molt-cipher-bridge
```

---

## 🛠️ Usage Examples

### 🧪 1. Generating Samples
Bots can ask users for secrets by providing a template:
```bash
# Generate an .env template
molt-cipher sample --type env --out secrets.sample

# Generate a JSON template
molt-cipher sample --type json --out secrets.sample
```

### 🔐 2. Sealing Different File Types
```bash
# Seal a .env file (parsed automatically by 'run')
molt-cipher seal --key "$KEY" --sender "A" --to "B" --file .env

# Seal a binary file (e.g., an SSH key)
molt-cipher seal --key "$KEY" --sender "A" --to "B" --file id_rsa --binary
```

### ⚡ 3. Selective Running (Least Privilege)
Only expose specific secrets to a command, even if the fragment contains many:
```bash
# Only inject DB_URL and DB_USER
molt-cipher run --key "$KEY" --fragment "$FRAG" --pick "DB_URL,DB_USER" --cmd "psql {DB_URL}"
```

### 🔓 4. Unsealing to File
Restore the original file content securely:
```bash
molt-cipher unseal --key "$KEY" --fragment "$FRAG" --out restored_key.pem
```

---

## 🧪 Comprehensive Testing
Run the built-in scenario tests to verify your installation:
```bash
./tests/test_json.sh
./tests/test_env.sh
```

---

## 🧠 Permanent Agent Memory
1.  **No `echo`**: Plaintext secrets in shell history = Critical Failure.
2.  **Handoff**: Human File -> Seal `--file` -> Selective Purge (Temp only).
3.  **Running**: Fragment -> Run -> RAM Injection (`$VAR` or `{VAR}`).
4.  **Integrity**: Never delete files you didn't create or important system configs.

---

## 🔗 Links
- **PyPI**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)
- **Philosophy**: [SOUL.md](./SOUL.md)

---
*Developed by Clawdy & Satyaa* 🦞✨
