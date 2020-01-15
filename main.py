import numpy as np

sudoku_0 = np.zeros((9, 9)).astype(int)
sudoku_1 = np.array([[3, 0, 6, 5, 0, 8, 4, 0, 0],
                     [5, 2, 0, 0, 0, 0, 0, 0, 0],
                     [0, 8, 7, 0, 0, 0, 0, 3, 1],
                     [0, 0, 3, 0, 1, 0, 0, 8, 0],
                     [9, 0, 0, 8, 6, 3, 0, 0, 5],
                     [0, 5, 0, 0, 9, 0, 6, 0, 0],
                     [1, 3, 0, 0, 0, 0, 2, 5, 0],
                     [0, 0, 0, 0, 0, 0, 0, 7, 4],
                     [0, 0, 5, 2, 0, 6, 3, 0, 0]])

sudoku_2 = np.array([[1, 4, 5, 3, 2, 7, 6, 9, 8],
                     [8, 3, 9, 6, 5, 4, 1, 2, 7],
                     [6, 7, 2, 9, 1, 8, 5, 4, 3],
                     [4, 9, 6, 1, 8, 5, 3, 7, 2],
                     [2, 1, 0, 4, 7, 3, 9, 5, 6],
                     [7, 5, 3, 2, 9, 6, 4, 8, 1],
                     [3, 6, 7, 5, 4, 2, 8, 1, 9],
                     [9, 8, 4, 7, 6, 1, 2, 3, 5],
                     [5, 2, 1, 8, 3, 9, 7, 6, 4]])


def find_empty_cells(sud):
    '''
    Returns the row and col of an unassigned cell
    '''
    empty_cells = np.empty((0, 2), int)
    for i in range(9):
        for j in range(9):
            if sud[i][j] == 0:
                empty_cells = np.append(
                    empty_cells, np.array([[i, j]]), axis=0)
    return empty_cells


def is_in_row(n, row, sud):
    '''
    There is n in row
    '''
    if n in sud[row, :]:
        return True

    return False


def is_in_column(n, column, sud):
    '''
    There is n in column
    '''
    if n in sud[:, column]:
        return True

    return False


def is_in_box(n, row, column, sud):
    '''
    n is in the 3x3 box
    '''

    if row <= 2:  # First 3 rows
        initial_row = 0
    elif row > 2 and row <= 5:  # Second 3 rows
        initial_row = 3
    elif row > 5:  # Last 3 rows
        initial_row = 6

    if column <= 2:  # First 3 columns
        initial_column = 0
    elif column > 2 and column <= 5:  # Second 3 columns
        initial_column = 3
    elif column > 5:  # Last 3 columns
        initial_column = 6

    # Now we iterate from initial_row/column to +2 (the end of the 3x3 box)
    for r in range(3):
        for c in range(3):
            cell = sud[initial_row + r][initial_column + c]
            if n == cell:
                return True

    return False


def check_cell_is_fine(n, row, column, sud):
    '''
    See if the row has that number
    See if the column has that number
    See if the 3x3 box has that number
    '''
    answer = not (is_in_column(n, column, sud)) and not (
        is_in_row(n, row, sud)) and not (is_in_box(n, row, column, sud))
    return answer


def solve_sudoku(sudoku, print_sudoku=False):
    '''
    Taking as input the matrix (9x9) of a sudoku. Use 0 for every
    not known number

    '''
    # Initialize parameters

    solved = False
    i = 0
    empty_cells = find_empty_cells(sudoku)

    while not(solved):

        if i == (np.shape(empty_cells)[0]):
            # There are no more empty cells, therefore, finished
            solved = True
        else:
            pos = empty_cells[i, ]
            print('%%%%%%\nNode ', i, 'Position ', pos)

            row = pos[0].astype(int)
            col = pos[1].astype(int)
            n_start = sudoku[row, col]
            print('n_start is ', n_start)

            for n in range(n_start + 1, 10):
                if check_cell_is_fine(n, row, col, sudoku):
                    sudoku[row, col] = n

                    if print_sudoku:
                        print('\nPosition ', row,
                              ' ', col, '\nNumber ', n, '\nSudoku: \n', sudoku)
                    i += 1
                    break

                else:
                    if n == 9:
                        sudoku[row, col] = 0
                        n_start = 9

            if n_start == 9:
                    # If no solution found
                if i == 0:
                    # No solution found and in the first iteration
                    print('There is no solution for this sudoku')
                    solved = True
                else:
                    print('No solution found for ', pos,
                          '. Go back one iteration')
                    sudoku[row, col] = 0
                    i -= 1  # No solution found, go back one iteration
    return sudoku


print('\n Final solution\n #########\n',
      solve_sudoku(sudoku_1, print_sudoku=True))
