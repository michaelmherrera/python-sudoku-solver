import math
import numpy as np


class Board:
    """ A sudoku board that can track what locations are unsolved, what moves are valid, and produce a string representation of itself

    """

    def __init__(self, path, blank=' '):
        """Generate a board from a csv.

        Parameters
        ----------
        path: 
            the path to the csv file. Must have the same dimensions as size. Must be comprised of integers

        blank: str, optional
            how blanks are rendered when the board is printed. 

        Returns
        -------
        A Board instance
        """

        self.blank = blank

        self.sudoku_board = np.genfromtxt(path, delimiter=',', dtype='int')
        shape = self.sudoku_board.shape
        if len(shape) == 2 and shape[0] == shape[1] and math.sqrt(shape[0]) % 1 == 0:
            self.size = shape[0]
            self.subgrid_size = int(math.sqrt(self.size))
        else:
            raise Exception(
                'Board must be 2-dimensional, square and the dimensions of the board must be square numbers.')
        self.unsolved = self.get_unsolved()
        self.row_indicators = np.zeros((self.size, self.size))
        self.column_indicators = np.zeros((self.size, self.size))
        self.subgrid_indicators = np.zeros((self.size, self.size))
        self.populate_indicator_arrays()
        self.indicators = None

    def savetxt(self, fname, delimiter=','):
        """Save the sudoku board to the file fname (by default, in the format of a csv)

        Parameters
        ----------
        fname: 
            The name of the file in which to save the board
        delimeter: str
            The delimeter for each value in the board. Be default, a comma
        """

        np.savetxt(fname, self.sudoku_board, fmt='%i', delimiter=delimiter)

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
        row_column: tup
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
        """ Update the row, column and subgrid indicators to reflect the changed value

        Parameters
        ----------
        row: int
            The row or the location to be updated
        column: int
            The column of the location to be update
        new_val: int
            The new value to be placed at the location
        """

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
        """ Checks if assigning val to (row, column) is valid

        Parameters
        ----------
        row: int
            The row of the location being checked
        column: int
            The column of the location being check
        val: int
            The value being checked
        """

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
