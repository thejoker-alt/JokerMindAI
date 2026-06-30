#!/bin/bash

# 🤡 Joker Mind AI - Installer for Kali/Parrot
# "Let's put a smile on your terminal!"

echo -e "\033[1;35m"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   🃏 JOKER MIND AI - INSTALLER 🃏                      ║"
echo "║                                                          ║"
echo "║   \"Why so serious? Let's install!\"                      ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "\033[1;31m❌ This script must be run as root! Use: sudo ./install.sh\033[0m"
   exit 1
fi

echo -e "\n📦 \033[1;33mUpdating system...\033[0m"
apt update -y

echo -e "\n📦 \033[1;33mInstalling Python3 and pip...\033[0m"
apt install python3 python3-pip git -y

echo -e "\n📦 \033[1;33mInstalling Python dependencies...\033[0m"
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo -e "\n🔑 \033[1;33mDo you want to add Gemini API key now? (y/n)\033[0m"
read -p "> " add_key

if [[ $add_key == "y" || $add_key == "Y" ]]; then
    echo -e "\n🔐 \033[1;33mEnter your Gemini API key:\033[0m"
    read -p "> " api_key
    
    if [[ ! -z "$api_key" ]]; then
        echo "{\"api_key\": \"$api_key\", \"offline_mode\": false, \"joker_persona\": true}" > config.json
        echo -e "\n✅ \033[1;32mAPI key saved! AI Mode enabled.\033[0m"
    else
        echo "{\"api_key\": \"\", \"offline_mode\": true, \"joker_persona\": true}" > config.json
        echo -e "\n⚠️ \033[1;33mNo API key. Offline mode enabled.\033[0m"
    fi
else
    echo "{\"api_key\": \"\", \"offline_mode\": true, \"joker_persona\": true}" > config.json
    echo -e "\n⚠️ \033[1;33mOffline mode enabled (no API required).\033[0m"
fi

echo -e "\n🔧 \033[1;33mCreating global command...\033[0m"
chmod +x joker.py
cp joker.py /usr/local/bin/joker
chmod +x /usr/local/bin/joker

echo -e "\n✅ \033[1;32mInstallation Complete!\033[0m"
echo -e "\n🎯 \033[1;36mTo start Joker Mind AI, type: joker\033[0m"
echo -e "\n📌 \033[1;36mCommands inside Joker: help, setup, mode, chat, fix\033[0m"

echo -e "\n\033[1;35m"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🃏 The Joker is ready to play! 🃏                     ║"
echo "║  \"Let's put a smile on that terminal!\"                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "\033[0m"
