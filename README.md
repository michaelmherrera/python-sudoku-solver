# Optimized Python Sudoku Solver

> A classic recursive backtracking sudoku solver, but with efficiency optimizations and a user-friendly interface.

## Usage

```
fast-solver.py [-h] [--board BOARD] [-t] [--blank {*,0}] [-s SAVETO]

optional arguments:
  -h, --help            show this help message and exit
  --board BOARD         load the sudoku board from BOARD, a csv file
  -t, --time            time how long it takes to solve
  --blank {*,0}         the character used to render blanks in a board (default is a space)
  -s SAVETO, --saveto SAVETO
                        if specified, saves board to the provided location, else, board is not saved 
```

### CSV input / output

Boards are input and output as CSV files. For example, the following CSV:

```
0,7,0,0,0,0,5,0,0  
1,0,0,0,0,2,0,3,0  
3,0,0,5,0,0,0,2,8  
0,2,0,0,6,0,0,0,0  
4,0,0,0,0,0,0,0,9  
0,0,0,0,1,0,0,7,0  
2,6,0,0,0,1,0,0,5  
0,9,0,7,0,0,0,0,2  
0,0,8,0,0,0,0,6,0  
```

Corresponds to the following board (blanks are represented by zeroes):

```
  1 3 |   4   | 2    
7     | 2     | 6 9  
      |       |     8
---------------------
    5 |       |   7  
      | 6   1 |      
  2   |       | 1    
---------------------
5     |       |      
  3 2 |     7 |     6
    8 |   9   | 5 2  
```

### Examples
(All csvs used in the example are stored in the `example-csv` directory)

Basic usage
```
$ python3 .\fast-solver.py --board .\example-csv\hard.csv
Original board:
  7   |       | 5     
1     |     2 |   3   
3     | 5     |   2 8 
--------------------- 
  2   |   6   |       
4     |       |     9 
      |   1   |   7   
--------------------- 
2 6   |     1 |     5 
  9   | 7     |     2
    8 |       |   6


Solved board:
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

```

Without --board specified
```
$ python3 .\fast-solver.py
Enter the csv file storing the sudoku board: example-csv/4x4-with-holes.csv
Original board:
  4 |     
3   |
---------
2   |   3
4   |   1


Solved board:
1 4 | 3 2
3 2 | 1 4
---------
2 1 | 4 3
4 3 | 2 1
```

With all options specified
```
python3 .\fast-solver.py --board .\example-csv\hard.csv -t --blank * -s solution.csv
Original board:
* 7 * | * * * | 5 * * 
1 * * | * * 2 | * 3 *
3 * * | 5 * * | * 2 8
---------------------
* 2 * | * 6 * | * * *
4 * * | * * * | * * 9
* * * | * 1 * | * 7 *
---------------------
2 6 * | * * 1 | * * 5
* 9 * | 7 * * | * * 2
* * 8 | * * * | * 6 *

Timing...
Took 2.8374 sec(s) to find a recursive solution.

Solved board:
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

Board successfully saved to solution.csv

```


## Efficiency optimizations

Normally, to check whether a value is valid for a certain box, a sudoku
solving algorithm would have to check the entries of every other box
along the same column, row and subgrid, meaning checking if a move is
valid is O(n) where n is the dimension of the board. However, this implementation
reduces it to O(1). The Board class leverages 4 2-d numpy matrices:

  1. A spatially-arranged matrix (the sudoku board that the user sees)
  2. A matrix where each row contains the values of the original row, but arranged in ascending order
  3. A matrix where each column contains the values of the original column, but arranged in ascending order
  4. A matrix where each row contains the values of the original subgrid, but arranged in ascending order

Take the following 4x4 sudoku board for example:

```
  4 |     
3   |
---------
2   |   3
4   |   1
```

Matrix 1 (original) would be arranged as:
```
  4 |     
3   |
---------
2   |   3
4   |   1
```

Matrix 2 (rows) would be arranged as:

```
    |   4 
    | 3
---------
 2  | 3 
1   |   4
```

Matrix 3 (columns) would be arranged as:


```
    |   1 
2   |
---------
3   |   3
4 4 |    
```


Matrix 4 (subgrids) would be arranged as (The upper-left subgrid corresponds to row 0, the upper-right to row 1, the lower-left to row 2 and the lower right to row 3):
```
    | 3  4  
    |
---------
  2 |   4
1   | 3  
```
 
I am always looking to improve my technical communication so I encourage any feedback on what could be improved about this explanation.

