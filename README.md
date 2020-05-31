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


### Implementation details
This sudoku solver uses recursive backtracking.
* It starts in the upper right box. 
* For each unsolved box, it first checks if 1 is a valid number for the location. 
    * If it is, the algorithm proceeds to the next box. If not, it iterates to 2, etc.
    * If it exhausts all options without a valid solution, it backtracks to the previous box.

Normally, to check whether a value is valid for a certain box, a sudoku solving algorithm would have to check the entries of every other box along the same column, row and 3x3 subgrid. However, this can be solved with the following optimization.
* Create an 18x18 numpy array
    * TODO: Write explanation XD
* Thus, when checking if some value n at location (x,y) is valid for a given box, it checks if 
 

