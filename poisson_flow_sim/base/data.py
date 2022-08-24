injury_extents = {5: {'light': 1.,
                      'moderate': 0.,
                      'grave': 0.},
                  6: {'light': 0.8775,
                      'moderate': 0.0817,
                      'grave': 0.0408},
                  7: {'light': 0.8229,
                      'moderate': 0.1094,
                      'grave': 0.0677},
                  8: {'light': 0.7751,
                      'moderate': 0.1336,
                      'grave': 0.0913},
                  9: {'light': 0.3703,
                      'moderate': 0.3085,
                      'grave': 0.3212},
                  10: {'light': 0.3012,
                       'moderate': 0.3316,
                       'grave': 0.3672},
                  11: {'light': 0.284,
                       'moderate': 0.3168,
                       'grave': 0.3992},
                  12: {'light': 0.2699,
                       'moderate': 0.2997,
                       'grave': 0.4304}
                  }

special_teams_distr = {3: {'thoracoabdominal': 1,
                           'trauma': 1,
                           'neuro': 1},
                       4: {'thoracoabdominal': 2,
                           'trauma': 1,
                           'neuro': 1},
                       5: {'thoracoabdominal': 3,
                           'trauma': 1,
                           'neuro': 1},
                       6: {'thoracoabdominal': 4,
                           'trauma': 1,
                           'neuro': 1},
                       7: {'thoracoabdominal': 4,
                           'trauma': 1,
                           'neuro': 2},
                       8: {'thoracoabdominal': 5,
                           'trauma': 1,
                           'neuro': 2},
                       9: {'thoracoabdominal': 6,
                           'trauma': 1,
                           'neuro': 2},
                       10: {'thoracoabdominal': 7,
                           'trauma': 1,
                           'neuro': 2}}

special_teams_distr_new = {'x': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1, 8: 0.3333,
                                 9: 0.3333, 10: 0.3333, 11: 0.3333, 12: 0.3333, 13: 0.3333, 14: 0.3333,
                                 15: 0.3333, 16: 0.1, 17: 0.1, 18: 0.1, 19: 0.1, 20: 0.1, 21: 0.1, 22: 0.1, 23: 0.1,
                                 24: 0.1, 25: 0.1, 26: 0.1, 27: 0.1, 28: 0.1, 29: 0.1, 30: 0.1, 31: 0.1, 32: 0.1,
                                 33: 0.1, 34: 0.1, 35: 0.1, 36: 0.1, 37: 0.1, 38: 0.1, 39: 0.1, 40: 0.1, 41: 0.1,
                                 42: 0.1, 43: 0.1, 44: 0.1, 45: 0.1, 46: 0.1, 47: 0.1, 48: 0.2, 49: 0.2, 50: 0.2,
                                 51: 0.2, 52: 0.2, 53: 0.2, 54: 0.2, 55: 0.2, 56: 0.2, 57: 0.2, 58: 0.2, 59: 0.2,
                                 60: 0.2, 61: 0.2, 62: 0.2, 63: 0.2, 64: 0.2, 65: 0.2, 66: 0.2, 67: 0.2, 68: 0.2,
                                 69: 0.2, 70: 0.2, 71: 0.2, 72: 0.3, 73: 0.3, 74: 0.3, 75: 0.3, 76: 0.3, 77: 0.3,
                                 78: 0.3, 79: 0.3},
                           'y': {0: 0.23, 1: 0.23, 2: 0.23, 3: 0.23, 4: 0.23, 5: 0.23, 6: 0.23, 7: 0.23, 8: 0.3333,
                                 9: 0.3333, 10: 0.3333, 11: 0.3333, 12: 0.3333, 13: 0.3333, 14: 0.3333, 15: 0.3333,
                                 16: 0.1, 17: 0.1, 18: 0.1, 19: 0.1, 20: 0.1, 21: 0.1, 22: 0.1, 23: 0.1, 24: 0.2,
                                 25: 0.2, 26: 0.2, 27: 0.2, 28: 0.2, 29: 0.2, 30: 0.2, 31: 0.2, 32: 0.3, 33: 0.3,
                                 34: 0.3, 35: 0.3, 36: 0.3, 37: 0.3, 38: 0.3, 39: 0.3, 40: 0.4, 41: 0.4, 42: 0.4,
                                 43: 0.4, 44: 0.4, 45: 0.4, 46: 0.4, 47: 0.4, 48: 0.2, 49: 0.2, 50: 0.2, 51: 0.2,
                                 52: 0.2, 53: 0.2, 54: 0.2, 55: 0.2, 56: 0.3, 57: 0.3, 58: 0.3, 59: 0.3, 60: 0.3,
                                 61: 0.3, 62: 0.3, 63: 0.3, 64: 0.4, 65: 0.4, 66: 0.4, 67: 0.4, 68: 0.4, 69: 0.4,
                                 70: 0.4, 71: 0.4, 72: 0.3, 73: 0.3, 74: 0.3, 75: 0.3, 76: 0.3, 77: 0.3, 78: 0.3,
                                 79: 0.3},
                           'z': {0: 0.67, 1: 0.67, 2: 0.67, 3: 0.67, 4: 0.67, 5: 0.67, 6: 0.67, 7: 0.67, 8: 0.3334,
                                 9: 0.3334, 10: 0.3334, 11: 0.3334, 12: 0.3334, 13: 0.3334, 14: 0.3334, 15: 0.3334,
                                 16: 0.8, 17: 0.8, 18: 0.8, 19: 0.8, 20: 0.8, 21: 0.8, 22: 0.8, 23: 0.8, 24: 0.7,
                                 25: 0.7, 26: 0.7, 27: 0.7, 28: 0.7, 29: 0.7, 30: 0.7, 31: 0.7, 32: 0.6, 33: 0.6,
                                 34: 0.6, 35: 0.6, 36: 0.6, 37: 0.6, 38: 0.6, 39: 0.6, 40: 0.5, 41: 0.5, 42: 0.5,
                                 43: 0.5, 44: 0.5, 45: 0.5, 46: 0.5, 47: 0.5, 48: 0.6, 49: 0.6, 50: 0.6, 51: 0.6,
                                 52: 0.6, 53: 0.6, 54: 0.6, 55: 0.6, 56: 0.5, 57: 0.5, 58: 0.5, 59: 0.5, 60: 0.5,
                                 61: 0.5, 62: 0.5, 63: 0.5, 64: 0.4, 65: 0.4, 66: 0.4, 67: 0.4, 68: 0.4, 69: 0.4,
                                 70: 0.4, 71: 0.4, 72: 0.4, 73: 0.4, 74: 0.4, 75: 0.4, 76: 0.4, 77: 0.4, 78: 0.4,
                                 79: 0.4},
                           'nt': {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7,
                                  13: 8, 14: 9, 15: 10, 16: 3, 17: 4, 18: 5, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 24: 3,
                                  25: 4, 26: 5, 27: 6, 28: 7, 29: 8, 30: 9, 31: 10, 32: 3, 33: 4, 34: 5, 35: 6, 36: 7,
                                  37: 8, 38: 9, 39: 10, 40: 3, 41: 4, 42: 5, 43: 6, 44: 7, 45: 8, 46: 9, 47: 10, 48: 3,
                                  49: 4, 50: 5, 51: 6, 52: 7, 53: 8, 54: 9, 55: 10, 56: 3, 57: 4, 58: 5, 59: 6, 60: 7,
                                  61: 8, 62: 9, 63: 10, 64: 3, 65: 4, 66: 5, 67: 6, 68: 7, 69: 8, 70: 9, 71: 10, 72: 3,
                                  73: 4, 74: 5, 75: 6, 76: 7, 77: 8, 78: 9, 79: 10},
                           'x_nt': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2, 12: 2,
                                    13: 2, 14: 3, 15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1,
                                    25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1,
                                    37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1,
                                    49: 1, 50: 1, 51: 1, 52: 1, 53: 2, 54: 2, 55: 2, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1,
                                    61: 2, 62: 2, 63: 2, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 2, 70: 2, 71: 2, 72: 1,
                                    73: 1, 74: 1, 75: 2, 76: 2, 77: 2, 78: 3, 79: 3},
                           'y_nt': {0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2, 8: 1, 9: 1, 10: 2, 11: 2, 12: 2,
                                    13: 3, 14: 3, 15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1,
                                    25: 1, 26: 1, 27: 1, 28: 1, 29: 2, 30: 2, 31: 2, 32: 1, 33: 1, 34: 2, 35: 2, 36: 2,
                                    37: 2, 38: 3, 39: 3, 40: 1, 41: 1, 42: 2, 43: 2, 44: 3, 45: 3, 46: 4, 47: 4, 48: 1,
                                    49: 1, 50: 1, 51: 1, 52: 1, 53: 2, 54: 2, 55: 2, 56: 1, 57: 1, 58: 2, 59: 2, 60: 2,
                                    61: 2, 62: 3, 63: 3, 64: 1, 65: 1, 66: 2, 67: 2, 68: 3, 69: 3, 70: 3, 71: 4, 72: 1,
                                    73: 1, 74: 2, 75: 2, 76: 2, 77: 2, 78: 3, 79: 3},
                           'z_nt': {0: 1, 1: 2, 2: 3, 3: 4, 4: 4, 5: 5, 6: 6, 7: 7, 8: 1, 9: 2, 10: 2, 11: 2, 12: 3,
                                    13: 3, 14: 3, 15: 4, 16: 1, 17: 2, 18: 3, 19: 4, 20: 5, 21: 6, 22: 7, 23: 8, 24: 1,
                                    25: 2, 26: 3, 27: 4, 28: 5, 29: 5, 30: 6, 31: 7, 32: 1, 33: 2, 34: 2, 35: 3, 36: 4,
                                    37: 5, 38: 5, 39: 6, 40: 1, 41: 2, 42: 2, 43: 3, 44: 3, 45: 4, 46: 4, 47: 5, 48: 1,
                                    49: 2, 50: 3, 51: 4, 52: 5, 53: 4, 54: 5, 55: 6, 56: 1, 57: 2, 58: 2, 59: 3, 60: 4,
                                    61: 4, 62: 4, 63: 5, 64: 1, 65: 2, 66: 2, 67: 3, 68: 3, 69: 3, 70: 4, 71: 4, 72: 1,
                                    73: 2, 74: 2, 75: 2, 76: 3, 77: 4, 78: 3, 79: 4}}
