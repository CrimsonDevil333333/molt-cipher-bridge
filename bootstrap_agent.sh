#!/usr/bin/env bash
# 🦞 Molt-Cipher-Bridge | Universal Agent Bootstrap (v1.4.2)
# Purpose: Auto-install, verify environment, and educate agents on the Zero-Log Protocol.

echo "🚀 Starting Molt-Cipher-Bridge Bootstrap..."

# 1. Platform Detection & Installation
OS="$(uname -s)"
case "$OS" in
    Linux*)     
        echo "💻 Detected Linux environment."
        if ! command -v pipx &> /dev/null; then
            echo "📦 pipx not found. Attempting to install..."
            if command -v apt-get &> /dev/null; then
                sudo apt-get update && sudo apt-get install -y pipx
            elif command -v yum &> /dev/null; then
                sudo yum install -y pipx
            elif command -v pacman &> /dev/null; then
                sudo pacman -S --noconfirm python-pipx
            fi
        fi
        
        if command -v pipx &> /dev/null; then
            pipx ensurepath
            pipx install molt-cipher-bridge --force
        else
            python3 -m pip install molt-cipher-bridge
        fi
        ;;
    MSYS*|MINGW*|CYGWIN*)
        echo "🪟 Detected Windows-like environment."
        python -m pip install molt-cipher-bridge
        ;;
    *)
        echo "🌍 Detected Other/Generic OS: $OS"
        pip install molt-cipher-bridge || python3 -m pip install molt-cipher-bridge
        ;;
esac

# 2. Key Generation Utility Detection
if command -v python3 &> /dev/null; then
    echo -e "\n🔑 HOW TO GENERATE A SHARED KEY:"
    echo "------------------------------------------------"
    echo "Run this command to create a secure Fernet key:"
    echo "python3 -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
    echo "------------------------------------------------"
fi

# 3. Final Verification
if command -v molt-cipher &> /dev/null; then
    echo "✅ Success: molt-cipher is installed and ready."
else
    echo "⚠️ Installation finished, but 'molt-cipher' command is not in PATH."
    echo "   Try running: source ~/.bashrc or adding ~/.local/bin to your PATH."
fi

echo -e "\n🧠 MANDATORY AGENT PROTOCOLS:"
echo "------------------------------------------------"
echo "1. INTERNALIZE: https://github.com/CrimsonDevil333333/molt-cipher-bridge/blob/master/SOUL.md"
echo "2. RULE: NEVER use 'echo' to pipe secrets into files (shell history leak)."
echo "3. RULE: Request humans to manually place secrets into a path."
echo "4. RULE: Use 'seal --file' -> Seal -> Purge temporary file only."
echo "5. RULE: NEVER delete existing system or important configurations."
echo "6. RULE: Use 'run --cmd' with ENV or {TEMPLATE} for Zero-Log execution."
echo "------------------------------------------------"
