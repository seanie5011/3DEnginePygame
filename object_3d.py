import pygame
import numpy as np
import transformations as tr
from numba import jit

@jit(nopython=True, fastmath=True)
def any_func(arr, a, b):
    '''
    Check if any arr is in a or b
    '''
    return np.any((arr == a) | (arr == b))

class Object3D_preset:  # for using models that are hardcoded
    def __init__(self, render, model, draw_vertices=True):
        self.render = render

        # set preset models
        preset_vertices = {
            'cube': np.array([
                (0, 0, 0, 1),
                (0, 1, 0, 1),
                (1, 1, 0, 1),
                (1, 0, 0, 1),
                (0, 0, 1, 1),
                (0, 1, 1, 1),
                (1, 1, 1, 1),
                (1, 0, 1, 1),
            ]),
        }

        preset_faces = {
            'cube': np.array([
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 5, 1),
            (2, 3, 7, 6),
            (1, 2, 6, 5),
            (0, 3, 7, 4),
        ])
        }

        # the vertices in homogeneous coordinates for a cube
        # 1st tuple (index 0) is the first vertex, 2nd tuple (index 1) is the second vertex, etc
        self.vertices = preset_vertices[model]

        # the faces, connecting 4 vertices
        # each tuple contains the indices of the 4 vertices which will be connected
        self.faces = preset_faces[model]

        # whether to draw vertices
        self.draw_vertices = draw_vertices

    def draw(self):
        # get vertices from screen projections
        vertices = self.screen_projections()

        # draw edges of each face as lines from a polygon
        for face in self.faces:
            polygon = vertices[face]
            if not any_func(polygon, self.render.WIDTH // 2, self.render.HEIGHT // 2):  # when a vertex is 0 (not shown) in normalised clip space, it is set equal to either half-width or half-height in screen space
                pygame.draw.polygon(self.render.screen, pygame.Color('orange'), polygon, 2)  # screen, color, vertices, width

        if self.draw_vertices:
            # draw vertices as points
            for vertex in vertices:
                if not any_func(vertex, self.render.WIDTH // 2, self.render.HEIGHT // 2):  # when a vertex is 0 (not shown) in normalised clip space, it is set equal to either half-width or half-height in screen space
                    pygame.draw.circle(self.render.screen, pygame.Color('white'), vertex, 4)  # screen, color, vertices, width

    # projections
    def screen_projections(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()  # world space to camera space
        vertices = vertices @ self.render.projection.projection_matrix  # camera space to clip space
        vertices /= vertices[:, -1].reshape(-1, 1)  # normalise clip space with respect to w, by extracting w of each and reshaping them into a compatible array before dividing (-1 means original size)
        vertices[(vertices > 2) | (vertices < -2)] = 0  # any vertices with values greater than 1 or less than -1 are not shown, as they are out of screen (clipping) {CHANGED TO 2 FOR A JANKY FIX TO CLIPPING}
        vertices = vertices @ self.render.projection.screen_matrix  # convert normalised clip space to screen space
        vertices = vertices[:, :2]  # only keep (x,y) coords of each vertex in this space

        return vertices

    # move object
    def translate(self, pos):
        self.vertices = self.vertices @ tr.translate(pos)  # @ is matrix mulitplication

    # scale object
    def scale(self, s):
        self.vertices = self.vertices @ tr.scale(s)

    # rotate object in x-direction
    def rotate_x(self, a):
        self.vertices = self.vertices @ tr.rotate_x(a)

    # rotate object in y-direction
    def rotate_y(self, a):
        self.vertices = self.vertices @ tr.rotate_y(a)

    # rotate object in z-direction
    def rotate_z(self, a):
        self.vertices = self.vertices @ tr.rotate_z(a)

class Object3D:  # same as above except now use custom vertices and faces
    def __init__(self, render, vertices, faces, draw_vertices=True):
        self.render = render

        # the vertices in homogeneous coordinates for a cube
        # 1st tuple (index 0) is the first vertex, 2nd tuple (index 1) is the second vertex, etc
        self.vertices = vertices

        # the faces, connecting 4 vertices
        # each tuple contains the indices of the 4 vertices which will be connected
        self.faces = faces

        # whether to draw vertices
        self.draw_vertices = draw_vertices

    def draw(self):
        # get vertices from screen projections
        vertices = self.screen_projections()

        # draw edges of each face as lines from a polygon
        for face in self.faces:
            polygon = vertices[face]
            if not any_func(polygon, self.render.WIDTH // 2, self.render.HEIGHT // 2):  # when a vertex is 0 (not shown) in normalised clip space, it is set equal to either half-width or half-height in screen space
                pygame.draw.polygon(self.render.screen, pygame.Color('orange'), polygon, 2)  # screen, color, vertices, width

        if self.draw_vertices:
            # draw vertices as points
            for vertex in vertices:
                if not any_func(vertex, self.render.WIDTH // 2, self.render.HEIGHT // 2):  # when a vertex is 0 (not shown) in normalised clip space, it is set equal to either half-width or half-height in screen space
                    pygame.draw.circle(self.render.screen, pygame.Color('white'), vertex, 4)  # screen, color, vertices, width

    # projections
    def screen_projections(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()  # world space to camera space
        vertices = vertices @ self.render.projection.projection_matrix  # camera space to clip space
        vertices /= vertices[:, -1].reshape(-1, 1)  # normalise clip space with respect to w, by extracting w of each and reshaping them into a compatible array before dividing (-1 means original size)
        vertices[(vertices > 2) | (vertices < -2)] = 0  # any vertices with values greater than 1 or less than -1 are not shown, as they are out of screen (clipping) {CHANGED TO 2 FOR A JANKY FIX TO CLIPPING}
        vertices = vertices @ self.render.projection.screen_matrix  # convert normalised clip space to screen space
        vertices = vertices[:, :2]  # only keep (x,y) coords of each vertex in this space

        return vertices

    # move object
    def translate(self, pos):
        self.vertices = self.vertices @ tr.translate(pos)  # @ is matrix mulitplication

    # scale object
    def scale(self, s):
        self.vertices = self.vertices @ tr.scale(s)

    # rotate object in x-direction
    def rotate_x(self, a):
        self.vertices = self.vertices @ tr.rotate_x(a)

    # rotate object in y-direction
    def rotate_y(self, a):
        self.vertices = self.vertices @ tr.rotate_y(a)

    # rotate object in z-direction
    def rotate_z(self, a):
        self.vertices = self.vertices @ tr.rotate_z(a)
