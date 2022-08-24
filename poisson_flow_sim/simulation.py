from abc import ABC, abstractmethod
from itertools import product
from collections import defaultdict
from typing import Union, Iterable, List, Optional
from multiprocessing import Pool

import numpy as np
import pandas as pd
from tqdm import tqdm

from poisson_flow_sim.base.patient import *
from poisson_flow_sim.base.evac_center import *
from poisson_flow_sim.base.data import *
from poisson_flow_sim.base.utils import get_quantiles_and_mean, softmax
from functools import partial


class Simulation(ABC):

    def __init__(self, time_horizon: int, flow_intensities: Union[List[int], List[float]], teams_amounts: List[int],
                 patients_cure_times: Union[List[int], int], verbosity: int = 0):
        self.time_horizon = time_horizon
        self.verbosity = verbosity
        self.report = {}
        self.pat_num = 0

        # Parameters
        self.flow_intensities = flow_intensities
        self.teams_amounts = teams_amounts
        if isinstance(patients_cure_times, int):
            self.patients_cure_times = [patients_cure_times]
        else:
            self.patients_cure_times = patients_cure_times

    @abstractmethod
    def step(self, **kwargs):
        pass

    @abstractmethod
    def single_sim_run(self, **kwargs):
        pass

    @abstractmethod
    def run(self, random_states: Union[List[int], None] = None):
        pass


class SimpleSimulation(Simulation):

    def __init__(self, time_horizon: int, flow_intensities: Union[List[int], List[float]], teams_amounts: List[int],
                 patients_cure_times: Union[List[int], int], verbosity: int = 0):
        super(SimpleSimulation, self).__init__(time_horizon, flow_intensities,
                                               teams_amounts, patients_cure_times, verbosity)
        self.params = (self.flow_intensities, self.teams_amounts, self.patients_cure_times)

    def single_sim_run(self, flow_intensity, mc, rs, patient_cure_time):
        np.random.seed(rs)
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        if self.verbosity > 0:
            time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        else:
            time_range = range(self.time_horizon)
        for t in time_range:
            self.step(t, mc, patients_flow[t], patient_cure_time)
        return patients_flow

    def step(self, cur_time, med_center, num_patients, pct):
        new_patients = []
        for i in range(num_patients):
            new_patients.append(CommonPatient(cur_time, f"Patient #{self.pat_num}", cure_time=pct))
            self.pat_num += 1
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(*self.params))
        report = defaultdict(dict)

        for param_setup in tqdm(params_combinations, desc='Combinations', position=0, leave=False):
            flow_intensity, num_teams, pct = param_setup
            local_report = defaultdict(list)

            for rs in tqdm(random_states, desc='Random states', position=1, leave=False):

                mc = SimpleEvacuationCenter(num_teams)
                patients_flow = self.single_sim_run(flow_intensity, mc, rs, pct)

                for mt in mc.free_teams + mc.busy_teams:
                    local_report['idle_time'].append(np.mean(mt.idle_time_list))

                queue_times_local_rs = []
                for patient in mc.patient_history:
                    queue_times_local_rs.append(patient.time_in_mc_queue)
                local_report['queue_time'].append(np.mean(queue_times_local_rs))

                local_report['num_cured'].append(len(mc.cured_patient_history))

                local_report['num_arrived'].append(np.sum(patients_flow))

                local_report['al_1_team_free'].append(
                    (np.array(mc.free_teams_history) != 0).sum() / len(mc.free_teams_history)
                )

                local_report['av_queue_size'].append(np.mean(mc.queue_history))

            for stat in ['idle_time', 'queue_time', 'al_1_team_free', 'av_queue_size']:
                report[param_setup][stat] = get_quantiles_and_mean(local_report[stat])

            report[param_setup]['uncured_rate'] = 1 - np.mean(local_report['num_cured']) / np.mean(
                local_report['num_arrived'])

        return report


class StateSpecificSimulation(Simulation):

    def __init__(self, time_horizon: int, flow_intensities: Union[List[int], List[float]], teams_amounts: List[int],
                 quake_intensities: List[int], patients_cure_times: Union[List[int], int], verbosity: int = 0):
        super(StateSpecificSimulation, self).__init__(time_horizon, flow_intensities,
                                                      teams_amounts, patients_cure_times, verbosity)
        self.quake_intensities = quake_intensities
        self.params = (self.flow_intensities, self.teams_amounts, self.quake_intensities, self.patients_cure_times)

    def single_sim_run(self, flow_intensity, mc, rs, injury_distr, patient_cure_time):
        np.random.seed(rs)
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        # if self.verbosity > 0:
        #     time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        # else:
        time_range = range(self.time_horizon)
        for t in time_range:
            self.step(t, mc, patients_flow[t], patient_cure_time, injury_distr)
        return patients_flow

    def step(self, cur_time, med_center, num_patients, pct, injury_distr):
        new_patients = []
        for i in range(num_patients):
            state = np.random.choice(['light', 'moderate', 'grave'], p=injury_distr)
            new_patients.append(CommonPatient(cur_time, f"Patient #{self.pat_num}", pct, state=state))
            self.pat_num += 1
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def parallel_eval(self, rs, num_teams, flow_intensity, injury_distr, pct):
        queue_times_local_rs = []
        queue_times_local_rs_states = {'grave': [],
                                       'moderate': [],
                                       'light': []}

        mc = StateSpecificEvacuationCenter(num_teams)
        patients_flow = self.single_sim_run(flow_intensity, mc, rs, injury_distr, pct)

        idle_time = []
        for mt in mc.free_teams + mc.busy_teams:
            idle_time.append(np.mean(mt.idle_time_list))

        for patient in mc.patient_history:
            queue_times_local_rs.append(patient.time_in_mc_queue)
            queue_times_local_rs_states[patient.state].append(patient.time_in_mc_queue)

        queue_time = np.mean(queue_times_local_rs)
        queue_time_states = {'grave': [],
                             'moderate': [],
                             'light': []}

        for state, qtlrss in queue_times_local_rs_states.items():
            queue_time_states[state].append(np.mean(qtlrss))

        num_cured = len(mc.cured_patient_history)

        num_arrived = np.sum(patients_flow)

        al_1_team_free = (np.array(mc.free_teams_history) != 0).sum() / len(mc.free_teams_history)

        av_queue_size = np.mean(mc.queue_history)

        return idle_time, queue_time, queue_time_states, num_cured, num_arrived, al_1_team_free, av_queue_size


    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(*self.params))
        report = defaultdict(dict)

        for param_setup in tqdm(params_combinations,
                                desc='Combinations',
                                position=0,
                                leave=False):
            flow_intensity, num_teams, qi, pct = param_setup
            local_report = {}
            for stat in ['idle_time', 'queue_time', 'al_1_team_free', 'av_queue_size', 'num_cured', 'num_arrived']:
                local_report[stat] = []
            local_report['queue_time_states'] = {'grave': [],
                                                 'moderate': [],
                                                 'light': []}

            injury_distr = [injury_extents[qi]['light'],
                            injury_extents[qi]['moderate'],
                            injury_extents[qi]['grave']]

            par_eval = partial(self.parallel_eval, num_teams=num_teams, flow_intensity=flow_intensity,
                               injury_distr=injury_distr, pct=pct)

            with Pool(8) as p:
                results = list(tqdm(p.imap(par_eval, random_states), desc='Random states',
                                    position=1, leave=False, total=len(random_states)))

            for stats in results:

                idle_time, queue_time, queue_time_states, num_cured, num_arrived, al_1_team_free, av_queue_size = stats

                local_report['idle_time'].extend(idle_time)

                local_report['queue_time'].append(queue_time)

                for state, qts in queue_time_states.items():
                    local_report['queue_time_states'][state].append(qts)

                local_report['num_cured'].append(num_cured)

                local_report['num_arrived'].append(num_arrived)

                local_report['al_1_team_free'].append(al_1_team_free)

                local_report['av_queue_size'].append(av_queue_size)

            for stat in ['idle_time', 'queue_time', 'al_1_team_free', 'av_queue_size']:
                report[param_setup][stat] = get_quantiles_and_mean(local_report[stat])

            report[param_setup]['uncured_rate'] = 1 - np.mean(local_report['num_cured']) / np.mean(
                local_report['num_arrived'])

            for state, means in local_report['queue_time_states'].items():
                report[param_setup][state] = get_quantiles_and_mean(means)

        return report


class InjurySpecificSimulation(StateSpecificSimulation):

    def __init__(self, time_horizon: int, flow_intensities: Union[List[int], List[float]], teams_amounts: List[int],
                 quake_intensities: List[int], patients_cure_times: Union[List[int], int],
                 injury_distr_num: Optional[List[int]] = None, verbosity: int = 0):
        super(InjurySpecificSimulation, self).__init__(time_horizon, flow_intensities, teams_amounts,
                                                       quake_intensities, patients_cure_times, verbosity)
        self.pat_num = {'thoracoabdominal': 0,
                        'trauma': 0,
                        'neuro': 0,
                        'all': 0}
        if injury_distr_num is None:
            self.injury_distr_num = list(range(10))
        else:
            self.injury_distr_num = injury_distr_num

        self.teams_distr = pd.DataFrame(special_teams_distr_new)

        self.params = (self.flow_intensities, self.teams_amounts, self.quake_intensities,
                       self.patients_cure_times, self.injury_distr_num)

    def single_sim_run(self, flow_intensity, mc, rs, injury_distr, localization_distr, patient_cure_time):
        np.random.seed(rs)
        patients_flow = np.random.poisson(flow_intensity, self.time_horizon)
        # if self.verbosity > 0:
        #     time_range = tqdm(range(self.time_horizon), desc='Simulation step (min)', position=2, leave=False)
        # else:
        time_range = range(self.time_horizon)
        for t in time_range:
            self.step(t, mc, patients_flow[t], patient_cure_time, localization_distr, injury_distr)
        return patients_flow

    def step(self, cur_time, med_center, num_patients, pat_cure_time, localization_distr, injury_distr=None):
        new_patients = []
        for i in range(num_patients):
            state = np.random.choice(['light', 'moderate', 'grave'], p=injury_distr)
            injury = np.random.choice(['thoracoabdominal', 'trauma', 'neuro'],
                                      p=localization_distr)
            new_patients.append(InjurySpecificPatient(cur_time,
                                                      f"{injury.title()} {state} patient #{self.pat_num[injury]}",
                                                      injury, pat_cure_time, state=state))
            self.pat_num[injury] += 1
        med_center.receive_patients(new_patients)
        med_center.check_teams(cur_time)

    def parallel_eval(self, rs, num_teams, flow_intensity, injury_distr, pct, idi):
        queue_times_local_rs = []
        queue_times_local_rs_states = {'grave': [],
                                       'moderate': [],
                                       'light': []}
        teams = self.teams_distr.iloc[idi*8:idi*8+8].query(f'nt == {num_teams}')

        nt = [1, 1, 1]
        r_nt = num_teams - 3
        for ii in range(r_nt):
            jj = np.random.choice([0, 1, 2], p=[0.1, 0.23, 0.67])
            nt[jj] += 1


        # mc = InjurySpecificEvacuationCenter({'thoracoabdominal': teams['z_nt'].values[0],
        #                                      'trauma': teams['x_nt'].values[0],
        #                                      'neuro': teams['y_nt'].values[0]})
        mc = InjurySpecificEvacuationCenter({'thoracoabdominal': nt[0],
                                             'trauma': nt[1],
                                             'neuro': nt[2]})

        patients_flow = self.single_sim_run(flow_intensity, mc, rs, injury_distr, teams[['z', 'x', 'y']].values[0], pct)
        #patients_flow = self.single_sim_run(flow_intensity, mc, rs, injury_distr, np.array([0.333, 0.3333, 0.3334]), pct)

        idle_time = []
        for mt in mc.teams:
            idle_time.append(np.mean(mt.idle_time_list))

        for patient in mc.all_patient_history:
            queue_times_local_rs.append(patient.time_in_mc_queue)
            queue_times_local_rs_states[patient.state].append(patient.time_in_mc_queue)
        queue_time = np.mean(queue_times_local_rs)

        queue_time_states = {'grave': [],
                             'moderate': [],
                             'light': []}

        for state, qtlrss in queue_times_local_rs_states.items():
            queue_time_states[state].append(np.mean(qtlrss))

        num_cured = sum([len(v) for v in mc.cured_patient_history.values()])

        num_arrived = np.sum(patients_flow)

        free_teams_history = np.sum(np.array([np.array(fth) for fth in mc.free_teams_history.values()]), axis=0)
        al_1_team_free = (free_teams_history != 0).sum() / len(free_teams_history)

        q_h = []
        for sp_q_h in mc.queue_history.values():
            q_h.extend(sp_q_h)
        av_queue_size = np.mean(q_h)

        return idle_time, queue_time, queue_time_states, num_cured, num_arrived, al_1_team_free, av_queue_size

    def run(self, random_states=None):
        if random_states is None:
            random_states = [0]
        params_combinations = list(product(*self.params))
        report = defaultdict(dict)

        for param_setup in tqdm(params_combinations,
                                desc='Combinations',
                                position=0,
                                leave=False):
            flow_intensity, num_teams, qi, pct, idn = param_setup
            local_report = {}
            for stat in ['idle_time', 'queue_time', 'al_1_team_free', 'av_queue_size', 'num_cured', 'num_arrived']:
                local_report[stat] = []
            local_report['queue_time_states'] = {'grave': [],
                                                 'moderate': [],
                                                 'light': []}

            injury_distr = [injury_extents[qi]['light'],
                            injury_extents[qi]['moderate'],
                            injury_extents[qi]['grave']]

            par_eval = partial(self.parallel_eval, num_teams=num_teams, flow_intensity=flow_intensity,
                               injury_distr=injury_distr, pct=pct, idi=idn)

            with Pool(8) as p:
                results = list(tqdm(p.imap(par_eval, random_states), desc='Random states',
                                    position=1, leave=False, total=len(random_states)))

            for stats in results:

                idle_time, queue_time, queue_time_states, num_cured, num_arrived, al_1_team_free, av_queue_size = stats

                local_report['idle_time'].extend(idle_time)

                local_report['queue_time'].append(queue_time)

                for state, qts in queue_time_states.items():
                    local_report['queue_time_states'][state].append(qts)

                local_report['num_cured'].append(num_cured)

                local_report['num_arrived'].append(num_arrived)

                local_report['al_1_team_free'].append(al_1_team_free)

                local_report['av_queue_size'].append(av_queue_size)

            for stat in ['idle_time', 'queue_time', 'al_1_team_free', 'av_queue_size']:
                report[param_setup][stat] = get_quantiles_and_mean(local_report[stat])

            report[param_setup]['uncured_rate'] = 1 - np.mean(local_report['num_cured']) / np.mean(
                local_report['num_arrived'])

            for state, means in local_report['queue_time_states'].items():
                report[param_setup][state] = get_quantiles_and_mean(means)


        return report
