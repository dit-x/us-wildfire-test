import pandas as pd
import numpy as np
import pickle

import datetime


def prepare_input_value(list_input):
    """
    performs same preparation processes as applied to the trainig
    data on the test data .
    """
    FIRE_SIZE,FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, DIS_DATETIME = list_input
    
    
    DIS_DATETIME = datetime.datetime.strptime(str(DIS_DATETIME), '%Y-%m-%d').date()
    
    Year, Month, Day, Week_of_Year = DIS_DATETIME.year, DIS_DATETIME.month, DIS_DATETIME.day, DIS_DATETIME.isocalendar()[1]
    
    
    fire_size_class_dict = {"A":0, "B":0, "C":0, "D":0,"E":0, "F":0, 'G':0}
    fire_size_class_dict[FIRE_SIZE_CLASS] = 1
    
    
    data_dict = {'FIRE_SIZE':FIRE_SIZE, 'LATITUDE':LATITUDE, 'LONGITUDE':LONGITUDE, 
                 'Year':Year, 'Day':Day, 'Week_of_Year':Week_of_Year,
                 'FIRE_SIZE_CLASS_A': fire_size_class_dict["A"], 'FIRE_SIZE_CLASS_B': fire_size_class_dict["B"],
                 'FIRE_SIZE_CLASS_C': fire_size_class_dict["C"], 'FIRE_SIZE_CLASS_D': fire_size_class_dict["D"], 
                 'FIRE_SIZE_CLASS_E': fire_size_class_dict["E"], 'FIRE_SIZE_CLASS_F': fire_size_class_dict["F"], 
                 'FIRE_SIZE_CLASS_G': fire_size_class_dict["G"], 'Season_autumn':0, 'Season_spring':0, 
                 'Season_summer':0, 'Season_winter':0}
    
    if Month in [12, 1, 2]:
        data_dict['Season_winter'] = 1
    elif Month in [3, 4, 5]:
        data_dict['Season_spring'] = 1
    elif Month in [6, 7, 8]:
        data_dict['Season_summer'] = 1
    elif Month in [9, 10, 11]:
        data_dict['Season_autumn'] = 1

    X = pd.DataFrame([data_dict])

    
    return X


def predict_cause(sample):

    input_ = prepare_input_value(sample)
    model = pickle.load(open("cb_clf.pkl", "rb" ))
    y_pred = model.predict(input_)
    cause_map = {0:'Miscellaneous',1: 'Lightning', 2: 'Debris Burning', 
                 3: 'Campfire', 4: 'Equipment Use', 5: 'Arson', 6: 'Children',
                 7: 'Railroad', 8: 'Smoking', 9: 'Powerline', 10: 'Structure', 
                 11: 'Fireworks', 12: 'Missing/Undefined'}
    print(y_pred)
    return cause_map[y_pred[0][0]]
    


