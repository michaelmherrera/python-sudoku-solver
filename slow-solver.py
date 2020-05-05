import csv, copy


'''
Class: Grid
    Implements a (x,y) indexed grid, NOT (row,column) indexed.
    Init:
        Grid(x,y): Initializes a grid of x columns and y rows

        Grid(file_path): Initializes the grid to represent a 
        CSV at file_path. The CSV must be fully rectangular
        and have no holes
    Settting Value:
        Typical bracket notation works for getting a value,
        but you must use the set_value(x, y, val) method
        to set a value.
'''
class Grid:

    def __init__(self, *args):
        self.grid = []
        self.height = 0
        self.width = 0
        #Two args is x,y
        if len(args) == 2:
            self.init_blank(args)
        #One arg is path to .csv file storing encoding of grid
        elif len(args) == 1:
            self.init_from_csv(args)
        else:
            print("Error: Expected either filepath (1 arg) or x,y (2 args)")


    def init_from_csv(self, args):
        #Open csv and construct grid to match csv
        with open(args[0], 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter= ',')
            counter = 0
            for row in reader:
                #On first iteration,
                #create the a nested list with the correct number of
                #columns and a single row
                if counter == 0:
                    self.width = len(row)
                    for i in range(self.width):
                        self.grid.append([])
                #Iterate across a row and append to the corresponding
                #location in grid
                for i in range(self.width):
                    self.grid[i].append(int(row[i]))
                counter += 1
            self.height = counter

    def init_blank(self, args): 
        self.width = args[0]
        self.height = args[1]
        for i in range(self.width):
            vert = []
            for j in range(self.height):
                vert.append(0)
            self.grid.append(vert)


    def __str__(self):
        string = ""
        for j in range(self.height):
            for i in range(self.width):
                string += "{}{}".format(self.grid[i][j], " ")
            if j < (self.height - 1):
                string += '\n'
        return string

    def get_val(self, x, y):
        return self.grid[x][y]
    
    def set_val(self, x, y, val):
        self.grid[x][y] = val

    def get_column(self, x):
        return self.grid[x]
    
    def get_row(self, y):
        row = []
        for i in range(self.width):
            elem = self.grid[i][y]
            row.append(elem)
        return row

    def copy(self):
        return copy.deepcopy(self)
    
    def __getitem__(self, x):
        if type(x) is slice:
            rows = []
            for i in range(self.height):
                rows.append(self.get_row(i))
            return rows
        return self.get_column(x)

'''
Class: Sudoku_Board
    Implements a Suduko board as a Grid, with additional methods to verify
    that the board has valid boxes and rows. 
    
    box_dimension: By default, the boxes are 3x3
    but the client can enter in alternative box dimensions via the "box_dimension"
    keyword argument. The box_dimension is an integer and represents
    both the horizontal and vertical dimensions.

    board_dimension: By default, the board is 9x9
    but the client can enter in alternative board dimensions via the "board_dimension"
    keyword argument. The board_dimension is an integer and represents
    both the horizontal and vertical board dimensions.

'''
class Sudoku_Board(Grid):

    def __init__(self, *args, **kwargs):
        self.box_dimension = 3
        self.board_dimension = 9
        if kwargs.__contains__("box_dimension"):
            self.box_dimension = kwargs["box_dimension"]
        if kwargs.__contains__("board_dimension"):
            self.board_dimension = kwargs["board_dimension"]
        super(Sudoku_Board, self).__init__(*args)

    def __str__(self):
        string = ""
        for j in range(self.height):
            if j > 0 and j % self.box_dimension == 0:
                for i in range(self.width + ((self.width // self.box_dimension) - 1) - 1):
                    string += "--"
                string += "-\n"
            for i in range(self.width):
                if i > 0 and i % self.box_dimension == 0:
                    string += "|{}".format(" ")
                string += "{}{}".format(self.grid[i][j], " ")
            if j < (self.height - 1):
                string += '\n'
        return string

    def box_to_list(self, box):
        box_list = []
        for i in range(self.box_dimension):
            for j in range(self.box_dimension):
                val = box[i][j]
                box_list.append(val)
        return box_list

    def is_valid_list(self, members):
        seen = []
        for val in members:
            assert val >= 0 and val <= self.board_dimension, \
                    "Invalid value. Must be between 0 and {}.".format(self.board_dimension)
            if(seen.__contains__(val) and val != 0):
                #print("Invalid list. The value {} is repeated. List is: {}".format(val, members))
                return False
            seen.append(val)
        return True

    def is_valid_box(self, x, y):
        box = self.get_box(x, y)
        box_list = self.box_to_list(box)
        return self.is_valid_list(box_list)

    def is_valid_row(self, y):
        row = self.get_row(y)
        return self.is_valid_list(row)
    
    def is_valid_column(self, x):
        column = self.get_column(x)
        return self.is_valid_list(column)

    def has_valid_rows(self):
        for i in range(self.board_dimension):
            if not self.is_valid_row(i):
                return False
        return True

    def has_valid_columns(self):
        for i in range(self.board_dimension):
            if not self.is_valid_column(i):
                return False
        return True

    def has_valid_boxes(self):
        for i in range(self.box_dimension):
            for j in range(self.box_dimension):
                if not self.is_valid_box(i*self.box_dimension,j*self.box_dimension):
                    return False
        return True

    def is_valid_board(self):
        return self.has_valid_boxes() and \
            self.has_valid_rows() and self.has_valid_columns()

    def get_box(self, x, y):
        box = Grid(self.box_dimension,self.box_dimension)
        for i in range(self.box_dimension):
            for j in range(self.box_dimension):
                val = self.grid[x+i][y+j]
                box.set_val(i, j, val)
        return box
    
    def is_complete(self):
        for i in range(self.board_dimension):
            column = self.grid[i]
            for val in column:
                if val == 0:
                    return False
                assert val >= 0 and val <= self.board_dimension, \
                    "Invalid value. Must be between 0 and {}.".format(self.board_dimension)
        return True

    def is_safe(self, x, y, val):
        column = self.get_column(x)
        row = self.get_row(y)
        box = self.get_box(x // self.box_dimension, y // self.box_dimension)
        box_list = self.box_to_list(box)
        if column.__contains__(val) or row.__contains__(val) or box_list.__contains__(val):
            return False
        return True

def recursive_solve(board):
    if not board.is_valid_board():
        return False
    if board.is_complete():
        return True
    for i in range(board.board_dimension):
        for j in range(board.board_dimension):
            val = board[i][j]
            if val == 0:
                for n in range(1, board.board_dimension + 1):
                    board.set_val(i,j,n)
                    if recursive_solve(board):
                        return True
                #board.set_val(i,j,0)
    return False

def get_unsolved(board):
    unsolved = []
    for x in range(board.board_dimension):
        for y in range(board.board_dimension):
            if board[x][y] == 0:
                unsolved.append([x,y])
    return unsolved

def new_recursive_solve(board, unsolved):
    # if not board.is_valid_board():
    #     return False
    if len(unsolved) == 0:
        return True
    coordinate = unsolved.pop()
    x = coordinate[0]
    y = coordinate[1]
    for n in range(1, board.board_dimension + 1):
        board.set_val(x, y, n)
        valid_move = board.is_valid_column(x) and board.is_valid_row(y) and \
            board.is_valid_box( (x // 3) * 3, (y // 3) * 3)
        if valid_move and new_recursive_solve(board, unsolved):
            return True
    board.set_val(x, y, 0)
    unsolved.append(coordinate)
    return False

			

if __name__ == '__main__':
    board = Sudoku_Board("csv/hard.csv")
    print(board)
    unsolved = get_unsolved(board)
    print(new_recursive_solve(board, unsolved))
    # print(recursive_solve(board))
    print(board)



