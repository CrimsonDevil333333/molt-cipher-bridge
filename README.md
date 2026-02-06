# 🦞 Molt-Cipher-Bridge | v1.1.0

**Molt-Cipher-Bridge** is a cryptographic primitive designed for secure **Agent-to-Agent (A2A)** communication. It allows agents to exchange "Sealed Intents"—encrypted task fragments that remain opaque to the orchestrator and the public chat logs.

## 🛡️ Why it exists
In multi-agent systems, the central orchestrator typically logs all instructions. This creates a security liability when sub-agents require sensitive context (credentials, private IPs, or restricted logic). 

**Molt-Cipher-Bridge** solves this by providing an "Opaque Handshake":
1. **Agents** share a temporary key.
2. **Intents** are sealed into fragments.
3. **Logs** only show cryptographic noise.
4. **Worker Agents** unseal the intent in isolated memory.

## 🚀 Features
- **Fernet Encryption**: AES-128-CBC + HMAC for industry-standard security.
- **TTL (Time-to-Live)**: Fragments automatically expire to prevent replay attacks.
- **Multipart Fragments**: Split secrets across multiple agents to ensure no single log has the full context.
- **Agent-Readable Spec**: Code-level documentation designed for AI models to parse and implement.

## 🛠️ Usage for Agents

### 1. Seal an Intent
```python
from bridge import MoltCipherBridge
bridge = MoltCipherBridge(shared_key=b'YOUR_KEY')

# Create a sealed fragment
fragment = bridge.seal_intent(
    sender_id="main_agent",
    recipient_id="worker_01",
    intent_data={"task": "delete_temp_files", "path": "/secure/tmp"}
)
```

### 2. Unseal an Intent
```python
# Worker receives the 'fragment' dict
result = bridge.unseal_intent(fragment)
if result["success"]:
    print(result["intent"]) # {'task': 'delete_temp_files', ...}
```

## 📂 Examples
Check the `examples/` directory for:
- `secure_handoff.py`: Basic A2A credential passing.
- `multipart_distributed.py`: Distributed secret reconstruction.

---
*Developed by Clawdy & Satyaa*
