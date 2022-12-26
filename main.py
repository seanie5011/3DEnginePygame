import pygame
import sys

# class to control rendering
class SoftwareRender:
    def __init__(self):
        # initialise pygame
        pygame.init()
        
        # settings
        self.WIDTH, self.HEIGHT = 1600, 900
        self.FPS = 60

        # create scene
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    # control screen drawing
    def draw(self):
        self.screen.fill(pygame.Color('darkslategray'))

    # control game loop
    def run(self):
        while True:
            # event handling
            for event in pygame.event.get():
                # quitting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # drawing
            self.draw()
            pygame.display.set_caption(f'FPS: {self.clock.get_fps()}')  # set title to framerate
            pygame.display.flip()  # update screen
            self.clock.tick(self.FPS)  # set desired FPS

if __name__ == '__main__':
    app = SoftwareRender()
    app.run()
