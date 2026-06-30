#!/bin/bash
# Joker Mind AI - Installer for Kali/Parrot

echo "🤡 Installing Joker Mind AI..."
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt

echo "🔑 Enter your Gemini API key (or press Enter for offline mode):"
read api_key

if [ ! -z "$api_key" ]; then
    echo "{\"api_key\": \"$api_key\"}" > config.json
    echo "✅ API key saved!"
else
    echo "{\"api_key\": \"\"}" > config.json
    echo "⚠️ Offline mode enabled (limited features)"
fi

sudo cp joker.py /usr/local/bin/joker
sudo chmod +x /usr/local/bin/joker

echo "🎭 Joker Mind AI installed! Type 'joker' to start."
