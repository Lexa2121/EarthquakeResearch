from poisson_flow_sim.base.med_team import MedTeam
from poisson_flow_sim.base.patient import InjurySpecificPatient
from bisect import insort
from typing import Dict, List


class SimpleEvacuationCenter:

    def __init__(self, num_teams):

        self.free_teams = [MedTeam(f"Team #{i}") for i in range(1, num_teams+1)]
        self.busy_teams = []
        self.queue = []
        self.patient_history = []
        self.cured_patient_history = []
        self.free_teams_history = []
        self.queue_history = []
        self.num_patients_in_mc = 0

    def receive_patients(self, patients):

        self.queue.extend(patients)
        self.num_patients_in_mc += len(patients)

    def check_teams(self, cur_time):

        for team in self.busy_teams:
            if team.will_be_free == cur_time:
                freed_patient = team.free_up(cur_time)
                self.cured_patient_history.append(freed_patient)
                self.free_teams.append(team)
                self.num_patients_in_mc -= 1
        self.busy_teams = list(filter(lambda team_: team_.is_busy, self.busy_teams))

        for team in self.free_teams:
            if not self.queue:
                break
            else:
                patient_to_op = self.queue.pop(0)
                self.patient_history.append(patient_to_op)
                team.occupy(cur_time, patient_to_op)
                self.busy_teams.append(team)
        self.free_teams = list(filter(lambda team_: not team_.is_busy, self.free_teams))
        self.free_teams_history.append(len(self.free_teams))
        self.queue_history.append(len(self.queue))


class StateSpecificEvacuationCenter(SimpleEvacuationCenter):

    def __init__(self, num_teams):
        super(StateSpecificEvacuationCenter, self).__init__(num_teams)

    def receive_patients(self, patients):
        for p in patients:
            insort(self.queue, p)
        self.num_patients_in_mc += len(patients)


class InjurySpecificEvacuationCenter:

    def __init__(self, num_teams: Dict):
        self.free_teams = {}
        for injury, teams_amount in num_teams.items():
            self.free_teams[injury] = [MedTeam(f"{injury} Team #{i}".title()) for i in range(1, teams_amount+1)]
        self.busy_teams = {injury: [] for injury in num_teams}
        self.queue = {injury: [] for injury in num_teams}
        self.patient_history = {injury: [] for injury in num_teams}
        self.cured_patient_history = {injury: [] for injury in num_teams}
        self.free_teams_history = {injury: [] for injury in num_teams}
        self.queue_history = {injury: [] for injury in num_teams}
        self.num_patients_in_mc = 0

    def receive_patients(self, patients: List[InjurySpecificPatient]):
        for p in patients:
            insort(self.queue[p.injury_type], p)
        self.num_patients_in_mc += len(patients)

    def check_teams(self, cur_time):

        for injury, injury_busy_teams in self.busy_teams.items():
            for team in injury_busy_teams:
                if team.will_be_free == cur_time:
                    freed_patient = team.free_up(cur_time)
                    self.cured_patient_history[injury].append(freed_patient)
                    self.free_teams[injury].append(team)
                    self.num_patients_in_mc -= 1
            self.busy_teams[injury] = list(filter(lambda team_: team_.is_busy, self.busy_teams[injury]))

        for injury, injury_free_teams in self.free_teams.items():
            for team in injury_free_teams:
                if not self.queue[injury]:
                    break
                else:
                    patient_to_op = self.queue[injury].pop(0)
                    self.patient_history[injury].append(patient_to_op)
                    team.occupy(cur_time, patient_to_op)
                    self.busy_teams[injury].append(team)
            self.free_teams[injury] = list(filter(lambda team_: not team_.is_busy, self.free_teams[injury]))
            self.free_teams_history[injury].append(len(self.free_teams[injury]))
            self.queue_history[injury].append(len(self.queue[injury]))
