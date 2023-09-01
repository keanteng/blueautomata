'''
This function performs data cleaning for function based on 3 different keys:
1. Key 1: Data cleaning for files that can be read directly
2. Key 2: Data cleaning for files that can be read directly but need filter with some condition
3. Key 3: Data cleaning for files that cannot be read directly because of different sheet
'''

import pandas as pd

def data_cleaning(dataframe, staff_data, checklist, key_name, key):
    if key == 1:
        df = pd.read_excel(dataframe)
        ref_code = pd.read_excel(checklist, sheet_name = 'code')
        ref_cube = pd.read_excel(checklist, sheet_name = 'cube')
        
        # clean up staff data
        staff = pd.read_excel(staff_data)
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = key_name
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept_Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
        
        
    elif key == 2:
        df = pd.read_excel(dataframe)
        ref_code = pd.read_excel(checklist, sheet_name = 'code')
        ref_cube = pd.read_excel(checklist, sheet_name = 'cube')
        
        # clean up staff data
        staff = pd.read_excel(staff_data)
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = key_name
        temp = ref_cube.columns
        df['Cube'] = df['role code'].map(ref_cube.set_index(temp[0])[temp[1]])
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept_Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    elif key == 3:
        df = pd.read_excel(dataframe)
        ref_code = pd.read_excel(checklist, sheet_name = 'code')
        ref_cube = pd.read_excel(checklist, sheet_name = 'cube')
        
        # clean up staff data
        staff = pd.read_excel(staff_data)
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = key_name
        temp = ref_cube.columns
        df['Cube'] = df['STATSMART CUBE'].map(ref_cube.set_index(temp[0])[temp[1]])
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept_Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 4:
        df = pd.read_excel(dataframe)
        ref_code = pd.read_excel(checklist, sheet_name = 'code')
        ref_cube = pd.read_excel(checklist, sheet_name = 'cube')
        
        # clean up staff data
        staff = pd.read_excel(staff_data)
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df = df[df['Status']== '*ENABLED']
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = key_name
        temp = ref_cube.columns
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept_Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 5:
        df = pd.read_excel(dataframe)
        ref_code = pd.read_excel(checklist, sheet_name = 'code')
        ref_cube = pd.read_excel(checklist, sheet_name = 'cube')
        
        # clean up staff data
        staff = pd.read_excel(staff_data)
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df = df[df['Disable Flag *'] == 'N']
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = key_name
        temp = ref_cube.columns
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept_Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 6:
        df1 = df[df['RBC Access'] == 'Yes']
        df2 = df[df['IFAS Access'] == 'Yes']
    else:
        sheetName = dataframe.sheet_names
        for i in range(len(sheetName)):
            df = pd.read_excel(dataframe, sheet_name = sheetName[i])
    print(df.head())
    # return df
    
data_cleaning(dataframe = pd.ExcelFile('data/fakesystem/experiment/sys_NASDAQ.xlsx'), staff_data = 'data/fake_hr_data.xlsx', checklist = 'data/checklist.xlsx', key_name = 'NASDAQ', key = 5)