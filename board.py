import math
import numpy as np


class Board:
    def __init__(self, path, size=9, blank=' '):
        """
        Generate a board from a csv.

        Parameters
        ----------
        path: the path to the csv file. Must have the same dimensions as size. Must be comprised of integers

        size: dimension of the board. For example, size = 9 leads to a 9x9 board -- the typical size.
            Must be a square number.

        blank: how blanks are rendered when the board is printed. 

        Returns
        -------
        A Board instance
        """
        self.size = size
        self.blank = blank
        self.subgrid_size = int(math.sqrt(size))
        self.sudoku_board = np.genfromtxt(path, delimiter=',', dtype='int')
        self.unsolved = self.get_unsolved()

        self.row_indicators = np.zeros((self.size, self.size))
        self.column_indicators = np.zeros((self.size, self.size))
        self.subgrid_indicators = np.zeros((self.size, self.size))
        self.populate_indicator_arrays()
        self.indicators = None

        # For the purposes of legacy code as I fully implement the class
        # TODO: Remove after implementation
        self.og_array = np.zeros((size * 2, size * 2), 'i')
        self.og_array[0:size, 0:size] = np.genfromtxt(
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
        for r in range(self.size):
            # Create horizontal dividers
            if r > 0 and r % self.subgrid_size == 0:
                for c in range(self.size + ((self.size // self.subgrid_size) - 1) - 1):
                    string += '--'
                string += '-\n'
            # Create vertical dividers and place values
            for c in range(self.size):
                if c > 0 and c % self.subgrid_size == 0:
                    string += '|{}'.format(' ')
                val = self.sudoku_board[r][c]
                if val == 0:
                    val = self.blank
                string += '{}{}'.format(val, ' ')
            if r < (self.size - 1):
                string += '\n'
        return string

    def populate_indicator_arrays(self):
        """ Populate the indicator arrays based on the initial state of the board.


        """
        for r in range(self.size):
            for c in range(self.size):
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

    def __setitem__(self, row_column, new_val):
        """ Place new_val in the specified row and column on the sudoku board and update corresponding indicators.

        If new_val = 0, sets the indicators corresponding to the current val at location (row, column) to False.

        Parameters
        ----------
        row_column:
            A tuple where row_column = (row, column) and (row, column) is the coordinates
            of the location being updated.
        new_val:
            The new value to be placed.

        """
        assert 0 <= new_val and new_val <= self.size, \
            "Value {0} is out of bounds for a sudoku board of size {2}. Please select a value between {1} and {2}".format(
                new_val, 0, self.size)

        row, column = row_column
        self.update_indicators(row, column, new_val)
        self.sudoku_board[row, column] = new_val

    def update_indicators(self, row, column, new_val):
        if new_val == 0:  # If zeroing out a location, update corresponding indicators to False
            curr_val = self.sudoku_board[row, column]
            self.row_indicators[row, curr_val - 1] = False
            self.column_indicators[curr_val - 1, column] = False
            subgrid_row = (row//self.subgrid_size) * \
                self.subgrid_size + (column//self.subgrid_size)
            self.subgrid_indicators[subgrid_row, curr_val - 1] = False
        else:
            self.row_indicators[row, new_val - 1] = True
            self.column_indicators[new_val - 1, column] = True
            subgrid_row = (row//self.subgrid_size) * \
                self.subgrid_size + (column//self.subgrid_size)
            self.subgrid_indicators[subgrid_row, new_val - 1] = True


    def is_valid_assignment(self, row, column, val):
        subgrid_row = (row//self.subgrid_size) * \
            self.subgrid_size + (column//self.subgrid_size)
        valid_row = not self.row_indicators[row, val-1]
        valid_col = not self.column_indicators[val-1, column]
        valid_subgrid = not self.subgrid_indicators[subgrid_row, val - 1]
        return valid_row and valid_col and valid_subgrid

    def get_unsolved(self):
        """Get a list of the unsolved locations on the board.

        Returns:
            A list of tuples where each tuple is the zero-indexed (row, column)
            coordinates of an unsolved location.

        """
        unsolved = []
        for r in range(self.size):
            for c in range(self.size):
                if self.sudoku_board[r, c] == 0:
                    unsolved.append((r, c))
        unsolved.reverse()
        return unsolved
