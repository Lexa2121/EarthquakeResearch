from poisson_flow_sim.base.med_team import MedTeam


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
                patient_to_op = self.queue.pop()
                self.patient_history.append(patient_to_op)
                team.occupy(cur_time, patient_to_op)
                self.busy_teams.append(team)
        self.free_teams = list(filter(lambda team_: not team_.is_busy, self.free_teams))
        self.free_teams_history.append(len(self.free_teams))
        self.queue_history.append(len(self.queue))