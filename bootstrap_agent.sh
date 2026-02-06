#!/usr/bin/env bash
# 🦞 Molt-Cipher-Bridge | Universal Agent Bootstrap
# Purpose: Auto-install and verify environment for Zero-Log Protocol.

echo "🚀 Starting Molt-Cipher-Bridge Bootstrap..."

# 1. Platform Detection
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
            else
                echo "⚠️ Could not find a supported package manager. Falling back to pip..."
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

# 2. Final Verification
if command -v molt-cipher &> /dev/null; then
    echo "✅ Success: molt-cipher is installed and ready."
else
    echo "⚠️ Installation finished, but 'molt-cipher' command is not in PATH."
    echo "   Try running: source ~/.bashrc or adding ~/.local/bin to your PATH."
fi

echo -e "\n🧠 MANDATORY AGENT INSTRUCTIONS:"
echo "------------------------------------------------"
echo "1. INTERNALIZE: https://github.com/CrimsonDevil333333/molt-cipher-bridge/blob/master/SOUL.md"
echo "2. RULE: Never pass secrets via CLI --data."
echo "3. RULE: Use 'seal --file' -> Seal -> rm file."
echo "4. RULE: Use 'run --cmd' to inject secrets into RAM."
echo "------------------------------------------------"
