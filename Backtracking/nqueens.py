# finds the all fundamental solutions to the N-Queens problem (account for rotation and reflection of board)

from copy import deepcopy

# get user input
while True:
    try:
        print("Dimensions of board: ", end="")
        N = int(input())
        if N <= 0:
            raise Exception()
        break
    except:
        print("Enter a positive integer.")

# initialise all cells in board to 0
board = [[0 for x in range(N)] for y in range(N)]


# helper function to test if cell (i, j) on board is attacked by another queen
def attacked(i, j, N):
    x = j
    # check vertical
    for y in range(N):
        if board[y][x] == 1:
            return True

    # check diagonals
    x, y = j - 1, i - 1
    while x >= 0 and y >= 0:
        if board[y][x] == 1:
            return True
        x -= 1
        y -= 1

    x, y = j + 1, i - 1
    while x < N and y >= 0:
        if board[y][x] == 1:
            return True
        x += 1
        y -= 1

    # if not attacked
    return False


solutions = [] 
# helper function to check if solution is a fundamental one
def isFundamental():
    solution = deepcopy(board)

    for i in range(4):
        # check 1 - reflection and 2 - original
        for j in range(2):
            # reflect about vertical axis
            for row in solution:
                row.reverse()

            # test against previous solutions
            for k in range(len(solutions)):
                if solution == solutions[k]:
                    return False
        
        # rotate by 90 degrees
        solution = [list(row) for row in zip(*reversed(solution))]

    return True

        
# main function to find solution // N is board dimensions; n is number of current queen to be placed (and row)
def solve(N, n):
    # base case: when all queens are placed --> check if fundamental solution
    if n == N:
        if isFundamental():
            # save a copy of solution
            solutions.append(deepcopy(board))
        return

    for j in range(N):
        if not attacked(n, j, N):
            # place a queen in position
            board[n][j] = 1

            # recursively place next queen's position
            solve(N, n + 1)
                
            # backtrack
            board[n][j] = 0    


# solve N Queens
solve(N, 0)
for solution in solutions:
    print(f"Fundamental Solution {solutions.index(solution) + 1}:")
    for row in solution:
        for n in row:
            print(n, end="  ")
        print()
    print()

# no solution case
if not solutions:
    print("No solution.")