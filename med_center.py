from receiver import Receiver
from med_team import MedTeam


class MedCenter:

    def __init__(self, receivers_number: int, med_teams: dict):
        self.receivers = [Receiver() for _ in range(receivers_number)]
        self.queue = []
        self.serving_ambulances = []
        self.med_teams = {}
        for k, v in med_teams.items():
            self.med_teams[k] = {}
            self.med_teams[k]['teams'] = [MedTeam(f'Бригада №{i}: {k} профиль') for i in range(v)]
            self.med_teams[k]['queue'] = []
        self.num_patients_in_mc = 0
        self.incoming_flow_history = []
        self.patient_history = []

    def check_receivers(self, cur_time):
        freed_ambulances = []
        incoming_patients_num = 0
        for receiver in self.receivers:
            if receiver.will_be_free == cur_time:
                freed_ambulances.append(self.free_up_receiver(receiver))
            if self.queue:
                if not receiver.is_busy:
                    receiver_incoming_patients_num = self.occupy_receiver(receiver, cur_time)
                    incoming_patients_num += receiver_incoming_patients_num
        self.check_med_teams(cur_time)
        self.incoming_flow_history.append(incoming_patients_num)
        return freed_ambulances

    def occupy_receiver(self, receiver, t):
        amb_to_receiver = self.queue.pop(0)
        patients = receiver.occupy(t, amb_to_receiver)
        self.sent_to_med_teams(patients)
        self.serving_ambulances.append(receiver.ambulance)
        return len(patients)

    def free_up_receiver(self, receiver):
        ambulance = receiver.free_up()
        freed_amb = self.serving_ambulances.pop(self.serving_ambulances.index(ambulance))
        freed_amb.from_mc = True
        return freed_amb

    def sent_to_med_teams(self, patients):
        for patient in patients:
            self.med_teams[patient.illness]['queue'].append(patient)
            self.num_patients_in_mc += 1

    def check_med_teams(self, cur_time):
        for k, v in self.med_teams.items():
            for med_team in v['teams']:
                if med_team.will_be_free == cur_time:
                    freed_patient = med_team.free_up()
                    freed_patient.surgery_end_time = cur_time
                    self.patient_history.append(freed_patient)
                    self.num_patients_in_mc -= 1
                if not med_team.is_busy and v['queue']:
                    patient_to_serve = v['queue'].pop(0)
                    patient_to_serve.surgery_start_time = cur_time
                    med_team.occupy(cur_time, patient_to_serve)