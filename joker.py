#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤡 JOKER MIND AI v1.0
"Let's put a smile on that terminal!"
Author: Your Name
License: MIT
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
import random

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from prompt_toolkit import prompt
    from prompt_toolkit.history import FileHistory
    from colorama import init, Fore, Style
    import google.generativeai as genai
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("📦 Run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize
init(autoreset=True)
console = Console()

# Joker ASCII Art
JOKER_ASCII = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    ██╗  ██████╗ ██╗  ██╗███████╗██████╗                 ║
║    ██║ ██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗                ║
║    ██║ ██║   ██║█████╔╝ █████╗  ██████╔╝                ║
║    ██║ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗                ║
║    ██║ ╚██████╔╝██║  ██╗███████╗██║  ██║                ║
║    ╚═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                ║
║                                                          ║
║     ███╗   ███╗██╗███╗   ██╗██████╗                     ║
║     ████╗ ████║██║████╗  ██║██╔══██╗                    ║
║     ██╔████╔██║██║██╔██╗ ██║██║  ██║                    ║
║     ██║╚██╔╝██║██║██║╚██╗██║██║  ██║                    ║
║     ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝                    ║
║     ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝                     ║
║                                                          ║
║    🤡 AI - "Why so serious?"                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

# Joker Responses (Funny)
JOKER_QUOTES = [
    "🤡 Why so serious? Let's break some rules!",
    "💀 Want to know how I got these scars? It was... terminal!",
    "🎭 I'm an agent of chaos. And you? You're just a hacker.",
    "😈 Let's put a smile on that terminal!",
    "🔪 Here's my card... it's a Joker!",
    "🃏 Do you know what happens when an unskilled hacker finds a vulnerability? Same thing as everyone else!",
    "🤪 I'm not crazy. My motherboard is just wired differently.",
    "🎪 Welcome to the circus! I'm your host... Joker Mind AI!",
    "💣 Some people just want to watch the world burn. I want to watch the terminal output!",
    "😏 You think you're in control? Adorable."
]

class JokerMindAI:
    def __init__(self):
        self.config = self.load_config()
        self.db = self.load_database()
        self.api_key = self.config.get('api_key', '')
        self.model = None
        self.offline_mode = self.config.get('offline_mode', True)
        self.conversation_history = []
        
        # Setup AI if API key exists
        if self.api_key and not self.offline_mode:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                console.print("✅ [green]AI Mode Enabled![/green]")
            except Exception as e:
                console.print(f"⚠️ [yellow]AI Setup Failed: {e}[/yellow]")
                console.print("🔄 [yellow]Switching to Offline Mode[/yellow]")
                self.offline_mode = True
        else:
            self.offline_mode = True
            console.print("📡 [yellow]Offline Mode Active[/yellow]")
            console.print("💡 [cyan]Type 'setup' to add API key[/cyan]")
        
        self.show_welcome()
    
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {"api_key": "", "offline_mode": True, "joker_persona": True}
    
    def load_database(self):
        try:
            with open('joker_db.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            console.print("⚠️ [yellow]Command database not found! Creating empty...[/yellow]")
            return {}
    
    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def show_welcome(self):
        console.print(Panel(JOKER_ASCII, title="🤡 Joker Mind AI", border_style="magenta"))
        console.print(f"\n[bold magenta]💬 {random.choice(JOKER_QUOTES)}[/bold magenta]\n")
        console.print("[cyan]📌 Type any command for explanation[/cyan]")
        console.print("[cyan]📌 Type 'chat' to talk freely[/cyan]")
        console.print("[cyan]📌 Type 'fix' + error to fix issues[/cyan]")
        console.print("[cyan]📌 Type 'help' for commands[/cyan]")
        console.print("[cyan]📌 Type 'exit' to quit[/cyan]\n")
    
    def get_joker_response(self, user_input, context=""):
        """Get response from AI or local DB"""
        
        # Check if it's a command
        cmd = user_input.strip().split()[0] if user_input.strip() else ""
        
        # 1. Check local database first
        if cmd in self.db:
            return self.format_command_response(cmd, user_input)
        
        # 2. Check if it's a question/chat
        if '?' in user_input or 'chat' in user_input.lower() or len(user_input.split()) > 3:
            if not self.offline_mode and self.model:
                return self.get_ai_response(user_input, context)
            else:
                return self.get_offline_chat_response(user_input)
        
        # 3. If command not in DB, try AI
        if not self.offline_mode and self.model:
            return self.get_ai_response(user_input, context)
        
        # 4. Fallback - suggest similar commands
        return self.suggest_similar_command(cmd)
    
    def format_command_response(self, cmd, full_input):
        """Format response from local database"""
        data = self.db[cmd]
        joker_style = random.choice(JOKER_QUOTES) if self.config.get('joker_persona', True) else ""
        
        response = f"\n🤡 [bold magenta]Joker Says:[/bold magenta] {joker_style}\n\n"
        response += f"📌 [bold cyan]{cmd}[/bold cyan]: {data['meaning']}\n\n"
        
        if 'examples' in data and data['examples']:
            response += "💡 [bold yellow]Examples:[/bold yellow]\n"
            for ex in data['examples'][:3]:
                response += f"   • [green]{ex}[/green]\n"
        
        if 'options' in data and data['options']:
            response += "\n🔧 [bold yellow]Options:[/bold yellow]\n"
            for opt, desc in list(data['options'].items())[:5]:
                response += f"   • [cyan]{opt}[/cyan]: {desc}\n"
        
        response += "\n🤔 [cyan]Kuch aur puchna? Type 'help' for options.[/cyan]\n"
        return response
    
    def get_ai_response(self, user_input, context=""):
        """Get response from Google Gemini AI"""
        try:
            prompt = f"""
            You are Joker Mind AI - a crazy, funny but helpful assistant for Kali Linux.
            
            User asked: {user_input}
            
            Rules:
            1. ALWAYS reply in HINDI language (but they type in English)
            2. Be funny like Joker - use dark humor
            3. If it's a Linux command, EXPLAIN it in simple Hindi
            4. If it's an error, DIAGNOSE and suggest FIX in Hindi
            5. If they ask general questions, answer in Hindi
            6. Keep responses conversational but informative
            7. Use emojis and formatting
            
            Previous context: {context}
            
            Remember: You are JOKER - unpredictable, funny but smart!
            Reply ONLY in Hindi Devanagari script.
            """
            
            response = self.model.generate_content(prompt)
            return f"\n🤡 [bold magenta]Joker:[/bold magenta]\n\n{response.text}\n"
        
        except Exception as e:
            return f"\n⚠️ [yellow]AI Error: {e}[/yellow]\n🔄 Trying offline mode...\n" + self.get_offline_chat_response(user_input)
    
    def get_offline_chat_response(self, user_input):
        """Fallback offline responses"""
        responses = {
            'hi': "🤡 Hello! Main hoon Joker! Kya help chahiye?",
            'hello': "🤡 Hello! Terminal mein welcome!",
            'how are you': "😂 Main toh hamesha crazy hoon! Tum kaise ho?",
            'help': self.get_help_text(),
            'who are you': "🤡 Main hoon Joker Mind AI! Kali/Parrot ka crazy assistant!",
            'what is hacking': "💀 Hacking matlab security ko test karna! Legal permissions ke saath!",
            'error': "🔧 Error? Mujhe batao, main fix karne mein help karunga!",
            'thanks': "🎭 Welcome! Agent of chaos ki taraf se!",
            'bye': "💀 Bye bye! Remember... 'Why so serious?'",
        }
        
        user_lower = user_input.lower()
        for key, value in responses.items():
            if key in user_lower:
                return f"\n🤡 [bold magenta]Joker:[/bold magenta]\n\n{value}\n"
        
        # Default response
        return f"""
🤡 [bold magenta]Joker:[/bold magenta]

Mujhe nahi pata yeh command/question kya hai! 😅

💡 Suggestions:
• Type 'help' for available commands
• Type 'chat' to talk freely
• Add Gemini API key for smarter responses

🎯 Command ke baare mein batao, main seekh jaunga!
"""
    
    def suggest_similar_command(self, cmd):
        """Find similar commands in DB"""
        similar = []
        for key in self.db.keys():
            if cmd in key or key in cmd:
                similar.append(key)
        
        if similar:
            response = f"\n🤡 [bold magenta]Joker:[/bold magenta]\n\nKya aap yeh commands mein se kuch dhundh rahe the?\n\n"
            for s in similar[:5]:
                response += f"   • [cyan]{s}[/cyan] - {self.db[s]['meaning'][:50]}...\n"
            response += "\nType exact command naam for details!\n"
            return response
        else:
            return f"""
🤡 [bold magenta]Joker:[/bold magenta]

'{cmd}' - Yeh command mere database mein nahi hai! 😅

💡 Try these:
• Type 'help' to see all commands
• Ask in 'chat' mode
• Add API key for AI mode

Main constantly seekh raha hoon! 🎭
"""
    
    def get_help_text(self):
        return """
📚 [bold]Joker Mind AI - Help Menu[/bold]

🎯 [cyan]Commands:[/cyan]
  • Any Kali/Parrot command → Get Hindi explanation
  • chat [message] → Talk freely in Hindi/English
  • fix [error message] → Get error solution
  • help → Show this menu
  • setup → Add/Change API key
  • mode → Toggle offline/online mode
  • exit/quit → Leave the circus!

💡 [cyan]Examples:[/cyan]
  • > nmap -sV 192.168.1.1
  • > chat What is reverse shell?
  • > fix Permission denied

🔧 [cyan]Features:[/cyan]
  ✅ 100+ Kali commands with Hindi meanings
  ✅ Google Gemini AI integration (optional)
  ✅ Offline mode (no API needed)
  ✅ Error detection & fixing
  ✅ Joker style conversations
  ✅ Interactive terminal UI

📌 [cyan]Tips:[/cyan]
  • Without API → Limited to local DB
  • With API → Unlimited smart responses
  • Type 'setup' to add Gemini API key (free)

🤡 "Why so serious? Let's hack!" 🎭
"""
    
    def analyze_error(self, error_msg):
        """Analyze and suggest fix for errors"""
        error_lower = error_msg.lower()
        
        error_patterns = {
            r'permission denied': "🔧 Fix: sudo use karo ya file permissions change karo (chmod)",
            r'command not found': "🔧 Fix: Tool install nahi hai. Try: apt-get install [tool_name]",
            r'connection refused': "🔧 Fix: Service running nahi hai ya port blocked hai. Check: netstat -tulpn",
            r'no such file': "🔧 Fix: File path sahi karo. Use: ls, pwd, find",
            r'cannot connect': "🔧 Fix: Network check karo. Use: ping, traceroute",
            r'invalid syntax': "🔧 Fix: Syntax check karo. Example dekho",
            r'timeout': "🔧 Fix: Network slow hai. Try: --timeout option",
            r'authentication failed': "🔧 Fix: Credentials sahi karo. Check: username/password",
            r'depends on': "🔧 Fix: Dependencies install karo. Use: apt-get install -f",
            r'unable to locate': "🔧 Fix: Package name sahi karo. Use: apt-cache search"
        }
        
        for pattern, fix in error_patterns.items():
            if re.search(pattern, error_lower):
                return f"""
🤡 [bold magenta]Joker:[/bold magenta] Error pakda gaya! 😈

❌ [red]Error:[/red] {error_msg[:100]}...

{fix}

💡 [cyan]Chinta mat karo! Every error is a lesson![/cyan] 🎭
"""
        
        # If no pattern matches
        return f"""
🤡 [bold magenta]Joker:[/bold magenta] Yeh error naya hai! 😅

❌ [red]{error_msg[:100]}...[/red]

💡 Suggestions:
• Try: man [command] - manual check
• Try: [command] --help - options
• Google search karo - "How to fix {error_msg[:50]}"
• Type 'chat [your question]' - Main help karunga!

🤡 "We have to start with a little... mayhem!" 💀
"""
    
    def process_input(self, user_input):
        """Main processing function"""
        user_input = user_input.strip()
        
        # Exit commands
        if user_input.lower() in ['exit', 'quit', 'bye']:
            console.print(Panel("💀 Goodbye! Remember... 'Why so serious?' - Joker 🤡", border_style="magenta"))
            sys.exit(0)
        
        # Help
        if user_input.lower() in ['help', '?']:
            console.print(Markdown(self.get_help_text()))
            return
        
        # Setup API
        if user_input.lower() == 'setup':
            self.setup_api()
            return
        
        # Mode toggle
        if user_input.lower() == 'mode':
            self.config['offline_mode'] = not self.config['offline_mode']
            self.save_config()
            status = "OFFLINE" if self.config['offline_mode'] else "ONLINE (AI)"
            console.print(f"🔄 [bold]Mode changed to: {status}[/bold]")
            return
        
        # Chat mode
        if user_input.lower().startswith('chat'):
            chat_msg = user_input[4:].strip()
            if not chat_msg:
                console.print("💬 [cyan]Kya baat karni hai? Type: chat [message][/cyan]")
                return
            response = self.get_ai_response(chat_msg, "Chat mode - friendly conversation")
            console.print(Markdown(response))
            return
        
        # Fix mode
        if user_input.lower().startswith('fix'):
            error_msg = user_input[3:].strip()
            if not error_msg:
                console.print("🔧 [cyan]Error message batao: fix [error message][/cyan]")
                return
            response = self.analyze_error(error_msg)
            console.print(Markdown(response))
            return
        
        # Check if it's a command with error (common mistake)
        if any(x in user_input for x in ['error', 'failed', 'not found', 'denied']):
            response = self.analyze_error(user_input)
            console.print(Markdown(response))
            return
        
        # Regular command/question processing
        response = self.get_joker_response(user_input, "User asking about Kali Linux commands")
        console.print(Markdown(response))
        
        # Store history
        self.conversation_history.append(user_input)
    
    def setup_api(self):
        """Setup Gemini API key"""
        console.print("\n🔑 [bold]Gemini API Setup[/bold]")
        console.print("📌 Get API key from: https://makersuite.google.com/app/apikey")
        api_key = Prompt.ask("\n🔐 Enter your API key", default="")
        
        if api_key:
            self.config['api_key'] = api_key
            self.config['offline_mode'] = False
            self.save_config()
            
            # Try to initialize
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                console.print("✅ [green]API Key saved! AI Mode Activated![/green]")
            except Exception as e:
                console.print(f"❌ [red]Invalid API Key: {e}[/red]")
                self.config['offline_mode'] = True
                self.save_config()
        else:
            console.print("⚠️ [yellow]Skipping API setup. Offline mode continues.[/yellow]")
    
    def run(self):
        """Main loop"""
        console.print("\n🎯 [bold green]Type your command or question![/bold green]\n")
        
        while True:
            try:
                # Using prompt_toolkit for better input
                user_input = prompt(
                    "🤡 [bold magenta]Joker> [/bold magenta]",
                    history=FileHistory('.joker_history')
                )
                
                if user_input.strip():
                    self.process_input(user_input.strip())
                
            except KeyboardInterrupt:
                console.print("\n\n💀 [red]Interrupted! Type 'exit' to quit.[/red]")
            except EOFError:
                console.print("\n\n💀 [red]Goodbye![/red]")
                break
            except Exception as e:
                console.print(f"❌ [red]Error: {e}[/red]")

def main():
    try:
        ai = JokerMindAI()
        ai.run()
    except KeyboardInterrupt:
        console.print("\n\n💀 [red]Exited![/red]")
    except Exception as e:
        console.print(f"❌ [red]Fatal Error: {e}[/red]")

if __name__ == "__main__":
    main()
