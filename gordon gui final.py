import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
from pynput.keyboard import Controller, Key

class GordonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GORDON - Automation System")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        self.keyboard = Controller()
        self.is_running = False
        self.sent_count = 0
        self.animals = ["███████████████████████████"
                        "███████▀▀▀░░░░░░░▀▀▀███████"
                        "████▀░░░░░░░░░░░░░░░░░▀████"
                        "███│░░░░░░░░░░░░░░░░░░░│███"
                        "██▌│░░░░░░░░░░░░░░░░░░░│▐██"
                        "██░└┐░░░░░░░░░░░░░░░░░┌┘░██"
                        "██░░└┐░░░░░░░░░░░░░░░┌┘░░██"
                        "██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██"
                        "██▌░│██████▌░░░▐██████│░▐██"
                        "███░│▐███▀▀░░▄░░▀▀███▌│░███"
                        "██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██"
                        "██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██"
                        "████▄─┘██▌░░░░░░░▐██└─▄████"
                        "█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████"
                        "████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████"
                        "█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████"
                        "███████▄░░░░░░░░░░░▄███████"
                        "██████████▄▄▄▄▄▄▄██████████"
                        "███████████████████████████", " ██████╗  ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗"
                                                       "██╔════╝ ██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║"
                                                       "██║  ███╗██║   ██║██████╔╝██║  ██║██║   ██║██╔██╗ ██║"
                                                       "██║   ██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╗██║"
                                                       "╚██████╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝██║ ╚████║"
                                                       " ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝", " █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██╗  ██╗"
                                                                                                                "██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ╚██╗██╔╝"
                                                                                                                "███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║        ╚███╔╝ "
                                                                                                                "██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║        ██╔██╗"
                                                                                                                "██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ██╔╝ ██╗"
                                                                                                                "╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═╝"]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="◆ GORDON ◆",
            font=("Arial", 36, "bold"),
            fg="#FF6B35",
            bg="#000000"
        )
        title.pack(pady=20)
        
        # Main frame
        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Settings frame
        settings = tk.LabelFrame(main, text="Settings", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10, "bold"), padx=15, pady=15)
        settings.pack(fill=tk.X, pady=10)
        
        # Number of messages
        tk.Label(settings, text="Number of Messages:", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_entry = tk.Entry(settings, width=15, bg="#000000", fg="#FF6B35", font=("Arial", 10))
        self.num_entry.insert(0, "100")
        self.num_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Delay between messages
        tk.Label(settings, text="Delay Between Messages (sec):", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.delay_entry = tk.Entry(settings, width=15, bg="#000000", fg="#FF6B35", font=("Arial", 10))
        self.delay_entry.insert(0, "1")
        self.delay_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Startup delay
        tk.Label(settings, text="Startup Delay (sec):", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.startup_entry = tk.Entry(settings, width=15, bg="#000000", fg="#FF6B35", font=("Arial", 10))
        self.startup_entry.insert(0, "15")
        self.startup_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Countdown frame
        self.countdown_frame = tk.Frame(main, bg="#2a2a2a", relief=tk.SUNKEN, bd=2, height=50)
        self.countdown_frame.pack(fill=tk.X, pady=10)
        self.countdown_frame.pack_propagate(False)
        
        self.countdown_label = tk.Label(
            self.countdown_frame,
            text="Ready",
            font=("Arial", 20, "bold"),
            fg="#FF6B35",
            bg="#2a2a2a"
        )
        self.countdown_label.pack(pady=10)
        
        # Status frame
        status = tk.Frame(main, bg="#2a2a2a", relief=tk.SUNKEN, bd=2)
        status.pack(fill=tk.X, pady=10)
        
        tk.Label(status, text="Progress:", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=15, pady=10)
        
        self.status_label = tk.Label(status, text="0 / 100", font=("Arial", 16, "bold"), fg="#FF6B35", bg="#2a2a2a")
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.progress = ttk.Progressbar(status, length=300, mode='determinate', maximum=100)
        self.progress.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Current animal
        animal_frame = tk.Frame(main, bg="#2a2a2a", relief=tk.SUNKEN, bd=2)
        animal_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(animal_frame, text="Current:", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=15, pady=10)
        
        self.animal_label = tk.Label(animal_frame, text="━━━━━━", font=("Arial", 18, "bold"), fg="#FF6B35", bg="#2a2a2a")
        self.animal_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Log frame
        log_frame = tk.Frame(main, bg="#2a2a2a", relief=tk.SUNKEN, bd=2, height=150)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        log_frame.pack_propagate(False)
        
        tk.Label(log_frame, text="Log:", bg="#2a2a2a", fg="#FF6B35", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=15, pady=5)
        
        self.log_text = tk.Text(log_frame, height=8, bg="#000000", fg="#00FF00", font=("Courier", 8), relief=tk.FLAT, padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        buttons = tk.Frame(main, bg="#1a1a1a")
        buttons.pack(fill=tk.X, pady=15)
        
        self.start_btn = tk.Button(buttons, text="▶ START", font=("Arial", 11, "bold"), bg="#FF6B35", fg="#000000", relief=tk.RAISED, bd=3, padx=25, pady=10, command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(buttons, text="⏹ STOP", font=("Arial", 11, "bold"), bg="#555555", fg="#CCCCCC", relief=tk.RAISED, bd=3, padx=25, pady=10, command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(buttons, text="↻ RESET", font=("Arial", 11, "bold"), bg="#333333", fg="#CCCCCC", relief=tk.RAISED, bd=3, padx=25, pady=10, command=self.reset)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        self.add_log("✓ GORDON System Ready")
        self.add_log("✓ Enter settings and press START")
        
    def add_log(self, msg):
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def start(self):
        if not self.is_running:
            try:
                num_messages = int(self.num_entry.get())
                delay = float(self.delay_entry.get())
                startup = int(self.startup_entry.get())
                
                if num_messages < 1:
                    messagebox.showerror("Error", "Please enter a valid number")
                    return
                
                self.is_running = True
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.progress.config(maximum=num_messages)
                
                self.add_log("🚀 Starting automation...")
                
                thread = threading.Thread(target=self.run_automation, args=(num_messages, delay, startup), daemon=True)
                thread.start()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
    def stop(self):
        self.is_running = False
        self.add_log("❌ Stopped by user")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def reset(self):
        self.is_running = False
        self.sent_count = 0
        self.status_label.config(text="0 / 100")
        self.progress.config(value=0)
        self.animal_label.config(text="━━━━━━")
        self.countdown_label.config(text="Ready")
        self.log_text.delete(1.0, tk.END)
        self.add_log("✓ System reset")
        self.add_log("✓ Enter settings and press START")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            if not self.is_running:
                return False
            self.countdown_label.config(text=f"{i} seconds")
            self.root.update()
            time.sleep(1)
        self.countdown_label.config(text="GO! 🚀")
        return True
        
    def run_automation(self, num_messages, delay, startup):
        self.add_log(f"⏳ Wait {startup} seconds...")
        
        if not self.countdown(startup):
            return
            
        self.add_log("⚙ Starting message cycle...")
        self.sent_count = 0
        
        while self.is_running and self.sent_count < num_messages:
            animal = random.choice(self.animals)
            message = f"you are a {animal}"
            
            try:
                # Type message
                self.keyboard.type(message)
                time.sleep(0.2)
                
                # Press Enter
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                
                # Update display
                self.animal_label.config(text=animal.upper())
                self.sent_count += 1
                self.status_label.config(text=f"{self.sent_count} / {num_messages}")
                self.progress.config(value=self.sent_count)
                
                if self.sent_count % 25 == 0:
                    self.add_log(f"⚡ Sent {self.sent_count} messages")
                
                time.sleep(delay)
                
            except Exception as e:
                self.add_log(f"❌ Error: {str(e)}")
                self.is_running = False
                break
                
        if self.sent_count >= num_messages and self.is_running:
            self.add_log(f"✅ Complete! Sent {num_messages} messages")
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.countdown_label.config(text="✓ Done!")


if __name__ == "__main__":
    root = tk.Tk()
    app = GordonGUI(root)
    root.mainloop()
