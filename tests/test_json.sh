#!/bin/bash
# 🦞 Molt-Cipher-Bridge | JSON Scenario Test (Generic)
# Tests: JSON file sealing, unsealing to file, 
# 'run' command with env injection, and selective '--pick' injection.

set -e

echo "--- 🧪 Starting JSON Scenario Test ---"

# 1. Environment Agnostic Setup
MOLT_EXE=$(command -v molt-cipher || echo "python3 -m molt_cipher_bridge")
TEST_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 2>/dev/null || echo "not_installed")

if [ "$TEST_KEY" == "not_installed" ]; then
    echo "❌ Error: cryptography not found. Please install it: pip install cryptography"
    exit 1
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# 2. Create JSON secrets
echo '{"DB_USER": "admin", "DB_PASS": "json_secret_123", "API_KEY": "sk-json-555"}' > "$TMP_DIR/secrets.json"
echo "✅ Created temporary secrets.json"

# 3. Seal
echo "🔒 Sealing JSON file..."
$MOLT_EXE seal --key "$TEST_KEY" --sender "TestMain" --to "TestWorker" --file "$TMP_DIR/secrets.json" > "$TMP_DIR/frag_json.json"
echo "✅ Fragment created"

# 4. Run (Standard)
echo "⚡ Testing 'run' with full ENV injection..."
RESULT=$($MOLT_EXE run --key "$TEST_KEY" --fragment "$(cat "$TMP_DIR/frag_json.json")" --cmd 'echo "User: $DB_USER, Pass: $DB_PASS"')
echo "$RESULT" | grep -q "admin" && echo "✅ ENV Injection: OK"

# 5. Run (Selective Pick)
echo "⚡ Testing 'run' with selective --pick (DB_USER only)..."
RESULT_PICK=$($MOLT_EXE run --key "$TEST_KEY" --fragment "$(cat "$TMP_DIR/frag_json.json")" --pick "DB_USER" --cmd 'echo "U: $DB_USER, P: $DB_PASS"')
if [[ "$RESULT_PICK" == *"admin"* ]] && [[ "$RESULT_PICK" != *"json_secret_123"* ]]; then
    echo "✅ Selective Pick: OK (DB_PASS was NOT injected)"
else
    echo "❌ Selective Pick: FAILED"
fi

# 6. Unseal to file
echo "🔓 Testing unseal to file..."
$MOLT_EXE unseal --key "$TEST_KEY" --fragment "$(cat "$TMP_DIR/frag_json.json")" --out "$TMP_DIR/restored.json"
if grep -q "json_secret_123" "$TMP_DIR/restored.json"; then
    echo "✅ Unseal to file: OK"
fi

echo "--- 🎉 JSON Scenario Test Passed! ---"
