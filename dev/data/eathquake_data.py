CITY_DATA = {'Комсомольск-на-Амуре': {'injured': 12290, 'distance_from_camp': 10, 'population': 241072},
             'Снежный': {'injured': 1265, 'distance_from_camp': 110, 'population': 2000},
             'Уктур': {'injured': 1000, 'distance_from_camp': 160, 'population': 1500},
             'Высокогорный': {'injured': 2000, 'distance_from_camp': 230, 'population': 2726},
             'Кенада': {'injured': 500, 'distance_from_camp': 270, 'population': 750},
             'Тумнин': {'injured': 580, 'distance_from_camp': 360, 'population': 1000},
             'Ягодный': {'injured': 1135, 'distance_from_camp': 160, 'population': 1700},
             'Циммермановка': {'injured': 785, 'distance_from_camp': 230, 'population': 1200},
             'Софийск': {'injured': 530, 'distance_from_camp': 330, 'population': 1000}}

ILLNESS_DATA = {'травматологический': {'frac': 0.67, 'mean_cure_time': 90},
                'торакоабдоминальный': {'frac': 0.1, 'mean_cure_time': 90},
                'нейрохирургичекий': {'frac': 0.23, 'mean_cure_time': 30}}

ILLNESS_DATA_ENHANCED = {'F': {'40': {'light': {'amount': 15, 'specialists': ['Psychotherapist'], 'op_time': 0}}},
                         'J': {'4': {'light': {'amount': 1, 'specialists': ['ENT surgeon'], 'op_time': 0}}},
                         'L': {'3': {'light': {'amount': 1, 'specialists': ['Dermatologist'], 'op_time': 0}},
                               '8': {'light': {'amount': 1, 'specialists': ['Dermatologist'], 'op_time': 0}}},
                         'S': {'1': {'light': {'amount': 19,
                                               'specialists': ['Surgeon'],
                                               'op_time': 20},
                                     'moderate': {'amount': 2,
                                                  'specialists': ['Surgeon',
                                                                  'Junior nurse'],
                                                  'op_time': 30},
                                     'grave': {'amount': 1,
                                               'specialists': ['Neurological surgeon',
                                                               'Anesthesiologist',
                                                               'Scrub nurse',
                                                               'Anesthesiologist nurse'],
                                               'op_time': 45},
                                     'critical': {'amount': 1,
                                                  'specialists': ['Neurological surgeon',
                                                                  'Anesthesiologist',
                                                                  'Senior scrub nurse',
                                                                  'Scrub nurse',
                                                                  'Anesthesiologist nurse'],
                                                  'op_time': 60}},
                               '6': {'light': {'amount': 2,
                                               'specialists': ['Neurological surgeon'],
                                               'op_time': 30},
                                     'moderate': {'amount': 87,
                                                  'specialists': ['Neurological surgeon',
                                                                  'Junior nurse'],
                                                  'op_time': 45},
                                     'grave': {'amount': 10,
                                               'specialists': ['Neurological surgeon',
                                                               'Anesthesiologist',
                                                               'Scrub nurse',
                                                               'Anesthesiologist nurse'],
                                               'op_time': 60},
                                     'critical': {'amount': 1,
                                                  'specialists': ['Neurological surgeon',
                                                                  'Anesthesiologist',
                                                                  'Senior scrub nurse',
                                                                  'Scrub nurse',
                                                                  'Anesthesiologist nurse'],
                                                  'op_time': 60}},
                               '20': {'light': {'amount': 17, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 3, 'specialists': [], 'op_time': 0}},
                               '21': {'light': {'amount': 1, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 4, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 7, 'specialists': [], 'op_time': 0}},
                               '22': {'light': {'amount': 3, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 7, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '27': {'grave': {'amount': 3, 'specialists': [], 'op_time': 0},
                                      'critical': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '30': {'light': {'amount': 13, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '31': {'light': {'amount': 5, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 1, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 3, 'specialists': [], 'op_time': 0},
                                      'critical': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '32': {'moderate': {'amount': 1, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 6, 'specialists': [], 'op_time': 0}},
                               '33': {'light': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '34': {'light': {'amount': 2, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '35': {'light': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '37': {'light': {'amount': 2, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 6, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '40': {'light': {'amount': 8, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '43': {'light': {'amount': 8, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 4, 'specialists': [], 'op_time': 0},
                                      'gravy': {'amount': 4, 'specialists': [], 'op_time': 0}},
                               '50': {'light': {'amount': 4, 'specialists': [], 'op_time': 0}},
                               '53': {'light': {'amount': 5, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '54': {'moderate': {'amount': 3, 'specialists': [], 'op_time': 0}},
                               '60': {'light': {'amount': 15, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '63': {'light': {'amount': 3, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 3, 'specialists': [], 'op_time': 0}},
                               '66': {'light': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '80': {'light': {'amount': 24, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '83': {'light': {'amount': 24, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 17, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 4, 'specialists': [], 'op_time': 0}},
                               '84': {'light': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '90': {'light': {'amount': 26, 'specialists': [], 'op_time': 0}}},
                         'T': {'0': {'light': {'amount': 3, 'specialists': [], 'op_time': 0},
                                     'moderate': {'amount': 3, 'specialists': [], 'op_time': 0}},
                               '1': {'light': {'amount': 1, 'specialists': [], 'op_time': 0},
                                     'grave': {'amount': 3, 'specialists': [], 'op_time': 0},
                                     'critical': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '20': {'light': {'amount': 6, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 7, 'specialists': [], 'op_time': 0}},
                               '52': {'moderate': {'amount': 3, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '53': {'light': {'amount': 1, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '57': {'moderate': {'amount': 2, 'specialists': [], 'op_time': 0}},
                               '58': {'light': {'amount': 1, 'specialists': [], 'op_time': 0},
                                      'moderate': {'amount': 2, 'specialists': [], 'op_time': 0},
                                      'grave': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '59': {'moderate': {'amount': 1, 'specialists': [], 'op_time': 0}},
                               '79.5': {'light': {'amount': 4, 'specialists': [], 'op_time': 0},
                                        'moderate': {'amount': 8, 'specialists': [], 'op_time': 0},
                                        'grave': {'amount': 2, 'specialists': [], 'op_time': 0}}}
                         }

MULTIDISCIPLINARY_TEAM = {'Surgeon': 1,
                          'Thoracic surgeon': 1,
                          'Abdominal surgeon': 1,
                          'Ophthalmologist': 1,
                          'Neurological surgeon': 1,
                          'ENT surgeon': 1,
                          'Combustiologist': 1,
                          'Maxillofacial surgeon': 1,
                          'Vascular surgeon': 1,
                          'Anesthesiologist': 2,
                          'Senior scrub nurse': 1,
                          'Scrub nurse': 3,
                          'Anesthesiologist nurse': 4,
                          'Junior nurse': 1,
                          'Statistician': 2}
