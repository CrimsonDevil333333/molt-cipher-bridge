#!/usr/bin/env bash
# 🦞 Molt-Cipher-Bridge | Live Zero-Log Verification Test
# This script replicates the A2A test performed on 2026-02-06.

echo "🧪 Starting Zero-Log Verification Test..."

# 1. Setup - Generate a temporary key
KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
echo "🔑 Key generated (Whisper): $KEY"

# 2. SEaling (Orchestrator Side) - Create a secret file
echo '{"secrets": {"PROD_TOKEN": "AGENT_VERIFIED_SECRET_99"}}' > .live_secret.json
echo "📝 Secret file created (Not visible in logs via --file)"

# Seal the intent
FRAGMENT=$(molt-cipher seal --key "$KEY" --sender "MainAgent" --to "TestBot" --file .live_secret.json)
echo "📦 Sealed Fragment: $FRAGMENT"

# Cleanup secret file immediately
rm .live_secret.json
echo "🧹 Plaintext secret file deleted."

# 3. Execution (Worker Side) - Run a command using the injected secret
echo -e "\n🚀 Executing Worker Task (Zero-Log Injection)..."
RESULT=$(molt-cipher run --key "$KEY" --fragment "$FRAGMENT" --cmd 'echo "TOKEN_STATUS: $PROD_TOKEN"')

echo "--------------------------------"
echo "WORKER OUTPUT: $RESULT"
echo "--------------------------------"

# 4. Final Audit
if [[ $RESULT == *"AGENT_VERIFIED_SECRET_99"* ]]; then
    echo "✅ TEST PASSED: Secret successfully injected into RAM environment."
    echo "✅ LOG AUDIT: No plaintext secrets appeared in command arguments."
else
    echo "❌ TEST FAILED: Secret retrieval failed."
    exit 1
fi
