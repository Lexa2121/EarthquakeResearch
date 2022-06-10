from collections import defaultdict

from poisson_flow_sim.simulation import SimpleSimulation
from poisson_flow_sim.base.theoretical_utils import MultiServerSystem
import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

parameters_setup = {'random_states': list(range(30)),
                    'simulation_args': {'flow_intensities': list(np.round(np.arange(100, 300, 50) / (24 * 4), 5)),
                                        'teams_amounts': list(range(1, 8))}}

state_specific = True
injury_specific = True

if state_specific:
    if injury_specific:
        ec_type = ''

sim = SimpleSimulation(time_horizon=10000,
                       flow_intensities=parameters_setup['simulation_args']['flow_intensities'],
                       teams_amounts=parameters_setup['simulation_args']['teams_amounts'],
                       evac_center_type='state_specific',
                       verbosity=1)

if __name__ == '__main__':

    sim_report = sim.run(parameters_setup['random_states'])

    intensities_data = {}

    for k, v in sim_report.items():

        mss = MultiServerSystem(k[1], k[0], 2)
        if k[0] not in intensities_data:
            intensities_data[k[0]] = defaultdict(list)
            intensities_data[k[0]]['minimum_teams'] = mss.rho

        intensities_data[k[0]]['lower_idle_bounds'].append(v['idle_time'][0])
        intensities_data[k[0]]['mean_idle'].append(v['idle_time'][1])
        intensities_data[k[0]]['upper_idle_bounds'].append(v['idle_time'][2])

        intensities_data[k[0]]['lower_queue_bounds'].append(v['queue_time'][0])
        intensities_data[k[0]]['mean_queue'].append(v['queue_time'][1])
        intensities_data[k[0]]['upper_queue_bounds'].append(v['queue_time'][2])

        intensities_data[k[0]]['uncured_rate'].append(v['uncured_rate'])

        intensities_data[k[0]]['num_teams'].append(k[1])

        intensities_data[k[0]]['lower_al_1_team_free_bounds'].append(v['al_1_team_free'][0])
        intensities_data[k[0]]['mean_al_1_team_free'].append(v['al_1_team_free'][1])
        intensities_data[k[0]]['upper_al_1_team_free_bounds'].append(v['al_1_team_free'][2])

        intensities_data[k[0]]['lower_av_queue_size_bounds'].append(v['av_queue_size'][0])
        intensities_data[k[0]]['mean_av_queue_size'].append(v['av_queue_size'][1])
        intensities_data[k[0]]['upper_av_queue_size_bounds'].append(v['av_queue_size'][2])

        intensities_data[k[0]]['theoretical_av_queue_size'].append(mss.average_queue_size)
        intensities_data[k[0]]['theoretical_al_1_team_free'].append(1 - mss.get_state_proba(k[1]))

        intensities_data[k[0]]['lower_light_queue_bounds'].append(v['light'][0])
        intensities_data[k[0]]['mean_light_queue'].append(v['light'][1])
        intensities_data[k[0]]['upper_light_queue_bounds'].append(v['light'][2])

        intensities_data[k[0]]['lower_moderate_queue_bounds'].append(v['moderate'][0])
        intensities_data[k[0]]['mean_moderate_queue'].append(v['moderate'][1])
        intensities_data[k[0]]['upper_moderate_queue_bounds'].append(v['moderate'][2])

        intensities_data[k[0]]['lower_grave_queue_bounds'].append(v['grave'][0])
        intensities_data[k[0]]['mean_grave_queue'].append(v['grave'][1])
        intensities_data[k[0]]['upper_grave_queue_bounds'].append(v['grave'][2])

    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Статистики симуляции'),
        html.P("Время в очереди vs Время простоя бригады"),
        dcc.Graph(id="graph"),
        html.P("Статистики"),
        dcc.Graph(id="graph2"),
        # html.P("Доля пациентов, над которыми не успели провести манипуляции vs Количество бригад"),
        # dcc.Graph(id="graph3"),
        html.P("Время в очереди для пациентов с различной степенью тяжести повреждений"),
        dcc.Graph(id="graph3"),
        html.P("Интенсивность входного потока (чел/сутки):"),
        dcc.Slider(id="fi",
                   value=parameters_setup['simulation_args']['flow_intensities'][0],
                   step=None,
                   # min=parameters_setup['simulation_args']['flow_intensities'][0],
                   # max=parameters_setup['simulation_args']['flow_intensities'][-1],
                   marks={k: np.arange(100, 350, 50)[i] for i, k in
                          enumerate(parameters_setup['simulation_args']['flow_intensities'])})
    ])


    @app.callback(
        Output("graph", "figure"),
        Output("graph2", "figure"),
        Output("graph3", "figure"),
        Input("fi", "value"))
    def display_color(fi):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=intensities_data[fi]['mean_idle'], y=intensities_data[fi]['mean_queue'],
            mode='lines+markers',
            name='Расчетные значения',
            error_x=dict(
                array=np.array(intensities_data[fi]['upper_idle_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_idle_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            ),
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_queue_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_queue_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            ),
            text=[f'Количество бригад: {nt}' for nt in intensities_data[fi]['num_teams']],
            marker=dict(color=intensities_data[fi]['num_teams'],
                        colorbar=dict(
                            title="Количество бригад"
                        ),
                        colorscale="Deep",
                        size=8)

        ))

        fig.update_xaxes(title_text="Среднее время простоя бригады")
        fig.update_yaxes(title_text="Среднее время ожидания пациента в очереди")

        fig2 = make_subplots(rows=2, cols=1,
                             row_heights=[0.5, 0.5],
                             shared_xaxes='columns',
                             specs=[[{"type": "scatter"}],
                                    [{"type": "scatter"}]])

        fig2.add_trace(go.Scatter(
            x=intensities_data[fi]['num_teams'], y=intensities_data[fi]['mean_av_queue_size'],
            mode='lines+markers',
            name='Расчетные значения',
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_av_queue_size_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_av_queue_size_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            ),
            line=dict(color='#0000f5')), row=1, col=1)

        fig2.add_trace(go.Scatter(
            x=intensities_data[fi]['num_teams'], y=intensities_data[fi]['theoretical_av_queue_size'],
            mode='lines+markers',
            name='Теоретические значения',
            line=dict(color='#009900')), row=1, col=1)

        # fig2.update_xaxes(title_text="Количество бригад")
        fig2.update_yaxes(title_text="Средний размер очереди", row=1, col=1)

        fig2.add_shape(type="line",
                       x0=intensities_data[fi]['minimum_teams'], x1=intensities_data[fi]['minimum_teams'],
                       line=dict(color="#cc0018", width=3),
                       yref="paper",
                       y0=0,
                       y1=1,
                       name='Предельное теоретическое минимальное количество бригад')

        # fig3 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=intensities_data[fi]['num_teams'], y=intensities_data[fi]['mean_al_1_team_free'],
            mode='lines+markers',
            name='Расчетные значения',
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_al_1_team_free_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_al_1_team_free_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            ),
            line=dict(color='#0000f5'),
            showlegend=False), row=2, col=1)

        fig2.add_trace(go.Scatter(
            x=intensities_data[fi]['num_teams'], y=intensities_data[fi]['theoretical_al_1_team_free'],
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

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Доля пациентов, над которыми не успели провести манипуляции',
                              x=intensities_data[fi]['num_teams'],
                              y=intensities_data[fi]['uncured_rate']))

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=intensities_data[fi]['num_teams'],
            y=intensities_data[fi]['mean_light_queue'],
            name='Light',
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_light_queue_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_light_queue_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            )
        ))
        fig3.add_trace(go.Bar(
            x=intensities_data[fi]['num_teams'],
            y=intensities_data[fi]['mean_moderate_queue'],
            name='Moderate',
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_moderate_queue_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_moderate_queue_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            )
        ))
        fig3.add_trace(go.Bar(
            x=intensities_data[fi]['num_teams'],
            y=intensities_data[fi]['mean_grave_queue'],
            name='Grave',
            error_y=dict(
                array=np.array(intensities_data[fi]['upper_grave_queue_bounds']),
                arrayminus=np.array(intensities_data[fi]['lower_grave_queue_bounds']),
                type='data',
                color='black',
                thickness=1,
                width=2,
            )
        ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig3.update_layout(barmode='group')

        return fig, fig2, fig3


    app.run_server(debug=False)
