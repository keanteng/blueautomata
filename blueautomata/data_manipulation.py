'''
This function will read the folder containing all the raw data files generated from the system
Subsequently, it will read and clean the data, so that they have the same format a
'''

import os
import pandas as pd
from data_cleaning import data_cleaning

def automata_execution(folder_path = r"C:\\Users\\Khor Kean Teng\\Downloads\\AUP Automata\\Data\\fakesystem\\experiment", checklist = 'data/checklist.csv', staff_data = 'data/fake_hr_data.csv', key_lib = 'data/library.xlsx', name_key = ['NaSdaq'], name_code = [1]):
    
    Department = []
    Dept = []
    UserID = []
    Fullname = []
    System1 = []
    Cube = []

    
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            for i in range(len(name_key)):
                if (name_key[i].lower() or name_key[i].upper()) in filename: 
                    file_path = os.path.join(folder_path, filename)
                    excelFile = pd.ExcelFile(file_path)
                    
                    keyname = pd.DataFrame({'key': name_key[i].upper()}, index=[0])
                    keyname['key_name'] = keyname['key'].map(key_lib.set_index('key')['key_name'])
                    key_name = keyname['key_name'][0]
                    
                    if name_code[i] == 1:
                        df = data_cleaning(excelFile, staff_data, checklist, key_name, namecode = 1)
                        for i in range(len(df)):
                            Department.append(df['Department'][i])
                            Dept.append(df['Dept'][i])
                            UserID.append(df['User ID'][i])
                            Fullname.append(df['Fullname'][i])
                            System1.append(df['System1'][i])
                            Cube.append(df['Cube'][i])
                    elif name_code[i] == 2:
                        df = data_cleaning(excelFile, staff_data, checklist, key_name, namecode = 2)
                        for i in range(len(df)):
                            Department.append(df['Department'][i])
                            Dept.append(df['Dept'][i])
                            UserID.append(df['User ID'][i])
                            Fullname.append(df['Fullname'][i])
                            System1.append(df['System1'][i])
                            Cube.append(df['Cube'][i])
                    else:
                        df = data_cleaning(excelFile, staff_data, checklist, key_name, namecode = 3)
                        for i in range(len(df)):
                            Department.append(df['Department'][i])
                            Dept.append(df['Dept'][i])
                            UserID.append(df['User ID'][i])
                            Fullname.append(df['Fullname'][i])
                            System1.append(df['System1'][i])
                            Cube.append(df['Cube'][i])
                else:
                    pass

    dataframes = pd.DataFrame({'Department': Department,
                                'Dept': Dept,
                                'UserID': UserID,
                                'Fullname': Fullname,
                                'System1': System1,
                                'Cube': Cube})
    
    print(dataframes.head())
    print(len(dataframes))

automata_execution()