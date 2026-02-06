# 🦞 Molt-Cipher-Bridge (v1.4.0)

A cryptographic standard for secure Agent-to-Agent (A2A) communication and "Sealed Intents."

## Overview

Molt-Cipher-Bridge is designed to solve the "Logged Secrets" problem in agentic workflows. When a primary agent (orchestrator) spawns a sub-agent (worker) to perform a task requiring credentials, those credentials often end up in the orchestrator's logs or the system's process history.

**Molt-Cipher** allows agents to pass encrypted fragments called "Sealed Intents" that are only decrypted and injected into the environment at the moment of execution.

## Features

-   🔐 **Zero-Log Context**: Secrets are passed as encrypted blobs.
-   🛠️ **Universal File Support**: Seal `.env`, `JSON`, plain text, or binary files.
-   📟 **Native .env Integration**: Automatically parses `.env` files for environment variable injection.
-   🧪 **Sample Generation**: Quickly create template secret files for users to fill.
-   ⏳ **TTL Security**: Fragments expire automatically based on a configurable Time-To-Live.
-   📦 **Production Ready**: Built with `cryptography` (Fernet) for high-grade security.

## Installation

```bash
pip install molt-cipher-bridge
```

## Usage

### 1. Generate a Shared Key
Agents must share a key (passed via secure channel or human handoff) to communicate.
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Prepare Secrets
You can use the built-in sample generator to create a template:
```bash
# Generate a JSON sample
molt-cipher sample --type json --out secrets.json

# Generate an .env sample
molt-cipher sample --type env --out .env
```

### 3. Seal an Intent (Sender)
Encrypt a file into a "Sealed Fragment."
```bash
molt-cipher seal --key YOUR_KEY --sender "orchestrator" --to "worker" --file .env --ttl 600 > fragment.json
```

### 4. Run with Secrets (Recipient/Worker)
Decrypt the fragment and execute a command with the secrets injected as environment variables.
```bash
molt-cipher run --key YOUR_KEY --fragment "$(cat fragment.json)" --cmd "python3 worker_script.py"
```

### 5. Unseal to File
If you just need the raw data back:
```bash
molt-cipher unseal --key YOUR_KEY --fragment "$(cat fragment.json)" --out restored_secrets.env
```

## Security Best Practices

1.  **Always use `--file`**: Never pass raw JSON strings via `--data` as they will appear in your shell history.
2.  **Use `run` over `unseal`**: The `run` command injects secrets directly into the subprocess environment in memory, which is safer than writing them to disk.
3.  **Short TTLs**: Keep fragment expiration short (e.g., 300s) to minimize the window of exposure.

## License

MIT - Developed by Satyaa & Clawdy 🦞✨
