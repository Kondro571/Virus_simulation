class CareTaker:
    def __init__(self):
        self.states = []

    def add_state(self, state):
        self.states.append(state)

    def get_state(self, index):
        return self.states[index]

    def get_last_state(self):
        return self.states[-1]
    
    def has_states(self):
        if not self.states:
            return False
        return True
