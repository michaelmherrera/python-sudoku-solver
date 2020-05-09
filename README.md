# Python Sudoku Solver
## This Sudoku solver is a classic recursion example, but with some added features:
* ### Simplifies the creation of the stargting board by allowing the user to input a board as a 9x9 csv file. Outputs solved board as CSV
* ### Leverages 18x18 numpy array to not only represent the board, but also all sorted forms of the board, significantly improving performance.

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
0 1 3 | 0 4 0 | 2 0 0
7 0 0 | 2 0 0 | 6 9 0
0 0 0 | 0 0 0 | 0 0 8
---------------------
0 0 5 | 0 0 0 | 0 7 0
0 0 0 | 6 0 1 | 0 0 0
0 2 0 | 0 0 0 | 1 0 0
---------------------
5 0 0 | 0 0 0 | 0 0 0
0 3 2 | 0 0 7 | 0 0 6
0 0 8 | 0 9 0 | 5 2 0
```

### Performance enhancements
This sudoku solver uses recursive backtracking.
* It starts in the upper right box. 
* For each unsolved box, it first checks if 1 is a valid number for the location. 
    * If it is, the algorithm proceeds to the next box. If not, it iterates to 2, etc.
    * If it exhausts all options without a valid solution, it backtracks to the previous box.

Normally, to check whether a value is valid for a certain box, a sudoku solving algorithm would have to check the entries of every other box along the same column, row and 3x3 subgrid. However, this can be solved with the following optimization.
* Create an 18x18 numpy array
    * TODO: Write explanation XD
* Thus, when checking if some value n at location (x,y) is valid for a given box, it checks if 

#### Diagram of the 18x18 numpy array. 

|         $r/c$          | $0 \leq c \leq 8$ | $9 \leq c \leq 18$ |
|:----------------------:|:-----------------:|:------------------:|
| **$0 \leq r \leq 8$**  |       $II$        |        $I$         |
| **$9 \leq r \leq 18$** |       $III$       |        $IV$        |
Quadrant $II$ stores the spatial arrangement of the elements. It is the contents of quadrant $II$ that are printed for the user to see the sudoku board. The rest of the quadrants store sorted binary indicators that represent whether an element is within a given row, column or 3x3 subgrid:
1. Each row of quadrant I indicates the contents of corresponding row of quadrant II. Say that the number 1 is present in the third row within quadrant II. Then the binary indicator at the third row and first column of quadrant I is set to 1. Because the first column of quadrant I is column 9, that means that the coordinates of the binary indicator are (r, c) = (3, 9). Say the number 2 was also present in the third row of quadrant II, then the binary indicator at (3, 10) is set to 1 as well. See below TODO: create visual.

The first column of quadrant I is column 9. 

### Printing the board
You can modify how blanks are displayed by altering the constant BLANK

BLANK = '0':  
```
0 1 3 | 0 4 0 | 2 0 0 
7 0 0 | 2 0 0 | 6 9 0
0 0 0 | 0 0 0 | 0 0 8
---------------------
0 0 5 | 0 0 0 | 0 7 0
0 0 0 | 6 0 1 | 0 0 0
0 2 0 | 0 0 0 | 1 0 0
---------------------
5 0 0 | 0 0 0 | 0 0 0
0 3 2 | 0 0 7 | 0 0 6
0 0 8 | 0 9 0 | 5 2 0
```

BLANK = '*':  
```
* 1 3 | * 4 * | 2 * * 
7 * * | 2 * * | 6 9 *
* * * | * * * | * * 8
---------------------
* * 5 | * * * | * 7 *
* * * | 6 * 1 | * * *
* 2 * | * * * | 1 * *
---------------------
5 * * | * * * | * * *
* 3 2 | * * 7 | * * 6
* * 8 | * 9 * | 5 2 *
```

BLANK = ' ':
```
  1 3 |   4   | 2     
7     | 2     | 6 9   
      |       |     8 
--------------------- 
    5 |       |   7   
  2   |       | 1
---------------------
5     |       |
  3 2 |     7 |     6
    8 |   9   | 5 2
```

