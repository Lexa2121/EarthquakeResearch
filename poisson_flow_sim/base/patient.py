from abc import ABC, abstractmethod


class Patient(ABC):

    def __init__(self, mc_arrival_time: int, name: str, state='light'):
        self.mc_arrival_time = mc_arrival_time
        self.op_start_time = None
        self.op_end_time = None
        self.name = name
        self.state = state
        self.states_priority = ['grave', 'moderate', 'light']

    @abstractmethod
    def start_operation(self, current_time: int):
        pass

    @abstractmethod
    def end_operation(self, current_time: int):
        pass

    @property
    def time_in_mc_queue(self):
        return self.op_start_time - self.mc_arrival_time

    def __repr__(self):
        return self.name


class CommonPatient(Patient):

    def __init__(self, mc_arrival_time: int, name: str, cure_time: int = 3, state='light'):
        super(CommonPatient, self).__init__(mc_arrival_time, name, state)
        self.cure_time = cure_time

    def start_operation(self, current_time):
        self.op_start_time = current_time

    def end_operation(self, current_time):
        self.op_end_time = current_time

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state

    def __lt__(self, other):
        return self.states_priority.index(self.state) < self.states_priority.index(other.state)

    def __gt__(self, other):
        return self.states_priority.index(self.state) > self.states_priority.index(other.state)

    def __le__(self, other):
        return self.states_priority.index(self.state) <= self.states_priority.index(other.state)

    def __ge__(self, other):
        return self.states_priority.index(self.state) >= self.states_priority.index(other.state)


class InjurySpecificPatient(CommonPatient):

    def __init__(self, mc_arrival_time: int, name: str, injury_type: str, cure_time: int = 2, state='light'):
        super(InjurySpecificPatient, self).__init__(mc_arrival_time, name, cure_time, state)
        self.injury_type = injury_type
