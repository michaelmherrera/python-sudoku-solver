class Grid:

    def __init__(self, numrows, numcolumns):
        self.numrows = numrows
        self.numcolumns = numcolumns
        self.grid = []
        for i in range(numrows*numcolumns):
            self.grid.append(0)

    def __str__(self):
        string = ""
        for row in range(self.numrows):
            for column in range(self.numcolumns):
                string += str(self.grid[row + column]) + " "
            string += '\n'
        return string

grid = Grid(10,10)
print(grid)
    

        
