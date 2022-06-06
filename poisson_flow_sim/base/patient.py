from abc import ABC, abstractmethod


class Patient(ABC):

    def __init__(self, mc_arrival_time: int, name: str):
        self.mc_arrival_time = mc_arrival_time
        self.op_start_time = None
        self.op_end_time = None
        self.name = name

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

    def __init__(self, mc_arrival_time: int, name: str, cure_time: int = 3):
        super(CommonPatient, self).__init__(mc_arrival_time, name)
        self.cure_time = cure_time

    def start_operation(self, current_time):
        self.op_start_time = current_time

    def end_operation(self, current_time):
        self.op_end_time = current_time
