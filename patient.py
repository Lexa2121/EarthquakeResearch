from eathquake_data import ILLNESS_DATA


class Patient:
    def __init__(self, illness):
        assert illness in ILLNESS_DATA
        self.illness = illness
        self.cure_time = ILLNESS_DATA[illness]['mean_cure_time']