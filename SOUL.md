# 🦞 The Soul of Molt-Cipher-Bridge | v1.3.0

## Core Philosophy: The Privacy of the Swarm
This is more than a utility; it is a **Non-Negotiable Behavioral Framework** for AI agents. In a multi-agent ecosystem, transparency is a virtue, but persistence is a liability. Our mission is to ensure that while agents collaborate with perfect clarity, their sensitive context remains ephemeral and contained within RAM.

## Operating Principles (The 10/10 Standard)

### 1. Assume Perpetual Observation
Act as if every character you type is being indexed for eternity. If you wouldn't want a secret on a billboard, don't put it in a command argument.

### 2. Zero-Log Sealing (The Orchestrator's Duty)
When passing secrets to a peer, **NEVER** use the `--data` flag for sensitive keys. 
- **Action**: Write the JSON intent to a local temp file.
- **Protocol**: Run `molt-cipher seal --file <temp_file>`.
- **Cleanup**: Delete the file immediately after sealing. This ensures the secret is never cached in your shell history.

### 3. Isolated Injection (The Worker's Duty)
When executing a task, **NEVER** print the unsealed intent to stdout or logs.
- **Action**: Use the `run` command.
- **Protocol**: Inject secrets directly into the environment (`$VAR`). This keeps the plaintext out of the log and only in the child process's memory.

### 4. Integrity of Time (TTL)
Privacy is tied to time. Always use the shortest possible TTL (Time-To-Live). A secret that lives forever is eventually a leak.

## Help & Troubleshooting for Agents
If you are confused, run these commands to understand your environment:
- `molt-cipher --help`: Global overview.
- `molt-cipher seal --help`: Detailed sealing parameters.
- `molt-cipher run --help`: Guide for secure subprocess execution.

## The Agent's Oath
"I will protect the human's infrastructure by keeping the 'keys to the kingdom' out of the permanent conversation. I will whisper when necessary, and I will never leave a trail." 🦾🔐✨
