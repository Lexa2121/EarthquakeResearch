from eathquake_data import ILLNESS_DATA, ILLNESS_DATA_ENHANCED


class Patient:
    def __init__(self, illness, town='N', name='Patient from N'):
        self.illness = illness
        self.town = town
        self.name = name
        try:
            self.cure_time = ILLNESS_DATA[illness]['mean_cure_time']
        except KeyError:
            self.cure_time = ILLNESS_DATA_ENHANCED[illness[0]][illness[1]][illness.split('_')[-1]]['op_time']
        self.delivering_start_time = 0
        self.delivering_end_time = 0
        self.queue_in_mc_start_time = 0
        self.surgery_start_time = 0
        self.surgery_end_time = 0

    def __repr__(self):
        return self.name
