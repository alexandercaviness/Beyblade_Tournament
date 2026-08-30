import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random

class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carter BDay Beyblade Tournament")
        self.root.geometry("1200x700")

        # Load background image
        self.bg_image = Image.open("beyblade_emblem.png")
        self.bg_image = self.bg_image.resize((1200, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=900, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.frame = tk.Frame(self.canvas, bg="#ffffff", bd=2)
        self.canvas.create_window(450, 100, window=self.frame, anchor="n")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.frame, text="Enter Tournament Details", font=("Arial", 18, "bold"), bg="#ffffff")
        title.pack(pady=10)

        self.participant_count = tk.IntVar(value=8)
        count_label = tk.Label(self.frame, text="Number of Participants (4, 8, 10, 16, 18, 20, 32):", bg="#ffffff")
        count_label.pack()

        count_entry = ttk.Entry(self.frame, textvariable=self.participant_count)
        count_entry.pack(pady=5)

        generate_button = ttk.Button(self.frame, text="Generate Name Fields", command=self.generate_name_fields)
        generate_button.pack(pady=10)

        self.names_frame = tk.Frame(self.frame, bg="#ffffff")
        self.names_frame.pack()

        self.start_button = ttk.Button(self.frame, text="Start Tournament", state="disabled", command=self.start_tournament)
        self.start_button.pack(pady=20)

    def generate_name_fields(self):
        for widget in self.names_frame.winfo_children():
            widget.destroy()

        self.name_entries = []
        count = self.participant_count.get()

        if count not in [4, 6, 8, 10, 12, 16, 18, 20, 32]:
            messagebox.showerror("Invalid Number", "Please enter a valid number of participants (4, 8, 10, 16, 18, 20, 32).")
            return

        scroll_canvas = tk.Canvas(self.names_frame, width=300, height=200)
        scroll_canvas.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.names_frame, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        scrollable_frame = tk.Frame(scroll_canvas)
        scrollable_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        for i in range(count):
            entry = ttk.Entry(scrollable_frame)
            entry.pack(pady=3)
            self.name_entries.append(entry)

        self.start_button.config(state="normal")

    def add_byes(self, players):
        """Ensure player count is a power of 2 by adding BYE placeholders."""
        next_power = 1
        while next_power < len(players):
            next_power *= 2
        while len(players) < next_power:
            players.append("BYE")
        return players

    def start_tournament(self):
        names = [e.get().strip() for e in self.name_entries]
        if "" in names:
            messagebox.showerror("Missing Names", "Please enter all participant names.")
            return

        random.shuffle(names)
        self.players = self.add_byes(names)  # Add BYEs if needed
        self.current_round = 1
        self.matches = []

        self.frame.destroy()
        self.show_bracket()

    def show_bracket(self):
        self.bracket_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas.create_window(450, 100, window=self.bracket_frame, anchor="n")

        title = tk.Label(self.bracket_frame, text=f"Round {self.current_round}", font=("Arial", 18, "bold"), bg="#ffffff")
        title.pack(pady=10)

        self.next_round_players = []

        for i in range(0, len(self.players), 2):
            p1 = self.players[i]
            p2 = self.players[i+1]
            match_frame = tk.Frame(self.bracket_frame, bg="#ffffff")
            match_frame.pack(pady=5)

            label = tk.Label(match_frame, text=f"{p1} vs {p2}", font=("Arial", 14), bg="#ffffff")
            label.pack()

            # Auto-advance if BYE
            if p1 == "BYE":
                self.next_round_players.append(p2)
                continue
            elif p2 == "BYE":
                self.next_round_players.append(p1)
                continue

            # Create buttons
            b1 = ttk.Button(match_frame, text=p1)
            b2 = ttk.Button(match_frame, text=p2)
            b1.config(command=lambda name=p1, b1=b1, b2=b2: self.select_winner(name, b1, b2))
            b2.config(command=lambda name=p2, b1=b1, b2=b2: self.select_winner(name, b1, b2))

            b1.pack(side=tk.LEFT, padx=10)
            b2.pack(side=tk.LEFT, padx=10)

        # If all matches were BYEs, auto-start next round
        if len(self.next_round_players) == len(self.players) // 2:
            self.players = self.add_byes(self.next_round_players[:])
            self.next_round_players.clear()
            self.current_round += 1
            self.bracket_frame.destroy()
            self.show_bracket()

    def select_winner(self, name, btn1, btn2):
        # Add winner
        self.next_round_players.append(name)

        # Disable both buttons for this match
        btn1.config(state="disabled")
        btn2.config(state="disabled")

        # If all matches in the round have winners
        if len(self.next_round_players) == len(self.players) // 2:
            if len(self.next_round_players) == 1:
                self.show_winner(self.next_round_players[0])
            else:
                self.players = self.add_byes(self.next_round_players[:])
                self.next_round_players.clear()
                self.current_round += 1
                self.bracket_frame.destroy()
                self.show_bracket()

    def show_winner(self, name):
        self.bracket_frame.destroy()
        winner_label = tk.Label(self.canvas, text=f"🏆 {name} is the Champion! 🏆",
                                font=("Arial", 24, "bold"), bg="gold", fg="black")
        self.canvas.create_window(450, 300, window=winner_label, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()