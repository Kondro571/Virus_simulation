from Vector2D.Vector2D import Vector2D
from Vector2D.IVector2D import IVector

from State.IsState import *
import copy



class Person(IVector):

    def __init__(self, state, x, y):
        super().__init__()
        self._state = state
        self._vector = Vector2D(x, y)
        self._sick_time = 0
        self._time_near_ill = 0
        self.directionX=1
        self.directionY=1

    def setDirectionX(self,x):
        self.directionX*=x
        
    def setDirectionY(self,y):
        self.directionY*=y

    def getDirection(self):
        return [self.directionX,self.directionY]

    def set_coordinate(self, x, y):
        self._vector.set_coordinate(x, y)

    def get_components(self):
        return self._vector.get_components()

    def set_state(self, state):
        self._state = state
    
    def get_state(self):
        return self._state.get_color()
    
    def set_sick_time(self, time):
        self._sick_time = time

    def increase_sick_time(self):
        self._sick_time = self._sick_time+1

    def get_sick_time(self):
        return self._sick_time

    def set_time_near_ill(self, time):
        self._time_near_ill = time

    def get_time_near_ill(self):
        return self._time_near_ill
    
    def increase_time_near_ill(self):
        self._time_near_ill = self._time_near_ill+1

    def abs(self,component):
        return self._vector.abs(component)

    def cdot(self, other_vector):
        return self._vector.cdot(other_vector)

    def clone(self):
        return copy.deepcopy(self)