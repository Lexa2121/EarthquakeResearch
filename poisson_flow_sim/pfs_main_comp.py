from collections import defaultdict
from poisson_flow_sim.simulation import *
import numpy as np
from poisson_flow_sim.base.utils import softmax
import json

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#daily_intensities = np.concatenate((np.arange(30, 100, 10), np.arange(100, 350, 50)))
daily_intensities = np.array([150])
pct = [30, 25, 20]
default_qi = 8

parameters_setup = {'random_states': list(range(30)),
                    'simulation_args': {'flow_intensities': list(np.round(daily_intensities / (24 * 60), 5)),
                                        'teams_amounts': list(range(3, 11)),
                                        'quake_intensities': [default_qi],
                                        'patients_cure_time': pct}}

STEPS = 100000
u_pct = 30

sims = dict()
# sims['universal'] = StateSpecificSimulation(time_horizon=STEPS,
#                                             flow_intensities=parameters_setup['simulation_args']['flow_intensities'],
#                                             teams_amounts=parameters_setup['simulation_args']['teams_amounts'],
#                                             quake_intensities=parameters_setup['simulation_args']['quake_intensities'],
#                                             patients_cure_times=u_pct,
#                                             verbosity=1)

sims['special'] = InjurySpecificSimulation(time_horizon=STEPS,
                                           flow_intensities=parameters_setup['simulation_args']['flow_intensities'],
                                           teams_amounts=parameters_setup['simulation_args']['teams_amounts'],
                                           quake_intensities=parameters_setup['simulation_args']['quake_intensities'],
                                           patients_cure_times=parameters_setup['simulation_args']['patients_cure_time'],
                                           injury_distr_num=[1],
                                           verbosity=1)


def write_stats(stats_dict, key, value):
    stats_dict[key]['lower_idle_bounds'].append(value['idle_time'][0])
    stats_dict[key]['mean_idle'].append(value['idle_time'][1])
    stats_dict[key]['upper_idle_bounds'].append(value['idle_time'][2])

    stats_dict[key]['lower_queue_bounds'].append(value['queue_time'][0])
    stats_dict[key]['mean_queue'].append(value['queue_time'][1])
    stats_dict[key]['upper_queue_bounds'].append(value['queue_time'][2])

    stats_dict[key]['uncured_rate'].append(value['uncured_rate'])

    stats_dict[key]['lower_al_1_team_free_bounds'].append(value['al_1_team_free'][0])
    stats_dict[key]['mean_al_1_team_free'].append(value['al_1_team_free'][1])
    stats_dict[key]['upper_al_1_team_free_bounds'].append(value['al_1_team_free'][2])

    stats_dict[key]['lower_av_queue_size_bounds'].append(value['av_queue_size'][0])
    stats_dict[key]['mean_av_queue_size'].append(value['av_queue_size'][1])
    stats_dict[key]['upper_av_queue_size_bounds'].append(value['av_queue_size'][2])

    stats_dict[key]['lower_light_queue_bounds'].append(value['light'][0])
    stats_dict[key]['mean_light_queue'].append(value['light'][1])
    stats_dict[key]['upper_light_queue_bounds'].append(value['light'][2])

    stats_dict[key]['lower_moderate_queue_bounds'].append(value['moderate'][0])
    stats_dict[key]['mean_moderate_queue'].append(value['moderate'][1])
    stats_dict[key]['upper_moderate_queue_bounds'].append(value['moderate'][2])

    stats_dict[key]['lower_grave_queue_bounds'].append(value['grave'][0])
    stats_dict[key]['mean_grave_queue'].append(value['grave'][1])
    stats_dict[key]['upper_grave_queue_bounds'].append(value['grave'][2])

    return stats_dict


if __name__ == '__main__':

    #intensities_data = {}
    for sim_type, sim in sims.items():
        sims_report = sim.run(parameters_setup['random_states'])
        #intensities_data[sim_type] = {}
        to_json = {}
        # with open(f'json_data/{sim_type}/intensities_data.json', 'r') as f:
        #     to_json = json.load(f)
        for params, v in sims_report.items():
            if sim_type == 'special':
                _flow, _nt, _qi, _pct, _smt = params
                changeable_params = str((_flow, _qi, _pct, _smt))
            else:
                _flow, _nt, _qi, _pct = params
                changeable_params = str((_flow, _qi, _pct))

            if changeable_params not in to_json:
                to_json[changeable_params] = defaultdict(list)

            to_json[changeable_params]['num_teams'].append(_nt)
            to_json = write_stats(to_json, changeable_params, v)

        with open(f'json_data/{sim_type}/intensities_data_1_uniform150. json', 'w') as f:
            json.dump(to_json, f)


    # app = Dash(__name__)
    #
    # app.layout = html.Div([
    #     html.H4('Диаграмма преимущества'),
    #     dcc.Dropdown(
    #         ['Среднее время простоя одной бригады', 'Средняя длина очереди',
    #          'Среднее время полного обслуживания (очередь+манипуляции)'],
    #         'Средняя длина очереди',
    #         id='data_type'
    #     ),
    #     html.P("Разница между универсальными и узкопрофильными бригадами:"),
    #     dcc.Graph(id="graph"),
    #     html.P("Интенсивность входного потока (чел/сутки):"),
    #     dcc.Slider(id="fi",
    #                value=parameters_setup['simulation_args']['flow_intensities'][0],
    #                step=None,
    #                marks={k: daily_intensities[i] for i, k in
    #                       enumerate(parameters_setup['simulation_args']['flow_intensities'])}),
    #     html.P("Сглаживание распределения по профилю повреждений:"),
    #     dcc.Slider(id="smt",
    #                value=parameters_setup['simulation_args']['sm_temperatures'][0],
    #                step=None,
    #                marks={str(k): sm_temperatures[i] for i, k in
    #                       enumerate(parameters_setup['simulation_args']['sm_temperatures'])})#,
    #     # html.P("Интенсивность землетрясения (влияет на распределение по степени тяжести):"),
    #     # dcc.Slider(id="qi",
    #     #            value=parameters_setup['simulation_args']['quake_intensities'][0],
    #     #            step=None,
    #     #            marks={str(i): i for i in parameters_setup['simulation_args']['quake_intensities']})
    # ])
    #
    #
    # @app.callback(
    #     Output("graph", "figure"),
    #     Input("data_type", "value"),
    #     Input("fi", "value"),
    #     Input("smt", "value"))
    #     #Input("qi", "value"))
    # def display_color(data_type, fi, smt):
    #
    #     if data_type == 'Среднее время простоя одной бригады':
    #         stat_key = 'mean_idle'
    #         m = 2
    #     elif data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
    #         stat_key = 'mean_queue'
    #         m = 2
    #     else:
    #         stat_key = 'mean_av_queue_size'
    #         m = 1
    #
    #     z = []
    #     uc_z = []
    #     x_names = [f'{(u_pct - c)*2} мин' for c in parameters_setup['simulation_args']['patients_cure_time']]
    #     y_names = [str(x) for x in intensities_data['universal'][(fi, default_qi, u_pct)]['num_teams']]
    #     for i, nt in enumerate(intensities_data['universal'][(fi, default_qi, u_pct)]['num_teams']):
    #         row = []
    #         uc_u = intensities_data['universal'][(fi, default_qi, u_pct)]['uncured_rate'][i]
    #         u_qs = intensities_data['universal'][(fi, default_qi, u_pct)][stat_key][i]
    #         if data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
    #             u_qs += u_pct
    #         for k, pct in enumerate(parameters_setup['simulation_args']['patients_cure_time']):
    #             j = intensities_data['special'][(fi, default_qi, pct, smt)]['num_teams'].index(nt)
    #             uc_s = intensities_data['universal'][(fi, default_qi, u_pct)]['uncured_rate'][j]
    #             s_qs = intensities_data['special'][(fi, default_qi, pct, smt)][stat_key][j]
    #             if (uc_u > 0.15) and (uc_s > 0.15):
    #                 uc_z.append((i, k))
    #             if data_type == 'Среднее время полного обслуживания (очередь+манипуляции)':
    #                 s_qs += pct
    #             row.append((u_qs-s_qs)*m)
    #         z.append(row)
    #     z = np.array(z)
    #     qr_z = np.power(np.abs(z), 1 / 3) * np.sign(z)
    #     qr_z = qr_z.tolist()
    #     for uc_coords in uc_z:
    #         qr_z[uc_coords[0]][uc_coords[1]] = None
    #
    #     fig = go.Figure(data=go.Heatmap(z=qr_z,
    #                                     x=x_names,
    #                                     y=y_names,
    #                                     text=np.round(z, 2).tolist(),
    #                                     texttemplate="%{text}",
    #                                     textfont={"size": 10}))
    #
    #     fig.update_xaxes(title_text="Преимущество специализированных бригад")
    #     fig.update_yaxes(title_text="Количество бригад")
    #     return fig
    #
    #
    # app.run_server(debug=False)
