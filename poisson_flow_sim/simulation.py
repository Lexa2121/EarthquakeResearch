from itertools import product
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from poisson_flow_sim.base.patient import *
from poisson_flow_sim.base.evac_center import *
from poisson_flow_sim.base.data import *


class SimpleSimulation:

    def __init__(self, time_horizon: int = 4320,
                 flow_intensities=None,
                 teams_amounts=None,
                 time_step: int = 1,
                 evac_center_type: str = 'simple',
                 verbosity=0,
                 quake_intensities=None):
        if flow_intensities is None:
            self.flow_intensities = [4]
        else:
            self.flow_intensities = flow_intensities
        if teams_amounts is None:
            self.teams_amounts = [270]
        else:
            self.teams_amounts = teams_amounts
        if quake_intensities is None:
            self.quake_intensities = list(range(5, 13))
        else:
            self.quake_intensities = quake_intensities
        self.verbosity = verbosity
        self.time_horizon = time_horizon // time_step
        self.evac_center_type = evac_center_type
        self.report = {}
        self.pat_num = 0

    def set_params_from_dict(self, **kwargs):
        for param, param_value in kwargs:
            self.__setattr__(param, param_value)

    def single_sim_run(self, flow_intensity, num_teams, rs, qi):
        np.random.seed(rs)
        if self.evac_center_type == 'simple':
            mc = SimpleEvacuationCenter(num_teams)
            injury_distr = None
        elif self.evac_center_type == 'state_specific':
            mc = StateSpecificEvacuationCenter(num_teams)
            injury_distr = [injury_extents[qi]['light'],
                            injury_extents[qi]['moderate'],
                            injury_extents[qi]['grave']]
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        if self.verbosity > 0:
            time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        else:
            time_range = range(self.time_horizon)
        for t in time_range:
            self.step(t, mc, patients_flow[t], injury_distr)
        return patients_flow, mc

    def step(self, cur_time, med_center, num_patients, injury_distr=None):
        new_patients = []
        for i in range(num_patients):
            if self.evac_center_type == 'state_specific':
                state = np.random.choice(['light', 'moderate', 'grave'], p=injury_distr)
            else:
                state = 'light'
            new_patients.append(CommonPatient(cur_time, f"Patient #{self.pat_num}", 3, state=state))
            self.pat_num += 1
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(self.flow_intensities, self.teams_amounts, self.quake_intensities))
        report = defaultdict(dict)

        for flow_intensity, num_teams, qi in tqdm(params_combinations, desc='Combinations', position=0, leave=False):
            mean_idle_times_local = []
            mean_queue_times_local = []
            if self.evac_center_type == 'state_specific':
                mean_queue_times_states_local = {'grave': [],
                                                 'moderate': [],
                                                 'light': []}
            num_cured_local = []
            num_arrived_local = []
            queue_history_local = []
            free_teams_history_local = []
            for rs in tqdm(random_states, desc='Random states', position=1, leave=False):
                queue_times_local_rs = []
                if self.evac_center_type == 'state_specific':
                    queue_times_local_rs_states = {'grave': [],
                                                   'moderate': [],
                                                   'light': []}
                patients_flow, mc = self.single_sim_run(flow_intensity, num_teams, rs, qi)

                for mt in mc.free_teams + mc.busy_teams:
                    mean_idle_times_local.append(np.mean(mt.idle_time_list))

                for patient in mc.patient_history:
                    queue_times_local_rs.append(patient.time_in_mc_queue)
                    if self.evac_center_type == 'state_specific':
                        queue_times_local_rs_states[patient.state].append(patient.time_in_mc_queue)
                mean_queue_times_local.append(np.mean(queue_times_local_rs))
                if self.evac_center_type == 'state_specific':
                    for state, qtlrss in queue_times_local_rs_states.items():
                        mean_queue_times_states_local[state].append(np.mean(qtlrss))

                num_cured_local.append(len(mc.cured_patient_history))
                num_arrived_local.append(np.sum(patients_flow))
                free_teams_history_local.append(
                    (np.array(mc.free_teams_history) != 0).sum() / len(mc.free_teams_history))
                queue_history_local.append(np.mean(mc.queue_history))
            report[(flow_intensity, num_teams, qi)]['idle_time'] = [np.quantile(mean_idle_times_local, 0.25),
                                                                    np.mean(mean_idle_times_local),
                                                                    np.quantile(mean_idle_times_local, 0.75)]
            report[(flow_intensity, num_teams, qi)]['queue_time'] = [np.quantile(mean_queue_times_local, 0.25),
                                                                     np.mean(mean_queue_times_local),
                                                                     np.quantile(mean_queue_times_local, 0.75)]
            report[(flow_intensity, num_teams, qi)]['al_1_team_free'] = [np.quantile(free_teams_history_local, 0.25),
                                                                         np.mean(free_teams_history_local),
                                                                         np.quantile(free_teams_history_local, 0.75)]
            report[(flow_intensity, num_teams, qi)]['av_queue_size'] = [np.quantile(queue_history_local, 0.25),
                                                                        np.mean(queue_history_local),
                                                                        np.quantile(queue_history_local, 0.75)]
            report[(flow_intensity, num_teams, qi)]['uncured_rate'] = 1 - np.mean(num_cured_local) / np.mean(
                num_arrived_local)

            if self.evac_center_type == 'state_specific':
                for state, means in mean_queue_times_states_local.items():
                    report[(flow_intensity, num_teams, qi)][state] = [np.quantile(means, 0.25),
                                                                      np.mean(means),
                                                                      np.quantile(means, 0.75)]

        return report


class InjurySpecificSimulation:

    def __init__(self, time_horizon: int = 4320,
                 flow_intensities=None,
                 teams_amounts=None,
                 time_step: int = 1,
                 verbosity=0,
                 quake_intensities=None):
        if flow_intensities is None:
            self.flow_intensities = [4]
        else:
            self.flow_intensities = flow_intensities
        if teams_amounts is None:
            self.teams_amounts = 4
        else:
            self.teams_amounts = teams_amounts
        if quake_intensities is None:
            self.quake_intensities = list(range(5, 13))
        else:
            self.quake_intensities = quake_intensities
        self.verbosity = verbosity
        self.time_horizon = time_horizon // time_step
        self.report = {}
        self.pat_num = {'thoracoabdominal': 0,
                        'trauma': 0,
                        'neuro': 0,
                        'all': 0}

    def set_params_from_dict(self, **kwargs):
        for param, param_value in kwargs:
            self.__setattr__(param, param_value)

    def single_sim_run(self, flow_intensity, nt, rs, qi):
        np.random.seed(rs)
        mc = InjurySpecificEvacuationCenter(special_teams_distr[nt])
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        injury_distr = [injury_extents[qi]['light'],
                        injury_extents[qi]['moderate'],
                        injury_extents[qi]['grave']]
        if self.verbosity > 0:
            time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        else:
            time_range = range(self.time_horizon)
        for t in time_range:
            self.step(t, mc, patients_flow[t], injury_distr)
        return patients_flow, mc

    def step(self, cur_time, med_center, num_patients, injury_distr=None):
        new_patients = []
        for i in range(num_patients):
            state = np.random.choice(['light', 'moderate', 'grave'], p=injury_distr)
            injury = np.random.choice(['thoracoabdominal', 'trauma', 'neuro'], p=[0.67, 0.1, 0.23])
            new_patients.append(InjurySpecificPatient(cur_time,
                                                      f"{injury.title()} {state} patient #{self.pat_num[injury]}",
                                                      injury, 2, state=state))
            self.pat_num[injury] += 1
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(self.flow_intensities,
                                           self.teams_amounts,
                                           self.quake_intensities))
        report = defaultdict(dict)

        for flow_intensity, nt, qi in tqdm(params_combinations,
                                           desc='Combinations',
                                           position=0,
                                           leave=False):
            mean_idle_times_local = []
            mean_queue_times_local = []
            mean_queue_times_states_local = {'grave': [],
                                             'moderate': [],
                                             'light': []}
            num_cured_local = []
            num_arrived_local = []
            queue_history_local = []
            free_teams_history_local = []
            for rs in tqdm(random_states, desc='Random states', position=1, leave=False):
                queue_times_local_rs = []
                queue_times_local_rs_states = {'grave': [],
                                               'moderate': [],
                                               'light': []}
                patients_flow, mc = self.single_sim_run(flow_intensity, nt, rs, qi)

                for mt in mc.teams:
                    mean_idle_times_local.append(np.mean(mt.idle_time_list))

                for patient in mc.all_patient_history:
                    queue_times_local_rs.append(patient.time_in_mc_queue)
                    queue_times_local_rs_states[patient.state].append(patient.time_in_mc_queue)
                mean_queue_times_local.append(np.mean(queue_times_local_rs))
                for state, qtlrss in queue_times_local_rs_states.items():  # TODO: закончил здесь
                    mean_queue_times_states_local[state].append(np.mean(qtlrss))

                num_cured_local.append(sum([len(v) for v in mc.cured_patient_history.values()]))
                num_arrived_local.append(np.sum(patients_flow))
                free_teams_history = np.sum(np.array([np.array(fth) for fth in mc.free_teams_history.values()]), axis=0)
                free_teams_history_local.append(
                    (free_teams_history != 0).sum() / len(free_teams_history))
                q_h = []
                for sp_q_h in mc.queue_history.values():
                    q_h.extend(sp_q_h)
                queue_history_local.append(np.mean(q_h))
            report[(flow_intensity, nt, qi)]['idle_time'] = [np.quantile(mean_idle_times_local, 0.25),
                                                             np.mean(mean_idle_times_local),
                                                             np.quantile(mean_idle_times_local, 0.75)]
            report[(flow_intensity, nt, qi)]['queue_time'] = [np.quantile(mean_queue_times_local,
                                                                          0.25),
                                                              np.mean(mean_queue_times_local),
                                                              np.quantile(mean_queue_times_local,
                                                                          0.75)]
            report[(flow_intensity, nt, qi)]['al_1_team_free'] = [np.quantile(free_teams_history_local,
                                                                              0.25),
                                                                  np.mean(free_teams_history_local),
                                                                  np.quantile(free_teams_history_local,
                                                                              0.75)]
            report[(flow_intensity, nt, qi)]['av_queue_size'] = [np.quantile(queue_history_local,
                                                                             0.25),
                                                                 np.mean(queue_history_local),
                                                                 np.quantile(queue_history_local,
                                                                             0.75)]
            report[(flow_intensity, nt, qi)]['uncured_rate'] = 1 - np.mean(num_cured_local) / np.mean(
                num_arrived_local)

            for state, means in mean_queue_times_states_local.items():
                report[(flow_intensity, nt, qi)][state] = [np.quantile(means, 0.25),
                                                           np.mean(means),
                                                           np.quantile(means, 0.75)]

        return report
