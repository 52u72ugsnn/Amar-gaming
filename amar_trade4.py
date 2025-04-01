
import random
import time
import threading
import tkinter as tk
from tkinter import messagebox
import winsound

class AmarTradeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Amar Trade⁴")
        self.root.geometry("400x700")
        self.root.configure(bg="#f0f0f0")
        
        self.bet_amount_var = tk.DoubleVar()
        self.auto_cashout_var = tk.DoubleVar()
        self.manual_cashout_var = tk.DoubleVar()
        self.player_name_var = tk.StringVar()
        
        self.balance = 1000.0
        self.winnings_history = []
        self.leaderboard = []
        self.player_stats = {}
        self.daily_bonus_claimed = False
        
        tk.Label(root, text="खिलाड़ी का नाम:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        tk.Entry(root, textvariable=self.player_name_var, font=("Arial", 12), bg="white", width=30).pack(pady=5)
        
        tk.Label(root, text="शर्त राशि:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        tk.Entry(root, textvariable=self.bet_amount_var, font=("Arial", 12), bg="white", width=30).pack(pady=5)
        
        tk.Label(root, text="ऑटो कैशआउट गुणक:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        tk.Entry(root, textvariable=self.auto_cashout_var, font=("Arial", 12), bg="white", width=30).pack(pady=5)
        
        tk.Label(root, text="मैनुअल कैशआउट गुणक (वैकल्पिक):", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        tk.Entry(root, textvariable=self.manual_cashout_var, font=("Arial", 12), bg="white", width=30).pack(pady=5)
        
        self.start_button = tk.Button(root, text="खेल शुरू करें", command=self.run_game, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20, height=1)
        self.start_button.pack(pady=10)
        
        self.claim_bonus_button = tk.Button(root, text="दैनिक बोनस प्राप्त करें", command=self.claim_daily_bonus, bg="#FFD700", fg="black", font=("Arial", 12, "bold"), width=20, height=1)
        self.claim_bonus_button.pack(pady=5)
        
        self.multiplier_label = tk.Label(root, text="गुणक: 1.0x", font=("Arial", 14, "bold"), fg="blue", bg="#f0f0f0")
        self.multiplier_label.pack(pady=5)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0")
        self.result_label.pack(pady=5)
        
        self.balance_label = tk.Label(root, text=f"शेष राशि: ₹{self.balance}", font=("Arial", 12, "bold"), fg="green", bg="#f0f0f0")
        self.balance_label.pack(pady=5)
        
        self.history_label = tk.Label(root, text="जीत का इतिहास:", font=("Arial", 12), bg="#f0f0f0")
        self.history_label.pack(pady=5)
        
        self.leaderboard_label = tk.Label(root, text="लीडरबोर्ड:", font=("Arial", 12, "bold"), fg="purple", bg="#f0f0f0")
        self.leaderboard_label.pack(pady=5)
        
        self.stats_label = tk.Label(root, text="खिलाड़ी आँकड़े:", font=("Arial", 12, "bold"), fg="dark blue", bg="#f0f0f0")
        self.stats_label.pack(pady=5)
        
        self.cashed_out = False
        self.multiplier = 1.0

    def claim_daily_bonus(self):
        if not self.daily_bonus_claimed:
            self.balance += 10.0
            self.daily_bonus_claimed = True
            self.update_stats()
            messagebox.showinfo("बोनस प्राप्त", "आपने ₹10 का दैनिक बोनस प्राप्त किया!")
        else:
            messagebox.showinfo("बोनस प्राप्त", "आपने आज का बोनस पहले ही प्राप्त कर लिया है!")

    def run_game(self):
        self.start_button.config(state=tk.DISABLED)
        player_name = self.player_name_var.get().strip()
        bet_amount = self.bet_amount_var.get()
        auto_cashout = self.auto_cashout_var.get()
        manual_cashout = self.manual_cashout_var.get() or 0
        
        if not player_name:
            messagebox.showerror("त्रुटि", "कृपया खिलाड़ी का नाम दर्ज करें!")
            self.start_button.config(state=tk.NORMAL)
            return
        
        if bet_amount > self.balance:
            messagebox.showerror("त्रुटि", "पर्याप्त शेष राशि नहीं है!")
            self.start_button.config(state=tk.NORMAL)
            return
        
        self.balance -= bet_amount
        crash_point = round(random.uniform(1.1, 5.0), 2)
        self.cashed_out = False
        self.update_stats()

        def manual_cashout():
            self.cashed_out = True

        cashout_button = tk.Button(self.root, text="मैनुअल कैशआउट", command=manual_cashout, bg="#FF5733", fg="white", font=("Arial", 12, "bold"), width=20)
        cashout_button.pack(pady=5)

        def update_multiplier():
            nonlocal bet_amount, auto_cashout, manual_cashout, crash_point, player_name
            while self.multiplier < crash_point and not self.cashed_out:
                time.sleep(0.5)
                self.multiplier = round(self.multiplier * 1.15, 2)
                self.multiplier_label.config(text=f"गुणक: {self.multiplier}x")
                
                if self.multiplier >= auto_cashout:
                    self.cashed_out = True
                    self.play_sound("win")
                    winnings = bet_amount * auto_cashout
                    self.update_balance(winnings, f"ऑटो कैशआउट {auto_cashout}x पर! आप जीते: ₹{winnings}", "green")
                    return

                if self.cashed_out or (manual_cashout > 0 and self.multiplier >= manual_cashout):
                    self.play_sound("win")
                    winnings = bet_amount * self.multiplier
                    self.update_balance(winnings, f"मैनुअल कैशआउट {self.multiplier}x पर! आप जीते: ₹{winnings}", "green")
                    return
            
            self.play_sound("lose")
            self.show_result(f"क्रैश {crash_point}x पर! आप ₹{bet_amount} हार गए", "red")

        threading.Thread(target=update_multiplier, daemon=True).start()

    def play_sound(self, result):
        if result == "win":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        elif result == "lose":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

    def update_balance(self, winnings, message, color):
        self.balance += winnings
        self.winnings_history.append(round(winnings, 2))
        self.show_result(message, color)
        self.update_stats()

    def show_result(self, message, color):
        self.result_label.config(text=message, fg=color)
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("खेल परिणाम", message)

    def update_stats(self):
        self.balance_label.config(text=f"शेष राशि: ₹{round(self.balance, 2)}")
        history_text = "जीत का इतिहास: " + ", ".join(map(str, self.winnings_history[-5:]))
        self.history_label.config(text=history_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = AmarTradeGame(root)
    root.mainloop()
