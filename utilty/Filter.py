import numpy as np


def createFilter(type, width,height):

    if type == 'square':
        return np.ones([height,width])
    if type == 'plus':
        filter = np.zeros([height,width])
        filter[ : , height//2] = 1
        filter[height//2 , : ] = 1
        return filter
    if type == 'hole_circle':
        m1 = create_circular_mask(height,width)
        m2 = create_circular_mask(height,width,radius= (height//2)- 1)
        mask = (m1 != m2) *1
        return mask
    if type == 'fill_circle':
        m1 = create_circular_mask(height,width)
        mask = m1  *1
        return mask

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    mask = dist_from_center <= radius
    return mask