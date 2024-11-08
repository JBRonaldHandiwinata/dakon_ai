import math
from game_env import GameEnv


class Minimax:

    def ai_move(self, game, depth, maximizing_player):
        if depth == 0 or game.is_game_over():
            return None, self.evaluate_board(game)

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in self.valid_moves(game, 0):
                new_game = self.simulate_move(game, move)
                _, eval = self.ai_move(new_game, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = math.inf
            best_move = None
            for move in self.valid_moves(game, 1):
                new_game = self.simulate_move(game, move)
                _, eval = self.ai_move(new_game, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move, min_eval

    # Evaluate minimax algorithm
    def evaluate_board(self, game):
        return game.board[6] - game.board[13]

    def valid_moves(self, game, player):
        if player == 0:
            return [i for i in range(6) if game.board[i] > 0]
        else:
            return [i for i in range(7, 13) if game.board[i] > 0]

    def simulate_move(self, game, move):
        new_game = GameEnv()
        new_game.board = game.board[:]
        new_game.current_player = game.current_player
        new_game.move(move)
        return new_game

