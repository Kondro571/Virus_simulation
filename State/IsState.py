from abc import ABC, abstractmethod

class IsState(ABC):
    @abstractmethod
    def get_color(self):
        pass

class HealtyState(IsState):
    def get_color(self):
       return "green"

class IllState(IsState):
    def get_color(self):
       return "red"

class ImmuneState(IsState):
    def get_color(self):
       return "blue"

class NoSymptomsState(IsState):
    def get_color(self):
       return "white"