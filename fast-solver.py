#!/usr/bin/env python3

import numpy as np
import time
from board import Board
import functools
import argparse

# TODO: 
# Implement profiling (timing decorator)
# Update README

def timer(func):
    def timer_wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Took {end - start:0.4f} sec(s) to find a recursive solution.')
        return value
    return timer_wrapper

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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board', help='the csv file storing the sudoku board')
    parser.add_argument('-t', '--time', help='time how long it takes to solve', action='store_true')
    parser.add_argument('--blank', help='the character used to display blanks in a board (default is a blank)', default=' ', choices=['*', '0'])
    parser.add_argument('-s', '--saveto', help='if specified, saves board to the provided location. Else, board is not saved')
    return parser.parse_args()



def main():
    board = ''
    args = get_args()

    if args.board:
        board = args.board
    else:
        board = input('Enter the csv file storing the sudoku board: ')
    board = Board(board, args.blank)

    print('Original board:')
    print(board)

    solved=None
    if args.time:
        print('Timing...')
        solved = timer(recursive_solve)(board)
    else:
        solved = recursive_solve(board)

    if not solved:
        print('Invalid board. Board not solvable. Check board.')
        print('Attempted solution:')
    else:
        print('\nSolved board:')
    print(board)

    if args.saveto:
        board.savetxt(args.saveto, delimiter=',')
        print(f'Board successfully saved to {args.saveto}')


if __name__ == '__main__':
    main()

