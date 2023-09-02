'''
This function will read the folder containing all the raw data files generated from the system
Subsequently, it will read and clean the data, so that they have the same format a
'''

import os
import pandas as pd
from data_cleaning import dataCleaning

def automata_execution(folder_path = r"C:\Users\Khor Kean Teng\Downloads\AUP Automata\rawdata", checklist = 'rawdata/Department Checklist.xlsx', staff_data = 'rawdata/stafflist.xlsx', name_key = ['CCRIS'], name_code = [1]):
    
    dfs = []

    folder_list = pd.Series(os.listdir(folder_path))
    
    for k in range(0, len(folder_list)):
        if folder_list[k].endswith(".xlsx"):
            for j in range(0,len(name_key)):
                checker = name_key[j].upper()
                if checker in folder_list[k]: 
                    file_path = folder_path + '/' + checker.upper() + '.xlsx'
                    excelFile = pd.ExcelFile(file_path)
                    
                    if name_code[j] == 1:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 1)
                        dfs.append(df)
                    elif name_code[j] == 2:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 2)
                        dfs.append(df)
                    elif name_code[j] == 3:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 3)
                        dfs.append(df)
                    elif name_code[j] == 4:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 4)
                        dfs.append(df)
                    elif name_code[j] == 5:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 5)
                        dfs.append(df)
                    elif name_code[j] == 6:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 6)
                        dfs.append(df)
                    else:
                        df = dataCleaning(excelFile, staff_data, checklist, key = 10)
                        #df = dataCleaning(pd.ExcelFile('rawdata/ADMIN.xlsx') , staff_data = 'rawdata/stafflist.xlsx', checklist = 'rawdata/Department Checklist.xlsx', key = 10)
                        dfs.append(df)

    dataframes = pd.concat([df for df in dfs], ignore_index=True)
    
    print(dataframes.head())
    print(len(dataframes))
    dataframes.to_excel('data/automataoutput.xlsx', index = False)

automata_execution(
    name_key= ['DP', 'STATSMART'],
    name_code= [1, 2],
)