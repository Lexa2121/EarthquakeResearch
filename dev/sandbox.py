# overall_sum = 0
# illnesses_list = []
# illnesses_fracs = []
# illnesses_op_times = []
# illnesses_specialists = []
# for global_illness_type, subtypes in ILLNESS_DATA_ENHANCED.items():
#     for subtype, subtype_info in subtypes.items():
#         for level, level_data in subtype_info.items():
#             overall_sum += level_data['amount']
#             illnesses_list.append(f'{global_illness_type}{subtype}_{level}')
#             illnesses_fracs.append(level_data['amount'])
#             illnesses_op_times.append(level_data['op_time'])
#             illnesses_specialists.append(level_data['specialists'])
# illnesses_fracs = np.array(illnesses_fracs) / overall_sum
#
# print(overall_sum)
# print(len(illnesses_fracs))
# print(len(np.cumsum(illnesses_fracs)))

# import plotly.graph_objects as go
# import numpy as np
#
# x_theo = np.linspace(-4, 4, 100)
# sincx = np.sinc(x_theo)
# x = [-3.8, -3.03, -1.91, -1.46, -0.89, -0.24, -0.0, 0.41, 0.89, 1.01, 1.91, 2.28, 2.79, 3.56]
# y = [-0.02, 0.04, -0.01, -0.27, 0.36, 0.75, 1.03, 0.65, 0.28, 0.02, -0.11, 0.16, 0.04, -0.15]
#
# fig = go.Figure()
# fig.add_trace(go.Scatter(
#     x=x_theo, y=sincx,
#     name='sinc(x)'
# ))
# fig.add_trace(go.Scatter(
#     x=x, y=y,
#     mode='markers',
#     name='measured',
#     error_y=dict(
#         type='constant',
#         value=0.1,
#         color='purple',
#         thickness=1.5,
#         width=3,
#     ),
#     error_x=dict(
#         array = np.array([2,3]),
#         arrayminus = np.array([3,2]),
#         type='data',
#         value=2,
#         symmetric=False,
#         color='purple',
#         thickness=1.5,
#         width=3,
#     ),
#     marker=dict(color='purple', size=8)
# ))
# fig.show()
#
# print(list(np.arange(3, 5.25, 0.25)))

from math import factorial

print(factorial(130)/factorial(240))