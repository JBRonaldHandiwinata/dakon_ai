import pygame

"""
This class manages board game user interface
"""


class GameBoard:

    def draw_board(self, game, screen):
        """
        it draws board of mancala
        :param game: GameEnv class object
        :param screen: pygame Surface object that represents the display surface
        where the Mancala board is drawn
        :return: Void
        """
        screen.fill((0, 128, 0))  # Green background
        for i in range(6):
            color = (
                (255, 255, 0)
                if game.highlighted_hole == 5 - i or game.highlighted_hole == 7 + i
                else (255, 255, 255)
            )
            self._draw_small_stores(game, screen, color, i)
        self._draw_big_stores(game, screen)
        self._player_indicator(game, screen)
        self._winner_information(game, screen)

    def _draw_small_stores(self, game, screen, color, index):
        i = index
        pygame.draw.circle(screen, color, (150 + i * 80, 250), 30)
        pygame.draw.circle(screen, color, (150 + i * 80, 150), 30)
        pygame.draw.circle(screen, (0, 0, 0), (150 + i * 80, 250), 28)
        pygame.draw.circle(screen, (0, 0, 0), (150 + i * 80, 150), 28)
        screen.blit(
            pygame.font.SysFont(None, 36).render(
                str(game.board[5 - i]), True, (255, 255, 255)
            ),
            (140 + i * 80, 240),
        )
        screen.blit(
            pygame.font.SysFont(None, 36).render(
                str(game.board[7 + i]), True, (255, 255, 255)
            ),
            (140 + i * 80, 140),
        )

    def _draw_big_stores(self, game, screen):
        pygame.draw.rect(screen, (255, 255, 255), (50, 120, 50, 170))  # Left store
        pygame.draw.rect(screen, (255, 255, 255), (600, 120, 50, 170))  # Right store
        screen.blit(
            pygame.font.SysFont(None, 36).render(str(game.board[6]), True, (0, 0, 0)),
            (65, 197),
        )
        screen.blit(
            pygame.font.SysFont(None, 36).render(str(game.board[13]), True, (0, 0, 0)),
            (615, 197),
        )

    def _player_indicator(self, game, screen):
        player_text = f"Player {game.current_player + 1}'s turn"
        screen.blit(
            pygame.font.SysFont(None, 36).render(player_text, True, (255, 255, 255)),
            (10, 10),
        )

    def _winner_information(self, game, screen):
        if game.is_game_over():
            winner = game.get_winner()
            if winner == 0:
                winner_text = "Player 1 Wins!"
            elif winner == 1:
                winner_text = "Player 2 Wins!"
            else:
                winner_text = "It's a Tie!"

            winner_surface = pygame.font.SysFont(None, 48).render(
                winner_text, True, (255, 255, 255)
            )
            winner_rect = winner_surface.get_rect(center=(350, 350))
            screen.blit(winner_surface, winner_rect)

    def draw_button(self, screen, text, position, size, color, text_color):
        """
        :param screen:
        :param text:
        :param position:
        :param size:
        :param color:
        :param text_color:
        """
        pygame.draw.rect(screen, color, (*position, *size))
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(
            center=(position[0] + size[0] // 2, position[1] + size[1] // 2)
        )
        screen.blit(text_surface, text_rect)

    def get_clicked_hole(self, pos, player):
        x, y = pos
        for i in range(6):
            hole_x = 150 + i * 80
            if player == 0 and 220 < y < 280 and hole_x - 30 < x < hole_x + 30:
                return 5 - i  # Bottom row (Player 1), right to left
            elif player == 1 and 120 < y < 180 and hole_x - 30 < x < hole_x + 30:
                return 7 + i  # Top row (Player 2), left to right
        return None
