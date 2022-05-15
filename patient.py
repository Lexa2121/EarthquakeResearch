from eathquake_data import ILLNESS_DATA


class Patient:
    def __init__(self, illness, town, name):
        assert illness in ILLNESS_DATA
        self.illness = illness
        self.town = town
        self.name = name
        self.cure_time = ILLNESS_DATA[illness]['mean_cure_time']
        self.delivering_start_time = 0
        self.delivering_end_time = 0
        self.queue_in_mc_start_time = 0
        self.surgery_start_time = 0
        self.surgery_end_time = 0

    def __repr__(self):
        return self.name