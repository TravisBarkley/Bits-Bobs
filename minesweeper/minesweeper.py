import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.mine_locations = set()
        self.reveal_board = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.setup()

    def setup(self):
        self.root.title("Minesweeper")
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.root, width=2, height=1, command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
        self.place_mines()

    def place_mines(self):
        while len(self.mine_locations) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) not in self.mine_locations:
                self.mine_locations.add((r, c))
                self.board[r][c] = '*'

    def adjacent_mines(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            if 0 <= row + dr < self.rows and 0 <= col + dc < self.cols:
                if self.board[row + dr][col + dc] == '*':
                    count += 1
        return count

    def reveal(self, row, col):
        if self.reveal_board[row][col] or self.flagged[row][col]:
            return
        self.reveal_board[row][col] = True
        adjacent_mines = self.adjacent_mines(row, col)
        if self.board[row][col] == '*':
            self.buttons[row][col].config(text='*', bg='red')
            self.game_over = True
            self.end_game(False)
        else:
            self.board[row][col] = str(adjacent_mines) if adjacent_mines > 0 else ' '
            self.buttons[row][col].config(text=self.board[row][col], state='disabled', relief=tk.SUNKEN)
            if adjacent_mines == 0:
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                for dr, dc in directions:
                    if 0 <= row + dr < self.rows and 0 <= col + dc < self.cols:
                        self.reveal(row + dr, col + dc)
        if self.check_win():
            self.end_game(True)

    def check_win(self):
        return all(self.reveal_board[r][c] or self.board[r][c] == '*' for r in range(self.rows) for c in range(self.cols))

    def end_game(self, win):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '*' and not self.flagged[r][c]:
                    self.buttons[r][c].config(text='*', bg='red')
        if win:
            messagebox.showinfo("Minesweeper", "Congratulations! You've won the game.")
        else:
            messagebox.showinfo("Minesweeper", "Game Over! You hit a mine.")
        self.root.quit()

    def click(self, row, col):
        if not self.flagged[row][col]:
            self.reveal(row, col)

    def right_click(self, row, col):
        if not self.reveal_board[row][col]:
            if self.flagged[row][col]:
                self.buttons[row][col].config(text='', bg='SystemButtonFace')
                self.flagged[row][col] = False
            else:
                self.buttons[row][col].config(text='F', bg='yellow')
                self.flagged[row][col] = True

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root, rows=10, cols=10, mines=10)
    root.mainloop()
