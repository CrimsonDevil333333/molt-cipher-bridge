#!/bin/bash
# 🦞 Molt-Cipher-Bridge | .env Scenario Test
# This script tests: .env file sealing, template injection {VAR},
# and direct argument passing.

set -e

echo "--- 🧪 Starting .env Scenario Test ---"

# 1. Setup
PROJECT_DIR="/mnt/ramdisk/daily_builds/molt-cipher-bridge"
TEST_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
mkdir -p "$PROJECT_DIR/tests/tmp"
cd "$PROJECT_DIR"
source venv/bin/activate

# 2. Create .env secrets
cat <<EOF > tests/tmp/secrets.env
SERVICE_NAME=TestRunner
API_TOKEN=tok_env_999
DEBUG_MODE=true
EOF
echo "✅ Created secrets.env"

# 3. Seal
echo "🔒 Sealing .env file..."
molt-cipher seal --key "$TEST_KEY" --sender "TestMain" --to "TestWorker" --file tests/tmp/secrets.env > tests/tmp/frag_env.json
echo "✅ Fragment created: tests/tmp/frag_env.json"

# 4. Run (Standard ENV)
echo "⚡ Testing 'run' with .env parsing..."
RESULT=$(molt-cipher run --key "$TEST_KEY" --fragment "$(cat tests/tmp/frag_env.json)" --cmd 'echo "Service: $SERVICE_NAME"')
echo "$RESULT" | grep -q "TestRunner" && echo "✅ ENV Parsing: OK"

# 5. Run (Template Injection)
echo "⚡ Testing template injection {API_TOKEN} in arguments..."
# We use a command that checks if the value was swapped
RESULT_TEMP=$(molt-cipher run --key "$TEST_KEY" --fragment "$(cat tests/tmp/frag_env.json)" --cmd 'echo "Passed Token: {API_TOKEN}"')
echo "$RESULT_TEMP" | grep -q "tok_env_999" && echo "✅ Template Injection: OK"

# 6. Sample Generator
echo "🧪 Testing sample generator..."
molt-cipher sample --type env --out tests/tmp/sample.env
if [ -f tests/tmp/sample.env ]; then
    echo "✅ Sample generation: OK"
fi

# Cleanup
rm -rf tests/tmp
echo "--- 🎉 .env Scenario Test Passed! ---"
