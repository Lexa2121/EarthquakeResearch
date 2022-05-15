from ambulance import Ambulance
from med_center import MedCenter
from patient import Patient

from eathquake_data import *

from itertools import product
import tqdm
from collections import defaultdict

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

illnesses = list(ILLNESS_DATA.keys())
probas = [ILLNESS_DATA[i]['frac'] for i in illnesses]


def model(num_recievers, amb_capacity, med_teams, ambs_per_1000, ill_probas=None, max_steps=200_000):
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

    total_injuries = {}
    for k, v in CITY_DATA.items():
        total_injuries[k] = v['injured']

    mc = MedCenter(num_recievers, med_teams)
    for i in mc.med_teams:
        mt_queue_history[i] = []
    while True:
        if t == max_steps:
            break
        for amb in ambs:
            if amb not in mc.queue + mc.serving_ambulances:  # скорая не в приемнике и не в очереди
                if total_injuries[amb.town] == 0 and amb.from_mc:  # скорая едет из приемника и все жертвы вывезены
                    ambs.pop(ambs.index(amb))  # снимаем с линии
                else:  # скорая едет из приемника и жертвы остались или едет в приемник
                    amb.ride(1)
                    # if not amb.from_mc:
                    #     for patient in amb.patients_onboard:
                    #         patient.delivering_time += 1
                    if amb.time_in_road == amb.time_to_road:  # скорая доехала ...
                        if amb.from_mc:  # ... в НП
                            patients = []
                            pat_num = CITY_DATA[amb.town]['population'] - total_injuries[amb.town] + len(patients)
                            victims_left = min(amb.capacity, total_injuries[amb.town])
                            for pat in range(victims_left):
                                p = np.random.uniform()
                                if p < ill_probas[0]:
                                    illness = illnesses[0]
                                elif p < ill_probas[0]+ill_probas[1]:
                                    illness = illnesses[1]
                                else:
                                    illness = illnesses[2]
                                patient = Patient(illness, amb.town, f'Patient_{pat_num}')
                                patient.delivering_start_time = t
                                patients.append(patient)
                            amb.load(patients)  # загружаем скорую
                        else:  # ... в ЭП
                            amb.time_in_road = 0
                            # print(f"{amb} arrived to med center at {t}")
                            for pat in amb.patients_onboard:
                                pat.delivering_end_time = t
                            mc.queue.append(amb)
        freed_ambs = mc.check_receivers(t)
        queue_history.append(len(mc.queue))
        for i in mc.med_teams:
            mt_queue_history[i].append(len(mc.med_teams[i]['queue']))
        t += 1
    return queue_history, mt_queue_history, mc.patient_history


# num_receivers_list = [2, 4, 6]
# amb_capacity_list = [2, 3, 4, 5]
#
# trauma_mt_amount_list = [3, 4]
# thorac_mt_amount_list = [1, 2]
# neuro_mt_amount_list = [1, 2]
#
# ambs_per_1000 = [0.01, 0.02, 0.1]

num_receivers_list = [4]
amb_capacity_list = [3]

trauma_mt_amount_list = [20, 25, 30, 35]
thorac_mt_amount_list = [3, 4, 5]
neuro_mt_amount_list = [3, 4]

ambs_per_1000 = [0.01]

sim_results = defaultdict(list)

combinations = list(product(num_receivers_list, amb_capacity_list, ambs_per_1000,
                            trauma_mt_amount_list, thorac_mt_amount_list, neuro_mt_amount_list))

waiting_types = ['delivery', 'time_in_amb_queue', 'time_in_mc_queue', 'surgery']
print('Modeling begins ...')
t_overall = {}
for num_r, amb_cap, ap1000, tra, tha, nea in tqdm.tqdm(combinations):
    mt_data = {'травматологический': tra,
               'торакоабдоминальный': tha,
               'нейрохирургичекий': nea}
    results = model(num_r, amb_cap, mt_data, ap1000)
    sim_results[(num_r, amb_cap, ap1000, tra, tha, nea)].extend(results[:-1])
    long_pats_dict = defaultdict(dict)
    town = []
    name = []
    delivering_start_time = []
    delivering_end_time = []
    queue_in_mc_start_time = []
    surgery_start_time = []
    surgery_end_time = []
    for i, pat in enumerate(results[-1]):
        waiting_times = [pat.delivering_end_time - pat.delivering_start_time,
                         pat.queue_in_mc_start_time - pat.delivering_end_time,
                         pat.surgery_start_time - pat.queue_in_mc_start_time,
                         pat.surgery_end_time - pat.surgery_start_time]
        for j in range(4):
            long_pats_dict['town'][j+i*4] = pat.town
            long_pats_dict['name'][j+i*4] = f'{pat.name}_from_{pat.town}'
            long_pats_dict['waiting_type'][j+i*4] = waiting_types[j]
            long_pats_dict['waiting_time'][j+i*4] = waiting_times[j]
    sim_results[(num_r, amb_cap, ap1000, tra, tha, nea)].append(pd.DataFrame(long_pats_dict))


print('Averaging random results over independent runs ... ')
for num_r, amb_cap, ap1000 in tqdm.tqdm(list(product(num_receivers_list, amb_capacity_list, ambs_per_1000))):
    same_runs = {}
    same_runs['травматологический'] = defaultdict(list)
    same_runs['торакоабдоминальный'] = defaultdict(list)
    same_runs['нейрохирургичекий'] = defaultdict(list)

    for tra, tha, nea in product(trauma_mt_amount_list, thorac_mt_amount_list, neuro_mt_amount_list):
        sr = sim_results[(num_r, amb_cap, ap1000, tra, tha, nea)]
        same_runs['травматологический'][tra].append(sr[-2]['травматологический'])
        same_runs['торакоабдоминальный'][tha].append(sr[-2]['торакоабдоминальный'])
        same_runs['нейрохирургичекий'][nea].append(sr[-2]['нейрохирургичекий'])

    for tra, tha, nea in product(trauma_mt_amount_list, thorac_mt_amount_list, neuro_mt_amount_list):
        sim_results[(num_r, amb_cap,
                     ap1000, tra,
                     tha, nea)][-2]['травматологический'] = np.mean(pad_sequences(same_runs['травматологический'][tra],
                                                                                  padding='post'), axis=0)
        sim_results[(num_r, amb_cap,
                     ap1000, tra,
                     tha, nea)][-2]['торакоабдоминальный'] = np.mean(pad_sequences(same_runs['торакоабдоминальный'][tha],
                                                                                   padding='post'), axis=0)
        sim_results[(num_r, amb_cap,
                     ap1000, tra,
                     tha, nea)][-2]['нейрохирургичекий'] = np.mean(pad_sequences(same_runs['нейрохирургичекий'][nea],
                                                                                  padding='post'), axis=0)

print('Modeling has been finished')

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Статистики симуляции'),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3"),
    html.P("Количество мест в приемнике для машин:"),
    dcc.Slider(id="nr",
               value=num_receivers_list[0],
               step=None,
               marks={k: str(k) for k in num_receivers_list}),
    html.P("Количество машин на 1000 населения (мин 1 машина):"),
    dcc.Slider(id="ap1000",
               value=ambs_per_1000[0],
               step=None,
               marks={k: str(k) for k in ambs_per_1000}),
    html.P("Количество мест в машинах:"),
    dcc.Slider(id="ac",
               value=amb_capacity_list[0],
               step=None,
               marks={k: str(k) for k in amb_capacity_list}),
    html.P("Количество травматологических бригад:"),
    dcc.Slider(id="tra",
               value=trauma_mt_amount_list[0],
               step=None,
               marks={k: str(k) for k in trauma_mt_amount_list}),
    html.P("Количество торакоабдоминальных бригад:"),
    dcc.Slider(id="tha",
               value=thorac_mt_amount_list[0],
               step=None,
               marks={k: str(k) for k in thorac_mt_amount_list}),
    html.P("Количество нейрохирургических:"),
    dcc.Slider(id="nea",
               value=neuro_mt_amount_list[0],
               step=None,
               marks={k: str(k) for k in neuro_mt_amount_list}),
])

@app.callback(
    Output("graph", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Input("nr", "value"),
    Input("ap1000", "value"),
    Input("ac", "value"),
    Input("tra", "value"),
    Input("tha", "value"),
    Input("nea", "value"))
def display_color(nr, ap1000, ac, tra, tha, nea):
    data, medt_data, pats_data = sim_results[(nr, ac, ap1000, tra, tha, nea)]
    data = np.array(data)
    data = data[data != 0]
    counts, bins = np.histogram(data, bins=range(0, 30, 1))

    fig = make_subplots(rows=3, cols=2,
                        column_widths=[0.6, 0.4],
                        row_heights=[0.333, 0.333, 0.333],
                        shared_xaxes='columns',
                        shared_yaxes='rows',
                        specs=[[{"type": "histogram", "rowspan": 3}, {"type": "scatter"}],
                               [                               None, {"type": "scatter"}],
                               [                               None, {"type": "scatter"}]],
                        column_titles=('Распределение очереди из скорых перед эвакоприемником',
                                       'Динамика очереди к бригадам'))

    fig.add_trace(
        go.Bar(x=bins, y=counts, marker=dict(color="crimson"), showlegend=False),
        row=1, col=1
    )
    fig.add_trace(go.Scatter(x=np.arange(len(medt_data['травматологический'])),
                             y=medt_data['травматологический'],
                             mode='lines',
                             name='травматологический'),
                  row=1, col=2
                  )
    fig.add_trace(go.Scatter(x=np.arange(len(medt_data['торакоабдоминальный'])),
                             y=medt_data['торакоабдоминальный'],
                             mode='lines',
                             name='торакоабдоминальный'),
                  row=2, col=2)
    fig.add_trace(go.Scatter(x=np.arange(len(medt_data['нейрохирургичекий'])),
                             y=medt_data['нейрохирургичекий'],
                             mode='lines',
                             name='нейрохирургичекий'),
                  row=3, col=2)

    # Update xaxis properties
    fig.update_xaxes(title_text="Длина очереди", row=1, col=1)
    fig.update_xaxes(title_text="Время симуляции (мин)", row=3, col=2)

    # Update yaxis properties
    fig.update_yaxes(title_text="Количество событий", row=1, col=1)
    fig.update_yaxes(title_text="Размер очереди", row=2, col=2)

    # fig2 = go.Figure()
    # fig2.add_trace(go.Heatmap(z=amb_t_data))

    fig2 = make_subplots(rows=1, cols=4,
                         specs=[[{"type": "box"}, {"type": "box"}, {"type": "box"}, {"type": "box"}]],
                         column_titles=('delivery', 'time_in_amb_queue', 'time_in_mc_queue', 'surgery'))
    fig2.add_trace(
        go.Box(y=pats_data[pats_data["waiting_type"] == 'delivery']["waiting_time"]),
        row=1, col=1
    )
    fig2.add_trace(
        go.Box(y=pats_data[pats_data["waiting_type"] == 'time_in_amb_queue']["waiting_time"]),
        row=1, col=2
    )
    fig2.add_trace(
        go.Box(y=pats_data[pats_data["waiting_type"] == 'time_in_mc_queue']["waiting_time"]),
        row=1, col=3
    )
    fig2.add_trace(
        go.Box(y=pats_data[pats_data["waiting_type"] == 'surgery']["waiting_time"]),
        row=1, col=4
    )
    fig3 = px.bar(pats_data, x="name", y="waiting_time", color="waiting_type", title="Waiting times per patient")
    return fig, fig2, fig3


app.run_server(debug=False)
