import numpy as np


class MedTeam:

    def __init__(self, name):
        self.is_busy = False
        self.will_be_free = np.inf
        self.patient = None
        self.name = name

    def occupy(self, cur_time, patient):
        self.patient = patient
        self.is_busy = True
        self.will_be_free = cur_time + patient.cure_time

    def free_up(self, cur_time=0):
        patient = self.patient
        self.is_busy = False
        self.patient = None
        return patient

    def __repr__(self):
        return self.name


class Specialist(MedTeam):

    def __init__(self, name):
        super(Specialist, self).__init__(name)
        self.idle_time_list = []
        self.last_op_end = None

    def occupy(self, cur_time, patient):
        super(Specialist, self).occupy(cur_time, patient)
        if self.last_op_end is not None:
            self.idle_time_list.append(cur_time - self.last_op_end)

    def free_up(self, cur_time=0):
        self.last_op_end = cur_time
        super(Specialist, self).free_up()


class OperationTeam(MedTeam):

    def __init__(self, name, specialists):
        super(OperationTeam, self).__init__(name)
        self.team = specialists

    def occupy(self, cur_time, patient):
        super(OperationTeam, self).occupy(cur_time, patient)
        for specialist in self.team:
            specialist.occupy(cur_time, patient)

    def free_up(self, cur_time=0):
        patient = self.patient
        for specialist in self.team:
            _ = specialist.free_up(cur_time)
        self.is_busy = False
        self.patient = None
        return patient

    def __repr__(self):
        return self.name
