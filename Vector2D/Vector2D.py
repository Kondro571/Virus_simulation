from .IVector2D import IVector

class Vector2D(IVector):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_components(self):
        return [self._x, self._y]

    def set_coordinate(self, x, y):
        self._x = x
        self._y = y

    def abs(self):
        return (self._x**2 + self._y**2)**(1/2)
    
    def abs(self, other_components):
        x2, y2 = other_components
        return ((x2 - self._x)**2 + (y2 - self._y)**2)**(1/2)

    def cdot(self, vector):
        vector = vector.get_components()
        return vector[0] * self._x + vector[1] * self._y
