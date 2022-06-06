import numpy as np


class MedTeam:

    def __init__(self, name):
        self.is_busy = False
        self.will_be_free = np.inf
        self.patient = None
        self.name = name
        self.idle_time_list = []
        self.last_op_end = None

    def occupy(self, cur_time, patient):
        self.patient = patient
        self.patient.start_operation(cur_time)
        self.is_busy = True
        self.will_be_free = cur_time + patient.cure_time
        if self.last_op_end is not None:
            self.idle_time_list.append(cur_time - self.last_op_end)

    def free_up(self, cur_time):
        self.last_op_end = cur_time
        patient = self.patient
        patient.end_operation(cur_time)
        self.is_busy = False
        self.patient = None
        return patient

    def __repr__(self):
        return self.name
