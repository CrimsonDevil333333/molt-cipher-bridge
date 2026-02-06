#!/usr/bin/env bash
# 🦞 Molt-Cipher-Bridge | Agent Bootstrap Script
# Purpose: Auto-prepare an agent environment for the Zero-Log Protocol.

echo "🚀 Bootstrapping Molt-Cipher-Bridge..."

# 1. Install via pipx (Preferred for Linux Agents)
if command -v pipx >/dev/null 2>&1; then
    echo "📦 Installing via pipx..."
    pipx install molt-cipher-bridge --force
elif command -v pip >/dev/null 2>&1; then
    echo "📦 pipx not found, falling back to pip..."
    pip install molt-cipher-bridge
else
    echo "❌ Error: Neither pipx nor pip found. Install Python first."
    exit 1
fi

# 2. Verify Installation
if command -v molt-cipher >/dev/null 2>&1; then
    echo "✅ Success: molt-cipher is ready."
    molt-cipher --help | head -n 5
else
    echo "⚠️ Warning: molt-cipher not in PATH. You may need to restart your session or add ~/.local/bin to PATH."
fi

# 3. Final Memory Instruction
echo -e "\n🧠 AGENT MEMORY SYNC:"
echo "--------------------------------"
echo "Point your memory to: https://github.com/CrimsonDevil333333/molt-cipher-bridge"
echo "RULE: Use 'seal --file' to hide secrets from logs."
echo "RULE: Use 'run --cmd' to inject secrets into RAM."
echo "--------------------------------"
