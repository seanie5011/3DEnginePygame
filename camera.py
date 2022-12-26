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

        # movement
        self.moving_speed = 0.02
        self.rotation_speed = 0.01

    def control(self):
        # get key presses to check controls
        key = pygame.key.get_pressed()

        # sprinting (fast camera movement)
        if key[pygame.K_LSHIFT]:  # if sprinting, double speed
            moving_speed = self.moving_speed * 2
        else:  # if not sprinting
            moving_speed = self.moving_speed

        # forward movement
        if key[pygame.K_w]:
            self.position += moving_speed * self.forward
        elif key[pygame.K_s]:
            self.position -= moving_speed * self.forward

        # right movement
        if key[pygame.K_d]:
            self.position += moving_speed * self.right
        elif key[pygame.K_a]:
            self.position -= moving_speed * self.right

        # up movement
        if key[pygame.K_SPACE]:
            self.position += moving_speed * self.up
        elif key[pygame.K_LCTRL]:
            self.position -= moving_speed * self.up

        # yaw movement
        if key[pygame.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        elif key[pygame.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)

        # pitch movement
        if key[pygame.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        elif key[pygame.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        # get rotation matrix and apply to each orientation vector
        rotation = tr.rotate_y(angle)
        self.forward = self.forward @ rotation
        self.right = self.right @ rotation
        self.up = self.up @ rotation

    def camera_pitch(self, angle):
        # get rotation matrix and apply to each orientation vector
        rotation = tr.rotate_x(angle)
        self.forward = self.forward @ rotation
        self.right = self.right @ rotation
        self.up = self.up @ rotation

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
