import numpy as np
import time
from board import Board


def recursive_solve(board):
    if len(board.unsolved) == 0:
        return True
    coordinate = board.unsolved.pop()
    r = coordinate[0]
    c = coordinate[1]
    for n in range(1, board.size + 1):
        if board.is_valid_assignment(r, c, n):
            board[r, c] = n
            if recursive_solve(board):
                return True
            else:
                board[r, c] = 0
    board.unsolved.append(coordinate)
    return False


def main():
    # load_path = input('Enter a path for the board you would like to load: ')
    load_path = 'csv/hard.csv'
    board = Board(load_path)
    print('Original board:')
    print(board)

    solved = recursive_solve(board)
    if not solved:
        print('\nInvalid board. Board not solvable. Check board.')
        print('Attempted solution:')
    else:
        print('\nSolved board:')
    print(board)
    # load_path = input('Enter a path to save the solved board: ')
    # board.savetxt(load_path, a, delimiter=',')


if __name__ == '__main__':
    main()

