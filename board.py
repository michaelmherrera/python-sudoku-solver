import math
import numpy as np

class Board:
    def fake_init(self, board_size=9, *args, **kwargs):
        """
        Generate a board from a text file. Besides board_size, accepts the same arguments at numpy.genfromtext.

        Parameters
        ----------
        board_size: dimension of the board. For example, board_size = 9 leads to a 9x9 board -- the typical size.
            Must be a square number.

        Returns
        -------
        A Board instance
        """
        self.board_size = board_size
        self.box_size = int(math.sqrt(board_size))
        # self.sudoku_board = np.genfromtxt(*args, **kwargs)
        board = np.zeros((board_size * 2, board_size* 2), 'i')
        board[0:board_size,0:board_size] = np.genfromtxt(*args, **kwargs)
        return board
        




    #Init method that accepts from csv, and also string maybe?

    #__str__ method for printing

    #another string method, but for printing entire board
        #use decorators somehow?
    
    #variables to store current location

    #flexible size based on init

    #methods for setting and zeroing out the sorted indices
        #maybe it's just easier to make it four numpy arrays
        #honestly, yeah. I think it may be. Math is less confusing
    
    #need to implement indexing!

    #populate sorted quadrants for initial setup (or keep as main method)

    #get unsolved -- in init

    #unsolved pop