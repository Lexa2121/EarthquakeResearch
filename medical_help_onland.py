class NotEnoughPersonnelError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'NotEnoughPersonnelError, {self.message}. '
        else:
            return 'NotEnoughPersonnelError has been raised'


class MedicalCenter(object):
    def __init__(self, total_personnel: dict, total_vehicles: dict):
        self.total_personnel = total_personnel
        self.total_vehicles = total_vehicles
        self.num_teams_on_field = 0
        self.team = {'small': {'surgeon': 3,
                               'anesthesiologist': 2,
                               'trauma_surgeon': 12,
                               'nurse': 5,
                               'attendant': 2
                               },
                     'big': {'surgeon': 8,
                             'anesthesiologist': 2,
                             'trauma_surgeon': 2,
                             'nurse': 12}}
        self.MEDICAL_PERSONNEL_WORKING_MINUTES = 600
        self.OPERATION_DURATION = {'sorting': 10,
                                   'first_aid_kit': 10
                                   }

    def request_team(self, size: str = 'small') -> None:
        """
        Checks whether medical center has enough specialists to send requested team.
        If it has, team will be sent.

        Parameters:
        ===========
            size: str, default: 'small'
            The size of requested medical team.
            Must be whether 'small' or 'big'.
        """
        if size not in ['small', 'big']:
            raise ValueError("Wrong size value: must be 'small' or 'big'")
        # TODO: add vehicle check
        requested_team = self.team[size]
        for specialist, req_num in requested_team.items():
            spec_num = self.total_personnel[specialist]
            if req_num > spec_num:
                raise NotEnoughPersonnelError(f'med-center has only {spec_num} {specialist}s, {req_num} were requested')
        for specialist, req_num in requested_team.items():
            self.total_personnel[specialist] -= req_num
        print(f'{size} medical team was sent')

    def team_returns(self, size: str = 'small'):
        returned_team = self.team[size]
        for specialist, req_num in returned_team.items():
            self.total_personnel[specialist] += req_num
        print(f'{size} medical team returned')
