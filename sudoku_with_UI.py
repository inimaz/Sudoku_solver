# Creating a Gui for the sudoku. Inspired by http://newcoder.io/gui/part-3/
import numpy as np
from copy import deepcopy  # To create 2 independent copies of the same matrix
from tkinter import Tk, Canvas, Frame, Label, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT
import main as sudoku_solver
import time

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
        try:
            self.canvas.destroy()
            self.clock.destroy()
        except:
            pass

        GameUI(self.master)
        self.start_button.destroy()


class GameUI (StartUI):
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(fill=BOTH, side=TOP)

        # Buttons
        self.check_mode = False
        self.check_button = Button(
            master, text="Check", fg='green', command=self.check_sudoku)
        self.check_button.pack(side=RIGHT)
        self.solve_button = Button(
            master, text="Solve", fg='blue', command=self.draw_solution)
        self.solve_button.pack(side=RIGHT)
        self.hint_button = Button(
            master, text="Hint", fg='purple', command=self.give_hint)
        self.hint_button.pack(side=LEFT)

        # Get a sudoku and its solution.
        self.original_sudoku = sudoku_solver.randomized_sudoku(
            N=35)  # Original
        self.user_sudoku = deepcopy(self.original_sudoku)  # User will change
        self.sudoku_solution = sudoku_solver.solve_sudoku(
            deepcopy(self.user_sudoku))  # Solution of the sudoku

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Key>", self.canvas_key)

        # Start some variables
        self.row, self.column = 0, 0
        self.start_time = time.time()

        # Set up the clock
        self.clock = Label(master)
        self.clock.pack(side=BOTTOM)
        self.__draw_clock()

        self.__draw_sudoku()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"

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

    def __draw_numbers(self):
        """
        Fills the grid with sudoku numbers
        """
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                number = self.user_sudoku[i][j]
                if number != 0:
                    if number == self.original_sudoku[i][j]:
                        color = "black"
                    # Highlight numbers that are wrong
                    elif self.check_mode and \
                            number != self.sudoku_solution[i][j]:
                        color = "red"
                    else:
                        color = "blue"

                    x = MARGIN + SIDE / 2 + i * SIDE
                    y = MARGIN + SIDE / 2 + j * SIDE
                    self.canvas.create_text(
                        x, y, text=number, tags="numbers", fill=color)

    def canvas_click(self, event):
        '''
        Selects which cell has been clicked
        '''
        x, y = event.x, event.y
        if WIDTH - MARGIN > x > MARGIN and HEIGHT - MARGIN > y > MARGIN:
            self.canvas.focus_set()

            row = (x - MARGIN) // SIDE
            column = (y - MARGIN) // SIDE

            if (row, column) == (self.row, self.column):
                (self.row, self.column) = (-1, -1)
            elif self.original_sudoku[row][column] == 0:
                self.row, self.column = row, column

        self.__draw_red_box()

    def __draw_red_box(self):
        '''
        Draw red box around the cell selected
        '''
        self.canvas.delete("red_square")
        if self.row >= 0 and self.column >= 0:
            x0 = MARGIN + self.row * SIDE + 1
            y0 = MARGIN + self.column * SIDE + 1
            x1 = MARGIN + (self.row + 1) * SIDE - 1
            y1 = MARGIN + (self.column + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="red_square")

    def canvas_key(self, event):
        '''
        Selects which key has been pressed
        '''
        number = event.char
        if number in "1234567890" and self.row >= 0 and self.column >= 0:
            self.user_sudoku[self.row][self.column] = int(number)
            self.__draw_sudoku()

    def __draw_sudoku(self):
        self.__draw_grid()
        self.__draw_numbers()
        self.__draw_red_box()
        if self.is_sudoku_solved():
            self.__draw_victory()

    def draw_solution(self):
        '''
        Solve the sudoku and draw it
        '''
        self.user_sudoku = self.sudoku_solution
        self.__draw_sudoku()

    def give_hint(self):
        '''
        Gives the solution for a random cell
        '''
        while True:
            i = np.random.randint(0, 9)
            j = np.random.randint(0, 9)
            if self.user_sudoku[i][j] == 0:
                self.user_sudoku[i][j] = self.sudoku_solution[i][j]
                print('Hint for cell: ', i, ',', j)
                self.__draw_sudoku()
                return

    def check_sudoku(self):
        self.check_mode = True
        self.__draw_numbers()
        self.check_mode = False

    def is_sudoku_solved(self):
        for i in range(9):
            for j in range(9):
                number = self.user_sudoku[i][j]
                if number != self.sudoku_solution[i][j]:
                    return False
        return True

    def __draw_clock(self):

        game_time = time.time() - self.start_time
        min = game_time // 60
        sec = game_time % 60
        t = "%02d:%02d" % (min, sec)
        self.clock.config(text=t)
        # Call this function to update the clock every 200 ms
        if not(self.is_sudoku_solved()):
            self.clock.after(200, self.__draw_clock)

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark blue", outline="blue"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="Congrats!", tags="winner",
            fill="white", font=("Arial", 32)
        )
        self.check_button.destroy()
        self.hint_button.destroy()
        self.solve_button.destroy()

        self.start_button = Button(
            self.master, text="Restart", fg='purple', command=self.start_game)
        self.start_button.pack(side=BOTTOM)


if __name__ == "__main__":
    root = Tk()
    StartUI(root)
    root.mainloop()
