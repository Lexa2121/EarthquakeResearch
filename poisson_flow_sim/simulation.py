from itertools import product
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from poisson_flow_sim.base.patient import CommonPatient
from poisson_flow_sim.base.evac_center import SimpleEvacuationCenter


class SimpleSimulation:

    def __init__(self, time_horizon: int = 4320,
                 flow_intensities=None,
                 teams_amounts=None,
                 time_step: int = 1,
                 verbosity=0):
        if flow_intensities is None:
            self.flow_intensities = [4]
        else:
            self.flow_intensities = flow_intensities
        if teams_amounts is None:
            self.teams_amounts = [270]
        else:
            self.teams_amounts = teams_amounts
        self.verbosity = verbosity
        self.time_horizon = time_horizon // time_step
        self.report = {}

    def set_params_from_dict(self, **kwargs):
        for param, param_value in kwargs:
            self.__setattr__(param, param_value)

    def single_sim_run(self, flow_intensity, num_teams, rs):
        np.random.seed(rs)
        mc = SimpleEvacuationCenter(num_teams)
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        if self.verbosity > 0:
            time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        else:
            time_range = range(self.time_horizon)
        for t in time_range:
            SimpleSimulation.step(t, mc, patients_flow[t])
        return patients_flow, mc

    @staticmethod
    def step(cur_time, med_center, num_patients):
        new_patients = []
        for i in range(num_patients):
            patient_number = med_center.num_patients_in_mc + len(med_center.patient_history) + i
            new_patients.append(CommonPatient(cur_time, f"Patient #{patient_number}"))
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(self.flow_intensities, self.teams_amounts))
        report = defaultdict(dict)

        for flow_intensity, num_teams in tqdm(params_combinations, desc='Combinations', position=0, leave=False):
            mean_idle_times_local = []
            mean_queue_times_local = []
            num_cured_local = []
            num_arrived_local = []
            queue_history_local = []
            free_teams_history_local = []
            for rs in tqdm(random_states, desc='Random states', position=1, leave=False):
                queue_times_local_rs = []

                patients_flow, mc = self.single_sim_run(flow_intensity, num_teams, rs)

                for mt in mc.free_teams + mc.busy_teams:
                    mean_idle_times_local.append(np.mean(mt.idle_time_list))

                for patient in mc.patient_history:
                    queue_times_local_rs.append(patient.time_in_mc_queue)
                mean_queue_times_local.append(np.mean(queue_times_local_rs))

                num_cured_local.append(len(mc.cured_patient_history))
                num_arrived_local.append(np.sum(patients_flow[:-30]))
                free_teams_history_local.append((np.array(mc.free_teams_history) != 0).sum()/len(mc.free_teams_history))
                queue_history_local.append(np.mean(mc.queue_history))
            report[(flow_intensity, num_teams)]['idle_time'] = [np.quantile(mean_idle_times_local, 0.25),
                                                                np.mean(mean_idle_times_local),
                                                                np.quantile(mean_idle_times_local, 0.75)]
            report[(flow_intensity, num_teams)]['queue_time'] = [np.quantile(mean_queue_times_local, 0.25),
                                                                 np.mean(mean_queue_times_local),
                                                                 np.quantile(mean_queue_times_local, 0.75)]
            report[(flow_intensity, num_teams)]['al_1_team_free'] = [np.quantile(free_teams_history_local, 0.25),
                                                                     np.mean(free_teams_history_local),
                                                                     np.quantile(free_teams_history_local, 0.75)]
            report[(flow_intensity, num_teams)]['av_queue_size'] = [np.quantile(queue_history_local, 0.25),
                                                                    np.mean(queue_history_local),
                                                                    np.quantile(queue_history_local, 0.75)]
            report[(flow_intensity, num_teams)]['uncured_rate'] = 1-np.mean(num_cured_local)/np.mean(num_arrived_local)

        return report
