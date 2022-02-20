import numpy as np
import random
from xmlrpc.client import boolean
from injury_types import operations, injury_distribution, operation_types, injuries

def find_operation_time(op: str) -> int:
  for inj in injuries:
    if op in operations[inj].keys():
      return operations[inj][op]
  return 0

class Patient:
  id: int
  alive: bool
  severity: int
  operations: list

  def __init__(self, id: int):
    self.id = id
    self.alive = True
    self.severity = 2
    self.operations = []

  def print_patient_info(self):
    print(f'id: {self.id}; is_alive: {self.alive}; severity: {self.severity}; operations to do: {",".join(self.operations)}')

  def make_dead(self):
    self.alive = False

  def add_operation(self, operation: str):
    self.operations.append(operation)

  """ Return full time in minutes """
  def calculate_operation_time(self) -> int:
    if self.alive == False:
      return 0

    full_time = 0
    for op in self.operations:
      full_time += find_operation_time(op)
    
    return full_time

def generate_patients(residents: int) -> list:
  patients = [Patient(i) for i in range (0, residents)]

  dead_patients = np.random.choice(patients, size=int(residents * injury_distribution['dead']))

  thoracoabdominal_patients = np.random.choice(patients, size=int(residents * injury_distribution['торакоабдоминальная']))
  traumathologic_patients = np.random.choice(patients, size=int(residents * injury_distribution['травматологическая']))
  neurosurgery_parients = np.random.choice(patients, size=int(residents * injury_distribution['нейрохирургическая']))

  [patient.make_dead() for patient in dead_patients]
  [patient.add_operation(random.choice(list(operations['торакоабдоминальная'].keys()))) for patient in thoracoabdominal_patients]
  [patient.add_operation(random.choice(list(operations['травматологическая'].keys()))) for patient in traumathologic_patients]
  [patient.add_operation(random.choice(list(operations['нейрохирургическая'].keys()))) for patient in neurosurgery_parients]

  return patients
