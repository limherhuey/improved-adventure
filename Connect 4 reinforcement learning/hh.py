import numpy as np
import pygame
import sys
import math
import random
from timeit import default_timer as timer
from datetime import timedelta

class Connect4():
    
    def __init__(self, config={}):
        self.config = {
            # board dimensions
            "ROWS": 3, # 6
            "COLUMNS": 3, # 7
        }
        self.game_restart()
        self.results = {
            "p1": 0,
            "p2": 0,
            "draw": 0
        }

    def game_restart(self):
        self.board = self.create_board()
        self.game_over = False
        self.turn = 0

    def available_actions(self):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        COLUMNS = self.config["COLUMNS"]
        for col in range(COLUMNS):
            row = self.lowest_empty_row(col)
            if row is not None:
                actions.add((row, col))
        return actions

    def get_current_player(self):
        PLAYER1 = 1
        PLAYER2 = 2
        if self.turn == 0:
            return PLAYER1
        else:
            return PLAYER2

    # functions
    def create_board(self):
        """ creates a new empty board """
        board = np.zeros((self.config["ROWS"], self.config["COLUMNS"]))
        return board

    def drop_disc(self, row, col):
        """ places a disc in the specified location """
        # disc is the player wtf
        disc = self.get_current_player()
        self.board[row][col] = disc

    def is_valid_location(self, col):
        """ checks if column still has an empty space """
        return self.board[self.config["ROWS"]-1][col] == 0

    def lowest_empty_row(self, col):
        """ returns the lowest unfilled row in specified column """
        for r in range(self.config["ROWS"]):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        """ prints board """
        print(np.flip(self.board, 0))

    def winning_move(self):
        """ checks if game is won """
        disc = self.get_current_player()
        COLUMNS = self.config["COLUMNS"]
        ROWS = self.config["ROWS"]
        results = False
        
        number_of_matches_to_win = 3
        # Check horizontally for win
        for c in range(COLUMNS-number_of_matches_to_win+1):
            for r in range(ROWS):
                temp_counter = 0
                for n in range(number_of_matches_to_win):
                    if self.board[r][c + n] == disc:
                        temp_counter += 1
                if temp_counter == number_of_matches_to_win:
                    results = True

        # Check vertically for win
        for c in range(COLUMNS):
            for r in range(ROWS-number_of_matches_to_win+1):
                temp_counter = 0
                for n in range(number_of_matches_to_win):
                    if self.board[r + n][c] == disc:
                        temp_counter += 1
                if temp_counter == number_of_matches_to_win:
                    results = True

        # Check positively sloped diaganols
        for c in range(COLUMNS-number_of_matches_to_win+1):
            for r in range(ROWS-number_of_matches_to_win+1):
                temp_counter = 0
                for n in range(number_of_matches_to_win):
                    if self.board[r + n][c + n] == disc:
                        temp_counter += 1
                if temp_counter == number_of_matches_to_win:
                    results = True

        # Check negatively sloped diaganols
        for c in range(COLUMNS-number_of_matches_to_win+1):
            for r in range(ROWS-number_of_matches_to_win+1, ROWS):
                temp_counter = 0
                for n in range(number_of_matches_to_win):
                    if self.board[r - n][c + n] == disc:
                        temp_counter += 1
                if temp_counter == number_of_matches_to_win:
                    results = True
        return results


    def is_tie(self):
        is_tie = True
        COLUMNS = self.config["COLUMNS"]
        for col in range(COLUMNS):
            if self.is_valid_location(col):
                is_tie = False
        return is_tie


class Connect4AI():
    
    def __init__(self, alpha=0.5, epsilon=0.1, game=None):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.game = game

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        array_of_tuples = map(tuple, state)
        tuple_of_tuples = tuple(array_of_tuples)
        state = tuple_of_tuples
        
        if (state, action) in self.q:
            return self.q[state, action]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        array_of_tuples = map(tuple, state)
        tuple_of_tuples = tuple(array_of_tuples)
        state = tuple_of_tuples

        self.q[state, action] = old_q + self.alpha * ((reward + future_rewards) - old_q)

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        # a set of all possible actions in state
        actions = self.game.available_actions()

        # initialise maximum Q-value to 0
        max = 0
        
        array_of_tuples = map(tuple, state)
        tuple_of_tuples = tuple(array_of_tuples)
        state = tuple_of_tuples

        # compare all Q-values of possible (state, action) pairs if they exist in self.q
        for action in actions:
            #import pdb; pdb.set_trace()
            if (state, action) in self.q:
                Q_value = self.q[state, action]

                if Q_value > max:
                    max = Q_value

        return max

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.
        - state is game.piles, which is [1, 3, 5, 7]

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        actions = self.game.available_actions()

        if epsilon:
            # with probability self.epsilon, chooose a random avaliable action
            explore = random.choices([True, False], weights = [self.epsilon, 1 - self.epsilon], k = 1)
            
            if explore[0]:
                return random.choice(tuple(actions))

        # choose best available action
        best_value = self.best_future_reward(state)

        array_of_tuples = map(tuple, state)
        tuple_of_tuples = tuple(array_of_tuples)
        state = tuple_of_tuples

        for action in actions:
            if (state, action) in self.q:
                if best_value == self.q[state, action]:
                    return action

        # if no actions in self.q yet, randomly choose
        return random.choice(tuple(actions))

    def move(self, action):
            """
            Make the move `action` for the current player.
            `action` must be a tuple `(i, j)`.
            """
            row, col = action

            if self.game.is_valid_location(col):
                row = self.game.lowest_empty_row(col)
                self.game.drop_disc(row, col)

                if self.game.winning_move():
                    #label = myfont.render("Player {} wins!!".format(self.game.get_current_player()), 1, RED)
                    #screen.blit(label, (40,10))
                    #####self.game.print_board()
                    player_num = self.game.get_current_player()
                    print("Player {} wins!!".format(player_num))
                    self.game.game_over = True
                    self.game.results["p{}".format(player_num)] += 1
                elif self.game.is_tie():
                    print("Tie Game".format(self.game.get_current_player()))
                    self.game.game_over = True
                    self.game.results["draw"] += 1

            self.game.turn = (self.game.turn + 1) % 2

            self.game.print_board()


def play(ai=False, human_player=False, display=False, training_cycles=1):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    

    # If no player order set, choose human's order randomly
    if human_player is True:
        human_player = random.randint(0, 1)

    # Create new game
    game = Connect4()
    COLUMNS = game.config["COLUMNS"]
    ROWS = game.config["ROWS"]

    def train(n, game):
        """
        Train an AI by playing `n` games against itself.
        """

        print("Hi im trg")

        player = Connect4AI(game=game)

        # Play n games
        for i in range(n):
            print(f"Playing training game {i + 1}")
            game.game_restart()

            # Keep track of last move made by either player
            last = {
                1: {"state": None, "action": None},
                2: {"state": None, "action": None}
            }

            # Game loop
            while True:

                # Keep track of current state and action
                # Creates a copy of the piles, which is [1, 3, 5, 7]
                state = game.board
                
                action = player.choose_action(state)

                # Keep track of last state and action
                last[game.get_current_player()]["state"] = state
                last[game.get_current_player()]["action"] = action

                # Make move
                player.move(action)
                new_state = game.board

                # When game is over, update Q values with rewards
                if game.game_over is True:
                    player.update(state, action, new_state, -1)
                    player.update(
                        last[game.get_current_player()]["state"],
                        last[game.get_current_player()]["action"],
                        new_state,
                        1
                    )
                    break

                # If game is continuing, no rewards yet
                elif last[game.get_current_player()]["state"] is not None:
                    player.update(
                        last[game.get_current_player()]["state"],
                        last[game.get_current_player()]["action"],
                        new_state,
                        0
                    )

        print("Done training")

        # Return the trained AI
        return player

    if ai is True:
        print("Hi im ai")
        start = timer()
        ai = train(training_cycles, game)
        end = timer()
        print("AI has completed trg <3")
        print(timedelta(seconds=end-start))
        ### import pdb; pdb.set_trace()
        #print(ai.q)
    game.game_restart()

    # This is the human vs AI part
    while game.game_over is not True:
        # Print contents of piles
        ##### game.print_board()

        # Compute available actions
        available_actions = game.available_actions()
        #time.sleep(1)

        # Let human make a move
        if game.get_current_player() == human_player:
            print("Your Turn")
            while True:
                col = int(input("Choose Col: "))
                row = game.lowest_empty_row(col)
                if (row, col) in available_actions:
                    ai.move((row, col))
                    #### game.print_board()
                    break
                #import pdb; pdb.set_trace()
                print("Invalid move, try again.")

        # Have AI make a move
        #else:
        print("AI's Turn")
        row, col = ai.choose_action(game.board, epsilon=False)
        print(f"AI chose ({row}, {col})")

        # Make move
        ai.move((row, col))

        # Check for winner
        #if game.winner is not None:
        #    print()
        #    print("GAME OVER")
        #    winner = "Human" if game.winner == human_player else "AI"
        #    print(f"Winner is {winner}")
        #    return
            

    if display is True:

        BLUE = (0,0,255)
        BLACK = (0,0,0)
        RED = (255,0,0)
        YELLOW = (255,255,0)

        pygame.init()

        
        #### THIS IS THE CANCEROUS PART ####
        def draw_board(board):
            for c in range(COLUMNS):
                for r in range(ROWS):
                    pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
            for c in range(COLUMNS):
                for r in range(ROWS):		
                    if board[r][c] == 1:
                        pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                    elif board[r][c] == 2: 
                        pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            pygame.display.update()


        SQUARESIZE = 80
        width = COLUMNS * SQUARESIZE
        height = (ROWS+1) * SQUARESIZE
        size = (width, height)
        RADIUS = int(SQUARESIZE/2 - 5)
        screen = pygame.display.set_mode(size)
        draw_board(game.board)
        pygame.display.update()

        myfont = pygame.font.SysFont("monospace", 75)

        while not game.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # create a circle that follows ur mouse
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if game.turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    #print(event.pos)
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if game.is_valid_location(col):
                        row = game.lowest_empty_row(col)
                        game.drop_disc(row, col)

                        if game.winning_move():
                            label = myfont.render("Player {} wins!!".format(game.get_current_player()), 1, RED)
                            screen.blit(label, (40,10))
                            game.game_over = True

                    game.turn = (game.turn + 1) % 2

                    #####game.print_board()
                    draw_board(game.board)

                    

                    if game.game_over:
                        pygame.time.wait(3000)



