class Ambulance:
    def __init__(self, name, town, path, capacity=2, speed=1, from_mc=True, time_to_load_patient=1):
        self.name = name
        self.town = town
        self.unload_time = 0
        self.time_to_load_patient = time_to_load_patient
        self.time_in_road = 0
        self.capacity = capacity
        self.time_to_road = path//speed
        self.time_in_road = path//speed - 1
        self.patients_onboard = []
        self.from_mc = from_mc

    def load(self, patients):
        self.patients_onboard.extend(patients)
        self.time_in_road = -len(patients) * self.time_to_load_patient
        self.unload_time = len(patients) * self.time_to_load_patient
        self.from_mc = False

    def ride(self, t):
        self.time_in_road += t

    def __repr__(self):
        return self.name
