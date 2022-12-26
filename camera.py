import pygame
import numpy as np
import transformations as tr

class Camera:
    def __init__(self, render, position):
        self.render = render

        # positions and orientations
        self.position = np.array([*position, 1.0])  # position is tuple of cameras (x,y,z) in world space

        self.forward = np.array([0, 0, 1, 1])  # homogeneous coords
        self.right = np.array([1, 0, 0, 1])
        self.up = np.array([0, 1, 0, 1])

        # view frustrum
        self.h_fov = np.pi / 3  # arbitrarily set
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)

        self.near_plane = 0.1  # arbitrarily set
        self.far_plane = 100

    def translate_matrix(self):
        '''
        Returns the translation required for world space to camera space
        '''
        x, y, z, w = self.position

        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1],
        ])

    def rotate_matrix(self):
        '''
        Returns the rotation matrix required for world space to camera space
        '''

        fx, fy, fz, w = self.forward
        rx, ry, rz, w = self.right
        ux, uy, uz, w = self.up

        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1],
        ])

    def camera_matrix(self):
        '''
        Returns the matrix required to convert world space to camera space
        '''
        return self.translate_matrix() @ self.rotate_matrix()
