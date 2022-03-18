import numpy as np
import random
from injury_types import operations, injury_distribution, injuries


def find_operation_time(op: str) -> int:
    for inj in injuries:
        if op in operations[inj].keys():
            return operations[inj][op]
    return 0


class Patient:

    def __init__(self, id: int):
        self.id = id
        self.alive = True
        self.severity = 2
        self.operations = []

    def print_patient_info(self):
        print(f'id: {self.id}')
        print(f'is_alive: {self.alive}')
        print(f'severity: {self.severity}')
        print(f'operations to do: {",".join(self.operations)}')

    def make_dead(self):
        self.alive = False

    def add_operation(self, operation: str) -> None:
        self.operations.append(operation)

    def calculate_operation_time(self) -> int:
        """
        Returns full needed operations time in minutes
        """
        if not self.alive:
            return 0
        return sum([find_operation_time(op) for op in self.operations])


def generate_patients(num_residents: int) -> list:
    patients = [Patient(i) for i in range(0, num_residents)]

    dead_patients = np.random.choice(patients,
                                     size=int(num_residents * injury_distribution['dead']))
    thoracoabdominal_patients = np.random.choice(patients,
                                                 size=int(num_residents * injury_distribution['торакоабдоминальная']))
    traumathologic_patients = np.random.choice(patients,
                                               size=int(num_residents * injury_distribution['травматологическая']))
    neurosurgery_patients = np.random.choice(patients,
                                             size=int(num_residents * injury_distribution['нейрохирургическая']))

    for patient in dead_patients:
        patient.make_dead()
    for patient in thoracoabdominal_patients:
        patient.add_operation(random.choice(list(operations['торакоабдоминальная'].keys())))
    for patient in traumathologic_patients:
        patient.add_operation(random.choice(list(operations['травматологическая'].keys())))
    for patient in neurosurgery_patients:
        patient.add_operation(random.choice(list(operations['нейрохирургическая'].keys())))

    return patients
