from receiver import Receiver
from med_team import MedTeam, Specialist, OperationTeam
from eathquake_data import ILLNESS_DATA_ENHANCED


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


class SpecialistsCenter:

    def __init__(self, specialists: dict):
        self.team = {}
        self.patients_in_mc = 0
        self.queue = []
        for k, v in specialists.items():
            self.team[k] = {}
            self.team[k]['specialists'] = [Specialist(f'{k} {i}') for i in range(v)]
            self.team[k]['queue'] = []
        self.patient_history = []
        self.levels = ['critical', 'grave', 'moderate', 'light']
        self.op_teams = []

    def add_patients(self, patients):
        self.queue.extend(patients)
        self.patients_in_mc += len(patients)
        self.queue = sorted(self.queue, key=lambda x: (self.levels.index(x.illness.split('_')[-1]),
                                                       x.queue_in_mc_start_time))

    def check_specialists(self, cur_time):
        teams_to_free_up = []
        for op_team in self.op_teams:
            if op_team.will_be_free == cur_time:
                freed_patient = op_team.free_up(cur_time)
                freed_patient.surgery_end_time = cur_time
                self.patient_history.append(freed_patient)
                teams_to_free_up.append(self.op_teams.index(op_team))
                self.patients_in_mc -= 1
        k = 0
        for free_team_index in teams_to_free_up:
            self.op_teams.pop(free_team_index-k)
            k += 1

    def check_queue(self, cur_time):
        self.check_specialists(cur_time)
        k = 0
        for i in range(len(self.queue)):
            patient = self.queue[i-k]
            global_illness_type = patient.illness[0]
            subtype = patient.illness[1]
            level = patient.illness.split('_')[-1]
            specialists_needed = ILLNESS_DATA_ENHANCED[global_illness_type][subtype][level]['specialists']
            potential_team = set()
            for specialist_needed in specialists_needed:
                for specialist in self.team[specialist_needed]['specialists']:
                    if not specialist.is_busy:
                        potential_team.add(specialist)
                        break
            if len(potential_team) == len(specialists_needed):
                patient_to_serve = self.queue.pop(i-k)
                patient_to_serve.surgery_start_time = cur_time
                op_team = OperationTeam(f'Operation team for {patient_to_serve.name}', potential_team)
                op_team.occupy(cur_time, patient_to_serve)
                self.op_teams.append(op_team)
                k += 1

