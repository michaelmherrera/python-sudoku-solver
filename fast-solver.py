#!/usr/bin/env python3

""" 
A sudoku solver that takes a csv file representing a sudoku board as
input and leverages recursive backtracking to find a solution. This
solver supports not only 9 x 9 sudoku boards, but a board of any
dimension n x n such that n is a square number.

While recursive suduko solvers are common, this one leverages multiple
numpy arrays storing sorted boards to signficantly improve speed.
This means checking valid values is not O(n), as it would be typically,
but is rather O(1). See the README for more explanation on how this arrays
are implemented.

This project leverages the following CS concepts:
    - Recursion
    - Runtime analysis
    - Object-oriented programming
    - First-class functions and closures (for timer wrapper)

This project leverages the following Python concepts:
    - Numpy
    - Argument parsing
    - *args and **kwargs
    - Dunder methods
    
"""

import numpy as np
import time
from board import Board
import argparse


def timer(func):
    """ A wrapper function for profiling the recursive solution

    Parameters:
    -----------
    func: function The solver function

    Returns:
    --------
    time_wrapper: The solver function, wrapped in a function to time how
        long the solution takes
    """

    def timer_wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Took {end - start:0.4f} sec(s) to find a recursive solution.')
        return value
    return timer_wrapper


def recursive_solve(board):
    """A recursive backtracking algorithm for solving a sudoku board

    Parameters
    ----------
    board : Board A sudoku board

    Returns
    -------
    Returns True if a recursive solution is found, else, False.
    """

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
    """ Parse arguments from the commandline

    Returns
    -------
    Namespace A collection of key-value pairs of options. For more
        information, read the documentation of parse_args().
    """
    
    description = 'A sudoku solver that takes a csv file representing a sudoku \
        board as input and leverages recursive backtracking to find a solution.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--board', help='load the sudoku board from BOARD, a csv file')
    parser.add_argument(
        '-t', '--time', help='time how long it takes to solve', action='store_true')
    parser.add_argument(
        '--blank', help='the character used to render blanks in a board (default is a space)', default=' ', choices=['*', '0'])
    parser.add_argument(
        '-s', '--saveto', help='if specified, saves board to the provided location, else, board is not saved')
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

    solved = None
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
