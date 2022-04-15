import pandas as pd

from ambulance import Ambulance
from med_center import MedCenter
from patient import Patient

from eathquake_data import *

from itertools import product
import tqdm

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

illnesses = list(ILLNESS_DATA.keys())
probas = [ILLNESS_DATA[i]['frac'] for i in illnesses]


def model(num_recievers, amb_capacity, med_teams, ill_probas=None):
    if ill_probas is None:
        ill_probas = [0.67, 0.1, 0.23]
    ambs = []
    # TODO: варьировать количество машин на 1000 (мин 1 машина)
    for k, v in CITY_DATA.items():
        for i in range(1, v['population'] // 10000 + 2):
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
    all_ambs_free = False
    all_teams_free = False
    while True:
        # if not t%50000 and t:
        #     print(f'Прошло {t} мин')
        if len(ambs) == 0 and not all_ambs_free:
            t_amb_max = t
            all_ambs_free = True
        if all_ambs_free:
            for k, v in mc.med_teams.items():
                for team in v['teams']:
                    if team.is_busy:
                        break
                else:
                    all_teams_free = True
                break
            if all_teams_free:
                break
        for amb in ambs:
            if amb not in mc.queue + mc.serving_ambulances:  # скорая не в приемнике и не в очереди
                if total_injuries[amb.town] == 0 and amb.from_mc:  # скорая едет из приемника и все жертвы вывезены
                    ambs.pop(ambs.index(amb))  # снимаем с линии
                else:  # скорая едет из приемника и жертвы остались или едет в приемник
                    amb.ride(1)
                    if amb.time_in_road == amb.time_to_road:  # скорая доехала ...
                        if amb.from_mc:  # ... в НП
                            rand_illnesses = np.random.choice(illnesses,
                                                              min(amb.capacity, total_injuries[amb.town]),
                                                              p=ill_probas)  # случайно выбираем больных
                            amb.load([Patient(illness) for illness in rand_illnesses])  # загружаем скорую
                            total_injuries[amb.town] -= len(amb.patients_onboard)
                        else:  # ... в ЭП
                            amb.time_in_road = 0
                            # print(f"{amb} arrived to med center at {t}")
                            mc.queue.append(amb)
        freed_ambs = mc.check_receivers(t)

        queue_history.append(len(mc.queue))
        for i in mc.med_teams:
            mt_queue_history[i].append(len(mc.med_teams[i]['queue']))
        t += 1
    return t_amb_max, queue_history, t, mt_queue_history


num_receivers_list = [2, 3, 4, 5]
amb_capacity_list = [2, 3, 4]

trauma_mt_amount_list = [2, 3, 4]
thorac_mt_amount_list = [1, 2, 3]
neuro_mt_amount_list = [1, 2, 3]

sim_results = {}

for num_r, amb_cap, tra, tha, nea in tqdm.tqdm(product(num_receivers_list, amb_capacity_list, trauma_mt_amount_list,
                                                       thorac_mt_amount_list, neuro_mt_amount_list)):
    mt_data = {'травматологический': tra,
               'торакоабдоминальный': tha,
               'нейрохирургичекий': nea}
    sim_results[(num_r, amb_cap, tra, tha, nea)] = model(num_r, amb_cap, mt_data)

# TODO: усреднить по прогонам
# TODO: посмотреть распределение времени в дороге/в очереди в эвакоприемник/в очереди к врачу/у врача для каждого пациента (см. картинку в тг)
# TODO: boxplot для времени в дороге/в очереди в эвакоприемник/в очереди к врачу/у врача для пациентов
# TODO: heatmap
# data = pd.DataFrame()
# data['num_receivers'], data['amb_capacity'] = [x for x, y in product(num_receivers_list, amb_capacity_list)], \
#                                               [y for x, y in product(num_receivers_list, amb_capacity_list)]
# data['t_overall'] = [v[2] for _, v in sim_results.items()]
# amb_t_data = data.pivot('num_receivers', 'amb_capacity', 't_overall').values

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Размер очереди'),
    dcc.Graph(id="graph"),
    html.P("Количество мест в приемнике для машин:"),
    dcc.Slider(id="nr",
               min=num_receivers_list[0],
               max=num_receivers_list[-1],
               value=num_receivers_list[0], step=1,
               marks={num_receivers_list[0]: str(num_receivers_list[0]),
                      num_receivers_list[-1]: str(num_receivers_list[-1])}),
    html.P("Количество мест в машинах:"),
    dcc.Slider(id="ac",
               min=amb_capacity_list[0],
               max=amb_capacity_list[-1],
               value=amb_capacity_list[0], step=1,
               marks={amb_capacity_list[-1]: str(amb_capacity_list[-1]),
                      amb_capacity_list[-1]: str(amb_capacity_list[-1])}),
    html.P("Количество травматологических бригад:"),
    dcc.Slider(id="tra",
               min=trauma_mt_amount_list[0],
               max=trauma_mt_amount_list[-1],
               value=trauma_mt_amount_list[0], step=1,
               marks={trauma_mt_amount_list[-1]: str(trauma_mt_amount_list[-1]),
                      trauma_mt_amount_list[-1]: str(trauma_mt_amount_list[-1])}),
    html.P("Количество торакоабдоминальных бригад:"),
    dcc.Slider(id="tha",
               min=thorac_mt_amount_list[0],
               max=thorac_mt_amount_list[-1],
               value=thorac_mt_amount_list[0], step=1,
               marks={thorac_mt_amount_list[-1]: str(thorac_mt_amount_list[-1]),
                      thorac_mt_amount_list[-1]: str(thorac_mt_amount_list[-1])}),
    html.P("Количество нейрохирургических:"),
    dcc.Slider(id="nea",
               min=neuro_mt_amount_list[0],
               max=neuro_mt_amount_list[-1],
               value=neuro_mt_amount_list[0], step=1,
               marks={neuro_mt_amount_list[-1]: str(neuro_mt_amount_list[-1]),
                      neuro_mt_amount_list[-1]: str(neuro_mt_amount_list[-1])}),
])

y_num = 650000

@app.callback(
    Output("graph", "figure"),
    Input("nr", "value"),
    Input("ac", "value"),
    Input("tra", "value"),
    Input("tha", "value"),
    Input("nea", "value"))
def display_color(nr, ac, tra, tha, nea):
    data, mt_data = np.array(sim_results[(nr, ac, tra, tha, nea)][1]), sim_results[(nr, ac, tra, tha, nea)][-1]
    data = data[data != 0]
    counts, bins = np.histogram(data, bins=range(0, 30, 1))

    fig = make_subplots(
        rows=3, cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.333, 0.333, 0.333],
        specs=[[{"type": "histogram", "rowspan": 3}, {"type": "scatter"}],
               [None, {"type": "scatter"}],
               [None, {"type": "scatter"}]])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    fig.add_trace(
        go.Bar(x=bins, y=counts, marker=dict(color="crimson"), showlegend=False),
        row=1, col=1
    )
    fig.add_trace(go.Scatter(x=np.arange(len(mt_data['травматологический'])),
                             y=mt_data['травматологический'],
                             mode='lines',
                             name='травматологический'),
                  row=1, col=2
                  )
    fig.add_trace(go.Scatter(x=np.arange(len(mt_data['торакоабдоминальный'])),
                             y=mt_data['торакоабдоминальный'],
                             mode='lines',
                             name='торакоабдоминальный'),
                  row=2, col=2)
    fig.add_trace(go.Scatter(x=np.arange(len(mt_data['нейрохирургичекий'])),
                             y=mt_data['нейрохирургичекий'],
                             mode='lines',
                             name='нейрохирургичекий'),
                  row=3, col=2)
    # fig.add_trace(go.Heatmap(z=amb_t_data),
    #               row=1, col=2)
    return fig


app.run_server(debug=False)
