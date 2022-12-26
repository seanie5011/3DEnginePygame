import pygame
import sys
import numpy as np
from object_3d import Object3D
from camera import Camera
from projection import Projection

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

        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D(self)

        # move object initially
        self.object.translate([0.2, 0.4, 0.2])
        self.object.rotate_y(np.pi / 6)

    # control screen drawing
    def draw(self):
        self.screen.fill(pygame.Color('darkslategray'))
        self.object.draw()

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
            self.camera.control()
            pygame.display.set_caption(f'FPS: {self.clock.get_fps()}')  # set title to framerate
            pygame.display.flip()  # update screen
            self.clock.tick(self.FPS)  # set desired FPS

if __name__ == '__main__':
    app = SoftwareRender()
    app.run()
