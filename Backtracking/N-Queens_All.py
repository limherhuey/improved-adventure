# finds all solutions to the N-Queens problem

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


# helper function to print solution board
count = 1
def solution():
    global count
    print(f"Solution {count}:")
    count += 1

    for row in board:
        for n in row:
            print(n, end="  ")
        print()
    print()


# main function to find solution // N is board dimensions; n is number of current queen to be placed (and row)
def solve(N, n):
    # base case: when all queens are placed in correct position, board is solved, print solution
    if n == N:
        solution()
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

# no solution case
if count == 1:
    print("No solution.")