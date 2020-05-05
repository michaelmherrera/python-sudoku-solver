import numpy, csv

BOARD_SIZE = 9
BOX_SIZE = 3

def create_board(path):
    array = numpy.zeros((9,9), 'i')
    #Open csv and construct grid to match csv
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter= ',')
        rowindex = 0
        for row in reader:
            array[rowindex] = row
            rowindex += 1
    return array

def no_duplicates(unsorted_list):
    sorted_list = sorted(unsorted_list)
    last = sorted_list.pop()
    list_size = BOARD_SIZE - 1
    while last != 0 and list_size > 0:
        penultimate = sorted_list.pop()
        if last == penultimate:
            return False
        last = penultimate
        list_size -= 1
    return True

def valid_column(board, column):
    column_list = board[:, column]
    return no_duplicates(column_list)
    

def valid_row(board, row):
    row_list = board[row, :]
    return no_duplicates(row_list)

def valid_box(board, row, column):
    box_row = (row // BOX_SIZE) * BOX_SIZE
    box_column = (column // BOX_SIZE) * BOX_SIZE
    box_list = []
    for r in range(BOX_SIZE):
        for c in range(BOX_SIZE):
            box_list.append(board[box_row + r, box_column + c])
    return no_duplicates(box_list)

def valid_move(board, row, column):
    return valid_box(board, row, column) and valid_row(board, row) and \
            valid_column(board, column)

def get_unsolved(board):
    unsolved = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r,c] == 0:
                unsolved.append([r,c])
    return unsolved

def recursive_solve(board, unsolved):
    if len(unsolved) == 0:
        return True
    coordinate = unsolved.pop()
    r = coordinate[0]
    c = coordinate[1]
    for n in range(1, BOARD_SIZE + 1):
        board[r,c] = n
        if valid_move(board, r, c) and recursive_solve(board, unsolved):
            return True
    board[r,c] = 0
    unsolved.append(coordinate)
    return False

board = create_board('csv/hard.csv')
print(board)
unsolved = get_unsolved(board)
print(recursive_solve(board, unsolved))
print(board)

