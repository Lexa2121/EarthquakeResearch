# coding=utf-8
import simpy
from eathquake_data import INITIAL_DATA
from transport import PLANES
from medical_help_onland import OPERATION_DURATION

# in this project each minute is symbolically prepresented by 1 second

def deliver_field_operations(env):
  print('Field Operations Delivered')
  yield env.timeout(100) #will be filled with further data

def take_ill(env, distance_oblast, distance_moscow):
  yield env.timeout(100) #will be filled with further data

""" Function defined how many brigades need to arrive """
def count_brigade_amount(people_nmb, operation_times, working_time):
  return people_nmb * operation_times / working_time


""" Arrival time from the capital of Oblast, time in full MINUTES """
def arrival_time(transport_data, distance):
  return int(distance / transport_data['speed'] * 60)

""" Main function initializing the whole earthquake and its forthcomings """
def initialize_earthquake(env):
  print('Starting EarthQuake...')
  print('Earthquake done, МЧС informed')

  people_severely_injured = INITIAL_DATA['people'] * INITIAL_DATA['severely_injured']
  people_dead = INITIAL_DATA['people'] * INITIAL_DATA['dead']
  people_lightly_injured = INITIAL_DATA['people'] * INITIAL_DATA['lightly_injured']

  print('Brigade coming to  tragedy place')
  yield env.timeout(arrival_time(PLANES['Ли-22'], INITIAL_DATA['distance_oblast_capital']))

  print('Sort people - 10 minutes')
  yield env.timeout(10000)

  print('Operations on the field')
  yield env.process(deliver_field_operations(env))

  print('Take the ill to the nearest big city')
  yield env.process(take_ill(env, INITIAL_DATA['distance_oblast_capital'], INITIAL_DATA['distance_moscow']))

  print('The operation can be successfully closed!')


env = simpy.Environment()
env.process(initialize_earthquake(env))
env.run()