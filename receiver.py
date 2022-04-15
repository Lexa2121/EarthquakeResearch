import numpy as np


class Receiver:

    def __init__(self):
        self.is_busy = False
        self.will_be_free = np.inf
        self.ambulance = None

    def occupy(self, cur_time, ambulance):
        self.ambulance = ambulance
        self.is_busy = True
        self.will_be_free = cur_time + ambulance.unload_time
        patients = self.ambulance.patients_onboard
        self.ambulance.patients_onboard = []
        return patients

    def free_up(self):
        freed_ambulance = self.ambulance
        self.is_busy = False
        self.ambulance = None
        return freed_ambulance
