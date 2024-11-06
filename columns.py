import pygame
import random
import math
import project4_game


# Hardcoded frame rate, width, height, background color, empty grid color,
# and size of the cells.
_FRAME_RATE = 30
_WIDTH = 276
_HEIGHT = 598
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)
_GRID_COLOR = pygame.Color(70, 70, 70)
_BLOCK_SIZE = 45

class ColumnsGame:
    def __init__(self):
        self._running = True
        self._game = project4_game.Game(13, 6, ['EMPTY'])

    def run(self) -> None:
        pygame.init()
        try:

            # Creates surface and a copy of it. The game will be drawn on the
            # copy, which will then be stretched using blit to scale with the
            # screen size.
            self._create_surface((_WIDTH, _HEIGHT))

            self._drawing_surface = self._surface.copy()
            
            clock = pygame.time.Clock()
            k = 0
            while self._running:
                clock.tick(30)
                # Every second, "move" the game (i.e. make faller go down one
                # cell, find matches, etc.)
                if math.floor(pygame.time.get_ticks() / 1000) > k:
                    k += 1
                    self._game.move()
                # if there is no faller current, check for matches, and if there
                # are no matches, add a new faller
                if not self._game.faller_exists():
                    if self._game._check_for_matches():
                        pass
                    else:
                        self._add_faller_to_random_clear_column()
                self._handle_events()
                self._redraw()
        except project4_game.GameOverError:
            # Catch the game over error created in the model of the game, and
            # displays "GAME OVER" for 3 seconds before closing the game window
            self._game_over_screen()
            pygame.time.delay(3000)
            pass
        finally:
            pygame.quit()
        
    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)


    def _game_over_screen(self) -> None:
        # Displays a "GAME OVER" message
        font = pygame.font.Font(None, 50)
        text = font.render('GAME OVER', True, pygame.Color(255, 255, 255), _BACKGROUND_COLOR)
        textRect = text.get_rect()
        textRect.center = (_WIDTH / 2, _HEIGHT / 2)
        self._drawing_surface.blit(text, textRect)
        self._surface.blit(pygame.transform.scale(self._drawing_surface,
                                                  self._surface.get_rect().size),
                            (0, 0))
        pygame.display.flip()

    def _add_faller_to_random_clear_column(self) -> None:
        # First goes through the game and creates a list of columns that
        # have the top tile empty
        list_of_free_columns = []
        for i in range(6):
            if self._game.state()[0][i][0] == ' ':
                list_of_free_columns.append(i + 1)
        # If no columns have the top tile empty, end the game
        if list_of_free_columns == []:
            raise project4_game.GameOverError
        # Create 3 random colors for the jewels of the faller, and create a
        # faller in the game
        else:
            c1 = random.randint(0, 6)
            c2 = random.randint(0, 6)
            c3 = random.randint(0, 6)
            ac = random.randint(list_of_free_columns[0],
                                list_of_free_columns[-1])
            self._game.add_faller(f'{ac} {c1} {c2} {c3}') 
    
    def _handle_events(self) -> None:
        # Handles user's actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._create_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._game.move_faller_left()
                elif event.key == pygame.K_RIGHT:
                    self._game.move_faller_right()
                elif event.key == pygame.K_SPACE:
                    self._game.rotate_faller()

    def _redraw(self) -> None:
        self._drawing_surface.fill(_BACKGROUND_COLOR)
        
        gamestate = self._game.state()
        for row in range(len(gamestate)):
            for col in range(len(gamestate[row])):
                x = _WIDTH / 6 * col
                y = _HEIGHT / 13 * row
                # Location of each cell will be 1/6th of the width and 1/13th
                # of the height
                rect = pygame.Rect(x, y, _BLOCK_SIZE, _BLOCK_SIZE)
                # if the cell is empty, fill it with the grid color
                if gamestate[row][col][0] == ' ':
                    pygame.draw.rect(self._drawing_surface, _GRID_COLOR, rect)
                else:
                    # if the jewel has landed, slightly darken the colors
                    if gamestate[row][col][1] == 'LANDED':
                        c = get_color(gamestate[row][col][0])
                        c.r -= 55
                        c.g -= 55
                        c.b -= 55
                        pygame.draw.rect(self._drawing_surface,
                                         c,
                                         rect)
                    # if the jewels has found a match, make all matching jewels
                    # white before disappearing
                    elif gamestate[row][col][1] == 'MATCH':
                        pygame.draw.rect(self._drawing_surface,
                                         pygame.Color(255, 255, 255),
                                         rect)
                    # otherwise display the falling/frozen jewel regularly
                    else:
                        pygame.draw.rect(self._drawing_surface,
                                         get_color(gamestate[row][col][0]),
                                         rect)
                                    
        # Fit the drawing screen onto the game window for scaling purposes
        self._surface.blit(pygame.transform.scale(self._drawing_surface,
                                                  self._surface.get_rect().size), (0, 0))
        pygame.display.flip()



def get_color(number: str) -> pygame.Color:
    # The color of the jewels are stored as numbers. This function turns the
    # numbers into a color for display in the game
    number = int(number)
    if number == 0:
        # purple
        return pygame.Color(255, 55, 255)
    elif number == 1:
        # orange
        return pygame.Color(255, 165, 55)
    elif number == 2:
        # green
        return pygame.Color(55, 255, 55)
    elif number == 3:
        # cyan
        return pygame.Color(55, 255, 255)
    elif number == 4:
        # yellow
        return pygame.Color(225, 255, 55)
    elif number == 5:
        # blue
        return pygame.Color(55, 55, 255)
    elif number == 6:
        # red
        return pygame.Color(255, 55, 55)
        
        

if __name__ == '__main__':
    ColumnsGame().run()




