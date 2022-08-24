import json
import os

import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

daily_intensities = np.concatenate((np.arange(30, 100, 10), np.arange(100, 350, 50)))
sm_temperatures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#sm_temperatures = np.arange(1, 3)
default_qi = 8

parameters_setup = {'random_states': list(range(30)),
                    'simulation_args': {'flow_intensities': list(np.round(daily_intensities / (24 * 60), 5)),
                                        'teams_amounts': list(range(3, 11)),
                                        'quake_intensities': [default_qi],
                                        'patients_cure_time': [30 - i for i in range(11)],
                                        'sm_temperatures': sm_temperatures}}

STEPS = 100000
u_pct = 30

intensities_data = {}

with open(os.path.join('json_data', 'universal', 'intensities_data.json'), 'r') as f:
    data  = json.load(f)
    intensities_data['universal'] = {}
    for k, v in data.items():
        intensities_data['universal'][eval(k)] = v

with open(os.path.join('json_data', 'special', 'intensities_data_full.json'), 'r') as f:
    data  = json.load(f)
    intensities_data['special'] = {}
    for k, v in data.items():
        intensities_data['special'][eval(k)] = v

injuries_fraction = {'0.1': {'0.23': '0.67',
                             '0.1': '0.8',
                             '0.2': '0.7',
                             '0.3': '0.6',
                             '0.4': '0.5'},
                     '0.2': {'0.2': '0.6',
                             '0.3': '0.5',
                             '0.4': '0.4'},
                     '0.3': {'0.3': '0.4'},
                     '1/3': {'1/3': '1/3'}}

frac_to_ind = {('0.1', '0.23', '0.67'): 0,
               ('1/3', '1/3', '1/3'): 1,
               ('0.1', '0.1', '0.8'): 2,
               ('0.1', '0.2', '0.7'): 3,
               ('0.1', '0.3', '0.6'): 4,
               ('0.1', '0.4', '0.5'): 5,
               ('0.2', '0.2', '0.6'): 6,
               ('0.2', '0.3', '0.5'): 7,
               ('0.2', '0.4', '0.4'): 8,
               ('0.3', '0.3', '0.4'): 9}

app = Dash(__name__)

app.layout = html.Div([
    html.H3('Диаграмма преимущества'),
    dcc.Dropdown(
        ['Среднее время простоя одной бригады', 'Средняя длина очереди',
         'Среднее время полного обслуживания (очередь+манипуляции)'],
        'Средняя длина очереди',
        id='data_type'
    ),
    html.P("Разница между универсальными и узкопрофильными бригадами:"),
    html.P("Формула в ячейке: показатель универсальных - показатель узкопрофильных"),
    dcc.Graph(id="graph"),
    html.Hr(),
    html.H4("Интенсивность входного потока (чел/сутки):"),
    dcc.Slider(id="fi",
               value=parameters_setup['simulation_args']['flow_intensities'][0],
               step=None,
               marks={k: daily_intensities[i] for i, k in
                      enumerate(parameters_setup['simulation_args']['flow_intensities'])}),
    html.Hr(),
    html.H4("Распределение пациентов по профилям повреждений."),
    html.P("Допускается, что есть три основных профиля повреждений. Ниже можно выбрать доли для каждого из трех профилей. "
           "Сначала необходимо выбрать долю наименее распространенного профиля, затем второго по частоте. "
           "Доля третьего профиля вычисляется автоматически. Также можно задать распределение, "
           "соответствующее эмпирическому: 0.1 : 0.23 : 0.67 и равномерному: 1/3 : 1/3 : 1/3."),
    html.Div([
        html.P('The least frequent:'),
        dcc.Dropdown(
            list(injuries_fraction.keys()),
            value = '0.1',
            id='x'
        )
    ], style={'width': '33%', 'display': 'inline-block'}),

    html.Div([
        html.P('The second least frequent:'),
        dcc.Dropdown(
            id='y'
        )
    ], style={'width': '33%', 'display': 'inline-block'}),

    #html.Div(id='z', style={'width': '33%', 'display': 'inline-block'})

    html.Div([
        html.P('The most frequent:'),
        dcc.Dropdown(
            id='z'
        )
    ], style={'width': '33%', 'display': 'inline-block'})
       ])
    # html.P("Сглаживание распределения по профилю повреждений:"),
    # dcc.Slider(id="smt",
    #            value=parameters_setup['simulation_args']['sm_temperatures'][0],
    #            step=None,
    #            marks={str(k): sm_temperatures[i] for i, k in
    #                   enumerate(parameters_setup['simulation_args']['sm_temperatures'])})#,
    # html.P("Интенсивность землетрясения (влияет на распределение по степени тяжести):"),
    # dcc.Slider(id="qi",
    #            value=parameters_setup['simulation_args']['quake_intensities'][0],
    #            step=None,
    #            marks={str(i): i for i in parameters_setup['simulation_args']['quake_intensities']})
#])

@app.callback(
    Output('y', 'options'),
    Input('x', 'value'))
def set_y_options(x):
    return sorted(list(injuries_fraction[x].keys()))


@app.callback(
    Output('y', 'value'),
    Input('y', 'options'))
def set_y_value(yy):
    return yy[0]

@app.callback(
    Output('z', 'value'),
    Input('z', 'options'))
def set_z_value(zz):
    return zz[0]

@app.callback(
    Output('z', 'options'),
    Input('x', 'value'),
    Input('y', 'value'))
def set_z_options(x, y):
    return [injuries_fraction[x][y]]


@app.callback(
    Output("graph", "figure"),
    Input("data_type", "value"),
    Input("fi", "value"),
    Input('x', 'value'),
    Input('y', 'value'),
    Input('z', 'value'))
def display_color(data_type, fi, x, y, z):

    #z = injuries_fraction[x][y]

    smt = frac_to_ind[(x, y, z)]

    if data_type == 'Среднее время простоя одной бригады':
        stat_key = 'mean_idle'
        m = 1
    elif data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
        stat_key = 'mean_queue'
        m = 1
    else:
        stat_key = 'mean_av_queue_size'
        m = 1
    u_z = []
    s_z = []
    z = []
    uc_z = []
    x_names = [f'{(u_pct - c)*1} min' for c in parameters_setup['simulation_args']['patients_cure_time']]
    y_names = [str(x) for x in intensities_data['universal'][(fi, default_qi, u_pct)]['num_teams']]
    for i, nt in enumerate(intensities_data['universal'][(fi, default_qi, u_pct)]['num_teams']):
        row = []
        u_row = []
        s_row = []
        uc_u = intensities_data['universal'][(fi, default_qi, u_pct)]['uncured_rate'][i]
        u_qs = intensities_data['universal'][(fi, default_qi, u_pct)][stat_key][i]
        if data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
            u_qs += u_pct
        for k, pct in enumerate(parameters_setup['simulation_args']['patients_cure_time']):
            j = intensities_data['special'][(fi, default_qi, pct, smt)]['num_teams'].index(nt)
            uc_s = intensities_data['universal'][(fi, default_qi, u_pct)]['uncured_rate'][j]
            s_qs = intensities_data['special'][(fi, default_qi, pct, smt)][stat_key][j]
            if (uc_u > 0.91) and (uc_s > 0.91):
                uc_z.append((i, k))
            if data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
                s_qs += pct
            u_row.append(u_qs*m)
            s_row.append(s_qs*m)
            row.append((u_qs-s_qs)*m)
        z.append(row)
        u_z.append(u_row)
        s_z.append(s_row)
    z = np.array(z)
    qr_z = np.power(np.abs(z), 1 / 3) * np.sign(z)
    qr_z = qr_z.tolist()
    for uc_coords in uc_z:
        qr_z[uc_coords[0]][uc_coords[1]] = None

    z_text = []
    for i, (u_r, s_r) in enumerate(zip(u_z, s_z)):
        z_text_row = []
        for j, (u_elem, s_elem) in enumerate(zip(u_r, s_r)):
            z_text_row.append(f'Разница:\n{round(u_elem, 2)} - {round(s_elem, 2)} = {np.round(z, 2)[i, j]}')
        z_text.append(z_text_row)

    fig = go.Figure(data=go.Heatmap(z=qr_z,
                                    x=x_names,
                                    y=y_names,
                                    text=np.round(z, 2),
                                    hovertext=z_text,
                                    texttemplate="%{text}",
                                    textfont={"size": 9}))

    fig.update_xaxes(title_text="Specialized teams advantage")
    fig.update_yaxes(title_text="Teams amount")
    return fig


app.run_server(debug=False)