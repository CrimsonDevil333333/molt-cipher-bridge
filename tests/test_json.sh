#!/bin/bash
# 🦞 Molt-Cipher-Bridge | JSON Scenario Test
# This script tests: JSON file sealing, unsealing to file, 
# 'run' command with env injection, and selective '--pick' injection.

set -e

echo "--- 🧪 Starting JSON Scenario Test ---"

# 1. Setup
PROJECT_DIR="/mnt/ramdisk/daily_builds/molt-cipher-bridge"
TEST_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
mkdir -p "$PROJECT_DIR/tests/tmp"
cd "$PROJECT_DIR"
source venv/bin/activate

# 2. Create JSON secrets
echo '{"DB_USER": "admin", "DB_PASS": "json_secret_123", "API_KEY": "sk-json-555"}' > tests/tmp/secrets.json
echo "✅ Created secrets.json"

# 3. Seal
echo "🔒 Sealing JSON file..."
molt-cipher seal --key "$TEST_KEY" --sender "TestMain" --to "TestWorker" --file tests/tmp/secrets.json > tests/tmp/frag_json.json
echo "✅ Fragment created: tests/tmp/frag_json.json"

# 4. Run (Standard)
echo "⚡ Testing 'run' with full ENV injection..."
RESULT=$(molt-cipher run --key "$TEST_KEY" --fragment "$(cat tests/tmp/frag_json.json)" --cmd 'echo "User: $DB_USER, Pass: $DB_PASS"')
echo "$RESULT" | grep -q "admin" && echo "✅ ENV Injection: OK"

# 5. Run (Selective Pick)
echo "⚡ Testing 'run' with selective --pick (DB_USER only)..."
RESULT_PICK=$(molt-cipher run --key "$TEST_KEY" --fragment "$(cat tests/tmp/frag_json.json)" --pick "DB_USER" --cmd 'echo "U: $DB_USER, P: $DB_PASS"')
if [[ "$RESULT_PICK" == *"admin"* ]] && [[ "$RESULT_PICK" != *"json_secret_123"* ]]; then
    echo "✅ Selective Pick: OK (DB_PASS was NOT injected)"
else
    echo "❌ Selective Pick: FAILED"
    echo "$RESULT_PICK"
fi

# 6. Unseal to file
echo "🔓 Testing unseal to file..."
molt-cipher unseal --key "$TEST_KEY" --fragment "$(cat tests/tmp/frag_json.json)" --out tests/tmp/restored.json
if grep -q "json_secret_123" tests/tmp/restored.json; then
    echo "✅ Unseal to file: OK"
fi

# Cleanup
rm -rf tests/tmp
echo "--- 🎉 JSON Scenario Test Passed! ---"
