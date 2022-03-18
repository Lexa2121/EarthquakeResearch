# coding=utf-8
import simpy
from eathquake_data import INITIAL_DATA
from transport import AMBULANCES
from medical_help_onland import MEDICAL_PERSONNEL_WORKING_HOURS
from injury_types import avg_help_time
from patient_manager import generate_patients


# in this project each minute is symbolically presented by 1 second

def deliver_field_operations(env):
    print('Field Operations Delivered')
    yield env.timeout(100)  # will be filled with further data


def take_ill(env, distance_oblast):
    yield env.timeout(100)  # will be filled with further data


""" Function defined how many brigades need to arrive """


def count_brigade_amount(patients_number: int) -> int:
    return int(avg_help_time * patients_number / MEDICAL_PERSONNEL_WORKING_HOURS)


""" Arrival time from the capital of Oblast, time in full MINUTES """


def arrival_time(transport_data, distance):
    return int(distance / transport_data['speed'] * 60)


""" Main function initializing the whole earthquake and its forthcomings """


def initialize_earthquake(env, patients_number: int = 100000):
    print('Starting EarthQuake...')
    patients = generate_patients(patients_number)

    print('МЧС informed')
    yield env.timeout(40000)  # the processing of the data by МЧС takes 30-40 minutes
    number_of_doctors = count_brigade_amount(patients_number)
    print(f'Needed {number_of_doctors} dictors')

    print('Brigade coming to tragedy place')
    yield env.timeout(arrival_time(AMBULANCES['Default'], INITIAL_DATA['distance_oblast_capital']))

    print('Sort people - 10 minutes')
    yield env.timeout(10000)

    print('Operations on the field')
    yield env.process(deliver_field_operations(env))

    print('Take the ill to the nearest big city')
    yield env.process(take_ill(env, INITIAL_DATA['distance_oblast_capital']))

    print('The operation can be successfully closed!')


env = simpy.Environment()
env.process(initialize_earthquake(env))
env.run()
