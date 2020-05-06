# Python Sudoku Solver
## This Sudoku solver is a classic recursion example, but with some added features:
* ### Simplifies the creation of the starting board by allowing the user to input a board as a 9x9 csv file. Outputs solved board as CSV
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

### Printing the board
With BLANKS_AS_ZEROES = True, blanks on the board are printed as zeroes. With false, the are printed as blanks.  

Blanks as zeroes:  
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

Blanks as blanks:
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

