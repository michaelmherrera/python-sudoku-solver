import numpy as np
import time
BOARD_SIZE = 9
BOX_SIZE = 3
BLANK = '*'

def create_board(path):
    board = np.zeros((BOARD_SIZE * 2, BOARD_SIZE * 2), 'i')
    board[0:BOARD_SIZE,0:BOARD_SIZE] = np.genfromtxt(path, delimiter=',', dtype='int')
    return board

def print_board(board):
    string = ''
    for r in range(BOARD_SIZE):
        # Create horizontal dividers
        if r > 0 and r % BOX_SIZE == 0:
            for c in range(BOARD_SIZE + ((BOARD_SIZE // BOX_SIZE) - 1) - 1):
                string += '--'
            string += '-\n'
        # Create vertical dividers and place values
        for c in range(BOARD_SIZE):
            if c > 0 and c % BOX_SIZE == 0:
                string += '|{}'.format(' ')
            val = board[r][c]
            if val == 0:
                val = BLANK
            string += '{}{}'.format(val, ' ')
        if r < (BOARD_SIZE - 1):
            string += '\n'
    print(string)
    return string

def get_quadrant_indices(row, column, n):
    """

    The top left 3x3 subgrid is index 0, the top middle 3x3 subgrid is
    index 1, etc. Thus, box indexing for the sudoku board (where each entry representes a 3x3 subgrid) 
    is as follows:
    0 1 2
    3 4 5
    6 7 8
    """
    # Doesn't handle an input of ZERO!!! It can write to a location, but it can't remove from
    # a location!!!! It needs n to figure where to remove! Get a prev val

    quad1_index = (row, n + BOARD_SIZE - 1)
    quad3_index = (n + BOARD_SIZE - 1, column)
    transposed_row = (row//BOX_SIZE)*BOX_SIZE +  column//BOX_SIZE
    quad4_index = (transposed_row + BOARD_SIZE, n + BOARD_SIZE - 1)
    return (quad1_index, quad3_index, quad4_index)

def remove_curr_val(board, row, column, curr_val):
    (quad1_index, quad3_index, quad4_index) = get_quadrant_indices(row, column, curr_val)
    board[row][column] = 0
    board[quad1_index] = 0
    board[quad3_index] = 0
    board[quad4_index] = 0

def place_new_val(board, row, column, new_val):
    (quad1_index, quad3_index, quad4_index) = get_quadrant_indices(row, column, new_val)
    board[row][column] = new_val
    board[quad1_index] = new_val
    board[quad3_index] = new_val
    board[quad4_index] = new_val


def valid_choice(board, row, column, n):
    (quad1_index, quad3_index, quad4_index) = get_quadrant_indices(row, column, n)
    # If n at (row,column) is a valid choice
    if (board[quad1_index] + board[quad3_index] + board[quad4_index] == 0):
        return True
    return False
 
def populate_sorted_quadrants(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            n = board[r,c]
            if n != 0:
                place_new_val(board, r, c, n)

def get_unsolved(board):
    unsolved = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r,c] == 0:
                unsolved.append((r,c))
    unsolved.reverse()
    return unsolved

def recursive_solve(board, unsolved):
    if len(unsolved) == 0:
        return True
    coordinate = unsolved.pop()
    r = coordinate[0]
    c = coordinate[1]
    for n in range(1, BOARD_SIZE + 1):
        if valid_choice(board, r, c, n):
            place_new_val(board, r, c, n)
            if recursive_solve(board, unsolved):
                return True
            else:
                remove_curr_val(board, r, c, n)
    unsolved.append(coordinate)
    return False

def initialize(load_path):
    board = create_board(load_path)
    print('Original board:')
    print_board(board)
    return board

def solve(board):
    unsolved = get_unsolved(board)
    populate_sorted_quadrants(board)
    return recursive_solve(board, unsolved)

def print_stats(initial_time, pre_recurse_time):
    finished_time = time.time()
    total_time = finished_time - initial_time
    solution_time = finished_time - pre_recurse_time
    print("\nTime for recursive solution: {:.4f} seconds. | Total time: {:.4f} seconds.".format(solution_time, total_time))

def main():
    # load_path = input('Enter a path for the board you would like to load: ')
    load_path = 'csv/hard.csv'
    initial_time = time.time()
    board = initialize(load_path)
    pre_recurse_time = time.time()
    solved = solve(board)
    if not solved:
        print('\nInvalid board. Board not solvable. Check board.')
        print('Attempted solution:')
    else:
        print('\nSolved board:')
    print_board(board)
    print_stats(initial_time, pre_recurse_time)
    # load_path = input('Enter a path to save the solved board: ')
    # board.savetxt(load_path, a, delimiter=',')

if __name__ == '__main__':
    main()




