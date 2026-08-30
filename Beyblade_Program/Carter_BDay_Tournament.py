import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class TournamentAppWithBackground:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Bracket with Background")

        # Load and set background image
        self.bg_image = Image.open("beyblade_emblem.png")  # 🔁 Replace with your image
        self.bg_image = self.bg_image.resize((1000, 500))  # Resize as needed
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root, width=1000, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # You will dynamically add widgets on top of this canvas
        self.num_var = tk.StringVar()
        self.setup_participant_number_selection()

    def setup_participant_number_selection(self):
        # Label
        label = ttk.Label(self.root, text="Select number of Bladers:", font=("Arial", 14), background="#F2F2F6")
        self.canvas.create_window(500, 100, window=label)

        # Dropdown
        participant_options = ["2", "4", "8", "10", "12", "14","16", "18", "20"]
        num_select = ttk.Combobox(self.root, textvariable=self.num_var, values=participant_options, state="readonly")
        self.canvas.create_window(500, 140, window=num_select)

        # Button
        start_button = ttk.Button(self.root, text="Next", command=self.setup_name_entry)
        self.canvas.create_window(500, 180, window=start_button)

    def setup_name_entry(self):
        try:
            self.num_participants = int(self.num_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please select a number.")
            return

        self.entries = []

        for i in range(self.num_participants):
            label = ttk.Label(self.root, text=f"Player {i+1}:", background="#ffffff")
            entry = ttk.Entry(self.root)
            self.canvas.create_window(400, 220 + i * 40, window=label)
            self.canvas.create_window(500, 220 + i * 40, window=entry)
            self.entries.append(entry)

        start_button = ttk.Button(self.root, text="Start Tournament", command=self.start_tournament)
        self.canvas.create_window(500, 230 + self.num_participants * 40, window=start_button)

    def start_tournament(self):
        names = [e.get().strip() for e in self.entries]
        if "" in names:
            messagebox.showwarning("Missing Names", "Please fill in all names.")
            return
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        TournamentBracket(self.root, self.canvas, names)


class TournamentBracket:
    def __init__(self, root, canvas, players):
        self.root = root
        self.canvas = canvas
        self.players = players
        self.rounds = []
        self.round_results = []
        import random
        random.shuffle(self.players)
        self.build_round(self.players, 1, 150)

    def build_round(self, current_players, round_number, x_pos):
        winners = []
        round_widgets = []

        for i in range(0, len(current_players), 2):
            y = 100 + i * 80
            p1, p2 = current_players[i], current_players[i + 1]
            label = ttk.Label(self.root, text=f"{p1} vs {p2}", background="#ffffff")
            self.canvas.create_window(x_pos, y, window=label)

            winner_select = ttk.Combobox(self.root, values=[p1, p2], state="readonly")
            self.canvas.create_window(x_pos, y + 30, window=winner_select)
            round_widgets.append(winner_select)

        self.rounds.append(round_widgets)
        self.round_results.append(winners)

        submit_button = ttk.Button(self.root, text="Submit Round", command=lambda: self.collect_winners(round_widgets, round_number + 1, x_pos + 200))
        self.canvas.create_window(x_pos, y + 80, window=submit_button)

    def collect_winners(self, widgets, next_round_number, next_x_pos):
        winners = []
        for widget in widgets:
            winner = widget.get()
            if not winner:
                messagebox.showwarning("Incomplete", "Select all winners first.")
                return
            winners.append(winner)

        self.round_results[-1] = winners

        if len(winners) == 1:
            messagebox.showinfo("Winner!", f"The winner is {winners[0]} 🎉")
        else:
            self.build_round(winners, next_round_number, next_x_pos)


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentAppWithBackground(root)
    root.mainloop()
