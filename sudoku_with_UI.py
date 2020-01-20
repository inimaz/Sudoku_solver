
# Creating a Gui for the sudoku. Inspired by http://newcoder.io/gui/part-3/
import numpy as np
from tkinter import Tk, Canvas, Frame, Label, Button, BOTH, TOP, BOTTOM
import main as sudoku_solver

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

# if __name__ == "__main__":


class StartUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")

        self.label = Label(
            master, text="If you are curious, you'll find the puzzles around"
            " you. If you are determined, you will solve them.")
        self.label.pack()

        self.start_button = Button(
            master, text="Start", fg='purple', command=self.start_game)
        self.start_button.pack(side=BOTTOM)

    def start_game(self):
        GameUI(self.master)
        self.start_button.destroy()


class GameUI:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.check_button = Button(
            master, text="Check", fg='green')
        self.check_button.pack(side=BOTTOM)

        # Get a sudoku and its solution
        self.user_sudoku, self.sudoku_solution = sudoku_solver.randomized_sudoku()

        self.__draw_grid()
        self.__draw_sudoku()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_sudoku(self):
        """
        Fills the grid with sudoku numbers
        """
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                number = sudoku_solver.sudoku_1[i][j]
                print(self.sudoku_solution)
                if number != 0:
                    color = "black"

                    x = MARGIN + SIDE / 2 + i * SIDE
                    y = MARGIN + SIDE / 2 + j * SIDE
                    self.canvas.create_text(
                        x, y, text=number, tags="numbers", fill=color)


root = Tk()
StartUI(root)
root.mainloop()
