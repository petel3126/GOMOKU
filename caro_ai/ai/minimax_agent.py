from .base_agent import BaseAgent
import math 

class MinimaxAgent(BaseAgent):
    def __init__(self, player, depth=3):
        super()._init_(player)
        self.depth = depth

    def choose_move(self, state):
        
        best_score = -math.inf
        best_move = None
        
        moves = self.get_valid_moves(state)

        for move in moves:
            child_state = self.make_move(
                state, move, self.player
            )

            score = self.minimax(
                child_state,
                self.depth - 1,
                False
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    def minimax(self, state, depth, maximizing):

        # terminal state
        if self.is_winner(state, self.player):
            return 100000

        if self.is_winner(state, self.opponent):
            return -100000

        if depth == 0:
            return self.evaluate(state)

        moves = self.get_valid_moves(state)

        if len(moves) == 0:
            return 0

    
        # MAX PLAYER
    
        if maximizing:

            best_score = -math.inf

            for move in moves:

                child_state = self.make_move(
                    state, move, self.player
                )

                score = self.minimax(
                    child_state, depth -1, False
                )

                best_score = max(best_score, score)

            return best_score
       
        # MIN PLAYER

        else:

            best_score = math.inf

            for move in moves:

                child_state = self.make_move(
                    state, depth, self.opponent
                )

                score = self.minimax(
                    child_state, depth -1, True
                )

                best_score = min(best_score, score)

            return best_score