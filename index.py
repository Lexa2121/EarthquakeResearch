from random import random
import simpy
from eathquake_data import INITIAL_DATA
from transport import PLANES
from medial_help_onland import OPERATION_DURATION, MEDICAL_PERSONEL

def provide_aid_kit(env, people_number):
  while people_number > 0:
    people_helped = people_number - MEDICAL_PERSONEL
    if (people_helped < 0):
      people_helped = people_number
    people_number -= people_helped
    yield env.timeout(people_helped * OPERATION_DURATION['first_aid_kit'] * 1000)

def choose_hospital(env):
  pass

def initialize_earthquake(env):
  print('Starting EarthQuake...')
  print('Earthquake done, МЧС informed')
  people_severely_injured = INITIAL_DATA['eq_strength'] * INITIAL_DATA['coefficients']['severely_injured'] * random() / 100 * INITIAL_DATA['living_people']
  print(f'Severely injured {people_severely_injured}')
  while people_severely_injured > 0:
    people_taken = people_severely_injured - PLANES['Ли-22']['seats']
    provide_aid_kit(env, people_severely_injured)
    if people_taken < 0:
      people_taken = people_severely_injured
    people_severely_injured -= people_taken
    print(f'Remaining people {people_severely_injured}')
    yield env.timeout(INITIAL_DATA['distance']/PLANES['Ли-22']['speed']*1000)


env = simpy.Environment()
env.process(initialize_earthquake(env))
env.run(until=15)