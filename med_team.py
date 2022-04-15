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

    def free_up(self):
        self.is_busy = False
        self.patient = None

    def __repr__(self):
        return self.name