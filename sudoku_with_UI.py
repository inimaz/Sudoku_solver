
# Creating a Gui for the sudoku. Inspired by http://newcoder.io/gui/part-3/
import numpy as np
from copy import deepcopy  # To create 2 independent copies of the same matrix
from tkinter import Tk, Canvas, Frame, Label, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT
import main as sudoku_solver

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

# if __name__ == "__main__":


class StartUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")

        self.frame = Frame(master)
        self.frame.pack(side=TOP)
        self.label = Label(
            self.frame, text="\"If you are curious, you'll find the puzzles around"
            " you. \nIf you are determined, you will solve them.\"")
        self.label.pack(side=TOP)

        self.start_button = Button(
            master, text="Start", fg='purple', command=self.start_game)
        self.start_button.pack(side=BOTTOM)

    def start_game(self):
        GameUI(self.master)
        self.start_button.destroy()


class GameUI:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(fill=BOTH, side=TOP)

        self.check_button = Button(
            master, text="Check", fg='green')
        self.check_button.pack(side=RIGHT)
        self.solve_button = Button(
            master, text="Solve", fg='blue')
        self.solve_button.pack(side=RIGHT)
        self.hint_button = Button(
            master, text="Hint", fg='purple')
        self.hint_button.pack(side=RIGHT)

        # Get a sudoku and its solution
        self.user_sudoku = sudoku_solver.randomized_sudoku()
        self.sudoku_solution = sudoku_solver.solve_sudoku(
            deepcopy(self.user_sudoku))

        self.canvas.bind("<Button-1>", self.canvas_click)
        #self.canvas.bind("<Key>", self.canvas_key)

        self.row, self.column = 0, 0

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
                number = self.user_sudoku[i, j]
                if number != 0:
                    color = "black"

                    x = MARGIN + SIDE / 2 + i * SIDE
                    y = MARGIN + SIDE / 2 + j * SIDE
                    self.canvas.create_text(
                        x, y, text=number, tags="numbers", fill=color)

    def canvas_click(self, event):
        x, y = event.x, event.y
        if WIDTH - MARGIN > x > MARGIN and HEIGHT - MARGIN > y > MARGIN:
            self.canvas.focus_set()

            row = (x - MARGIN) // SIDE
            column = (y - MARGIN) // SIDE

            if (row, column) == (self.row, self.column):
                (self.row, self.column) = (-1, -1)
            elif self.user_sudoku[row][column] == 0:
                self.row, self.column = row, column

        self.__draw_red_box()

    def __draw_red_box(self):

        self.canvas.delete("red_square")
        if self.row >= 0 and self.column >= 0:
            x0 = MARGIN + self.row * SIDE + 1
            y0 = MARGIN + self.column * SIDE + 1
            x1 = MARGIN + (self.row + 1) * SIDE - 1
            y1 = MARGIN + (self.column + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="red_square")


root = Tk()
StartUI(root)
root.mainloop()
