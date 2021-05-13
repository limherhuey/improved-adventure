# finds the first solution of the N-Queens problem

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
board = [[0 for j in range(N)] for i in range(N)]


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


# main function to find solution
def solve(N, n):
    # base case: when all queens are placed in correct position, board is solved
    if n == N:
        return True

    for j in range(N):
        if not attacked(n, j, N):
            # place a queen in position
            board[n][j] = 1

            # recursively place next queen's position, True if successful
            if solve(N, n + 1):
                return True
                
            # if no solution available for next queen, remove current queen's position to backtrack
            board[n][j] = 0

    # signal unsuccessful if no solution for current queen after looping through whole board
    return False

    
# output result
if solve(N, 0):
    print("Solved:")
    for row in board:
        for n in row:
            print(n, end="  ")
        print()
    print()

else:
    print("No solution.")