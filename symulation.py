import random
import pygame
import pygame_gui
from pygame.locals import *
from objects.Person import Person
from State.IsState import *
from objects.memento import *
from objects.CareTaker import *
import copy

class Symulation():

    def __init__(self, dimensions, size, immune=0):
        pygame.init()
        height = dimensions[1]
        width = dimensions[0]
        self.win = pygame.display.set_mode((width, height + 100))
        pygame.display.set_caption("symulacja")
        self.manager = pygame_gui.UIManager((width, height + 100))
        self.button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width*0.25, height + 30), (width*0.2, 50)),
            text='save', manager=self.manager
        )

        self.button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width*0.5, height + 30), (width*0.2, 50)),
            text='load', manager=self.manager
        )

        self.dimensions = dimensions
        self.population_list = []
        self.size=size
        for i in range(self.size):
            x = random.randrange(0, self.dimensions[0])
            y = random.randrange(0, self.dimensions[1])
            
            if random.random() < 0.1:
                self.population_list.append(Person(IllState(), x, y))
            elif random.random() < 0.2 and immune:
                self.population_list.append(Person(ImmuneState(), x, y))
            else:
                self.population_list.append(Person(HealtyState(), x, y))

        self.target_fps = 250
        self.clock = pygame.time.Clock()
        self.run = True
        self.caretaker = CareTaker()
        self.time_since_last_update = 0

        self.i=0

    def create_memento(self):
        memento = Memento(self.dimensions, self.population_list)
        self.caretaker.add_state(memento)
        print("Symulacja zapisana!")

    def restore_from_memento(self):
        if self.caretaker.has_states():
            memento = self.caretaker.get_last_state()
            self.dimensions = memento.dimensions
            self.population_list = copy.deepcopy(memento.list)
            print("Symulacja przywrocona!")

    def Run(self):
        while self.run:
            self.handle_events()

            time_delta = self.clock.tick(self.target_fps)
            self.time_since_last_update += time_delta

            while self.time_since_last_update >= 1000:
                self.time_since_last_update -= 1000
                self.symulation()
           
            self.manager.update(time_delta)
            self.draw_ui()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button1.rect.collidepoint(event.pos):
                        self.create_memento()

                    if self.button2.rect.collidepoint(event.pos):
                        self.restore_from_memento()

            self.manager.process_events(event)

    def draw_ui(self):
        self.i+=1
        self.win.fill((0, 0, 0))
        for person in self.population_list:
            self.move(person)
            self.update_position(person)
            
            
        
        pygame.draw.rect(
            self.win, (200, 200, 200),
            pygame.Rect(0, self.dimensions[1] + 2, self.dimensions[0], 100)
        )

        self.manager.draw_ui(self.win)
        pygame.display.flip()

    def update_position(self, person0):
        color = person0.get_state()
        position = person0.get_components()
        radius = 5
        pygame.draw.circle(self.win, color, (int(position[0]), int(position[1])), radius)

    def move(self, person):
        position = person.get_components()
        if random.random()<0.2:
            person.setDirectionX(-1)
        if random.random()<0.2:
            person.setDirectionY(-1)
        x = position[0] + person.getDirection()[0] * random.uniform(0, 5) / 7
        y = position[1] + person.getDirection()[1] * random.uniform(0, 5) / 7

        if x > self.dimensions[0] or x < 0:
            if random.random() < 0.5:
                x = -x
                person.set_coordinate(x, y)
            else:
                y = 0
                x = random.randrange(0, self.dimensions[1])
                state = IllState() if random.random() < 0.1 else HealtyState()

                person.set_coordinate(x, y)
                person.set_state(state)
                person.set_sick_time(0)
                person.set_time_near_ill(0)

        elif y > self.dimensions[1] or y < 0:
            if random.random() < 0.5:
                y = -y
                person.set_coordinate(x, y)
            else:
                y = random.randrange(0, self.dimensions[0])
                x = 0
                state = IllState() if random.random() < 0.1 else HealtyState()

                person.set_coordinate(x, y)
                person.set_state(state)
                person.set_sick_time(0)
                person.set_time_near_ill(0)
        else:
            person.set_coordinate(x, y)

    def check_distance(self):
        for i in range(len(self.population_list)):
            for j in range(i + 1, len(self.population_list)):
                person1 = self.population_list[i]
                person2 = self.population_list[j]

                distance = person1.abs(person2.get_components())

                if distance < 20:
                    if person1.get_state() == "green" and (person2.get_state() == "red" or person2.get_state() == "white"):
                        if person2.get_state() == "white":
                            if random.random()<0.5:
                                person1.increase_time_near_ill()
                        else:
                            person1.increase_time_near_ill()
                    elif person2.get_state() == "green" and (person1.get_state() == "red" or person1.get_state() == "white"):
                        if person1.get_state() == "white":
                            if random.random()<0.5:
                                person2.increase_time_near_ill()
                        else:
                            person2.increase_time_near_ill()

    def check_state(self, person):
        if person.get_state() == "red" or person.get_state() == "white":
            person.increase_sick_time()

            if person.get_sick_time() > random.randrange(25, 30):
                person.set_state(ImmuneState())

        if person.get_time_near_ill() >= 3 and person.get_state() == "green":
            if random.random()<0.3:
                person.set_state(NoSymptomsState())
            else:
                person.set_state(IllState())

    def symulation(self):
        self.check_distance()

        for person0 in self.population_list:
            self.check_state(person0)
      
        
if __name__ == "__main__":
    simulation = Symulation([600, 400], 100)
    simulation.Run()
    pygame.quit()
