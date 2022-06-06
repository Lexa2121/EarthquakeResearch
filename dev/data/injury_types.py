""" Injury cure methods with maximal time of their impelemntation"""
operations = {
    'торакоабдоминальная': {
        'пункция': 10,
        'торакоцентез': 15,
        'субксифоидальная': 30,
        'лапароцентез': 30,
        'стернотомия': 20
    },
    'травматологическая': {
        'наложение противошоковой тазовой повязки': 15,
        'КСТ': 90
    },
    'нейрохирургическая': {
        'временная остановка наружного кровотечения': 30
    }
}

""" The distribution of injuries depending on their type """
injury_distribution = {
    'травматологическая': 0.67,
    'торакоабдоминальная': 0.095,
    'нейрохирургическая': 0.23,
    'dead': 0.2
}

injuries = [
    'торакоабдоминальная',
    'травматологическая',
    'нейрохирургическая'
]

avg_help_time = 0
operation_types = []

for inj in injuries:
    operation_types.extend(list(operations[inj].keys()))

op_amount = 0
for inj in injuries:
    for op in operations[inj].keys():
        op_amount += 1
        avg_help_time += operations[inj][op]

avg_help_time /= op_amount
