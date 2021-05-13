# solves Sudoku with backtracking


# ____________________ generate random 9x9 Sudoku board ____________________
#                        by Alain T. on stackoverflow
base  = 3
side  = base*base

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s)) 
rBase = range(base) 
rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

# remove some numbers from board
squares = side*side
empties = squares * 3//5
for p in sample(range(squares),empties):
    board[p//side][p%side] = 0

# print incomplete Sudoku board
print("Incomplete version:")
numSize = len(str(side))
for line in board: print("  ".join(f"{n or '.':{numSize}}" for n in line))
print()

# __________________________________________________________________________




# helper function to check if digit n can be placed at position (row, column)
def placeable(row, col, n):
    # check vertical
    for r in range(side):
        if board[r][col] == n:
            return False
    
    # check horizontal
    for c in range(side):
        if board[row][c] == n:
            return False

    # check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(3):
        for j in range(3):
            if board[box_y * 3 + i][box_x * 3 + j] == n:
                return False
    
    return True


# helper function to loop through board to find blank
def blank():
    for row in range(side):
        for col in range(side):

            if board[row][col] == 0:
                return row, col
    
    return False 


# main function to find solution
def solve():
    b = blank()
    if not b:
        # base case, whole board solved
        return True
        
    # get the coordinates of blank cell
    row, col = b
    
    # try all digits from 1-9
    for n in range(1, 10):
        if placeable(row, col, n):
            board[row][col] = n

            # recursively solve next blank cell      
            if solve():
                return True

            # if wrong digit, backtrack 
            board[row][col] = 0

    # if no possible digit, previous cells are wrong, signal unsuccessful
    return False


# print solution once found
solve()

print("Solved:")
for line in board:
    for n in line:
        print(n, end="  ")
    print()