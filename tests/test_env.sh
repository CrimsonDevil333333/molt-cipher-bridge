#!/bin/bash
# 🦞 Molt-Cipher-Bridge | .env Scenario Test (Generic)
# Tests: .env file sealing, template injection {VAR},
# and direct argument passing.

set -e

echo "--- 🧪 Starting .env Scenario Test ---"

# 1. Environment Agnostic Setup
MOLT_EXE=$(command -v molt-cipher || echo "python3 -m molt_cipher_bridge")
TEST_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 2>/dev/null || echo "not_installed")

if [ "$TEST_KEY" == "not_installed" ]; then
    echo "❌ Error: cryptography not found. Please install it: pip install cryptography"
    exit 1
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# 2. Create .env secrets
cat <<EOF > "$TMP_DIR/secrets.env"
SERVICE_NAME=TestRunner
API_TOKEN=tok_env_999
DEBUG_MODE=true
EOF
echo "✅ Created temporary secrets.env"

# 3. Seal
echo "🔒 Sealing .env file..."
$MOLT_EXE seal --key "$TEST_KEY" --sender "TestMain" --to "TestWorker" --file "$TMP_DIR/secrets.env" > "$TMP_DIR/frag_env.json"
echo "✅ Fragment created"

# 4. Run (Standard ENV)
echo "⚡ Testing 'run' with .env parsing..."
RESULT=$($MOLT_EXE run --key "$TEST_KEY" --fragment "$(cat "$TMP_DIR/frag_env.json")" --cmd 'echo "Service: $SERVICE_NAME"')
echo "$RESULT" | grep -q "TestRunner" && echo "✅ ENV Parsing: OK"

# 5. Run (Template Injection)
echo "⚡ Testing template injection {API_TOKEN} in arguments..."
RESULT_TEMP=$($MOLT_EXE run --key "$TEST_KEY" --fragment "$(cat "$TMP_DIR/frag_env.json")" --cmd 'echo "Passed Token: {API_TOKEN}"')
echo "$RESULT_TEMP" | grep -q "tok_env_999" && echo "✅ Template Injection: OK"

# 6. Sample Generator
echo "🧪 Testing sample generator..."
$MOLT_EXE sample --type env --out "$TMP_DIR/sample.env"
if [ -f "$TMP_DIR/sample.env" ]; then
    echo "✅ Sample generation: OK"
fi

echo "--- 🎉 .env Scenario Test Passed! ---"
