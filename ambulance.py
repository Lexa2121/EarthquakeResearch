class Ambulance:
    def __init__(self, town, receiving_time, service_time, amb_num=1):
        self.receiving_time = receiving_time
        self.town = town
        self.service_time = service_time
        self.processing_start_time = -1
        self.amb_num = amb_num

    def __str__(self):
        return f'''Бригада №{self.amb_num} из {self.town}:
    время поступления в эвакоприемник: {self.receiving_time},
    время начала обслуживания: {self.processing_start_time},
    время обслуживания: {self.service_time}'''

    def __repr__(self):
        return f'''Бригада №{self.amb_num} из {self.town}:
    время поступления в эвакоприемник: {self.receiving_time},
    время начала обслуживания: {self.processing_start_time},
    время обслуживания: {self.service_time}'''