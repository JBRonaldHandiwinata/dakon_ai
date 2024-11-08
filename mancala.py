import math
import random
import pygame
from game_board import GameBoard
from game_env import GameEnv
from minimax import Minimax


MENU, PLAYING = 0, 1
HUMAN_VS_AI, AI_VS_AI = 1, 2


class Mancala:

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((700, 400))
        pygame.display.set_caption("Congklak")
        game_state, mode, game, running, animating = MENU, None, None, True, False
        animation_generator, clock = None, pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game, mode, game_state, \
                    animation_generator, animating = self._event_handler(event, game_state, mode, game,
                                                                         animation_generator, animating)
            screen.fill((0, 128, 0))
            if game_state == MENU:
                self._draw_menu(screen)
            elif game_state == PLAYING:
                animating, animation_generator = self._process_game(game, animating, mode, animation_generator)
                GameBoard().draw_board(game, screen)

                if game.is_game_over():
                    GameEnv().print_game_state(game)
                    print(f"Game Over! Winner: Player {game.get_winner() + 1}")
                    pygame.time.delay(5000)
                    running = False

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def _draw_menu(self, screen):
        GameBoard().draw_button(screen, "Human vs AI", (200, 150), (300, 50), (255, 255, 255), (0, 0, 0))
        GameBoard().draw_button(screen, "AI vs AI", (200, 250), (300, 50), (255, 255, 255), (0, 0, 0))

    def _event_handler(self, event, game_state, mode, game, animation_generator, animating):
        if game_state == MENU:
            game = GameEnv()
            game_state = PLAYING
            if 200 <= event.pos[0] <= 500:
                if 150 <= event.pos[1] <= 200:
                    mode = HUMAN_VS_AI  # Human vs AI
                elif 250 <= event.pos[1] <= 300:
                    mode = AI_VS_AI  # AI vs AI
        elif (game_state == PLAYING and mode == HUMAN_VS_AI and game.current_player == 0 and not animating):
            clicked_hole = GameBoard().get_clicked_hole(event.pos, game.current_player)
            if clicked_hole is not None and game.board[clicked_hole] > 0:
                print(f"Player 1 chooses hole {clicked_hole + 1}")
                game.set_highlighted_hole(clicked_hole)
                animation_generator = game.animate_move(clicked_hole)
                animating = True
        return game, mode, game_state, animation_generator, animating

    def _process_game(self, game, animating, mode, animation_generator):
        if not game.is_game_over() and not animating:
            GameEnv().print_game_state(game)
            if mode == AI_VS_AI or (mode == HUMAN_VS_AI and game.current_player == 1):
                best_move, _ = Minimax().ai_move(game, 4, game.current_player == 0)
                if best_move is not None:
                    player_name = ("Player 1" if game.current_player == 0 else "Player 2")
                    hole_number = (best_move + 1 if game.current_player == 0 else best_move - 6)
                    print(f"{player_name} chooses hole {hole_number}")
                    game.set_highlighted_hole(best_move)
                    animation_generator = game.animate_move(best_move)
                    animating = True
        if animating:
            try:
                result = next(animation_generator)
                if isinstance(result, bool):
                    animating = False
                    if not result:
                        game.current_player = 1 - game.current_player
                    game.set_highlighted_hole(None)
                pygame.time.delay(600)
            except StopIteration:
                animating = False
                game.set_highlighted_hole(None)
        return animating, animation_generator


if __name__ == "__main__":
    Mancala().main()

