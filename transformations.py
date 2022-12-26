import numpy as np

# these are all relative to the world axes, in left-hand coords

def translate(pos):
    '''
    Returns the numpy array to move an object

    pos: a tuple of (x,y,z) indicating the amount we want to move in each direction
    '''

    tx, ty, tz = pos  # the amount to move in x,y,z directions

    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1],
    ])

def scale(s):
    '''
    Returns the numpy array to scale an object

    s: a float indicating how much we want to scale by
    '''

    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1],
    ])

def rotate_x(a):
    '''
    Returns the numpy array to rotate an object in the x-direction

    a: angle (in radians) to rotate by
    '''

    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(a), np.sin(a), 0],
        [0, -np.sin(a), np.cos(a), 0],
        [0, 0, 0, 1],
    ])

def rotate_y(a):
    '''
    Returns the numpy array to rotate an object in the y-direction

    a: angle (in radians) to rotate by
    '''

    return np.array([
        [np.cos(a), 0, -np.sin(a), 0],
        [0, 1, 0, 0],
        [np.sin(a), 0, np.cos(a), 0],
        [0, 0, 0, 1],
    ])

def rotate_z(a):
    '''
    Returns the numpy array to rotate an object in the z-direction

    a: angle (in radians) to rotate by
    '''

    return np.array([
        [np.cos(a), np.sin(a), 0, 0],
        [-np.sin(a), np.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])