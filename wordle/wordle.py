import tkinter as tk
from tkinter import messagebox
import random

class WordleApp:
    def __init__(self, root, word_list):
        self.root = root
        self.word_list = word_list
        self.max_attempts = 6
        self.word_length = 5  # Assuming all words are 5 letters long
        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        self.root.title("Wordle")

        self.entries = []
        self.result_labels = []

        for i in range(self.max_attempts):
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            
            entry = tk.Entry(frame, width=self.word_length, font=('Helvetica', 24), justify='center')
            entry.grid(row=0, column=0)
            self.entries.append(entry)
            
            result_label = tk.Label(frame, text='', font=('Helvetica', 24))
            result_label.grid(row=0, column=1, padx=10)
            self.result_labels.append(result_label)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_guess)
        self.submit_button.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.start_new_game)
        self.restart_button.pack(pady=5)

        self.root.bind('<Return>', lambda event: self.check_guess())

    def start_new_game(self):
        self.target_word = random.choice(self.word_list).lower()
        self.current_attempt = 0
        for entry in self.entries:
            entry.delete(0, tk.END)
            entry.config(state='normal')
        for label in self.result_labels:
            label.config(text='', bg=self.root.cget('bg'))
        self.submit_button.config(state='normal')

    def check_guess(self):
        if self.current_attempt >= self.max_attempts:
            return

        guess = self.entries[self.current_attempt].get().lower()
        if len(guess) != self.word_length:
            messagebox.showwarning("Invalid Input", f"Please enter a {self.word_length}-letter word.")
            return

        result, colors = self.evaluate_guess(guess)
        self.display_result(self.current_attempt, guess, result, colors)

        if guess == self.target_word:
            messagebox.showinfo("Congratulations", "You've guessed the word!")
            self.end_game()
        elif self.current_attempt == self.max_attempts - 1:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts. The word was '{self.target_word}'.")
            self.end_game()
        else:
            self.current_attempt += 1

    def evaluate_guess(self, guess):
        result = ["_"] * self.word_length
        colors = [""] * self.word_length
        target_word_chars = list(self.target_word)
        
        # First pass for correct positions
        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                result[i] = guess[i].upper()
                colors[i] = 'green'
                target_word_chars[i] = None  # Mark this char as used

        # Second pass for correct letters in wrong positions
        for i in range(self.word_length):
            if result[i] == "_" and guess[i] in target_word_chars:
                result[i] = guess[i].lower()
                colors[i] = 'yellow'
                target_word_chars[target_word_chars.index(guess[i])] = None

        return "".join(result), colors

    def display_result(self, attempt, guess, result, colors):
        for i, char in enumerate(result):
            label = self.result_labels[attempt]
            label.config(text=result, bg=colors[i] if colors[i] else self.root.cget('bg'))

    def end_game(self):
        for entry in self.entries:
            entry.config(state='disabled')
        self.submit_button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
word_list = [
    "apple", "grape", "peach", "berry", "melon", "lemon", "plums", "mango",
    "kiwis", "papaw", "guava", "chili", "onion", "spice", "cider", "honey",
    "bread", "pizza", "pasta", "salad", "sauce", "tacos", "candy", "chefs",
    "wheat", "yeast", "grill", "bacon", "beans", "beefy", "basil", "cheese",
    "chips", "cocoa", "cream", "crisp", "cumin", "dates", "dough", "fruit",
    "grain", "herbs", "jelly", "knife", "latte", "lemon", "limes", "liver",
    "loafs", "meats", "mints", "mocha", "munch", "nacho", "olive", "pecan",
    "pesto", "pilaf", "pizza", "plant", "plums", "prune", "ramen", "rolls",
    "salsa", "seeds", "sherd", "smoke", "spice", "spoon", "squid", "steak",
    "sugar", "sushi", "syrup", "tango", "toast", "torte", "treat", "trout",
    "tulip", "tummy", "tunis", "turns", "turbo", "tusks", "ultra", "umbra",
    "uncle", "under", "union", "unite", "unity", "urged", "urges", "users",
    "usual", "vases", "vivid", "vocal", "vodka", "voice", "voted", "voter",
    "votes", "wager", "wagon", "wages", "waist", "water", "whale", "wheat",
    "wheel", "whine", "wiped", "wiper", "wipes", "wired", "wires", "wiser",
    "witch", "wives", "woken", "woman", "women", "woods", "woody", "words",
    "works", "worms", "worry", "worse", "worst", "worth", "wound", "wraps",
    "wrist", "write", "wrong", "wrote", "yacht", "yards", "yarns", "yawns",
    "yearn", "years", "yeast", "yield", "young", "yours", "youth", "zebra",
    "zeros", "zesty", "zonal", "zones"
]
    app = WordleApp(root, word_list)
    root.mainloop()
