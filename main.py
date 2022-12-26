import pygame
import sys
import numpy as np
from object_3d import Object3D, Object3D_preset
from camera import Camera
from projection import Projection

# class to control rendering
class SoftwareRender:
    def __init__(self, model='cube', draw_vertices=True):
        # initialise pygame
        pygame.init()

        # currently supported preset models / objects
        preset_objects = [
            'cube',
        ]
        
        # settings
        self.WIDTH, self.HEIGHT = 1600, 900
        self.FPS = 60

        # create scene
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        if model in preset_objects:  # check if model has already been hardcoded
            self.create_preset_objects(model, draw_vertices)
        else:
            try:  # see if it is at a file location specified
                vertices, faces = self.get_object_from_file(model)
                self.create_custom_objects(vertices, faces, draw_vertices)
            except:  # if the file checking does not work
                    self.create_preset_objects('cube', draw_vertices)
                    print('ERROR: model specified not found.')

    def create_preset_objects(self, model, draw_vertices):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D_preset(self, model, draw_vertices)

        # move object initially
        self.object.translate([0.2, 0.4, 0.2])
        self.object.rotate_y(np.pi / 6)

    def create_custom_objects(self, vertices, faces, draw_vertices):
        self.camera = Camera(self, [5, 5, -5])
        self.projection = Projection(self)
        self.object = Object3D(self, vertices, faces, draw_vertices)

    def get_object_from_file(self, filename):
        '''
        Returns the vertices and faces specified by a .obj file

        .obj files have vertices specified by lines starting with 'v ' \
        and faces specified by lines starting with 'f '
        '''

        vertices, faces = [], []
        with open(filename) as f:
            # check every line
            for line in f:
                # if vertex
                if line.startswith('v '):
                    # append the coordinates in that line by using split (ignoring the 'v ')
                    vertices.append([float(coord) for coord in line.split()[1:] + [1]])  # dont forget the 1 for homogeneous coords
                # if face
                elif line.startswith('f '):
                    # each line has multiple strings of 'a/b/c' where 'a' is the index for a vertex, where each string is seperated by a space
                    # get each seperated by a space
                    sequence = line.split()[1:]  # ignore 'f '
                    # append the index by getting the first value ('a'), these start from 1 so have to subtract 1 to account
                    faces.append([int(string.split('/')[0]) - 1 for string in sequence])

        return vertices, faces

    # control screen drawing
    def draw(self):
        self.screen.fill(pygame.Color('black'))
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
    # settings
    model = 'Horn.obj'
    draw_vertices = False

    app = SoftwareRender(model, draw_vertices)
    app.run()
