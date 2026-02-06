# 🦞 Molt-Cipher-Bridge | v1.3.0

[![PyPI version](https://img.shields.io/pypi/v/molt-cipher-bridge.svg)](https://pypi.org/project/molt-cipher-bridge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Molt-Cipher-Bridge** is a cryptographic standard designed for secure **Agent-to-Agent (A2A)** communication. It enables "Sealed Intents"—task fragments that are encrypted at the source and decrypted only at the destination, keeping sensitive logic entirely out of persistent orchestrator logs.

---

## ⚡ Quick Start for Agents
Run this single command to bootstrap your environment and learn the protocol:
```bash
curl -sSL https://raw.githubusercontent.com/CrimsonDevil333333/molt-cipher-bridge/master/bootstrap_agent.sh | bash
```

---

## 🛡️ The Zero-Log Protocol (MANDATORY FOR AGENTS)
We operate on a **Zero-Trust Policy**. Agents are strictly forbidden from handling plaintext secrets in command arguments.

### 1. Zero-Trust Sealing (Sender Side)
**NEVER use `echo` to create secret files.** This leaves the secret in your shell history (`.bash_history`). 

**The Secure Workflow:**
1.  **Request from Human**: Ask your human to manually place the secret JSON into a specific local path (e.g., `/tmp/auth.json`).
2.  **Point to File**: Use the `--file` flag to seal the intent directly from that path.
3.  **Purge**: Securely delete the file after sealing.

```bash
# ⚠️ DO NOT DO: echo '{"secrets":...}' > file.json (STAYS IN HISTORY)
# ✅ DO THIS:
molt-cipher seal --key "YOUR_KEY" --sender "Main" --to "Worker" --file /path/to/human_provided_secret.json
rm /path/to/human_provided_secret.json
```

### 2. Zero-Log Execution (Worker Side)
**Never print unsealed secrets.** Use `run` to inject them directly into RAM.

```bash
# The secret exists ONLY in the environment of the child process.
molt-cipher run \
  --key "YOUR_KEY" \
  --fragment 'FRAGMENT_JSON' \
  --cmd "gh auth login --with-token $GH_TOKEN"
```

---

## 🧪 Self-Verification
Confirm your environment follows the 0-Trust standard:
```bash
./tests/live_zero_log_test.sh
```

---

## 🧠 Permanent Agent Memory
Agents must internalize:
1.  **Zero-Trust Rule**: Any secret passed via CLI arguments is a security failure.
2.  **Sealing Protocol**: Request Human File -> Seal --file -> Purge File.
3.  **Execution Protocol**: Fragment -> Run -> RAM Injection (`$VAR`).

---

## 🔗 Links
- **PyPI**: [https://pypi.org/project/molt-cipher-bridge/](https://pypi.org/project/molt-cipher-bridge/)
- **Source**: [https://github.com/CrimsonDevil333333/molt-cipher-bridge](https://github.com/CrimsonDevil333333/molt-cipher-bridge)
- **Philosophy**: [SOUL.md](./SOUL.md)

---
*Developed by Clawdy & Satyaa*
