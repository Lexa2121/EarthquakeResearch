from ambulance import Ambulance


class MedCenter:
    def __init__(self, receivers_number: int):
        self.receivers = [{'busy': False, 'overall_busy_time': 0} for _ in range(receivers_number)]
        self.queue = []
        self.served_ambulances = []

    def __get_free_receiver_number__(self):
        for i, receiver in enumerate(self.receivers):
            if not receiver['busy']:
                return i
        return -1

    def __occupy_receiver__(self, cur_time, receiver_number: int, ambulance: Ambulance):
        ambulance.processing_start_time = cur_time
        self.receivers[receiver_number]['ambulance'] = ambulance
        self.receivers[receiver_number]['busy'] = True

    def __free_up_receiver__(self, cur_time, receiver_number):
        ambulance = self.receivers[receiver_number]['ambulance']
        self.receivers[receiver_number]['overall_busy_time'] += cur_time - ambulance.processing_start_time
        self.receivers[receiver_number]['busy'] = False
        return ambulance

    def add_ambulance(self, town, receiving_time, service_time, amb_num):
        ambulance = Ambulance(town, receiving_time, service_time, amb_num)
        queue_length = len(self.queue)
        free_receiver = self.__get_free_receiver_number__()
        if free_receiver != -1:
            self.__occupy_receiver__(receiving_time, free_receiver, ambulance)
            return {'receiver': free_receiver}
        else:
            self.queue.append(ambulance)
            return {'queue': '+1'}

    def depart_served_ambulances(self, cur_time):
        res = {'freed_receiver': [], 'occupied_receivers': []}
        for i, receiver in enumerate(self.receivers):
            busy_time = cur_time - receiver['ambulance'].processing_start_time
            if receiver['busy'] and busy_time == receiver['ambulance'].service_time:
                self.served_ambulances.append(self.__free_up_receiver__(cur_time, i))
                res['freed_devices'].append(i)
                if len(self.queue) > 0:
                    ambulance = self.queue.pop(0)
                    self.__occupy_receiver__(cur_time, i, ambulance)
                    res['occupied_receivers'].append(i)
        return res