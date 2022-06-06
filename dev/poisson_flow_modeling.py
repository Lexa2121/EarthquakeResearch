from dev.base.med_center import SpecialistsCenter
from dev.base.patient import Patient

from dev.data.eathquake_data import *
from dev.data.estimated_params import mean_flow_intensities

from itertools import product
import tqdm

import numpy as np
import matplotlib.pyplot as plt

overall_sum = 0
illnesses_list = []
illnesses_fracs = []
illnesses_op_times = []
illnesses_specialists = []
for global_illness_type, subtypes in ILLNESS_DATA_ENHANCED.items():
    for subtype, subtype_info in subtypes.items():
        for level, level_data in subtype_info.items():
            overall_sum += level_data['amount']
            illnesses_list.append(f'{global_illness_type}{subtype}_{level}')
            illnesses_fracs.append(level_data['amount'])
            illnesses_op_times.append(level_data['op_time'])
            illnesses_specialists.append(level_data['specialists'])
illnesses_fracs = np.array(illnesses_fracs) / overall_sum
probas_uniform_grid = np.cumsum(illnesses_fracs)


def model(num_recievers, amb_capacity, ambs_per_1000, op_specialists, max_steps=1000):
    #pbar = tqdm.tqdm(position=1, leave=False)
    queue_list = []
    poisson_lambda = mean_flow_intensities[(num_recievers, amb_capacity, ambs_per_1000)]
    flow = np.random.poisson(poisson_lambda, max_steps)

    mc = SpecialistsCenter(op_specialists)

    patient_number = 0
    t = 0
    while True:
        if t < max_steps:
            n_patients = flow[t]
            # Generating patients
            patients = []
            for p in range(n_patients):
                u_rand_value = np.random.uniform()
                for i, i_proba in enumerate(probas_uniform_grid):
                    if u_rand_value <= i_proba:
                        illness = illnesses_list[i]
                        if illness.startswith('S1') or illness.startswith('S6'):
                            patient = Patient(illness, name=f'Patient_{patient_number}')
                            patient.queue_in_mc_start_time = t
                            patients.append(patient)
                            patient_number += 1
                            break
            if len(patients) == 0:
                mc.check_queue(t)
                #print(len(mc.op_teams))
                #pbar.update()
                t += 1
                continue
            mc.add_patients(patients)

        # Manipulating medcenter
        mc.check_queue(t)
        # if mc.team['Surgeon']['specialists'][0].is_busy:
        #     print('hey')
        #pbar.update()
        t += 1
        if t % 2000 == 0:
            print('Patients left:', mc.patients_in_mc)
        queue_list.append(len(mc.queue))
        if t >= max_steps and mc.patients_in_mc == 0:
            break
    return poisson_lambda, flow, mc, queue_list


team_combinations = {'Surgeon': [1, 2, 3],
                     'Neurological surgeon': [1, 2, 3],
                     'Anesthesiologist': [2, 4, 6],
                     'Senior scrub nurse': [1, 2, 3],
                     'Scrub nurse': [3, 6, 9],
                     'Anesthesiologist nurse': [4, 8, 12],
                     'Junior nurse': [1, 2, 3]}

num_receivers_list = [2, 4]
amb_capacity_list = [2, 3]
ambs_per_1000_list = [0.02, 0.1]

team_combinations = {'Surgeon': [2],
                     'Neurological surgeon': [1],
                     'Anesthesiologist': [2],
                     'Senior scrub nurse': [1],
                     'Scrub nurse': [3],
                     'Anesthesiologist nurse': [4],
                     'Junior nurse': [1]}

team_combinations_list = [team_combinations['Surgeon'],
                          team_combinations['Neurological surgeon'],
                          team_combinations['Anesthesiologist'],
                          team_combinations['Senior scrub nurse'],
                          team_combinations['Scrub nurse'],
                          team_combinations['Anesthesiologist nurse'],
                          team_combinations['Junior nurse']]

num_receivers_list = [2]
amb_capacity_list = [2]
ambs_per_1000_list = [0.1]

combinations_list = [num_receivers_list, amb_capacity_list, ambs_per_1000_list] + team_combinations_list
sim_results = {}

combinations = list(product(*combinations_list))

print('Modeling begins ...')

comb_bar = tqdm.tqdm(combinations, position=0, desc='Combinations', leave=False)
for num_r, amb_cap, ap1000, s, ns, a, ssn, sn, an, jn in comb_bar:
    team = {'Surgeon': s,
            'Neurological surgeon': ns,
            'Anesthesiologist': a,
            'Senior scrub nurse': ssn,
            'Scrub nurse': sn,
            'Anesthesiologist nurse': an,
            'Junior nurse': jn}
    poisson_lambda, flow, mc, queue_list = model(num_r, amb_cap, ap1000, team)

plt.plot(queue_list)
plt.show()
print(mc.team['Surgeon']['specialists'][0].name)
print(mc.team['Surgeon']['specialists'][0].idle_time_list)
print(mc.team['Surgeon']['specialists'][1].name)
print(mc.team['Surgeon']['specialists'][1].idle_time_list)

