import pygame
import numpy
from Day13.aoc import ArcadeGame


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("AOC: Arcade Game")
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    colors = numpy.array([[0, 0, 0], [255, 255, 255], [0, 0, 255], [160, 160, 160], [255, 0, 0]])
    arcade = ArcadeGame()
    arcade.start_game()
    score = 0
    ai = True

    running = True
    while running:
        if ai:
            arcade.computer.inputs.append(arcade.get_suggested_move())
            arcade.update_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    arcade.start_game()
                    score = 0
                if not arcade.computer.is_halted and arcade.computer.awaiting_input:
                    if not ai and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            arcade.computer.inputs.append(-1)
                        elif event.key == pygame.K_RIGHT:
                            arcade.computer.inputs.append(1)
                        else:
                            arcade.computer.inputs.append(0)
                        arcade.update_grid()
        score = arcade.score
        grid_array = numpy.array(arcade.grid.copy())
        surface = pygame.surfarray.make_surface(colors[grid_array])
        surface = pygame.transform.rotate(surface, -90)
        surface = pygame.transform.flip(surface, True, False)
        surface = pygame.transform.scale(surface, (500, 275))  # Scaled a bit.
        font = pygame.font.SysFont(None, 25)
        score_text = "Score: {}".format(score)
        if arcade.computer.is_halted:
            if arcade.get_blocks_remaining() > 0:
                score_text += " (Game Over!)"
            else:
                score_text += " (You Win!)"
        text = font.render(score_text, True, (255, 255, 255))

        screen.fill((30, 30, 30))
        screen.blit(surface, (100, 100))
        screen.blit(text, (0, 0))
        pygame.display.flip()
        clock.tick(60)
