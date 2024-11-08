
"""
This class manages game rules related to
currect player indicator, movement, game current state
"""
class GameEnv:

    def __init__(self):
        self.board = [7] * 6 + [0] + [7] * 6 + [0]
        self.current_player = 0
        self.highlighted_hole = None

    def set_highlighted_hole(self, index):
        self.highlighted_hole = index

    def move(self, index):
        seeds = self.board[index]
        self.board[index] = 0
        i = index
        while seeds > 0:
            i = (i + 1) % 14
            if (i == 6 and self.current_player == 1) or (i == 13 and self.current_player == 0):
                continue  # Skip opponent's store
            self.board[i] += 1
            seeds -= 1

        # Determine next turn
        if self.current_player == 0 and i == 6:
            return True  # Player 0 gets another turn
        elif self.current_player == 1 and i == 13:
            return True  # Player 1 gets another turn

        self.current_player = 1 - self.current_player  # Switch player
        return False

    def animate_move(self, index):
        seeds = self.board[index]
        self.board[index] = 0
        i = index
        while seeds > 0:
            i = (i + 1) % 14
            if (i == 6 and self.current_player == 1) or (i == 13 and self.current_player == 0):
                continue  # Skip opponent's store
            self.board[i] += 1
            seeds -= 1
            yield i  # Yield the current position for animation

        # Determine next turn
        if self.current_player == 0 and i == 6:
            yield True  # Player 0 gets another turn
        elif self.current_player == 1 and i == 13:
            yield True  # Player 1 gets another turn
        else:
            yield False

    def is_game_over(self) -> bool:
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def get_winner(self):
        if self.is_game_over():
            if self.board[6] > self.board[13]:
                return 0  # Player 1 wins
            elif self.board[6] < self.board[13]:
                return 1  # Player 2 wins
            else:
                return -1  # Tie
        return None

    def print_game_state(self, game):
        print(f"Current Player: {game.current_player + 1}")
        print("Player 2 (top)   :", " ".join(f"{x:2d}" for x in reversed(game.board[7:13])))
        print(
            "Stores: ",
            f"P2:{game.board[13]:2d}".rjust(16),
            f"P1:{game.board[6]:2d}".ljust(16),
        )
        print("Player 1 (bottom):", " ".join(f"{x:2d}" for x in game.board[:6]))
        print("-" * 40)

