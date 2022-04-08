# import simpy
from eathquake_data import CITY_DATA
# import random
#
NUM_RECIEVERS = 5
RECIEVE_TIME = 5
# SIM_TIME = 120     # Simulation time in minutes
# T_INTER = 7
# RANDOM_SEED = 42
#
# class MedCenter(object):
#     """A carwash has a limited number of machines (``NUM_MACHINES``) to
#     clean cars in parallel.
#
#     Cars have to request one of the machines. When they got one, they
#     can start the washing processes and wait for it to finish (which
#     takes ``washtime`` minutes).
#
#     """
#     def __init__(self, env, recievers_num, recievetime):
#         self.env = env
#         self.reciever = simpy.Resource(env, recievers_num)
#         self.recievetime = recievetime
#
#     def recieve(self, name):
#         """The washing processes. It takes a ``car`` processes and tries
#         to clean it."""
#         yield self.env.timeout(self.recievetime)
#         print(f"Ambulance from {name} recieved")
#
#
# class Ambulance(object):
#     def __init__(self, env, town, name, recievetime, num_patience_seats=2, speed=1):
#         self.env = env
#         self.town = town
#         self.name = name
#         self.recievetime = recievetime
#         self.num_patience_seats = num_patience_seats
#         self.speed = speed
#
#     def unload(self, mc):
#         print(f'{self.name} arrived at {self.env.now}')
#         with mc.reciever.request() as request:
#             yield request
#             print(f'{self.name} recieved at {self.env.now}')
#             yield self.env.process(mc.recieve(self.name))
#             print(f'{self.name} leaves med center at {self.env.now}')
#
#     def load(self, injuries):
#         yield injuries.get(self.num_patience_seats)
#         yield self.env.timeout(self.recievetime)
#         print(f"Patiens by {self.name} were loaded")
#
#     def move(self, path_len):
#         yield self.env.timeout(path_len/self.speed)
#
#     def full_process(self, injuries, mc, path_len):
#         yield self.env.process(self.load(injuries))
#         yield self.env.process(self.move(path_len))
#         yield self.env.process(self.unload(mc))
#         yield self.env.process(self.move(path_len))
#
#
# def setup(env, num_recievers, recievetime):
#
#     # Create the medcenter
#     medcenter = MedCenter(env, num_recievers, recievetime)
#
#     # Create the towns
#     town_containers = {}
#     for k, v in CITY_DATA.items():
#         town_containers[k] = simpy.Container(env, init=v['injured'], capacity=v['injured'])
#
#     # Create initial cars
#     ambulances = {}
#     for k, v in CITY_DATA.items():
#         ambulances[k] = []
#         for i in range(1, v['population']//10000+2):
#             if k != 'Комсомольск-на-Амуре':
#                 ambulances[k].append(Ambulance(env, k, f'Бригада из {k} №{i}', recievetime, speed=1.5))
#             else:
#                 ambulances[k].append(Ambulance(env, k, f'Бригада из {k} №{i}', recievetime))
#     # Create more cars while the simulation is running
#     while True:
#         for k, v in ambulances.items():
#             for car in v:
#                 print(car.name)
#                 yield env.process(car.full_process(town_containers[k], medcenter, CITY_DATA[k]['distance_from_camp']))
#
#
# # Setup and start the simulation
# print('Carwash')
# print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
# random.seed(RANDOM_SEED)  # This helps reproducing the results
#
# # Create an environment and start the setup process
# env = simpy.Environment()
# env.process(setup(env, NUM_RECIEVERS, RECIEVE_TIME))
#
# # Execute!
# env.run(until=SIM_TIME)
#
# import simpy
# from eathquake_data import CITY_DATA
# import random
#
# NUM_RECIEVERS = 1
# RECIEVE_TIME = 5
# SIM_TIME = 120     # Simulation time in minutes
# T_INTER = 7
# RANDOM_SEED = 42

# class Ambulance(object):
#     def __init__(self, name, unload_time = 5, num_patience_seats=2, speed=1):
#         self.name = name
#         self.num_patience_seats = num_patience_seats
#         self.speed = speed
#         self.t_on_medcenter = 0
#
#     def unload(self, ):
#         print(f'{self.name} arrived at medcenter')
#             self.env.process(mc.recieve(self.name))
#             print(f'{self.name} leaves med center at {self.env.now}')
#
#     def load(self, injuries):
#         yield injuries.get(self.num_patience_seats)
#         yield self.env.timeout(self.recievetime)
#         print(f"Patiens by {self.name} were loaded")
#
#     def move(self, path_len):
#         yield self.env.timeout(path_len/self.speed)
#
#     def full_process(self, injuries, mc, path_len):
#         yield self.env.process(self.load(injuries))
#         yield self.env.process(self.move(path_len))
#         yield self.env.process(self.unload(mc))
#         yield self.env.process(self.move(path_len))

class Ambulance(object):
    def __init__(self, name, town, path, unload_time = 5, capacity=2, speed=1):
        self.name = name
        self.t_on_medcenter = 0
        self.total_time = 0
        self.town = town
        self.unload_time = unload_time
        self.time_in_road = 0
        self.capacity = capacity
        self.time_to_road = path//speed
        self.waiting_time = 0


    def ride(self, t):
        self.time_in_road += t

    def wait(self, t):
        self.waiting_time += t

    def __repr__(self):
        return self.name

ambs = []
for k, v in CITY_DATA.items():
    for i in range(1, v['population']//10000+2):
        if k != 'Комсомольск-на-Амуре':
            ambs.append(Ambulance(f'Бригада из {k} №{i}', k, v['distance_from_camp'], speed=1.5))
        else:
            ambs.append(Ambulance(f'Бригада из {k} №{i}', k, v['distance_from_camp']))

t = 0
queue_history = []
queue = []
free_spaces_for_amb = []

total_injuries = {}
for k, v in CITY_DATA.items():
    total_injuries[k] = v['injured']

while True:

    # Смотрим, прибыли ли какие-либо бригады.
    # Всем прибавляем время в дороге, прибывших помещаем в очередь
    for amb_on_way in ambs:
        amb_on_way.total_time += 1
        if amb_on_way not in queue and amb_on_way not in free_spaces_for_amb:
            amb_on_way.total_time += 1
            amb_on_way.ride(1)
            if amb_on_way.time_in_road == amb_on_way.time_to_road:
                amb_on_way.time_in_road = 0
                queue.append(amb_on_way)
                total_injuries[amb_on_way.town] = max(total_injuries[amb_on_way.town]-amb_on_way.capacity, 0)
                print(f"{amb_on_way} arrived to med center at {t}")

    # Если есть место помещаем бригады из очереди в ЭП
    just_recieved = 0
    for i in range(NUM_RECIEVERS):
        if (len(free_spaces_for_amb) < NUM_RECIEVERS) and (len(queue) > 0):
            amb_to_unload = queue.pop(0)
            print(f"Med Center recieved {amb_to_unload} at {t}")
            just_recieved += 1
            free_spaces_for_amb.append(amb_to_unload)
        else:
            break

    for amb_in_mc in free_spaces_for_amb[:NUM_RECIEVERS-just_recieved]:
        amb_in_mc.wait(1)
        if amb_in_mc.unload_time == amb_in_mc.waiting_time:
            amb_in_mc.waiting_time = 0
            print(f"{amb_in_mc} left med center at {t}")
            free_spaces_for_amb.pop(free_spaces_for_amb.index(amb_in_mc))

    for i, amb in enumerate(ambs):
        if amb not in queue and amb not in free_spaces_for_amb:
            if total_injuries[amb.town]==0:
                print(f'{amb.town} was done!')
                ambs.pop(ambs.index(amb))
                print(f"{amb} left rout at {t}")

    queue_history.append(len(queue))
    if sum(list(total_injuries.values())) == 0:
        break
    t+=1



