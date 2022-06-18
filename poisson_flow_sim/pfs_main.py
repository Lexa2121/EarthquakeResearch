from collections import defaultdict

from poisson_flow_sim.simulation import *
from poisson_flow_sim.base.theoretical_utils import MultiServerSystem
import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

parameters_setup = {'random_states': list(range(3)),
                    'simulation_args': {'flow_intensities': list(np.round(np.arange(150, 250, 50) / (24 * 6), 5)),
                                        'teams_amounts': list(range(8, 11)),
                                        'quake_intensities': list(range(11, 13))}}

state_specific = True
injury_specific = True

# usim = SimpleSimulation(time_horizon=10000,
#                         flow_intensities=parameters_setup['simulation_args']['flow_intensities'],
#                         teams_amounts=parameters_setup['simulation_args']['teams_amounts'],
#                         evac_center_type='state_specific',
#                         verbosity=1,
#                         quake_intensities=parameters_setup['simulation_args']['quake_intensities'])

sim = InjurySpecificSimulation(time_horizon=10000,
                               flow_intensities=parameters_setup['simulation_args']['flow_intensities'],
                               teams_amounts=parameters_setup['simulation_args']['teams_amounts'],
                               verbosity=1,
                               quake_intensities=parameters_setup['simulation_args']['quake_intensities'])


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

    sim_report = sim.run(parameters_setup['random_states'])
    #usim_report = usim.run(parameters_setup['random_states'])

    intensities_data = {}
    #u_intensities_data = {}

    for k, v in sim_report.items():
        _flow = k[0]
        _nt = k[1]
        mss = MultiServerSystem(_nt, _flow, 3)
        # nt_th = k[1]
        # nt_tr = k[2]
        # nt_ne = k[3]
        _qi = k[2]

        if (_flow, _qi) not in intensities_data:
            intensities_data[(_flow, _qi)] = defaultdict(list)
            intensities_data[(_flow, _qi)]['minimum_teams'] = mss.rho

        intensities_data[(_flow, _qi)]['num_teams'].append(_nt)
        intensities_data[(_flow, _qi)]['theoretical_av_queue_size'].append(mss.average_queue_size)
        intensities_data[(_flow, _qi)]['theoretical_al_1_team_free'].append(1 - mss.get_state_proba(_nt))
        intensities_data = write_stats(intensities_data, (_flow, _qi), v)

        # if (_flow, _qi) not in u_intensities_data:
        #     u_intensities_data[(_flow, _qi)] = defaultdict(list)
        #     u_intensities_data[(_flow, _qi)]['minimum_teams'] = mss.rho
        #
        # u_intensities_data[(_flow, _qi)]['num_teams'].append(_nt)
        # u_intensities_data[(_flow, _qi)]['theoretical_av_queue_size'].append(mss.average_queue_size)
        # u_intensities_data[(_flow, _qi)]['theoretical_al_1_team_free'].append(1 - mss.get_state_proba(_nt))
        # u_intensities_data = write_stats(u_intensities_data, (_flow, _qi), usim_report[(_flow, _nt, _qi)])

    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Статистики симуляции'),
        html.P("Статистики"),
        dcc.Graph(id="graph2"),
        html.P("Время в очереди vs Время простоя бригады"),
        dcc.Graph(id="graph"),
        # html.P("Доля пациентов, над которыми не успели провести манипуляции vs Количество бригад"),
        # dcc.Graph(id="graph3"),
        # html.P("Время в очереди для пациентов с различной степенью тяжести повреждений"),
        # dcc.Graph(id="graph3"),
        html.P("Интенсивность входного потока (чел/сутки):"),
        dcc.Slider(id="fi",
                   value=parameters_setup['simulation_args']['flow_intensities'][0],
                   step=None,
                   marks={k: np.arange(150, 350, 50)[i] for i, k in
                          enumerate(parameters_setup['simulation_args']['flow_intensities'])}),
        html.P("Интенсивность землетрясения (влияет на распределение по степени тяжести):"),
        dcc.Slider(id="qi",
                   value=parameters_setup['simulation_args']['quake_intensities'][0],
                   step=None,
                   marks={str(i): i for i in parameters_setup['simulation_args']['quake_intensities']})
    ])


    @app.callback(
        Output("graph2", "figure"),
        Output("graph", "figure"),
        #Output("graph3", "figure"),
        Input("fi", "value"),
        Input("qi", "value"))
    def display_color(fi, qi):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=intensities_data[(fi, qi)]['mean_idle'], y=intensities_data[(fi, qi)]['mean_queue'],
            mode='lines+markers',
            name='Узкопрофильные бригады',
            error_x=dict(
                array=np.array(intensities_data[(fi, qi)]['upper_idle_bounds']),
                arrayminus=np.array(intensities_data[(fi, qi)]['lower_idle_bounds']),
                type='data',
                color='#0000f5',
                thickness=1.1,
                width=2,
            ),
            error_y=dict(
                array=np.array(intensities_data[(fi, qi)]['upper_queue_bounds']),
                arrayminus=np.array(intensities_data[(fi, qi)]['lower_queue_bounds']),
                type='data',
                color='#0000f5',
                thickness=1.1,
                width=2,
            ),
            text=[f'Количество бригад: {nt}' for nt in intensities_data[(fi, qi)]['num_teams']],
            line=dict(color='#0000f5'),
            marker=dict(color=intensities_data[(fi, qi)]['num_teams'],
                        colorbar=dict(
                            title="Количество бригад"
                        ),
                        colorscale="Turbo",
                        size=8)

        ))

        # fig.add_trace(go.Scatter(
        #     x=u_intensities_data[(fi, qi)]['mean_idle'], y=u_intensities_data[(fi, qi)]['mean_queue'],
        #     mode='lines+markers',
        #     name='Универсальные бригады',
        #     error_x=dict(
        #         array=np.array(u_intensities_data[(fi, qi)]['upper_idle_bounds']),
        #         arrayminus=np.array(u_intensities_data[(fi, qi)]['lower_idle_bounds']),
        #         type='data',
        #         color='#ffa500',
        #         thickness=1.1,
        #         width=2,
        #     ),
        #     error_y=dict(
        #         array=np.array(u_intensities_data[(fi, qi)]['upper_queue_bounds']),
        #         arrayminus=np.array(u_intensities_data[(fi, qi)]['lower_queue_bounds']),
        #         type='data',
        #         color='#ffa500',
        #         thickness=1.1,
        #         width=2,
        #     ),
        #     text=[f'Количество бригад: {nt}' for nt in u_intensities_data[(fi, qi)]['num_teams']],
        #     line=dict(color='#ffa500'),
        #     marker=dict(color=u_intensities_data[(fi, qi)]['num_teams'],
        #                 colorbar=dict(
        #                     title="Количество бригад"
        #                 ),
        #                 colorscale="Turbo",
        #                 size=8)
        #
        # ))

        fig.update_xaxes(title_text="Среднее время простоя бригады")
        fig.update_yaxes(title_text="Среднее время ожидания пациента в очереди")
        fig.update_layout(legend=dict(
            orientation="h"
        ))

        fig2 = make_subplots(rows=2, cols=1,
                             row_heights=[0.5, 0.5],
                             shared_xaxes='columns',
                             specs=[[{"type": "scatter"}],
                                    [{"type": "scatter"}]])

        fig2.add_trace(go.Scatter(
            x=intensities_data[(fi, qi)]['num_teams'], y=intensities_data[(fi, qi)]['mean_av_queue_size'],
            mode='lines+markers',
            name='Узкопрофильные бригады',
            error_y=dict(
                array=np.array(intensities_data[(fi, qi)]['upper_av_queue_size_bounds']),
                arrayminus=np.array(intensities_data[(fi, qi)]['lower_av_queue_size_bounds']),
                type='data',
                color='#0000f5',
                thickness=1.1,
                width=2,
            ),
            line=dict(color='#0000f5')), row=1, col=1)

        # fig2.add_trace(go.Scatter(
        #     x=u_intensities_data[(fi, qi)]['num_teams'], y=u_intensities_data[(fi, qi)]['mean_av_queue_size'],
        #     mode='lines+markers',
        #     name='Универсальные бригады',
        #     error_y=dict(
        #         array=np.array(u_intensities_data[(fi, qi)]['upper_av_queue_size_bounds']),
        #         arrayminus=np.array(u_intensities_data[(fi, qi)]['lower_av_queue_size_bounds']),
        #         type='data',
        #         color='#ffa500',
        #         thickness=1.1,
        #         width=2,
        #     ),
        #     line=dict(color='#ffa500')), row=1, col=1)

        fig2.add_trace(go.Scatter(
            x=intensities_data[(fi, qi)]['num_teams'], y=intensities_data[(fi, qi)]['theoretical_av_queue_size'],
            mode='lines+markers',
            name='Теоретические значения',
            line=dict(color='#009900')), row=1, col=1)

        # fig2.update_xaxes(title_text="Количество бригад")
        fig2.update_yaxes(title_text="Средний размер очереди", row=1, col=1)

        fig2.add_shape(type="line",
                       x0=intensities_data[(fi, qi)]['minimum_teams'], x1=intensities_data[(fi, qi)]['minimum_teams'],
                       line=dict(color="#cc0018", width=3),
                       yref="paper",
                       y0=0,
                       y1=1,
                       name='Предельное теоретическое минимальное количество бригад')

        fig2.add_trace(go.Scatter(
            x=intensities_data[(fi, qi)]['num_teams'], y=intensities_data[(fi, qi)]['mean_al_1_team_free'],
            mode='lines+markers',
            name='Узкопрофильные бригады',
            error_y=dict(
                array=np.array(intensities_data[(fi, qi)]['upper_al_1_team_free_bounds']),
                arrayminus=np.array(intensities_data[(fi, qi)]['lower_al_1_team_free_bounds']),
                type='data',
                color='#0000f5',
                thickness=1.1,
                width=2,
            ),
            line=dict(color='#0000f5'),
            showlegend=False), row=2, col=1)

        # fig2.add_trace(go.Scatter(
        #     x=u_intensities_data[(fi, qi)]['num_teams'], y=u_intensities_data[(fi, qi)]['mean_al_1_team_free'],
        #     mode='lines+markers',
        #     name='Универсальные бригады',
        #     error_y=dict(
        #         array=np.array(u_intensities_data[(fi, qi)]['upper_al_1_team_free_bounds']),
        #         arrayminus=np.array(u_intensities_data[(fi, qi)]['lower_al_1_team_free_bounds']),
        #         type='data',
        #         color='#ffa500',
        #         thickness=1.1,
        #         width=2,
        #     ),
        #     line=dict(color='#ffa500'),
        #     showlegend=False), row=2, col=1)

        fig2.add_trace(go.Scatter(
            x=intensities_data[(fi, qi)]['num_teams'], y=intensities_data[(fi, qi)]['theoretical_al_1_team_free'],
            mode='lines+markers',
            name='Теоретические значения',
            line=dict(color='#009900'), showlegend=False), row=2, col=1)

        fig2.update_xaxes(title_text="Количество бригад", row=2, col=1)
        fig2.update_yaxes(title_text="Доля отрезков с простоем как минимум одной бригады", row=2, col=1)
        fig2.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=parameters_setup['simulation_args']['teams_amounts']
            ),
            height=800
        )

        # fig3 = go.Figure()
        # fig3.add_trace(go.Bar(name='Доля пациентов, над которыми не успели провести манипуляции',
        #                       x=intensities_data[(fi, qi)]['num_teams'],
        #                       y=intensities_data[(fi, qi)]['uncured_rate']))
        #
        # fig3 = go.Figure()
        # fig3.add_trace(go.Bar(
        #     x=intensities_data[(fi, qi)]['num_teams'],
        #     y=intensities_data[(fi, qi)]['mean_light_queue'],
        #     name='Light',
        #     error_y=dict(
        #         array=np.array(intensities_data[(fi, qi)]['upper_light_queue_bounds']),
        #         arrayminus=np.array(intensities_data[(fi, qi)]['lower_light_queue_bounds']),
        #         type='data',
        #         color='black',
        #         thickness=1,
        #         width=2,
        #     )
        # ))
        # fig3.add_trace(go.Bar(
        #     x=intensities_data[(fi, qi)]['num_teams'],
        #     y=intensities_data[(fi, qi)]['mean_moderate_queue'],
        #     name='Moderate',
        #     error_y=dict(
        #         array=np.array(intensities_data[(fi, qi)]['upper_moderate_queue_bounds']),
        #         arrayminus=np.array(intensities_data[(fi, qi)]['lower_moderate_queue_bounds']),
        #         type='data',
        #         color='black',
        #         thickness=1,
        #         width=2,
        #     )
        # ))
        # fig3.add_trace(go.Bar(
        #     x=intensities_data[(fi, qi)]['num_teams'],
        #     y=intensities_data[(fi, qi)]['mean_grave_queue'],
        #     name='Grave',
        #     error_y=dict(
        #         array=np.array(intensities_data[(fi, qi)]['upper_grave_queue_bounds']),
        #         arrayminus=np.array(intensities_data[(fi, qi)]['lower_grave_queue_bounds']),
        #         type='data',
        #         color='black',
        #         thickness=1,
        #         width=2,
        #     )
        # ))
        #
        # # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        # fig3.update_layout(barmode='group')

        return fig2, fig#, fig3


    app.run_server(debug=False)
