import math
import numpy as np


class Board:
    def __init__(self, path, board_size=9, blank=' '):
        """
        Generate a board from a csv.

        Parameters
        ----------
        path: the path to the csv file. Must have the same dimensions as board_size. Must be comprised of integers

        board_size: dimension of the board. For example, board_size = 9 leads to a 9x9 board -- the typical size.
            Must be a square number.

        blank: how blanks are rendered when the board is printed. 

        Returns
        -------
        A Board instance
        """
        self.board_size = board_size
        self.blank = blank
        self.subgrid_size = int(math.sqrt(board_size))
        self.sudoku_board = np.genfromtxt(path, delimiter=',', dtype='int')
        self.unsolved = self.get_unsolved()

        self.row_indicators = np.zeros((self.board_size, self.board_size))
        self.column_indicators = np.zeros((self.board_size, self.board_size))
        self.subgrid_indicators = np.zeros((self.board_size, self.board_size))
        self.populate_indicator_arrays()
        print(self.row_indicators)
        print(self.column_indicators)
        print(self.subgrid_indicators)

        # For the purposes of legacy code as I fully implement the class
        # TODO: Remove after implementation
        self.og_array = np.zeros((board_size * 2, board_size * 2), 'i')
        self.og_array[0:board_size, 0:board_size] = np.genfromtxt(
            path, delimiter=',', dtype='int')

    def __str__(self):
        """Return the sudoku board as a string, with boxes deliniated.

        An example of what a full board looks like when printed:
        8 7 2 | 1 4 3 | 5 9 6
        1 5 9 | 6 8 2 | 4 3 7
        3 4 6 | 5 7 9 | 1 2 8
        ---------------------
        9 2 7 | 4 6 5 | 3 8 1
        4 8 1 | 3 2 7 | 6 5 9
        6 3 5 | 9 1 8 | 2 7 4
        ---------------------
        2 6 3 | 8 9 1 | 7 4 5
        5 9 4 | 7 3 6 | 8 1 2
        7 1 8 | 2 5 4 | 9 6 3

        """
        string = ''
        for r in range(self.board_size):
            # Create horizontal dividers
            if r > 0 and r % self.subgrid_size == 0:
                for c in range(self.board_size + ((self.board_size // self.subgrid_size) - 1) - 1):
                    string += '--'
                string += '-\n'
            # Create vertical dividers and place values
            for c in range(self.board_size):
                if c > 0 and c % self.subgrid_size == 0:
                    string += '|{}'.format(' ')
                val = self.sudoku_board[r][c]
                if val == 0:
                    val = self.blank
                string += '{}{}'.format(val, ' ')
            if r < (self.board_size - 1):
                string += '\n'
        return string

    def populate_indicator_arrays(self):
        """ Populate the indicator arrays based on the initial state of the board.


        """
        for r in range(self.board_size):
            for c in range(self.board_size):
                n = self.sudoku_board[r, c]
                if n != 0:
                    self.__setitem__((r, c), n)

    def __getitem__(self, row_colum):
        """ Retrieve the item from the specified row and column on the sudoku board.

        Parameters
        ----------
        row_column:
            A tuple where row_column = (row, column) and (row, column) is the coordinates
            of the location being updated.

        Returns
        -------
        The value at (row, column)

        """
        row, column = row_colum
        return self.sudoku_board[row, column]

    def __setitem__(self, row_column, val):
        """ Place val in the specified row and column on the sudoku board and update corresponding indicators.

        Parameters
        ----------
        row_column:
            A tuple where row_column = (row, column) and (row, column) is the coordinates
            of the location being updated.
        val:
            The new value to be placed.

        """
        assert 1 <= val and val <= self.board_size, \
            "Value {0} is out of bounds for a sudoku board of size {2}. Please select a value between {1} and {2}".format(
                val, 1, self.board_size)

        row, column = row_column
        self.sudoku_board[row, column] = val
        self.row_indicators[row, val - 1] = True
        self.column_indicators[val - 1, column] = True
        subgrid_row = (row//self.subgrid_size) * \
            self.subgrid_size + (column//self.subgrid_size)
        self.subgrid_indicators[subgrid_row, val - 1] = True

    def get_unsolved(self):
        """Get a list of the unsolved locations on the board.

        Returns:
            A list of tuples where each tuple is the zero-indexed (row, column)
            coordinates of an unsolved location.

        """
        unsolved = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.sudoku_board[r, c] == 0:
                    unsolved.append((r, c))
        unsolved.reverse()
        return unsolved

    # another string method, but for printing entire board
        # use decorators somehow?

    # variables to store current location

    # unsolved pop
