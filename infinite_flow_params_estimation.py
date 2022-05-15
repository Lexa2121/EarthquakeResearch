from ambulance import Ambulance
from med_center import MedCenter
from patient import Patient

from eathquake_data import *

from itertools import product
import tqdm

import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt


illnesses = list(ILLNESS_DATA.keys())
probas = [ILLNESS_DATA[i]['frac'] for i in illnesses]


def model(num_recievers, amb_capacity, med_teams, ambs_per_1000, ill_probas=None, max_steps=200_000):
    pbar = tqdm.tqdm(total=max_steps, position=1, leave=False)
    if ill_probas is None:
        ill_probas = [0.67, 0.1, 0.23]
    ambs = []

    for k, v in CITY_DATA.items():
        num_cars = v['population'] * ambs_per_1000 / 1000
        num_cars = int(num_cars // 1 + (num_cars % 1 > 0)*1)
        for i in range(1, num_cars + 1):
            if k != 'Комсомольск-на-Амуре':
                ambs.append(
                    Ambulance(f'Бригада из {k} №{i}', k, v['distance_from_camp'], capacity=amb_capacity, speed=1.5))
            else:
                ambs.append(Ambulance(f'Бригада из {k} №{i}', k, v['distance_from_camp'], capacity=amb_capacity))

    t = 0
    queue_history = []
    mt_queue_history = {}

    patient_nums = {}
    for k in CITY_DATA:
        patient_nums[k] = 0

    mc = MedCenter(num_recievers, med_teams)
    for i in mc.med_teams:
        mt_queue_history[i] = []
    while True:
        if t == max_steps:
            break
        for amb in ambs:
            if amb not in mc.queue + mc.serving_ambulances:  # скорая не в приемнике и не в очереди
                amb.ride(1)
                if amb.time_in_road == amb.time_to_road:  # скорая доехала ...
                    if amb.from_mc:  # ... в НП
                        patients = []
                        for _ in range(amb.capacity):
                            p = np.random.uniform()
                            if p < ill_probas[0]:
                                illness = illnesses[0]
                            elif p < ill_probas[0]+ill_probas[1]:
                                illness = illnesses[1]
                            else:
                                illness = illnesses[2]
                            patient = Patient(illness, amb.town, f'Patient_{patient_nums[amb.town]}')
                            patient.delivering_start_time = t
                            patients.append(patient)
                            patient_nums[amb.town] += 1
                        amb.load(patients)  # загружаем скорую
                    else:  # ... в ЭП
                        amb.time_in_road = 0
                        for patient in amb.patients_onboard:
                            patient.delivering_end_time = t
                        mc.queue.append(amb)
        freed_ambs = mc.check_receivers(t)
        t += 1
        pbar.update()
    return mc.incoming_flow_history


mt_data = {'травматологический': 100,
           'торакоабдоминальный': 100,
           'нейрохирургичекий': 100}

num_receivers_list = [2, 4]
amb_capacity_list = [2, 3]
ambs_per_1000_list = [0.02, 0.1]

sim_results = {}

combinations = list(product(num_receivers_list, amb_capacity_list, ambs_per_1000_list))

print('Modeling begins ...')

comb_bar = tqdm.tqdm(combinations, position=0, desc='Combinations', leave=False)
for num_r, amb_cap, ap1000 in comb_bar:
    flow_history = model(num_r, amb_cap, mt_data, ap1000)
    m = np.mean(flow_history)
    sim_results[(num_r, amb_cap, ap1000)] = m
print(sim_results)
#{(2, 2, 0.02): 0.47544, (2, 2, 0.1): 1.99988, (2, 3, 0.02): 0.664395, (2, 3, 0.1): 1.99989, (4, 2, 0.02): 0.47552, (4, 2, 0.1): 2.14206, (4, 3, 0.02): 0.66447, (4, 3, 0.1): 2.97156}
